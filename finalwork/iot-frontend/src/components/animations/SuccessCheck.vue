<template>
  <svg :width="size" :height="size" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
    <!-- Background circle -->
    <circle
      cx="32"
      cy="32"
      r="26"
      stroke="currentColor"
      stroke-width="2"
      stroke-opacity="0.2"
      class="bg-circle"
    />

    <!-- Animated checkmark -->
    <path
      d="M20 32l8 8 16-16"
      stroke="currentColor"
      stroke-width="3"
      stroke-linecap="round"
      stroke-linejoin="round"
      class="checkmark"
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
.bg-circle {
  animation: circle-appear 0.3s ease-out forwards;
}

.checkmark {
  stroke-dasharray: 40;
  stroke-dashoffset: 40;
  animation: check-draw 0.4s ease-out 0.15s forwards;
}

@keyframes circle-appear {
  from { opacity: 0; transform: scale(0.8); }
  to { opacity: 0.2; transform: scale(1); }
}

@keyframes check-draw {
  to { stroke-dashoffset: 0; }
}
</style>
