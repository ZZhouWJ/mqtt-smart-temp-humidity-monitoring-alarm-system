<template>
  <svg :width="size" :height="size" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
    <!-- Cloud shape -->
    <path
      d="M52 36c4.4 0 8-3.6 8-8s-3.6-8-8-8c-.3 0-.7 0-1 .1C49.5 14.1 44.3 10 38 10c-8.3 0-15 6.7-15 15 0 .3 0 .7.1 1C16.3 26.6 11 32.6 11 40c0 8.8 7.2 16 16 16h24c6.6 0 12-5.4 12-12 0-5.8-4.2-10.7-9.8-11.8"
      stroke="currentColor"
      stroke-width="2"
      stroke-linecap="round"
      stroke-linejoin="round"
      fill="none"
      class="cloud-path"
    />

    <!-- Sync arrows -->
    <path
      d="M28 32l4 4 8-8"
      stroke="currentColor"
      stroke-width="2"
      stroke-linecap="round"
      stroke-linejoin="round"
      class="sync-arrow"
    />
    <path
      d="M36 44l-4-4-8 8"
      stroke="currentColor"
      stroke-width="2"
      stroke-linecap="round"
      stroke-linejoin="round"
      class="sync-arrow-2"
    />

    <!-- Pulse ring -->
    <circle cx="32" cy="38" r="16" stroke="currentColor" stroke-width="1" stroke-opacity="0.3" class="pulse-ring" />
  </svg>
</template>

<script setup>
defineProps({
  size: {
    type: Number,
    default: 64,
  },
})
</script>

<style scoped>
.cloud-path {
  animation: cloud-float 4s ease-in-out infinite;
}

.sync-arrow {
  animation: sync-draw 2s ease-in-out infinite;
}

.sync-arrow-2 {
  animation: sync-draw 2s ease-in-out infinite 1s;
}

.pulse-ring {
  animation: ring-pulse 2s ease-out infinite;
}

@keyframes cloud-float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-2px); }
}

@keyframes sync-draw {
  0%, 100% { opacity: 0.4; }
  50% { opacity: 1; }
}

@keyframes ring-pulse {
  0% { transform: scale(0.8); opacity: 0.6; }
  100% { transform: scale(1.4); opacity: 0; }
}
</style>
