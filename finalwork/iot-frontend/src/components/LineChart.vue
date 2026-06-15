<template>
  <div ref="chartRef" class="chart"></div>
</template>

<script setup>
import { onMounted, onBeforeUnmount, ref, watch } from 'vue'
import * as echarts from 'echarts'

const props = defineProps({
  title: String,
  xData: Array,
  rawData: Array,
  filteredData: Array,
  unit: String,
})

const chartRef = ref(null)
let chart = null
let resizeHandler = null

function renderChart() {
  if (!chart) return
  chart.setOption({
    title: { text: props.title, left: 12, top: 8, textStyle: { color: '#d8e7ff', fontSize: 16 } },
    tooltip: { trigger: 'axis' },
    legend: { data: ['原始值', '滤波值'], top: 8, right: 16, textStyle: { color: '#a8bedc' } },
    grid: { left: 48, right: 28, top: 58, bottom: 36 },
    xAxis: { type: 'category', data: props.xData, axisLabel: { color: '#9fb3d1' } },
    yAxis: { type: 'value', name: props.unit, axisLabel: { color: '#9fb3d1' } },
    series: [
      { name: '原始值', type: 'line', data: props.rawData, smooth: true, showSymbol: false },
      { name: '滤波值', type: 'line', data: props.filteredData, smooth: true, showSymbol: false },
    ],
  })
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
