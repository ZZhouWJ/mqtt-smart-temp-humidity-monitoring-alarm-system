<template>
  <div class="log-table">
    <div class="table-header">
      <div class="header-left">
        <svg class="header-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
          <polyline points="14 2 14 8 20 8" />
          <line x1="8" y1="13" x2="16" y2="13" />
          <line x1="8" y1="17" x2="14" y2="17" />
        </svg>
        <div>
          <div class="table-title">DATA_STREAM</div>
          <div class="table-subtitle">最近 8 条采集记录</div>
        </div>
      </div>
      <div class="header-right">
        <span class="live-indicator">
          <span class="pulse-dot" style="color: var(--color-success)"></span>
          <span class="mono">LIVE</span>
        </span>
      </div>
    </div>

    <div v-if="displayData.length === 0" class="empty">
      <div class="empty-line">// AWAITING DATA STREAM...</div>
    </div>

    <div v-else class="table-wrapper">
      <div class="table-head mono">
        <div class="th col-seq">SEQ</div>
        <div class="th col-time">TIMESTAMP</div>
        <div class="th col-num">TEMP_RAW</div>
        <div class="th col-num">TEMP_FILT</div>
        <div class="th col-num">HUMI_RAW</div>
        <div class="th col-num">HUMI_FILT</div>
        <div class="th col-status">STATUS</div>
      </div>
      <div class="table-body">
        <div
          v-for="item in displayData"
          :key="item.seq"
          class="table-row"
          :class="{
            'row-danger': item.alarmType && item.alarmType !== 'NORMAL',
            'row-warning': item.outlier
          }"
        >
          <div class="td col-seq mono">#{{ item.seq.toString().padStart(4, '0') }}</div>
          <div class="td col-time mono">{{ item.timestamp?.slice(11) || '--' }}</div>
          <div class="td col-num mono" :class="{ 'cell-danger': item.rawTemperature > 35 }">
            {{ formatNum(item.rawTemperature) }}<span class="suffix">℃</span>
          </div>
          <div class="td col-num mono">{{ formatNum(item.filteredTemperature) }}<span class="suffix">℃</span></div>
          <div class="td col-num mono" :class="{ 'cell-danger': item.rawHumidity > 80 }">
            {{ formatNum(item.rawHumidity) }}<span class="suffix">%</span>
          </div>
          <div class="td col-num mono">{{ formatNum(item.filteredHumidity) }}<span class="suffix">%</span></div>
          <div class="td col-status">
            <span class="status-chip" :class="getStatusClass(item.rawStatus)">
              {{ formatStatus(item.rawStatus) }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({ history: Array })

const displayData = computed(() => {
  return props.history?.slice().reverse().slice(0, 8) || []
})

function formatNum(v) {
  if (v == null) return '--'
  return Number(v).toFixed(1)
}

function formatStatus(s) {
  const map = {
    'normal': 'OK',
    'jump': 'JUMP',
    'temp_high': 'T_HI',
    'humidity_high': 'H_HI',
    'both_high': 'CRIT',
    'offline': 'OFF',
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
</script>

<style scoped>
.log-table {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: var(--space-4);
  display: flex;
  flex-direction: column;
  height: 100%;
  position: relative;
  overflow: hidden;
}

.log-table::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--color-primary), transparent);
  opacity: 0.5;
}

.table-header {
  display: flex;
  align-items: center;
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

.header-icon {
  width: 32px;
  height: 32px;
  padding: var(--space-2);
  background: var(--color-primary-soft);
  border: 1px solid var(--color-primary);
  border-radius: var(--radius-sm);
  color: var(--color-primary);
  box-sizing: border-box;
}

.table-title {
  font-family: var(--font-display);
  font-size: 13px;
  font-weight: 600;
  color: var(--color-text-primary);
  letter-spacing: 0.05em;
}

.table-subtitle {
  font-family: var(--font-mono);
  font-size: 10px;
  color: var(--color-text-tertiary);
  margin-top: 2px;
}

.live-indicator {
  display: flex;
  align-items: center;
  gap: var(--space-1);
  padding: 2px 8px;
  background: var(--color-success-soft);
  border: 1px solid var(--color-success);
  border-radius: var(--radius-sm);
  font-size: 10px;
  font-weight: 700;
  color: var(--color-success);
  letter-spacing: 0.1em;
}

.empty {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 200px;
}

.empty-line {
  font-family: var(--font-mono);
  font-size: 12px;
  color: var(--color-text-tertiary);
  letter-spacing: 0.05em;
  animation: blink 1.5s ease-in-out infinite;
}

@keyframes blink {
  0%, 100% { opacity: 0.5; }
  50% { opacity: 1; }
}

.table-wrapper {
  flex: 1;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.table-head, .table-row {
  display: grid;
  grid-template-columns: 80px 110px 1fr 1fr 1fr 1fr 90px;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-3);
  align-items: center;
}

.table-head {
  font-size: 9px;
  font-weight: 700;
  color: var(--color-text-tertiary);
  letter-spacing: 0.1em;
  border-bottom: 1px solid var(--color-border);
}

.table-body {
  flex: 1;
  overflow-y: auto;
}

.table-row {
  font-size: 11px;
  color: var(--color-text-secondary);
  border-bottom: 1px solid var(--color-border-subtle);
  transition: background var(--duration-base);
}

.table-row:hover {
  background: var(--color-bg-elevated);
}

.table-row.row-danger {
  background: linear-gradient(90deg, var(--color-danger-soft) 0%, transparent 100%);
  border-left: 2px solid var(--color-danger);
  padding-left: calc(var(--space-3) - 2px);
}

.table-row.row-warning {
  background: linear-gradient(90deg, var(--color-warning-soft) 0%, transparent 100%);
  border-left: 2px solid var(--color-warning);
  padding-left: calc(var(--space-3) - 2px);
}

.col-num {
  text-align: right;
}

.col-status {
  display: flex;
  justify-content: center;
}

.suffix {
  color: var(--color-text-tertiary);
  font-size: 9px;
  margin-left: 2px;
}

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

.status-chip.ok {
  background: var(--color-success-soft);
  color: var(--color-success);
  border: 1px solid var(--color-success);
}

.status-chip.warning {
  background: var(--color-warning-soft);
  color: var(--color-warning);
  border: 1px solid var(--color-warning);
}

.status-chip.danger {
  background: var(--color-danger-soft);
  color: var(--color-danger);
  border: 1px solid var(--color-danger);
  animation: pulse-chip 1s ease-in-out infinite;
}

.status-chip.offline {
  background: var(--color-bg-elevated);
  color: var(--color-text-tertiary);
  border: 1px solid var(--color-border);
}

.status-chip.info {
  background: var(--color-info-soft);
  color: var(--color-info);
  border: 1px solid var(--color-info);
}

@keyframes pulse-chip {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.6; }
}
</style>
