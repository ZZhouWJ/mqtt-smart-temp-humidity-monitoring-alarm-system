<template>
  <div class="panel">
    <div class="panel-title">报警记录与诊断建议</div>
    <div v-if="alarms.length === 0" class="empty">暂无报警记录</div>
    <div v-for="(item, index) in alarms.slice().reverse().slice(0, 8)" :key="index" class="alarm-item">
      <div class="alarm-type">{{ item.alarmType }}</div>
      <div class="alarm-msg">{{ item.alarmMessage }}</div>
      <div class="alarm-advice">{{ item.diagnosisAdvice || '暂无诊断建议' }}</div>
      <div class="alarm-time">{{ item.timestamp }}</div>
    </div>
  </div>
</template>

<script setup>
defineProps({ alarms: Array })
</script>
