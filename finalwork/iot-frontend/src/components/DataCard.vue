<template>
  <div class="data-card" :class="{ danger }">
    <div class="label">{{ label }}</div>
    <div class="value">{{ value }}</div>
    <div class="sub">{{ sub }}</div>
  </div>
</template>

<script setup>
defineProps({
  label: String,
  value: [String, Number],
  sub: String,
  danger: Boolean,
})
</script>
