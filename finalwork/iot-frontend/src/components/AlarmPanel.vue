<template>
  <div class="panel" :class="{ 'has-alarms': alarms.length > 0 }">
    <div class="panel-header">
      <h3 class="panel-title">
        <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9" />
          <path d="M13.73 21a2 2 0 0 1-3.46 0" />
        </svg>
        报警记录
      </h3>
      <span v-if="alarms.length > 0" class="count-badge">{{ alarms.length }}</span>
    </div>

    <div v-if="alarms.length === 0" class="empty-state">
      <svg class="empty-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
        <circle cx="12" cy="12" r="10" />
        <path d="M8 14s1.5 2 4 2 4-2 4-2" />
        <line x1="9" y1="9" x2="9.01" y2="9" />
        <line x1="15" y1="9" x2="15.01" y2="9" />
      </svg>
      <span class="empty-text">系统运行正常</span>
      <span class="empty-hint">暂无报警记录</span>
    </div>

    <div v-else class="alarm-list">
      <TransitionGroup name="alarm">
        <div
          v-for="(item, index) in displayAlarms"
          :key="item.timestamp + index"
          class="alarm-item"
          :class="getAlarmClass(item.alarmType)"
        >
          <div class="alarm-header">
            <span class="alarm-type">{{ formatAlarmType(item.alarmType) }}</span>
            <span class="alarm-time">{{ formatTime(item.timestamp) }}</span>
          </div>

          <div class="alarm-message">{{ item.alarmMessage }}</div>

          <div v-if="item.diagnosisAdvice" class="alarm-advice">
            <svg class="advice-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <circle cx="12" cy="12" r="10" />
              <line x1="12" y1="16" x2="12" y2="12" />
              <line x1="12" y1="8" x2="12.01" y2="8" />
            </svg>
            <span>{{ item.diagnosisAdvice }}</span>
          </div>

          <div class="alarm-data">
            <span class="data-item">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M14 4v10.54a4 4 0 1 1-4 0V4a2 2 0 1 1 4 0Z" />
              </svg>
              {{ item.temperature }}℃
            </span>
            <span class="data-item">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z" />
              </svg>
              {{ item.humidity }}%
            </span>
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
  return props.alarms?.slice().reverse().slice(0, 6) || []
})

function formatAlarmType(type) {
  const map = {
    'TEMP_HIGH': '高温告警',
    'HUMIDITY_HIGH': '高湿告警',
    'BOTH_HIGH': '复合告警',
    'DATA_OUTLIER': '数据异常',
    'PACKET_LOSS': '丢包告警',
    'DEVICE_OFFLINE': '设备离线',
  }
  return map[type] || type
}

function formatTime(timestamp) {
  if (!timestamp) return ''
  return timestamp.slice(11, 19)
}

function getAlarmClass(type) {
  if (!type) return ''
  if (type.includes('TEMP') || type.includes('HUMIDITY') || type.includes('BOTH')) {
    return 'alarm-danger'
  }
  if (type.includes('OUTLIER') || type.includes('PACKET')) {
    return 'alarm-warning'
  }
  return 'alarm-info'
}
</script>

<style scoped>
.panel {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--space-5);
  box-shadow: var(--shadow-sm);
  height: fit-content;
  max-height: 600px;
  display: flex;
  flex-direction: column;
}

.panel.has-alarms {
  border-color: rgba(220, 38, 38, 0.2);
}

.panel-header {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  margin-bottom: var(--space-4);
  padding-bottom: var(--space-3);
  border-bottom: 1px solid var(--color-border-subtle);
  flex-shrink: 0;
}

.panel-title {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0;
}

.panel-title .icon {
  width: 18px;
  height: 18px;
  color: var(--color-text-tertiary);
}

.count-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 20px;
  height: 20px;
  padding: 0 6px;
  font-size: 11px;
  font-weight: 600;
  color: var(--color-text-inverse);
  background: var(--color-danger);
  border-radius: var(--radius-full);
  animation: badge-bounce 0.5s ease-out;
}

@keyframes badge-bounce {
  0% { transform: scale(0); }
  50% { transform: scale(1.2); }
  100% { transform: scale(1); }
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--space-8) var(--space-4);
  color: var(--color-text-tertiary);
  text-align: center;
  flex: 1;
}

.empty-icon {
  width: 48px;
  height: 48px;
  margin-bottom: var(--space-4);
  opacity: 0.4;
  color: var(--color-success);
}

.empty-text {
  font-size: 14px;
  font-weight: 500;
  color: var(--color-success);
}

.empty-hint {
  font-size: 12px;
  margin-top: var(--space-1);
  color: var(--color-text-tertiary);
}

.alarm-list {
  overflow-y: auto;
  flex: 1;
  padding-right: var(--space-2);
}

.alarm-item {
  padding: var(--space-4);
  background: var(--color-surface-hover);
  border: 1px solid var(--color-border-subtle);
  border-radius: var(--radius-md);
  margin-bottom: var(--space-3);
  transition: all var(--transition-fast);
  position: relative;
  overflow: hidden;
}

.alarm-item::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 3px;
  background: var(--color-primary);
}

.alarm-item:hover {
  border-color: var(--color-border);
  box-shadow: var(--shadow-sm);
  transform: translateX(2px);
}

.alarm-item:last-child {
  margin-bottom: 0;
}

.alarm-danger {
  background: var(--color-danger-bg);
  border-color: rgba(220, 38, 38, 0.2);
}

.alarm-danger::before {
  background: var(--color-danger);
  animation: alarm-pulse 1s ease-in-out infinite;
}

.alarm-warning {
  background: var(--color-warning-bg);
  border-color: rgba(217, 119, 6, 0.2);
}

.alarm-warning::before {
  background: var(--color-warning);
}

.alarm-info {
  background: var(--color-info-bg);
  border-color: rgba(2, 132, 199, 0.2);
}

.alarm-info::before {
  background: var(--color-info);
}

@keyframes alarm-pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.alarm-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-2);
  margin-bottom: var(--space-2);
}

.alarm-type {
  font-size: 11px;
  font-weight: 600;
  padding: var(--space-1) var(--space-2);
  border-radius: var(--radius-sm);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.alarm-danger .alarm-type {
  color: var(--color-danger);
  background: rgba(220, 38, 38, 0.1);
}

.alarm-warning .alarm-type {
  color: var(--color-warning);
  background: rgba(217, 119, 6, 0.1);
}

.alarm-info .alarm-type {
  color: var(--color-info);
  background: rgba(2, 132, 199, 0.1);
}

.alarm-time {
  font-size: 11px;
  color: var(--color-text-tertiary);
  font-family: var(--font-mono);
}

.alarm-message {
  font-size: 13px;
  color: var(--color-text-primary);
  line-height: 1.5;
}

.alarm-advice {
  display: flex;
  align-items: flex-start;
  gap: var(--space-2);
  margin-top: var(--space-3);
  padding: var(--space-3);
  font-size: 12px;
  background: rgba(255, 255, 255, 0.5);
  border-radius: var(--radius-sm);
  color: var(--color-warning);
  line-height: 1.5;
}

.advice-icon {
  flex-shrink: 0;
  width: 14px;
  height: 14px;
  margin-top: 1px;
}

.alarm-data {
  display: flex;
  gap: var(--space-4);
  margin-top: var(--space-3);
  padding-top: var(--space-3);
  border-top: 1px solid var(--color-border-subtle);
}

.data-item {
  display: flex;
  align-items: center;
  gap: var(--space-1);
  font-size: 11px;
  color: var(--color-text-tertiary);
  font-family: var(--font-mono);
}

.data-item svg {
  width: 12px;
  height: 12px;
}

/* Transition animations */
.alarm-enter-active {
  animation: alarm-slide-in 0.3s ease-out;
}

.alarm-leave-active {
  animation: alarm-slide-out 0.3s ease-in;
}

@keyframes alarm-slide-in {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes alarm-slide-out {
  from {
    opacity: 1;
    transform: translateX(0);
  }
  to {
    opacity: 0;
    transform: translateX(20px);
  }
}
</style>
