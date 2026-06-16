<template>
  <div class="history-page">
    <header class="page-header">
      <div>
        <div class="title-label mono">DATA_ARCHIVE / 历史数据</div>
        <h1 class="title-main">HISTORICAL ANALYTICS</h1>
      </div>
      <div class="actions">
        <button class="btn-primary" @click="exportCSV">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
            <polyline points="7 10 12 15 17 10" />
            <line x1="12" y1="15" x2="12" y2="3" />
          </svg>
          <span class="mono">EXPORT_CSV</span>
        </button>
      </div>
    </header>

    <section class="overview-grid">
      <div class="overview-card" v-for="(item, idx) in overviewItems" :key="idx">
        <div class="stat-corner tl"></div><div class="stat-corner tr"></div>
        <div class="stat-corner bl"></div><div class="stat-corner br"></div>
        <div class="card-header">
          <span class="card-label mono">{{ item.label }}</span>
          <span class="card-unit mono">{{ item.unit }}</span>
        </div>
        <div class="card-value mono" :style="{ color: item.color }">{{ item.value }}</div>
      </div>
    </section>

    <section class="trend-panel">
      <div class="panel-header">
        <div class="header-info">
          <div class="section-num mono">01</div>
          <h2 class="panel-title">TREND_ANALYSIS</h2>
          <span class="panel-sub">历史趋势图</span>
        </div>
        <div class="chart-controls">
          <button
            v-for="range in timeRanges"
            :key="range.value"
            :class="['ctrl', { active: selectedRange === range.value }]"
            @click="selectedRange = range.value"
          >
            <span class="mono">{{ range.label }}</span>
          </button>
        </div>
      </div>
      <div ref="trendChartRef" class="trend-chart"></div>
    </section>

    <section class="data-table-panel">
      <div class="panel-header">
        <div class="header-info">
          <div class="section-num mono">02</div>
          <h2 class="panel-title">RECORD_STREAM</h2>
          <span class="panel-sub">历史数据记录</span>
        </div>
        <div class="table-search">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <circle cx="11" cy="11" r="8" />
            <line x1="21" y1="21" x2="16.65" y2="16.65" />
          </svg>
          <input v-model="searchText" placeholder="// SEARCH..." />
        </div>
      </div>

      <div v-if="filteredHistory.length === 0" class="empty">
        <div class="empty-line mono">// NO_RECORDS_FOUND</div>
      </div>

      <div v-else class="table-wrapper">
        <div class="table-head mono">
          <div class="th">SEQ</div>
          <div class="th">TIMESTAMP</div>
          <div class="th num">TEMP_RAW</div>
          <div class="th num">TEMP_FILT</div>
          <div class="th num">HUMI_RAW</div>
          <div class="th num">HUMI_FILT</div>
          <div class="th">STATUS</div>
        </div>
        <div class="table-body">
          <div
            v-for="item in filteredHistory"
            :key="item.seq"
            class="table-row"
            :class="{
              'row-danger': item.alarmType && item.alarmType !== 'NORMAL',
              'row-warning': item.outlier
            }"
          >
            <div class="td mono">#{{ item.seq.toString().padStart(4, '0') }}</div>
            <div class="td mono">{{ item.timestamp?.slice(11) || '--' }}</div>
            <div class="td num mono" :class="{ 'cell-danger': item.rawTemperature > 35 }">{{ formatNum(item.rawTemperature) }}℃</div>
            <div class="td num mono">{{ formatNum(item.filteredTemperature) }}℃</div>
            <div class="td num mono" :class="{ 'cell-danger': item.rawHumidity > 80 }">{{ formatNum(item.rawHumidity) }}%</div>
            <div class="td num mono">{{ formatNum(item.filteredHumidity) }}%</div>
            <div class="td">
              <span class="status-chip" :class="getStatusClass(item.rawStatus)">
                {{ formatStatus(item.rawStatus) }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, watch, nextTick } from 'vue'
import * as echarts from 'echarts'
import { fetchHistory } from '../api/sensor'

const history = ref([])
const trendChartRef = ref(null)
const searchText = ref('')
const selectedRange = ref('all')
let trendChart = null

const timeRanges = [
  { value: 'all', label: 'ALL' },
  { value: '20', label: 'LAST_20' },
  { value: '50', label: 'LAST_50' },
]

const stats = computed(() => {
  const data = history.value
  if (data.length === 0) {
    return { totalCount: 0, avgTemp: '--', avgHumidity: '--', maxTemp: '--', minTemp: '--', packetLossRate: '0.0' }
  }
  const temps = data.map(d => d.rawTemperature).filter(v => v != null)
  const humis = data.map(d => d.rawHumidity).filter(v => v != null)
  const losses = data.filter(d => d.packetLoss).length
  return {
    totalCount: data.length,
    avgTemp: (temps.reduce((a, b) => a + b, 0) / temps.length).toFixed(1),
    avgHumidity: (humis.reduce((a, b) => a + b, 0) / humis.length).toFixed(1),
    maxTemp: Math.max(...temps).toFixed(1),
    minTemp: Math.min(...temps).toFixed(1),
    packetLossRate: ((losses / data.length) * 100).toFixed(1),
  }
})

const overviewItems = computed(() => [
  { label: 'TOTAL', unit: 'REC', value: stats.value.totalCount.toString().padStart(3, '0'), color: 'var(--color-primary)' },
  { label: 'AVG_TEMP', unit: '℃', value: stats.value.avgTemp, color: 'var(--color-primary)' },
  { label: 'AVG_HUMI', unit: '%', value: stats.value.avgHumidity, color: 'var(--color-success)' },
  { label: 'PEAK_TEMP', unit: '℃', value: stats.value.maxTemp, color: 'var(--color-danger)' },
  { label: 'MIN_TEMP', unit: '℃', value: stats.value.minTemp, color: 'var(--color-info)' },
  { label: 'LOSS_RATE', unit: '%', value: stats.value.packetLossRate, color: 'var(--color-warning)' },
])

const filteredHistory = computed(() => {
  let data = history.value.slice().reverse()
  if (selectedRange.value !== 'all') {
    data = data.slice(0, parseInt(selectedRange.value))
  }
  if (searchText.value) {
    const kw = searchText.value.toLowerCase()
    data = data.filter(d =>
      d.rawStatus?.toLowerCase().includes(kw) ||
      d.alarmType?.toLowerCase().includes(kw) ||
      d.alarmMessage?.toLowerCase().includes(kw)
    )
  }
  return data
})

function formatNum(v) {
  if (v == null) return '--'
  return Number(v).toFixed(1)
}

function formatStatus(s) {
  const map = {
    'normal': 'OK', 'jump': 'JUMP',
    'temp_high': 'T_HI', 'humidity_high': 'H_HI',
    'both_high': 'CRIT', 'offline': 'OFF',
  }
  return map[s] || s?.toUpperCase() || '--'
}

function getStatusClass(s) {
  if (!s || s === 'normal') return 'ok'
  if (s.includes('high')) return 'danger'
  if (s === 'jump') return 'warning'
  if (s === 'offline') return 'offline'
  return 'info'
}

async function loadHistory() {
  try {
    history.value = await fetchHistory()
    await nextTick()
    renderTrendChart()
  } catch (err) {
    console.warn('加载历史数据失败', err)
  }
}

function renderTrendChart() {
  if (!trendChartRef.value) return
  if (!trendChart) {
    trendChart = echarts.init(trendChartRef.value, null, { renderer: 'canvas' })
    window.addEventListener('resize', () => trendChart?.resize())
  }
  const data = history.value
  const option = {
    backgroundColor: 'transparent',
    animation: true,
    animationDuration: 600,
    legend: {
      data: ['原始温度', '滤波温度', '原始湿度'],
      textStyle: { color: '#8b96b0', fontFamily: 'JetBrains Mono', fontSize: 10 },
      top: 0,
      icon: 'rect',
      itemWidth: 12,
      itemHeight: 4,
    },
    grid: { left: 50, right: 50, top: 35, bottom: 30 },
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(15, 21, 37, 0.95)',
      borderColor: '#00d9ff',
      borderWidth: 1,
      textStyle: { color: '#e8edf5', fontFamily: 'JetBrains Mono', fontSize: 11 },
      axisPointer: { type: 'cross', lineStyle: { color: '#00d9ff', type: 'dashed' } },
    },
    xAxis: {
      type: 'category',
      data: data.map(d => d.timestamp?.slice(11, 19) || ''),
      axisLine: { lineStyle: { color: 'rgba(0, 217, 255, 0.2)' } },
      axisLabel: { color: '#5a6480', fontSize: 10, fontFamily: 'JetBrains Mono', interval: Math.max(1, Math.floor(data.length / 10)) },
    },
    yAxis: [
      { type: 'value', name: '℃', position: 'left', nameTextStyle: { color: '#5a6480', fontSize: 9 }, axisLabel: { color: '#5a6480', fontSize: 10, fontFamily: 'JetBrains Mono' }, splitLine: { lineStyle: { type: 'dashed', color: 'rgba(0, 217, 255, 0.06)' } } },
      { type: 'value', name: '%', position: 'right', nameTextStyle: { color: '#5a6480', fontSize: 9 }, axisLabel: { color: '#5a6480', fontSize: 10, fontFamily: 'JetBrains Mono' }, splitLine: { show: false } },
    ],
    series: [
      {
        name: '原始温度', type: 'line', data: data.map(d => d.rawTemperature),
        smooth: 0.3, showSymbol: false,
        lineStyle: { color: 'rgba(139, 150, 176, 0.5)', width: 1.5 },
      },
      {
        name: '滤波温度', type: 'line', data: data.map(d => d.filteredTemperature),
        smooth: 0.3, showSymbol: false,
        lineStyle: { color: '#00d9ff', width: 2.5, shadowColor: '#00d9ff', shadowBlur: 6 },
        areaStyle: { color: { type: 'linear', x: 0, y: 0, x2: 0, y2: 1, colorStops: [{ offset: 0, color: 'rgba(0, 217, 255, 0.15)' }, { offset: 1, color: 'rgba(0, 217, 255, 0)' }] } },
      },
      {
        name: '原始湿度', type: 'line', yAxisIndex: 1, data: data.map(d => d.rawHumidity),
        smooth: 0.3, showSymbol: false,
        lineStyle: { color: '#00ff9d', width: 2, type: 'dashed' },
      },
    ],
  }
  trendChart.setOption(option, true)
}

function exportCSV() {
  const headers = ['序号', '时间', '原始温度', '滤波温度', '原始湿度', '滤波湿度', '状态', '报警', '诊断建议']
  const rows = filteredHistory.value.map(d => [
    d.seq, d.timestamp, d.rawTemperature, d.filteredTemperature,
    d.rawHumidity, d.filteredHumidity, d.rawStatus, d.alarmType, d.diagnosisAdvice
  ])
  const csv = [headers, ...rows].map(r => r.join(',')).join('\n')
  const blob = new Blob(['\uFEFF' + csv], { type: 'text/csv' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `sensor_data_${new Date().toISOString().slice(0, 10)}.csv`
  a.click()
  URL.revokeObjectURL(url)
}

watch([history, selectedRange], () => nextTick(renderTrendChart), { deep: true })

onMounted(loadHistory)
onBeforeUnmount(() => trendChart?.dispose())
</script>

<style scoped>
.history-page {
  padding: var(--space-6);
  min-height: 100%;
}

.page-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  margin-bottom: var(--space-6);
  padding-bottom: var(--space-5);
  border-bottom: 1px solid var(--color-border);
  position: relative;
}

.page-header::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 0;
  width: 80px;
  height: 2px;
  background: var(--color-primary);
  box-shadow: 0 0 8px var(--color-primary);
}

.title-label {
  font-size: 10px;
  font-weight: 600;
  color: var(--color-primary);
  letter-spacing: 0.2em;
  margin-bottom: var(--space-1);
}

.title-main {
  font-family: var(--font-display);
  font-size: 26px;
  font-weight: 700;
  color: var(--color-text-primary);
  letter-spacing: -0.02em;
  margin: 0;
}

.btn-primary {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-4);
  font-size: 11px;
  font-weight: 700;
  color: var(--color-text-inverse);
  background: var(--color-primary);
  border: 1px solid var(--color-primary);
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: all var(--duration-base);
  letter-spacing: 0.1em;
  box-shadow: 0 0 12px var(--color-primary-glow);
}

.btn-primary:hover {
  background: var(--color-primary);
  box-shadow: 0 0 20px var(--color-primary-glow);
  transform: translateY(-1px);
}

.btn-primary svg { width: 14px; height: 14px; }

/* Overview */
.overview-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: var(--space-3);
  margin-bottom: var(--space-6);
}

.overview-card {
  position: relative;
  padding: var(--space-4);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  transition: all var(--duration-base);
}

.overview-card:hover {
  border-color: var(--color-border-strong);
  transform: translateY(-2px);
}

.stat-corner {
  position: absolute;
  width: 6px;
  height: 6px;
  border-color: var(--color-primary);
  opacity: 0.3;
}

.stat-corner.tl { top: 3px; left: 3px; border-top: 1px solid; border-left: 1px solid; }
.stat-corner.tr { top: 3px; right: 3px; border-top: 1px solid; border-right: 1px solid; }
.stat-corner.bl { bottom: 3px; left: 3px; border-bottom: 1px solid; border-left: 1px solid; }
.stat-corner.br { bottom: 3px; right: 3px; border-bottom: 1px solid; border-right: 1px solid; }

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-2);
}

.card-label {
  font-size: 9px;
  color: var(--color-text-tertiary);
  letter-spacing: 0.1em;
}

.card-unit {
  font-size: 9px;
  color: var(--color-text-tertiary);
}

.card-value {
  font-size: 22px;
  font-weight: 700;
  text-shadow: 0 0 8px currentColor;
  line-height: 1;
}

/* Trend Panel */
.trend-panel, .data-table-panel {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: var(--space-5);
  margin-bottom: var(--space-6);
  position: relative;
  overflow: hidden;
}

.trend-panel::before, .data-table-panel::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--color-primary), transparent);
  opacity: 0.5;
}

.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-4);
  padding-bottom: var(--space-3);
  border-bottom: 1px dashed var(--color-border);
  flex-wrap: wrap;
  gap: var(--space-3);
}

.header-info {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.section-num {
  font-size: 10px;
  font-weight: 700;
  color: var(--color-primary);
  letter-spacing: 0.1em;
  padding: 2px 8px;
  background: var(--color-primary-soft);
  border: 1px solid var(--color-primary);
  border-radius: var(--radius-sm);
}

.panel-title {
  font-family: var(--font-display);
  font-size: 15px;
  font-weight: 700;
  color: var(--color-text-primary);
  margin: 0;
  letter-spacing: 0.02em;
}

.panel-sub {
  font-family: var(--font-mono);
  font-size: 10px;
  color: var(--color-text-tertiary);
}

.chart-controls {
  display: flex;
  gap: var(--space-1);
  background: var(--color-bg-elevated);
  padding: var(--space-1);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
}

.ctrl {
  padding: var(--space-1) var(--space-3);
  font-size: 10px;
  color: var(--color-text-secondary);
  background: transparent;
  border: none;
  border-radius: var(--radius-xs);
  cursor: pointer;
  transition: all var(--duration-base);
  letter-spacing: 0.1em;
}

.ctrl:hover { color: var(--color-primary); }

.ctrl.active {
  background: var(--color-primary);
  color: var(--color-text-inverse);
  box-shadow: 0 0 8px var(--color-primary-glow);
}

.trend-chart {
  height: 300px;
}

.table-search {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-3);
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  width: 240px;
  transition: border-color var(--duration-base);
}

.table-search:focus-within { border-color: var(--color-primary); }

.table-search svg {
  width: 14px;
  height: 14px;
  color: var(--color-text-tertiary);
}

.table-search input {
  flex: 1;
  border: none;
  background: transparent;
  font-family: var(--font-mono);
  font-size: 12px;
  outline: none;
  color: var(--color-text-primary);
}

.empty {
  padding: var(--space-12);
  text-align: center;
}

.empty-line {
  font-size: 12px;
  color: var(--color-text-tertiary);
  letter-spacing: 0.1em;
  animation: blink 1.5s ease-in-out infinite;
}

@keyframes blink {
  0%, 100% { opacity: 0.5; }
  50% { opacity: 1; }
}

.table-wrapper { overflow-x: auto; }

.table-head, .table-row {
  display: grid;
  grid-template-columns: 80px 110px 1fr 1fr 1fr 1fr 100px;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-3);
  align-items: center;
}

.table-head {
  font-size: 9px;
  color: var(--color-text-tertiary);
  letter-spacing: 0.1em;
  border-bottom: 1px solid var(--color-border);
}

.table-row {
  font-size: 11px;
  color: var(--color-text-secondary);
  border-bottom: 1px solid var(--color-border-subtle);
  transition: background var(--duration-base);
}

.table-row:hover { background: var(--color-bg-elevated); }
.table-row.row-danger { background: linear-gradient(90deg, var(--color-danger-soft), transparent 50%); border-left: 2px solid var(--color-danger); padding-left: calc(var(--space-3) - 2px); }
.table-row.row-warning { background: linear-gradient(90deg, var(--color-warning-soft), transparent 50%); border-left: 2px solid var(--color-warning); padding-left: calc(var(--space-3) - 2px); }

.th.num, .td.num { text-align: right; }

.cell-danger {
  color: var(--color-danger) !important;
  font-weight: 700;
  text-shadow: 0 0 6px rgba(255, 56, 96, 0.4);
}

.status-chip {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 2px 8px;
  font-family: var(--font-mono);
  font-size: 9px;
  font-weight: 700;
  letter-spacing: 0.05em;
  border-radius: var(--radius-sm);
}

.status-chip.ok { background: var(--color-success-soft); color: var(--color-success); border: 1px solid var(--color-success); }
.status-chip.warning { background: var(--color-warning-soft); color: var(--color-warning); border: 1px solid var(--color-warning); }
.status-chip.danger { background: var(--color-danger-soft); color: var(--color-danger); border: 1px solid var(--color-danger); animation: pulse-chip 1s infinite; }
.status-chip.offline { background: var(--color-bg-elevated); color: var(--color-text-tertiary); border: 1px solid var(--color-border); }
.status-chip.info { background: var(--color-info-soft); color: var(--color-info); border: 1px solid var(--color-info); }

@keyframes pulse-chip {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.6; }
}

@media (max-width: 1024px) {
  .overview-grid { grid-template-columns: repeat(3, 1fr); }
}
</style>
