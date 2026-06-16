<template>
  <Transition name="loader">
    <div v-if="visible" class="loader-screen">
      <div class="loader-bg">
        <LottieScene :show-floaters="true" />
      </div>

      <div class="loader-content">
        <div class="loader-logo">
          <LottieAnimation
            type="dataflow"
            :src="mainAnimation"
            :size="180"
            :speed="1"
            color="#00d9ff"
          />
        </div>

        <div class="loader-text">
          <div class="loader-title">
            SENTINEL<span class="accent">.IoT</span>
          </div>
          <div class="loader-subtitle mono">INITIALIZING SYSTEM</div>
        </div>

        <div class="loader-bar">
          <div class="loader-progress" :style="{ width: progress + '%' }"></div>
          <div class="loader-progress-glow" :style="{ left: progress + '%' }"></div>
        </div>

        <div class="loader-status mono">
          <span class="status-text">{{ statusText }}</span>
          <span class="status-percent">{{ progress.toString().padStart(3, '0') }}%</span>
        </div>

        <div class="loader-steps">
          <div
            v-for="(step, idx) in steps"
            :key="idx"
            class="step"
            :class="{ done: progress > (idx + 1) * 25, active: currentStep === idx }"
          >
            <span class="step-dot"></span>
            <span class="step-text mono">{{ step }}</span>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, computed } from 'vue'
import LottieAnimation from './LottieAnimation.vue'
import LottieScene from './LottieScene.vue'

const props = defineProps({
  show: { type: Boolean, default: true },
  duration: { type: Number, default: 2000 },
})

const visible = ref(props.show)
const progress = ref(0)

const steps = [
  'CONNECTING_MQTT',
  'LOADING_HISTORY',
  'INITIALIZING_WS',
  'SYSTEM_READY',
]

const currentStep = computed(() => Math.min(3, Math.floor(progress.value / 25)))

const statusText = computed(() => {
  if (progress.value < 25) return '> Establishing MQTT connection...'
  if (progress.value < 50) return '> Fetching historical data...'
  if (progress.value < 75) return '> Opening WebSocket...'
  if (progress.value < 100) return '> Calibrating sensors...'
  return '> System online'
})

// LottieFiles 公开 CDN - 数据流动画
const mainAnimation = 'https://assets1.lottiefiles.com/packages/lf20_obhph3sh.json'

let timer = null

onMounted(() => {
  if (!props.show) {
    visible.value = false
    return
  }
  const interval = 30
  const increment = (interval / props.duration) * 100
  timer = setInterval(() => {
    progress.value = Math.min(100, progress.value + increment)
    if (progress.value >= 100) {
      clearInterval(timer)
      setTimeout(() => { visible.value = false }, 400)
    }
  }, interval)
})

onBeforeUnmount(() => {
  if (timer) clearInterval(timer)
})
</script>

<style scoped>
.loader-screen {
  position: fixed;
  inset: 0;
  background: var(--color-bg);
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.loader-bg {
  position: absolute;
  inset: 0;
  opacity: 0.4;
}

.loader-content {
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-6);
  padding: var(--space-8);
  text-align: center;
  max-width: 480px;
}

.loader-logo {
  position: relative;
  width: 180px;
  height: 180px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.loader-logo::before,
.loader-logo::after {
  content: '';
  position: absolute;
  inset: 0;
  border: 1px solid var(--color-primary);
  border-radius: 50%;
  opacity: 0.4;
}

.loader-logo::before {
  animation: ring-expand 2s ease-out infinite;
}

.loader-logo::after {
  animation: ring-expand 2s ease-out infinite 1s;
}

@keyframes ring-expand {
  0% { transform: scale(0.8); opacity: 0.6; }
  100% { transform: scale(1.6); opacity: 0; }
}

.loader-text {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.loader-title {
  font-family: var(--font-display);
  font-size: 32px;
  font-weight: 700;
  color: var(--color-text-primary);
  letter-spacing: 0.05em;
  text-shadow: 0 0 20px var(--color-primary-glow);
}

.accent { color: var(--color-primary); }

.loader-subtitle {
  font-size: 11px;
  color: var(--color-primary);
  letter-spacing: 0.3em;
}

.loader-bar {
  position: relative;
  width: 100%;
  max-width: 320px;
  height: 4px;
  background: var(--color-bg-elevated);
  border-radius: var(--radius-full);
  overflow: visible;
  border: 1px solid var(--color-border);
}

.loader-progress {
  height: 100%;
  background: linear-gradient(90deg, var(--color-primary), var(--color-success));
  border-radius: var(--radius-full);
  transition: width 0.1s linear;
  box-shadow: 0 0 10px var(--color-primary);
}

.loader-progress-glow {
  position: absolute;
  top: 50%;
  transform: translate(-50%, -50%);
  width: 12px;
  height: 12px;
  background: var(--color-primary);
  border-radius: 50%;
  box-shadow: 0 0 12px var(--color-primary), 0 0 24px var(--color-primary);
  transition: left 0.1s linear;
}

.loader-status {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  max-width: 320px;
  font-size: 11px;
  color: var(--color-text-tertiary);
  letter-spacing: 0.05em;
}

.status-text {
  color: var(--color-primary);
  font-weight: 500;
  flex: 1;
  text-align: left;
}

.status-percent {
  color: var(--color-accent);
  font-weight: 700;
  text-shadow: 0 0 8px var(--color-accent-soft);
}

.loader-steps {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  width: 100%;
  max-width: 320px;
  text-align: left;
}

.step {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: 10px;
  color: var(--color-text-tertiary);
  letter-spacing: 0.1em;
  transition: all var(--duration-base);
}

.step.active {
  color: var(--color-primary);
}

.step.done {
  color: var(--color-success);
}

.step-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border);
  transition: all var(--duration-base);
  flex-shrink: 0;
}

.step.active .step-dot {
  background: var(--color-primary);
  border-color: var(--color-primary);
  box-shadow: 0 0 8px var(--color-primary);
  animation: pulse-step 1s ease-in-out infinite;
}

.step.done .step-dot {
  background: var(--color-success);
  border-color: var(--color-success);
}

@keyframes pulse-step {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.3); }
}

.loader-enter-active, .loader-leave-active {
  transition: opacity 0.5s var(--ease-out);
}

.loader-enter-from, .loader-leave-to {
  opacity: 0;
}
</style>
