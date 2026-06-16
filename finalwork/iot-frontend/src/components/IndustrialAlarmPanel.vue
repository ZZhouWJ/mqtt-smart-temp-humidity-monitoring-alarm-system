<template>
  <div class="alarm-panel">
    <div class="panel-header">
      <div class="header-left">
        <div class="indicator" :class="alarms.length > 0 ? 'active' : 'idle'">
          <span class="pulse-dot" :style="{ color: alarms.length > 0 ? 'var(--color-danger)' : 'var(--color-success)' }"></span>
        </div>
        <div>
          <div class="panel-title">ALARM_LOG</div>
          <div class="panel-subtitle">实时报警流</div>
        </div>
      </div>
      <div class="count-badge mono">
        <span class="count-label">COUNT</span>
        <span class="count-value">{{ alarms.length.toString().padStart(3, '0') }}</span>
      </div>
    </div>

    <div v-if="alarms.length === 0" class="empty">
      <div class="empty-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <circle cx="12" cy="12" r="10" />
          <path d="M8 14s1.5 2 4 2 4-2 4-2" />
          <circle cx="9" cy="9" r="0.5" fill="currentColor" />
          <circle cx="15" cy="9" r="0.5" fill="currentColor" />
        </svg>
      </div>
      <div class="empty-text">SYSTEM_NOMINAL</div>
      <div class="empty-hint">所有传感器读数正常</div>
    </div>

    <div v-else class="alarm-list">
      <TransitionGroup name="alarm">
        <div
          v-for="(item, index) in displayAlarms"
          :key="item.timestamp + index"
          class="alarm-item"
          :class="getAlarmClass(item.alarmType)"
        >
          <div class="alarm-marker">
            <div class="marker-line"></div>
            <div class="marker-dot"></div>
          </div>
          <div class="alarm-content">
            <div class="alarm-header">
              <span class="alarm-type mono">{{ formatAlarmType(item.alarmType) }}</span>
              <span class="alarm-time mono">{{ formatTime(item.timestamp) }}</span>
            </div>
            <div class="alarm-message">{{ item.alarmMessage }}</div>
            <div v-if="item.diagnosisAdvice" class="alarm-advice">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <circle cx="12" cy="12" r="10" />
                <line x1="12" y1="16" x2="12" y2="12" />
                <line x1="12" y1="8" x2="12.01" y2="8" />
              </svg>
              <span>{{ item.diagnosisAdvice }}</span>
            </div>
            <div class="alarm-data">
              <span class="data-chip">
                <span class="chip-key">T</span>
                <span class="chip-val mono">{{ item.temperature }}℃</span>
              </span>
              <span class="data-chip">
                <span class="chip-key">H</span>
                <span class="chip-val mono">{{ item.humidity }}%</span>
              </span>
            </div>
          </div>
        </div>
      </TransitionGroup>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({ alarms: Array })

const displayAlarms = computed(() => {
  return props.alarms?.slice().reverse().slice(0, 5) || []
})

function formatAlarmType(type) {
  const map = {
    'TEMP_HIGH': '[TEMP_HIGH]',
    'HUMIDITY_HIGH': '[HUMI_HIGH]',
    'BOTH_HIGH': '[CRITICAL]',
    'DATA_OUTLIER': '[OUTLIER]',
    'PACKET_LOSS': '[PKT_LOSS]',
    'DEVICE_OFFLINE': '[OFFLINE]',
  }
  return map[type] || `[${type}]`
}

function formatTime(ts) {
  if (!ts) return '--:--:--'
  return ts.length >= 19 ? ts.slice(11, 19) : ts
}

function getAlarmClass(type) {
  if (!type) return ''
  if (type.includes('TEMP') || type.includes('HUMIDITY') || type.includes('BOTH')) return 'danger'
  if (type.includes('OUTLIER') || type.includes('PACKET')) return 'warning'
  return 'info'
}
</script>

<style scoped>
.alarm-panel {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: var(--space-4);
  height: 100%;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
}

.alarm-panel::before {
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
  margin-bottom: var(--space-3);
  padding-bottom: var(--space-3);
  border-bottom: 1px dashed var(--color-border);
}

.header-left {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: var(--radius-sm);
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border);
}

.indicator.active {
  background: var(--color-danger-soft);
  border-color: var(--color-danger);
  box-shadow: 0 0 10px rgba(255, 56, 96, 0.3);
}

.indicator.idle {
  background: var(--color-success-soft);
  border-color: var(--color-success);
}

.panel-title {
  font-family: var(--font-display);
  font-size: 13px;
  font-weight: 600;
  color: var(--color-text-primary);
  letter-spacing: 0.05em;
}

.panel-subtitle {
  font-family: var(--font-mono);
  font-size: 10px;
  color: var(--color-text-tertiary);
  margin-top: 2px;
}

.count-badge {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-1) var(--space-2);
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
}

.count-label {
  font-size: 9px;
  color: var(--color-text-tertiary);
  letter-spacing: 0.1em;
}

.count-value {
  font-size: 12px;
  font-weight: 700;
  color: var(--color-accent);
  text-shadow: 0 0 8px var(--color-accent-soft);
}

.empty {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--space-6);
  text-align: center;
  min-height: 200px;
}

.empty-icon {
  color: var(--color-success);
  opacity: 0.4;
  margin-bottom: var(--space-3);
}

.empty-icon svg { width: 48px; height: 48px; }

.empty-text {
  font-family: var(--font-mono);
  font-size: 12px;
  font-weight: 600;
  color: var(--color-success);
  letter-spacing: 0.1em;
  margin-bottom: var(--space-1);
}

.empty-hint {
  font-size: 11px;
  color: var(--color-text-tertiary);
}

.alarm-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  overflow-y: auto;
  flex: 1;
}

.alarm-item {
  display: flex;
  gap: var(--space-3);
  padding: var(--space-3);
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  position: relative;
  transition: all var(--duration-base) var(--ease-out);
}

.alarm-item:hover {
  transform: translateX(2px);
}

.alarm-item.danger {
  background: linear-gradient(90deg, var(--color-danger-soft), var(--color-bg-elevated));
  border-color: var(--color-danger);
}

.alarm-item.warning {
  background: linear-gradient(90deg, var(--color-warning-soft), var(--color-bg-elevated));
  border-color: var(--color-warning);
}

.alarm-item.info {
  background: linear-gradient(90deg, var(--color-info-soft), var(--color-bg-elevated));
  border-color: var(--color-info);
}

.alarm-marker {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex-shrink: 0;
}

.marker-line {
  width: 1px;
  flex: 1;
  background: currentColor;
  opacity: 0.3;
}

.marker-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: currentColor;
  box-shadow: 0 0 8px currentColor;
}

.alarm-item.danger { color: var(--color-danger); }
.alarm-item.warning { color: var(--color-warning); }
.alarm-item.info { color: var(--color-info); }

.alarm-content {
  flex: 1;
  min-width: 0;
}

.alarm-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-1);
}

.alarm-type {
  font-size: 10px;
  font-weight: 700;
  color: currentColor;
  letter-spacing: 0.05em;
}

.alarm-time {
  font-size: 10px;
  color: var(--color-text-tertiary);
  letter-spacing: 0.05em;
}

.alarm-message {
  font-size: 12px;
  color: var(--color-text-primary);
  line-height: 1.4;
  margin-bottom: var(--space-2);
}

.alarm-advice {
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
  margin-bottom: var(--space-2);
}

.alarm-advice svg {
  width: 12px;
  height: 12px;
  flex-shrink: 0;
  margin-top: 1px;
}

.alarm-data {
  display: flex;
  gap: var(--space-2);
}

.data-chip {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 2px 6px;
  background: var(--color-bg);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  font-size: 10px;
}

.chip-key {
  color: var(--color-text-tertiary);
  font-family: var(--font-mono);
  font-weight: 700;
}

.chip-val {
  color: var(--color-text-primary);
}

/* Transitions */
.alarm-enter-active { animation: alarm-in 0.3s var(--ease-out); }
.alarm-leave-active { animation: alarm-out 0.3s var(--ease-in-out); }

@keyframes alarm-in {
  from { opacity: 0; transform: translateX(-20px); }
  to { opacity: 1; transform: translateX(0); }
}

@keyframes alarm-out {
  to { opacity: 0; transform: translateX(20px); }
}
</style>
