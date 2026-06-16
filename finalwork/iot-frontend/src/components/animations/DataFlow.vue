<template>
  <svg :width="size" :height="size" viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
    <!-- Central node -->
    <circle cx="40" cy="40" r="10" stroke="currentColor" stroke-width="2" fill="none" />
    <circle cx="40" cy="40" r="4" fill="currentColor" class="pulse-dot" />

    <!-- Connecting lines with flowing dots -->
    <path d="M40 30 L40 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-opacity="0.5" />
    <path d="M50 40 L68 40" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-opacity="0.5" />
    <path d="M40 50 L40 68" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-opacity="0.5" />
    <path d="M30 40 L12 40" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-opacity="0.5" />

    <!-- Data flow dots -->
    <circle r="2" fill="currentColor" class="flow-dot-1" />
    <circle r="2" fill="currentColor" class="flow-dot-2" />
    <circle r="2" fill="currentColor" class="flow-dot-3" />
    <circle r="2" fill="currentColor" class="flow-dot-4" />

    <!-- Outer nodes -->
    <circle cx="40" cy="8" r="4" stroke="currentColor" stroke-width="1.5" fill="none" />
    <circle cx="72" cy="40" r="4" stroke="currentColor" stroke-width="1.5" fill="none" />
    <circle cx="40" cy="72" r="4" stroke="currentColor" stroke-width="1.5" fill="none" />
    <circle cx="8" cy="40" r="4" stroke="currentColor" stroke-width="1.5" fill="none" />
  </svg>
</template>

<script setup>
defineProps({
  size: {
    type: Number,
    default: 80,
  },
})
</script>

<style scoped>
.pulse-dot {
  animation: pulse 2s ease-in-out infinite;
}

.flow-dot-1 {
  animation: flow-top 3s ease-in-out infinite;
}
.flow-dot-2 {
  animation: flow-right 3s ease-in-out infinite 0.75s;
}
.flow-dot-3 {
  animation: flow-bottom 3s ease-in-out infinite 1.5s;
}
.flow-dot-4 {
  animation: flow-left 3s ease-in-out infinite 2.25s;
}

@keyframes pulse {
  0%, 100% { opacity: 0.4; transform: scale(1); }
  50% { opacity: 1; transform: scale(1.2); }
}

@keyframes flow-top {
  0% { transform: translate(0, 0); opacity: 0; }
  10% { opacity: 1; }
  90% { opacity: 1; }
  100% { transform: translate(0, -22px); opacity: 0; }
}
@keyframes flow-right {
  0% { transform: translate(0, 0); opacity: 0; }
  10% { opacity: 1; }
  90% { opacity: 1; }
  100% { transform: translate(22px, 0); opacity: 0; }
}
@keyframes flow-bottom {
  0% { transform: translate(0, 0); opacity: 0; }
  10% { opacity: 1; }
  90% { opacity: 1; }
  100% { transform: translate(0, 22px); opacity: 0; }
}
@keyframes flow-left {
  0% { transform: translate(0, 0); opacity: 0; }
  10% { opacity: 1; }
  90% { opacity: 1; }
  100% { transform: translate(-22px, 0); opacity: 0; }
}
</style>
