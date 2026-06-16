<template>
  <div class="chart" :class="{ 'has-alarm': hasAlarm }">
    <div class="chart-header">
      <div class="chart-title">
        <svg class="chart-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M3 3v18h18" />
          <path d="M18 17l-5-5-4 4-3-3" />
        </svg>
        {{ title }}
      </div>
      <div class="chart-values">
        <span class="current-value" :class="{ danger: isAlarm }">
          {{ currentValue }}
        </span>
        <span class="unit">{{ unit }}</span>
      </div>
    </div>
    <div ref="chartRef" class="chart-canvas"></div>
    <div v-if="hasAlarm" class="alarm-overlay">
      <span class="alarm-badge">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z" />
          <line x1="12" y1="9" x2="12" y2="13" />
          <line x1="12" y1="17" x2="12.01" y2="17" />
        </svg>
        {{ alarmText }}
      </span>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, onBeforeUnmount, ref, watch } from 'vue'
import * as echarts from 'echarts'

const props = defineProps({
  title: String,
  xData: Array,
  rawData: Array,
  filteredData: Array,
  unit: String,
  alarmThreshold: {
    type: Number,
    default: 35
  },
  alarmLowThreshold: {
    type: Number,
    default: 10
  }
})

const chartRef = ref(null)
let chart = null
let resizeHandler = null

const hasAlarm = computed(() => {
  if (!props.filteredData || props.filteredData.length === 0) return false
  const last = props.filteredData[props.filteredData.length - 1]
  return last > props.alarmThreshold || last < props.alarmLowThreshold
})

const isAlarm = computed(() => hasAlarm.value)

const currentValue = computed(() => {
  if (!props.filteredData || props.filteredData.length === 0) return '--'
  const last = props.filteredData[props.filteredData.length - 1]
  return last?.toFixed(1) || '--'
})

const alarmText = computed(() => {
  if (!props.filteredData || props.filteredData.length === 0) return ''
  const last = props.filteredData[props.filteredData.length - 1]
  if (last > props.alarmThreshold) return '温度过高'
  if (last < props.alarmLowThreshold) return '温度过低'
  return ''
})

function renderChart() {
  if (!chart) return

  const rawColor = hasAlarm.value ? '#ef476f' : '#94a3b8'
  const filteredColor = hasAlarm.value ? '#ef476f' : '#4f46e5'

  const option = {
    backgroundColor: 'transparent',
    animation: true,
    animationDuration: 300,
    grid: {
      left: 45,
      right: 15,
      top: 10,
      bottom: 25,
      containLabel: false,
    },
    xAxis: {
      type: 'category',
      data: props.xData,
      boundaryGap: false,
      axisLine: {
        lineStyle: { color: '#e2e8f0' },
      },
      axisTick: { show: false },
      axisLabel: {
        color: '#94a3b8',
        fontSize: 10,
        interval: Math.floor((props.xData?.length || 10) / 5),
        formatter: (val) => val?.slice(-5) || '',
      },
      splitLine: { show: false },
    },
    yAxis: {
      type: 'value',
      name: props.unit,
      nameTextStyle: {
        color: '#94a3b8',
        fontSize: 10,
        padding: [0, 0, 0, -8],
      },
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: {
        color: '#94a3b8',
        fontSize: 10,
      },
      splitLine: {
        lineStyle: {
          color: '#f1f5f9',
          type: 'dashed',
        },
      },
    },
    series: [
      {
        name: '原始值',
        type: 'line',
        data: props.rawData,
        smooth: 0.3,
        showSymbol: false,
        lineStyle: {
          width: 2,
          color: rawColor,
          opacity: 0.5,
        },
        areaStyle: null,
      },
      {
        name: '滤波值',
        type: 'line',
        data: props.filteredData,
        smooth: 0.3,
        showSymbol: false,
        lineStyle: {
          width: 3,
          color: filteredColor,
        },
        areaStyle: {
          color: {
            type: 'linear',
            x: 0, y: 0, x2: 0, y2: 1,
            colorStops: [
              { offset: 0, color: hasAlarm.value ? 'rgba(239, 71, 111, 0.15)' : 'rgba(79, 70, 229, 0.12)' },
              { offset: 1, color: 'rgba(0, 0, 0, 0)' },
            ],
          },
        },
        markLine: hasAlarm.value ? {
          silent: true,
          symbol: 'none',
          lineStyle: {
            color: '#ef476f',
            type: 'dashed',
            width: 1,
          },
          data: [
            { yAxis: props.alarmThreshold, label: { show: false } },
          ],
        } : null,
      },
    ],
  }

  chart.setOption(option)
}

onMounted(() => {
  chart = echarts.init(chartRef.value)
  resizeHandler = () => chart && chart.resize()
  renderChart()
  window.addEventListener('resize', resizeHandler)
})

onBeforeUnmount(() => {
  if (resizeHandler) window.removeEventListener('resize', resizeHandler)
  chart?.dispose()
})

watch(() => [props.xData, props.rawData, props.filteredData, props.title, props.unit], renderChart, { deep: true })
</script>

<style scoped>
.chart {
  position: relative;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--space-4);
  box-shadow: var(--shadow-sm);
  height: 260px;
  transition: all var(--transition-base);
}

.chart.has-alarm {
  border-color: rgba(239, 71, 111, 0.3);
  animation: chart-pulse 1.5s ease-in-out infinite;
}

@keyframes chart-pulse {
  0%, 100% { box-shadow: var(--shadow-sm); }
  50% { box-shadow: 0 0 15px rgba(239, 71, 111, 0.2); }
}

.chart-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-2);
  padding: 0 var(--space-1);
}

.chart-title {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: 13px;
  font-weight: 600;
  color: var(--color-text-secondary);
}

.chart-icon {
  width: 16px;
  height: 16px;
  color: var(--color-primary);
}

.chart-values {
  display: flex;
  align-items: baseline;
  gap: var(--space-1);
}

.current-value {
  font-size: 20px;
  font-weight: 700;
  font-family: var(--font-mono);
  color: var(--color-text-primary);
  transition: color var(--transition-base);
}

.current-value.danger {
  color: var(--color-danger);
  animation: value-pulse 0.5s ease-in-out infinite;
}

@keyframes value-pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}

.chart-values .unit {
  font-size: 12px;
  color: var(--color-text-tertiary);
}

.chart-canvas {
  width: 100%;
  height: calc(100% - 45px);
}

.alarm-overlay {
  position: absolute;
  top: var(--space-4);
  right: var(--space-4);
}

.alarm-badge {
  display: flex;
  align-items: center;
  gap: var(--space-1);
  padding: var(--space-1) var(--space-3);
  font-size: 11px;
  font-weight: 600;
  color: var(--color-danger);
  background: rgba(239, 71, 111, 0.1);
  border: 1px solid rgba(239, 71, 111, 0.3);
  border-radius: var(--radius-full);
  animation: badge-flash 1s ease-in-out infinite;
}

.alarm-badge svg {
  width: 12px;
  height: 12px;
}

@keyframes badge-flash {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.6; }
}
</style>
