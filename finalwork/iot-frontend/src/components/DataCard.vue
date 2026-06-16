<template>
  <div class="data-card" :class="{ danger, warning, [`type-${type}`]: true }">
    <div class="card-corner top-left"></div>
    <div class="card-corner top-right"></div>
    <div class="card-corner bottom-left"></div>
    <div class="card-corner bottom-right"></div>

    <div class="card-glow"></div>

    <div class="card-header">
      <div class="header-left">
        <div class="lottie-icon" :class="{ active: hasValue && !danger }">
          <LottieAnimation
            :type="icon"
            :size="32"
            :speed="0.8"
            :color="iconColor"
          />
        </div>
        <span class="label">{{ label }}</span>
      </div>
      <span v-if="danger" class="badge danger">
        <span class="badge-dot"></span>
        CRIT
      </span>
      <span v-else-if="warning" class="badge warn">WARN</span>
      <span v-else-if="hasValue" class="badge ok">OK</span>
    </div>

    <div class="card-value">
      <span class="value" :class="{ 'value-danger': danger, 'value-warning': warning }">
        {{ formattedValue }}
      </span>
      <span class="unit">{{ unit }}</span>
    </div>

    <div class="card-footer">
      <div class="footer-row">
        <span class="sub">{{ sub }}</span>
        <span v-if="subStatus" class="sub-status mono">{{ subStatus }}</span>
      </div>
      <div v-if="hasValue && (type === 'temp' || type === 'humi')" class="progress-bar">
        <div
          class="progress-fill"
          :class="{ danger, warning }"
          :style="{ width: `${progressPercent}%` }"
        >
          <div class="progress-shine"></div>
        </div>
        <div class="progress-ticks">
          <span v-for="i in 5" :key="i"></span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import LottieAnimation from './LottieAnimation.vue'

const props = defineProps({
  label: String,
  value: [String, Number],
  unit: String,
  sub: String,
  subStatus: String,
  danger: Boolean,
  warning: Boolean,
  type: { type: String, default: 'temp' },
  icon: { type: String, default: 'thermometer' },
})

const hasValue = computed(() => props.value !== '--' && props.value !== null && props.value !== undefined)

const formattedValue = computed(() => {
  if (!hasValue.value) return '--'
  const num = Number(props.value)
  if (isNaN(num)) return props.value
  return num.toFixed(1)
})

const progressPercent = computed(() => {
  if (!hasValue.value) return 0
  const num = Number(props.value)
  if (props.type === 'temp') {
    return Math.min(100, Math.max(0, ((num + 10) / 50) * 100))
  }
  if (props.type === 'humi') {
    return Math.min(100, Math.max(0, num))
  }
  return 50
})

const iconColor = computed(() => {
  if (props.danger) return '#ff3860'
  if (props.warning) return '#ffb800'
  if (props.type === 'temp') return '#00d9ff'
  if (props.type === 'humi') return '#00ff9d'
  if (props.type === 'device') return '#4cc9f0'
  if (props.type === 'alarm') return '#ff9e00'
  return '#00d9ff'
})
</script>

<style scoped>
.data-card {
  position: relative;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: var(--space-4);
  transition: all var(--duration-base) var(--ease-out);
  overflow: hidden;
}

.card-glow {
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle at center, var(--color-primary-soft) 0%, transparent 50%);
  opacity: 0;
  transition: opacity var(--duration-slow);
  pointer-events: none;
}

.data-card:hover .card-glow { opacity: 0.5; }

.data-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--color-primary), transparent);
  opacity: 0;
  transition: opacity var(--duration-base);
}

.data-card:hover {
  border-color: var(--color-border-strong);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.data-card:hover::before { opacity: 0.6; }

.data-card.danger {
  background: linear-gradient(135deg, var(--color-danger-soft), var(--color-surface));
  border-color: var(--color-danger);
  animation: card-alarm 1s ease-in-out infinite;
}

@keyframes card-alarm {
  0%, 100% { box-shadow: 0 0 0 0 rgba(255, 56, 96, 0.2); }
  50% { box-shadow: 0 0 20px 0 rgba(255, 56, 96, 0.4); }
}

.data-card.warning {
  background: linear-gradient(135deg, var(--color-warning-soft), var(--color-surface));
  border-color: var(--color-warning);
}

.card-corner {
  position: absolute;
  width: 8px;
  height: 8px;
  border-color: var(--color-primary);
  opacity: 0.4;
  transition: opacity var(--duration-base);
}

.card-corner.top-left { top: 4px; left: 4px; border-top: 1px solid; border-left: 1px solid; }
.card-corner.top-right { top: 4px; right: 4px; border-top: 1px solid; border-right: 1px solid; }
.card-corner.bottom-left { bottom: 4px; left: 4px; border-bottom: 1px solid; border-left: 1px solid; }
.card-corner.bottom-right { bottom: 4px; right: 4px; border-bottom: 1px solid; border-right: 1px solid; }

.data-card:hover .card-corner { opacity: 0.8; }
.data-card.danger .card-corner { border-color: var(--color-danger); opacity: 1; }
.data-card.warning .card-corner { border-color: var(--color-warning); opacity: 1; }

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-3);
}

.header-left {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.lottie-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: var(--radius-sm);
  background: var(--color-primary-soft);
  border: 1px solid var(--color-border);
  transition: all var(--duration-base);
}

.lottie-icon.active {
  border-color: var(--color-primary);
  box-shadow: 0 0 12px var(--color-primary-glow);
}

.data-card.danger .lottie-icon {
  background: var(--color-danger-soft);
  border-color: var(--color-danger);
  box-shadow: 0 0 12px rgba(255, 56, 96, 0.3);
}

.data-card.warning .lottie-icon {
  background: var(--color-warning-soft);
  border-color: var(--color-warning);
}

.label {
  font-family: var(--font-mono);
  font-size: 10px;
  font-weight: 600;
  color: var(--color-text-tertiary);
  letter-spacing: 0.15em;
}

.badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-family: var(--font-mono);
  font-size: 9px;
  font-weight: 700;
  padding: 2px 6px;
  border-radius: var(--radius-sm);
  letter-spacing: 0.1em;
}

.badge-dot {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: currentColor;
  animation: pulse-dot 0.8s ease-in-out infinite;
}

.badge.ok { color: var(--color-success); background: var(--color-success-soft); border: 1px solid var(--color-success); }
.badge.warn { color: var(--color-warning); background: var(--color-warning-soft); border: 1px solid var(--color-warning); }
.badge.danger { color: var(--color-danger); background: var(--color-danger-soft); border: 1px solid var(--color-danger); animation: blink 0.8s ease-in-out infinite; }

@keyframes pulse-dot {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.4; transform: scale(0.6); }
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.card-value {
  display: flex;
  align-items: baseline;
  gap: var(--space-1);
  margin-bottom: var(--space-3);
}

.value {
  font-family: var(--font-mono);
  font-size: 36px;
  font-weight: 700;
  color: var(--color-text-primary);
  letter-spacing: -0.02em;
  line-height: 1;
  transition: all var(--duration-base);
}

.value-danger {
  color: var(--color-danger);
  text-shadow: 0 0 12px rgba(255, 56, 96, 0.5);
}

.value-warning {
  color: var(--color-warning);
  text-shadow: 0 0 12px rgba(255, 184, 0, 0.5);
}

.unit {
  font-family: var(--font-mono);
  font-size: 14px;
  color: var(--color-text-tertiary);
  font-weight: 500;
}

.card-footer {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.footer-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-2);
}

.sub {
  font-size: 11px;
  color: var(--color-text-tertiary);
}

.sub-status {
  font-size: 10px;
  color: var(--color-text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.progress-bar {
  position: relative;
  height: 4px;
  background: var(--color-bg-elevated);
  border-radius: var(--radius-full);
  overflow: hidden;
}

.progress-fill {
  position: relative;
  height: 100%;
  background: var(--color-primary);
  border-radius: var(--radius-full);
  transition: width 0.5s var(--ease-out), background 0.3s;
  box-shadow: 0 0 8px currentColor;
  overflow: hidden;
}

.progress-fill.warning { background: var(--color-warning); }
.progress-fill.danger { background: var(--color-danger); }

.progress-shine {
  position: absolute;
  top: 0;
  left: -100%;
  width: 50%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
  animation: shine 2s ease-in-out infinite;
}

@keyframes shine {
  to { left: 200%; }
}

.progress-ticks {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  justify-content: space-between;
  padding: 0 20%;
  pointer-events: none;
}

.progress-ticks span {
  width: 1px;
  height: 100%;
  background: rgba(255, 255, 255, 0.1);
}
</style>
