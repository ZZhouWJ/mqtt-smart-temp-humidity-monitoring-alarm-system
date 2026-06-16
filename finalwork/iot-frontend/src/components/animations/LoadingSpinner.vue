<template>
  <svg :width="size" :height="size" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
    <!-- Outer rotating ring -->
    <circle
      cx="32"
      cy="32"
      r="28"
      stroke="currentColor"
      stroke-width="3"
      stroke-linecap="round"
      stroke-dasharray="44 132"
      class="spinner-ring"
    />
    <!-- Inner rotating ring (opposite direction) -->
    <circle
      cx="32"
      cy="32"
      r="18"
      stroke="currentColor"
      stroke-width="2"
      stroke-linecap="round"
      stroke-dasharray="28 84"
      stroke-opacity="0.4"
      class="spinner-ring-inner"
    />
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
.spinner-ring {
  transform-origin: center;
  animation: spin 1.4s linear infinite;
}

.spinner-ring-inner {
  transform-origin: center;
  animation: spin-reverse 2.1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@keyframes spin-reverse {
  from { transform: rotate(360deg); }
  to { transform: rotate(0deg); }
}
</style>
