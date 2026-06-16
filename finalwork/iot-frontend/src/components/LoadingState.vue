<template>
  <div class="loading-state">
    <div class="loading-animation">
      <svg class="sensor-icon" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
        <!-- Central sensor node -->
        <circle cx="24" cy="24" r="6" stroke="currentColor" stroke-width="2" fill="none" />
        <circle cx="24" cy="24" r="2" fill="currentColor" class="pulse" />

        <!-- Scanning arc -->
        <path
          d="M24 8 A16 16 0 0 1 40 24"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          fill="none"
          class="scan-arc"
        />

        <!-- Data lines -->
        <line x1="24" y1="18" x2="24" y2="12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" opacity="0.4" />
        <line x1="30" y1="24" x2="36" y2="24" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" opacity="0.4" />
        <line x1="24" y1="30" x2="24" y2="36" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" opacity="0.4" />
        <line x1="18" y1="24" x2="12" y2="24" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" opacity="0.4" />
      </svg>
    </div>
    <div class="loading-text">{{ text }}</div>
    <div class="loading-dots">
      <span></span>
      <span></span>
      <span></span>
    </div>
  </div>
</template>

<script setup>
defineProps({
  text: {
    type: String,
    default: '正在连接数据源...',
  },
})
</script>

<style scoped>
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--space-12);
  color: var(--color-text-tertiary);
}

.loading-animation {
  margin-bottom: var(--space-4);
}

.sensor-icon {
  width: 48px;
  height: 48px;
  color: var(--color-primary);
}

.pulse {
  animation: pulse 1.5s ease-in-out infinite;
}

.scan-arc {
  stroke-dasharray: 25 75;
  animation: scan 2s linear infinite;
  transform-origin: center;
}

@keyframes pulse {
  0%, 100% { opacity: 0.5; }
  50% { opacity: 1; }
}

@keyframes scan {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.loading-text {
  font-size: 13px;
  color: var(--color-text-secondary);
  margin-bottom: var(--space-3);
}

.loading-dots {
  display: flex;
  gap: var(--space-2);
}

.loading-dots span {
  width: 6px;
  height: 6px;
  background: var(--color-primary);
  border-radius: 50%;
  animation: bounce 1.4s ease-in-out infinite;
}

.loading-dots span:nth-child(1) { animation-delay: 0s; }
.loading-dots span:nth-child(2) { animation-delay: 0.2s; }
.loading-dots span:nth-child(3) { animation-delay: 0.4s; }

@keyframes bounce {
  0%, 80%, 100% { transform: scale(0.6); opacity: 0.4; }
  40% { transform: scale(1); opacity: 1; }
}
</style>
