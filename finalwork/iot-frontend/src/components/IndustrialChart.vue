<template>
  <div class="industrial-chart" :class="{ 'has-alarm': hasAlarm }">
    <div class="chart-corner top-left"></div>
    <div class="chart-corner top-right"></div>
    <div class="chart-corner bottom-left"></div>
    <div class="chart-corner bottom-right"></div>

    <div class="chart-header">
      <div class="header-left">
        <span class="chart-icon">
          <component :is="iconComponent" />
        </span>
        <div>
          <div class="chart-title">{{ title }}</div>
          <div class="chart-subtitle">{{ subtitle }}</div>
        </div>
      </div>
      <div class="header-right">
        <div class="readout">
          <div class="readout-label">CURRENT</div>
          <div class="readout-value mono" :class="{ danger: hasAlarm }">
            {{ currentValueDisplay }}<span class="readout-unit">{{ unit }}</span>
          </div>
        </div>
      </div>
    </div>

    <div class="chart-body">
      <div ref="chartRef" class="chart-canvas"></div>
    </div>

    <div class="chart-footer">
      <div class="legend-item">
        <span class="legend-line raw"></span>
        <span class="legend-text">RAW</span>
      </div>
      <div class="legend-item">
        <span class="legend-line filtered"></span>
        <span class="legend-text">FILTERED</span>
      </div>
      <div class="threshold-info">
        <span class="threshold-key">THRESHOLD</span>
        <span class="threshold-val mono">&gt; {{ alarmThreshold }} / &lt; {{ alarmLowThreshold }}</span>
      </div>
      <div v-if="hasAlarm" class="alarm-flag">
        <span class="flag-pulse"></span>
        <span class="flag-text">ALARM_ACTIVE</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, onBeforeUnmount, ref, watch, h, nextTick } from 'vue'
import * as echarts from 'echarts'

const props = defineProps({
  title: String,
  subtitle: String,
  xData: Array,
  rawData: Array,
  filteredData: Array,
  unit: String,
  alarmThreshold: { type: Number, default: 35 },
  alarmLowThreshold: { type: Number, default: 10 },
  currentValue: [String, Number],
  color: { type: String, default: 'var(--color-primary)' },
  icon: { type: String, default: 'thermometer' },
})

const chartRef = ref(null)
let chart = null
let resizeHandler = null

const hasAlarm = computed(() => {
  if (!props.filteredData || props.filteredData.length === 0) return false
  const last = props.filteredData[props.filteredData.length - 1]
  return last > props.alarmThreshold || last < props.alarmLowThreshold
})

const currentValueDisplay = computed(() => {
  if (props.currentValue === '--' || props.currentValue == null) return '--'
  return Number(props.currentValue).toFixed(1)
})

const iconComponent = computed(() => {
  const icons = {
    thermometer: () => h('svg', { viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '1.5' }, [
      h('path', { d: 'M14 14.76V3.5a2.5 2.5 0 0 0-5 0v11.26a4 4 0 1 0 5 0z' }),
    ]),
    droplet: () => h('svg', { viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '1.5' }, [
      h('path', { d: 'M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z' }),
    ]),
  }
  return icons[props.icon] || icons.thermometer
})

function getColorValue() {
  if (hasAlarm.value) return '#ff3860'
  if (props.color.includes('success')) return '#00ff9d'
  return '#00d9ff'
}

function renderChart() {
  if (!chart) return
  const lineColor = getColorValue()

  const option = {
    backgroundColor: 'transparent',
    animation: true,
    animationDuration: 400,
    animationEasing: 'cubicOut',
    grid: { left: 50, right: 20, top: 20, bottom: 30 },
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(15, 21, 37, 0.95)',
      borderColor: lineColor,
      borderWidth: 1,
      textStyle: { color: '#e8edf5', fontFamily: 'JetBrains Mono', fontSize: 11 },
      axisPointer: {
        type: 'cross',
        lineStyle: { color: lineColor, width: 1, type: 'dashed', opacity: 0.5 },
        crossStyle: { color: lineColor, opacity: 0.5 },
        label: { backgroundColor: lineColor, color: '#0a0e1a', fontFamily: 'JetBrains Mono' },
      },
    },
    xAxis: {
      type: 'category',
      data: props.xData,
      boundaryGap: false,
      axisLine: { lineStyle: { color: 'rgba(0, 217, 255, 0.2)' } },
      axisTick: { show: false },
      axisLabel: {
        color: '#5a6480',
        fontSize: 10,
        fontFamily: 'JetBrains Mono',
        interval: Math.max(1, Math.floor((props.xData?.length || 10) / 6)),
        formatter: (val) => val?.slice(-5) || '',
      },
      splitLine: { show: false },
    },
    yAxis: {
      type: 'value',
      name: props.unit,
      nameTextStyle: {
        color: '#5a6480',
        fontSize: 9,
        fontFamily: 'JetBrains Mono',
        padding: [0, 0, 0, -10],
      },
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: {
        color: '#5a6480',
        fontSize: 10,
        fontFamily: 'JetBrains Mono',
      },
      splitLine: {
        lineStyle: {
          color: 'rgba(0, 217, 255, 0.06)',
          type: 'dashed',
        },
      },
    },
    series: [
      {
        name: 'RAW',
        type: 'line',
        data: props.rawData,
        smooth: 0.3,
        showSymbol: false,
        lineStyle: {
          width: 1.5,
          color: 'rgba(139, 150, 176, 0.5)',
          type: 'solid',
        },
        z: 1,
      },
      {
        name: 'FILTERED',
        type: 'line',
        data: props.filteredData,
        smooth: 0.3,
        showSymbol: false,
        lineStyle: {
          width: 2.5,
          color: lineColor,
          shadowColor: lineColor,
          shadowBlur: 8,
        },
        areaStyle: {
          color: {
            type: 'linear',
            x: 0, y: 0, x2: 0, y2: 1,
            colorStops: [
              { offset: 0, color: lineColor + '25' },
              { offset: 1, color: lineColor + '00' },
            ],
          },
        },
        z: 2,
        markLine: {
          silent: true,
          symbol: 'none',
          lineStyle: {
            color: '#ff3860',
            type: 'dashed',
            width: 1,
            opacity: 0.5,
          },
          data: [
            { yAxis: props.alarmThreshold, label: { show: false } },
            { yAxis: props.alarmLowThreshold, label: { show: false } },
          ],
        },
      },
    ],
  }

  chart.setOption(option, true)
}

onMounted(async () => {
  await nextTick()
  chart = echarts.init(chartRef.value, null, { renderer: 'canvas' })
  resizeHandler = () => chart && chart.resize()
  window.addEventListener('resize', resizeHandler)
  renderChart()
})

onBeforeUnmount(() => {
  if (resizeHandler) window.removeEventListener('resize', resizeHandler)
  chart?.dispose()
})

watch(() => [props.xData, props.rawData, props.filteredData, hasAlarm.value], () => nextTick(renderChart), { deep: true })
</script>

<style scoped>
.industrial-chart {
  position: relative;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: var(--space-4);
  display: flex;
  flex-direction: column;
  height: 320px;
  transition: all var(--duration-base) var(--ease-out);
  overflow: hidden;
}

.industrial-chart::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--color-primary), transparent);
  opacity: 0;
  transition: opacity var(--duration-base);
}

.industrial-chart:hover::before { opacity: 0.5; }

.industrial-chart.has-alarm {
  border-color: var(--color-danger);
  box-shadow: 0 0 20px rgba(255, 56, 96, 0.2);
}

.industrial-chart.has-alarm::before {
  background: linear-gradient(90deg, transparent, var(--color-danger), transparent);
  opacity: 0.8;
}

/* 角标 */
.chart-corner {
  position: absolute;
  width: 10px;
  height: 10px;
  border-color: var(--color-primary);
  opacity: 0.4;
  z-index: 1;
  pointer-events: none;
  transition: opacity var(--duration-base);
}

.chart-corner.top-left { top: 4px; left: 4px; border-top: 1.5px solid; border-left: 1.5px solid; }
.chart-corner.top-right { top: 4px; right: 4px; border-top: 1.5px solid; border-right: 1.5px solid; }
.chart-corner.bottom-left { bottom: 4px; left: 4px; border-bottom: 1.5px solid; border-left: 1.5px solid; }
.chart-corner.bottom-right { bottom: 4px; right: 4px; border-bottom: 1.5px solid; border-right: 1.5px solid; }

.industrial-chart:hover .chart-corner { opacity: 0.8; }
.industrial-chart.has-alarm .chart-corner { border-color: var(--color-danger); opacity: 1; }

.chart-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: var(--space-3);
  padding-bottom: var(--space-3);
  border-bottom: 1px dashed var(--color-border);
}

.header-left {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.chart-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: var(--color-primary-soft);
  border: 1px solid var(--color-primary);
  border-radius: var(--radius-sm);
  color: var(--color-primary);
  box-shadow: var(--shadow-glow);
}

.industrial-chart.has-alarm .chart-icon {
  background: var(--color-danger-soft);
  border-color: var(--color-danger);
  color: var(--color-danger);
}

.chart-icon svg { width: 18px; height: 18px; }

.chart-title {
  font-family: var(--font-display);
  font-size: 13px;
  font-weight: 600;
  color: var(--color-text-primary);
  letter-spacing: 0.05em;
}

.chart-subtitle {
  font-family: var(--font-mono);
  font-size: 10px;
  color: var(--color-text-tertiary);
  margin-top: 2px;
  letter-spacing: 0.05em;
}

.readout {
  text-align: right;
}

.readout-label {
  font-family: var(--font-mono);
  font-size: 9px;
  color: var(--color-text-tertiary);
  letter-spacing: 0.1em;
}

.readout-value {
  font-size: 22px;
  font-weight: 700;
  color: var(--color-primary);
  text-shadow: 0 0 12px var(--color-primary-glow);
  line-height: 1.1;
  margin-top: 2px;
}

.readout-value.danger {
  color: var(--color-danger);
  text-shadow: 0 0 12px rgba(255, 56, 96, 0.5);
  animation: pulse-val 0.8s ease-in-out infinite;
}

@keyframes pulse-val {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}

.readout-unit {
  font-size: 12px;
  color: var(--color-text-tertiary);
  margin-left: 2px;
  font-weight: 500;
}

.chart-body {
  flex: 1;
  min-height: 0;
  margin: 0 calc(-1 * var(--space-4));
}

.chart-canvas {
  width: 100%;
  height: 100%;
}

.chart-footer {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  padding-top: var(--space-2);
  margin-top: var(--space-2);
  border-top: 1px dashed var(--color-border);
  flex-wrap: wrap;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: var(--space-1);
}

.legend-line {
  display: inline-block;
  width: 16px;
  height: 2px;
  border-radius: 1px;
}

.legend-line.raw {
  background: rgba(139, 150, 176, 0.5);
}

.legend-line.filtered {
  background: var(--color-primary);
  box-shadow: 0 0 4px var(--color-primary);
}

.industrial-chart.has-alarm .legend-line.filtered {
  background: var(--color-danger);
  box-shadow: 0 0 4px var(--color-danger);
}

.legend-text {
  font-family: var(--font-mono);
  font-size: 9px;
  color: var(--color-text-tertiary);
  letter-spacing: 0.1em;
}

.threshold-info {
  display: flex;
  align-items: center;
  gap: var(--space-1);
  padding-left: var(--space-3);
  border-left: 1px solid var(--color-border);
}

.threshold-key {
  font-family: var(--font-mono);
  font-size: 9px;
  color: var(--color-text-tertiary);
  letter-spacing: 0.1em;
}

.threshold-val {
  font-size: 10px;
  color: var(--color-warning);
  letter-spacing: 0.05em;
}

.alarm-flag {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  margin-left: auto;
  padding: 2px 8px;
  background: var(--color-danger-soft);
  border: 1px solid var(--color-danger);
  border-radius: var(--radius-sm);
}

.flag-pulse {
  width: 6px;
  height: 6px;
  background: var(--color-danger);
  border-radius: 50%;
  box-shadow: 0 0 6px var(--color-danger);
  animation: blink 0.5s ease-in-out infinite;
}

.flag-text {
  font-family: var(--font-mono);
  font-size: 9px;
  font-weight: 700;
  color: var(--color-danger);
  letter-spacing: 0.1em;
}
</style>
