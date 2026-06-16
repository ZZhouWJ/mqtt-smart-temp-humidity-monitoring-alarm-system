<template>
  <div class="alarms-page">
    <div class="page-decor">
      <LottieAnimation
        type="alert"
        :size="100"
        :speed="0.6"
        color="rgba(255, 56, 96, 0.4)"
      />
    </div>

    <header class="page-header">
      <div>
        <div class="title-label">ALERT_HISTORY / 报警历史</div>
        <h1 class="title-main">ALARM ARCHIVE</h1>
      </div>
      <div class="filter-tabs">
        <button
          v-for="tab in tabs"
          :key="tab.value"
          :class="['tab', { active: activeTab === tab.value }]"
          @click="activeTab = tab.value"
        >
          <span class="tab-bracket">[</span>
          <span>{{ tab.label }}</span>
          <span class="tab-count mono">{{ (tab.count || 0).toString().padStart(2, '0') }}</span>
          <span class="tab-bracket">]</span>
        </button>
      </div>
    </header>

    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-corner tl"></div>
        <div class="stat-corner tr"></div>
        <div class="stat-corner bl"></div>
        <div class="stat-corner br"></div>
        <div class="stat-header">
          <span class="stat-label mono">TOTAL</span>
          <span class="stat-bar"></span>
        </div>
        <div class="stat-value danger mono">{{ totalCount.toString().padStart(3, '0') }}</div>
        <div class="stat-desc">累计报警总数</div>
      </div>
      <div class="stat-card">
        <div class="stat-corner tl"></div>
        <div class="stat-corner tr"></div>
        <div class="stat-corner bl"></div>
        <div class="stat-corner br"></div>
        <div class="stat-header">
          <span class="stat-label mono">TODAY</span>
          <span class="stat-bar"></span>
        </div>
        <div class="stat-value warning mono">{{ todayCount.toString().padStart(3, '0') }}</div>
        <div class="stat-desc">今日新增</div>
      </div>
      <div class="stat-card">
        <div class="stat-corner tl"></div>
        <div class="stat-corner tr"></div>
        <div class="stat-corner bl"></div>
        <div class="stat-corner br"></div>
        <div class="stat-header">
          <span class="stat-label mono">TEMP_RELATED</span>
          <span class="stat-bar"></span>
        </div>
        <div class="stat-value mono">{{ tempCount.toString().padStart(3, '0') }}</div>
        <div class="stat-desc">温度相关</div>
      </div>
      <div class="stat-card">
        <div class="stat-corner tl"></div>
        <div class="stat-corner tr"></div>
        <div class="stat-corner bl"></div>
        <div class="stat-corner br"></div>
        <div class="stat-header">
          <span class="stat-label mono">HUMI_RELATED</span>
          <span class="stat-bar"></span>
        </div>
        <div class="stat-value mono">{{ humidityCount.toString().padStart(3, '0') }}</div>
        <div class="stat-desc">湿度相关</div>
      </div>
    </div>

    <div class="alarms-list-panel">
      <div class="panel-header">
        <div class="header-info">
          <div class="title-label mono">— EVENT_STREAM</div>
          <div class="header-sub">实时报警事件流</div>
        </div>
        <button class="btn-refresh" @click="refresh">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8" />
            <path d="M21 3v5h-5" />
            <path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16" />
            <path d="M3 21v-5h5" />
          </svg>
          <span class="mono">REFRESH</span>
        </button>
      </div>

      <div v-if="filteredAlarms.length === 0" class="empty">
        <svg class="empty-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <circle cx="12" cy="12" r="10" />
          <path d="M9 12l2 2 4-4" />
        </svg>
        <div class="empty-text mono">// NO_EVENTS_IN_QUEUE</div>
        <div class="empty-hint">当前筛选条件下暂无报警记录</div>
      </div>

      <div v-else class="alarms-list">
        <div
          v-for="(item, idx) in filteredAlarms"
          :key="item.timestamp + idx"
          class="alarm-row"
          :class="getAlarmClass(item.alarmType)"
        >
          <div class="row-time">
            <div class="time-main mono">{{ formatTime(item.timestamp) }}</div>
            <div class="time-date mono">{{ formatDate(item.timestamp) }}</div>
          </div>
          <div class="row-status">
            <div class="status-indicator">
              <span class="pulse-dot" :style="{ color: getAlarmColor(item.alarmType) }"></span>
            </div>
            <span class="status-text mono">{{ formatAlarmType(item.alarmType) }}</span>
          </div>
          <div class="row-msg">
            <div class="msg-text">{{ item.alarmMessage }}</div>
            <div v-if="item.diagnosisAdvice" class="msg-advice">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <circle cx="12" cy="12" r="10" />
                <line x1="12" y1="16" x2="12" y2="12" />
                <line x1="12" y1="8" x2="12.01" y2="8" />
              </svg>
              <span>{{ item.diagnosisAdvice }}</span>
            </div>
          </div>
          <div class="row-data">
            <div class="data-row">
              <span class="data-key mono">T</span>
              <span class="data-val mono">{{ item.temperature }}℃</span>
            </div>
            <div class="data-row">
              <span class="data-key mono">H</span>
              <span class="data-val mono">{{ item.humidity }}%</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useSensorData } from '../composables/useSensorData'
import { fetchAlarms } from '../api/sensor'
import LottieAnimation from '../components/LottieAnimation.vue'

const { alarms, wsConnected } = useSensorData()
const activeTab = ref('all')

const tabs = computed(() => [
  { value: 'all', label: 'ALL', count: alarms.value.length },
  { value: 'temp', label: 'TEMP', count: alarms.value.filter(a => a.alarmType?.includes('TEMP') || a.alarmType === 'BOTH_HIGH').length },
  { value: 'humidity', label: 'HUMI', count: alarms.value.filter(a => a.alarmType?.includes('HUMIDITY') || a.alarmType === 'BOTH_HIGH').length },
  { value: 'outlier', label: 'OUTLIER', count: alarms.value.filter(a => ['DATA_OUTLIER', 'PACKET_LOSS', 'DEVICE_OFFLINE'].includes(a.alarmType)).length },
])

const filteredAlarms = computed(() => {
  const sorted = alarms.value.slice().reverse()
  switch (activeTab.value) {
    case 'temp':
      return sorted.filter(a => a.alarmType?.includes('TEMP') || a.alarmType === 'BOTH_HIGH')
    case 'humidity':
      return sorted.filter(a => a.alarmType?.includes('HUMIDITY') || a.alarmType === 'BOTH_HIGH')
    case 'outlier':
      return sorted.filter(a => ['DATA_OUTLIER', 'PACKET_LOSS', 'DEVICE_OFFLINE'].includes(a.alarmType))
    default:
      return sorted
  }
})

const totalCount = computed(() => alarms.value.length)
const todayCount = computed(() => {
  const today = new Date().toISOString().slice(0, 10)
  return alarms.value.filter(a => a.timestamp?.startsWith(today)).length
})
const tempCount = computed(() => alarms.value.filter(a => a.alarmType?.includes('TEMP') || a.alarmType === 'BOTH_HIGH').length)
const humidityCount = computed(() => alarms.value.filter(a => a.alarmType?.includes('HUMIDITY') || a.alarmType === 'BOTH_HIGH').length)

async function refresh() {
  try {
    alarms.value = await fetchAlarms()
  } catch (err) {
    console.warn('刷新失败', err)
  }
}

function formatAlarmType(type) {
  const map = {
    'TEMP_HIGH': 'TEMP_HIGH',
    'HUMIDITY_HIGH': 'HUMI_HIGH',
    'BOTH_HIGH': 'CRITICAL',
    'DATA_OUTLIER': 'OUTLIER',
    'PACKET_LOSS': 'PKT_LOSS',
    'DEVICE_OFFLINE': 'OFFLINE',
  }
  return map[type] || type
}

function formatTime(ts) {
  if (!ts) return '--:--:--'
  return ts.length >= 19 ? ts.slice(11, 19) : ts
}

function formatDate(ts) {
  if (!ts) return '--'
  return ts.length >= 10 ? ts.slice(0, 10) : ts
}

function getAlarmClass(type) {
  if (!type) return ''
  if (type.includes('TEMP') || type.includes('HUMIDITY') || type.includes('BOTH')) return 'danger'
  if (type.includes('OUTLIER') || type.includes('PACKET')) return 'warning'
  return 'info'
}

function getAlarmColor(type) {
  if (type?.includes('TEMP') || type?.includes('HUMIDITY') || type?.includes('BOTH')) return 'var(--color-danger)'
  if (type?.includes('OUTLIER') || type?.includes('PACKET')) return 'var(--color-warning)'
  return 'var(--color-info)'
}
</script>

<style scoped>
.alarms-page {
  padding: var(--space-6);
  min-height: 100%;
  position: relative;
}

.page-decor {
  position: absolute;
  top: 60px;
  right: var(--space-4);
  opacity: 0.5;
  pointer-events: none;
  z-index: 0;
}

.alarms-page > *:not(.page-decor) {
  position: relative;
  z-index: 1;
}

.page-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  margin-bottom: var(--space-6);
  padding-bottom: var(--space-5);
  border-bottom: 1px solid var(--color-border);
  position: relative;
  flex-wrap: wrap;
  gap: var(--space-4);
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
  font-family: var(--font-mono);
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

.filter-tabs {
  display: flex;
  gap: var(--space-1);
  background: var(--color-surface);
  padding: var(--space-1);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
}

.tab {
  display: flex;
  align-items: center;
  gap: var(--space-1);
  padding: var(--space-2) var(--space-3);
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 600;
  color: var(--color-text-secondary);
  background: transparent;
  border: 1px solid transparent;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: all var(--duration-base);
  letter-spacing: 0.05em;
}

.tab:hover {
  color: var(--color-primary);
  background: var(--color-primary-soft);
}

.tab.active {
  color: var(--color-primary);
  background: var(--color-primary-soft);
  border-color: var(--color-primary);
  box-shadow: 0 0 8px var(--color-primary-glow);
}

.tab-bracket {
  color: var(--color-text-tertiary);
  font-weight: 300;
}

.tab.active .tab-bracket { color: var(--color-primary); }

.tab-count {
  padding: 1px 6px;
  background: var(--color-bg-elevated);
  border-radius: var(--radius-sm);
  font-size: 10px;
  color: var(--color-text-secondary);
}

.tab.active .tab-count {
  background: var(--color-primary);
  color: var(--color-text-inverse);
}

/* ============================================
   Stats
   ============================================ */

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--space-4);
  margin-bottom: var(--space-6);
}

.stat-card {
  position: relative;
  padding: var(--space-4);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  transition: all var(--duration-base);
}

.stat-card:hover {
  border-color: var(--color-border-strong);
  transform: translateY(-2px);
}

.stat-corner {
  position: absolute;
  width: 8px;
  height: 8px;
  border-color: var(--color-primary);
  opacity: 0.4;
  transition: opacity var(--duration-base);
}

.stat-corner.tl { top: 4px; left: 4px; border-top: 1px solid; border-left: 1px solid; }
.stat-corner.tr { top: 4px; right: 4px; border-top: 1px solid; border-right: 1px solid; }
.stat-corner.bl { bottom: 4px; left: 4px; border-bottom: 1px solid; border-left: 1px solid; }
.stat-corner.br { bottom: 4px; right: 4px; border-bottom: 1px solid; border-right: 1px solid; }

.stat-card:hover .stat-corner { opacity: 0.8; }

.stat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-2);
}

.stat-label {
  font-size: 9px;
  color: var(--color-text-tertiary);
  letter-spacing: 0.15em;
}

.stat-bar {
  flex: 1;
  height: 1px;
  margin-left: var(--space-2);
  background: linear-gradient(90deg, var(--color-border), transparent);
}

.stat-value {
  font-size: 32px;
  font-weight: 700;
  color: var(--color-primary);
  text-shadow: 0 0 12px var(--color-primary-glow);
  line-height: 1;
}

.stat-value.danger {
  color: var(--color-danger);
  text-shadow: 0 0 12px rgba(255, 56, 96, 0.4);
}

.stat-value.warning {
  color: var(--color-accent);
  text-shadow: 0 0 12px var(--color-accent-soft);
}

.stat-desc {
  font-size: 11px;
  color: var(--color-text-tertiary);
  margin-top: var(--space-2);
}

/* ============================================
   List Panel
   ============================================ */

.alarms-list-panel {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: var(--space-5);
  position: relative;
  overflow: hidden;
}

.alarms-list-panel::before {
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
}

.title-label {
  color: var(--color-primary);
}

.header-sub {
  font-size: 11px;
  color: var(--color-text-tertiary);
  margin-top: 2px;
}

.btn-refresh {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-3);
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  color: var(--color-text-secondary);
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.1em;
  cursor: pointer;
  transition: all var(--duration-base);
}

.btn-refresh:hover {
  background: var(--color-primary-soft);
  border-color: var(--color-primary);
  color: var(--color-primary);
}

.btn-refresh svg {
  width: 14px;
  height: 14px;
}

.empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--space-12);
  text-align: center;
  color: var(--color-text-tertiary);
}

.empty-icon {
  width: 48px;
  height: 48px;
  margin-bottom: var(--space-3);
  color: var(--color-success);
  opacity: 0.5;
}

.empty-text {
  font-size: 12px;
  color: var(--color-success);
  letter-spacing: 0.1em;
  margin-bottom: var(--space-1);
}

.empty-hint {
  font-size: 11px;
}

.alarms-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.alarm-row {
  display: grid;
  grid-template-columns: 110px 150px 1fr 130px;
  gap: var(--space-4);
  padding: var(--space-4);
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  transition: all var(--duration-base) var(--ease-out);
  position: relative;
}

.alarm-row:hover {
  transform: translateX(2px);
  box-shadow: var(--shadow-sm);
}

.alarm-row.danger {
  border-color: var(--color-danger);
  background: linear-gradient(90deg, var(--color-danger-soft), var(--color-bg-elevated) 30%);
}

.alarm-row.warning {
  border-color: var(--color-warning);
  background: linear-gradient(90deg, var(--color-warning-soft), var(--color-bg-elevated) 30%);
}

.alarm-row.info {
  border-color: var(--color-info);
  background: linear-gradient(90deg, var(--color-info-soft), var(--color-bg-elevated) 30%);
}

.row-time {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.time-main {
  font-size: 18px;
  font-weight: 700;
  color: var(--color-text-primary);
  letter-spacing: 0.02em;
}

.time-date {
  font-size: 10px;
  color: var(--color-text-tertiary);
}

.row-status {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.status-indicator {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-bg);
  border-radius: var(--radius-sm);
}

.alarm-row.danger .status-text { color: var(--color-danger); }
.alarm-row.warning .status-text { color: var(--color-warning); }
.alarm-row.info .status-text { color: var(--color-info); }

.status-text {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.05em;
}

.row-msg {
  min-width: 0;
}

.msg-text {
  font-size: 13px;
  color: var(--color-text-primary);
  line-height: 1.4;
  margin-bottom: var(--space-2);
}

.msg-advice {
  display: flex;
  align-items: flex-start;
  gap: var(--space-2);
  padding: var(--space-2);
  background: rgba(255, 184, 0, 0.08);
  border-left: 2px solid var(--color-warning);
  border-radius: var(--radius-sm);
  font-size: 11px;
  color: var(--color-warning);
  line-height: 1.4;
}

.msg-advice svg {
  width: 12px;
  height: 12px;
  flex-shrink: 0;
  margin-top: 1px;
}

.row-data {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
  align-items: flex-end;
}

.data-row {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: 2px 6px;
  background: var(--color-bg);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  min-width: 90px;
}

.data-key {
  color: var(--color-text-tertiary);
  font-size: 9px;
  font-weight: 700;
}

.data-val {
  color: var(--color-text-primary);
  font-size: 11px;
  font-weight: 600;
}

@media (max-width: 1024px) {
  .stats-grid { grid-template-columns: repeat(2, 1fr); }
  .alarm-row { grid-template-columns: 1fr; gap: var(--space-2); }
  .row-data { flex-direction: row; align-items: center; }
}
</style>
