<template>
  <div class="monitoring-page" :class="{ 'has-alarm': hasActiveAlarm }">
    <!-- Lottie 装饰 - 背景角落动画 -->
    <div class="page-decor top-right">
      <LottieAnimation
        type="wifi"
        :src="'https://assets1.lottiefiles.com/packages/lf20_xxxxxxx.json'"
        :size="80"
        :speed="0.6"
        color="rgba(0, 217, 255, 0.6)"
      />
    </div>
    <div class="page-decor bottom-left">
      <LottieAnimation
        type="network"
        :src="'https://assets10.lottiefiles.com/packages/lf20_qp1q7mct.json'"
        :size="100"
        :speed="0.4"
        color="rgba(0, 255, 157, 0.4)"
      />
    </div>
    <!-- Header -->
    <header class="page-header">
      <div class="header-left">
        <div class="title-block">
          <div class="title-label">REAL-TIME / 实时监测</div>
          <h1 class="title-main">ENVIRONMENT MONITOR</h1>
        </div>
        <div class="status-strip">
          <div class="strip-item">
            <span class="strip-label">DEV</span>
            <span class="strip-value mono">env-node-001</span>
          </div>
          <div class="strip-item">
            <span class="strip-label">FREQ</span>
            <span class="strip-value mono">1.0 Hz</span>
          </div>
          <div class="strip-item">
            <span class="strip-label">TOPIC</span>
            <span class="strip-value mono">iot/env/.../data</span>
          </div>
        </div>
      </div>
      <div class="header-right">
        <div class="status-block" :class="connectionBlockClass">
          <div class="status-pulse">
            <span class="pulse-dot" :style="{ color: connectionDotColor }"></span>
          </div>
          <div class="status-info">
            <div class="status-title">{{ connectionStatusText }}</div>
            <div class="status-meta mono">WEBSOCKET · BACKEND PUSH</div>
            <div class="status-detail mono">{{ connectionDetailText }}</div>
          </div>
        </div>
        <div class="counter-block">
          <div class="counter-label">PACKETS_RX</div>
          <div class="counter-value mono">{{ totalReceived.toString().padStart(5, '0') }}</div>
        </div>
        <div class="counter-block alarm">
          <div class="counter-label">ALARMS</div>
          <div class="counter-value mono">{{ alarmCount.toString().padStart(3, '0') }}</div>
        </div>
      </div>
    </header>

    <!-- 数据卡片区 -->
    <section class="data-grid">
      <DataCard
        label="TEMPERATURE"
        sub="原始实时温度 / ℃"
        :value="displayTemp"
        unit="℃"
        :danger="isTempAlarm"
        :warning="isTempWarning"
        type="temp"
        icon="thermometer"
      />
      <DataCard
        label="HUMIDITY"
        sub="原始实时湿度 / %RH"
        :value="displayHumidity"
        unit="%RH"
        :danger="isHumidityAlarm"
        :warning="isHumidityWarning"
        type="humi"
        icon="droplet"
      />
      <DataCard
        label="DEVICE"
        sub="设备运行状态"
        :value="deviceStatusText"
        :sub-status="latest?.rawStatus || 'IDLE'"
        :danger="latest?.deviceStatus === 'offline'"
        type="device"
        icon="cpu"
      />
      <DataCard
        label="ALARM"
        sub="当前告警状态"
        :value="alarmStatusText"
        :sub-status="latest?.alarmMessage || 'NO_ALARM'"
        :danger="isActiveAlarm"
        type="alarm"
        icon="bell"
      />
    </section>

    <!-- 图表区 -->
    <section class="charts-grid">
      <IndustrialChart
        title="TEMPERATURE"
        subtitle="温度实时曲线 (°C)"
        :xData="timeLabels"
        :rawData="rawTemps"
        :filteredData="filteredTemps"
        :alarmThreshold="35"
        :alarmLowThreshold="10"
        :currentValue="displayTemp"
        unit="℃"
        color="var(--color-primary)"
        icon="thermometer"
      />
      <IndustrialChart
        title="HUMIDITY"
        subtitle="湿度实时曲线 (%RH)"
        :xData="timeLabels"
        :rawData="rawHumidities"
        :filteredData="filteredHumidities"
        :alarmThreshold="80"
        :alarmLowThreshold="20"
        :currentValue="displayHumidity"
        unit="%RH"
        color="var(--color-success)"
        icon="droplet"
      />
    </section>

    <!-- 报警 + 数据表 -->
    <section class="bottom-grid">
      <IndustrialAlarmPanel :alarms="alarms" />
      <IndustrialLogTable :history="history" />
    </section>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import DataCard from '../components/DataCard.vue'
import IndustrialChart from '../components/IndustrialChart.vue'
import IndustrialAlarmPanel from '../components/IndustrialAlarmPanel.vue'
import IndustrialLogTable from '../components/IndustrialLogTable.vue'
import LottieAnimation from '../components/LottieAnimation.vue'
import { useSensorData } from '../composables/useSensorData'

const {
  latest, history, alarms, wsConnected, connectionStatus, totalReceived, alarmCount,
  timeLabels, rawTemps, filteredTemps, rawHumidities, filteredHumidities,
  displayTemp, displayHumidity, isTempAlarm, isHumidityAlarm, isActiveAlarm, hasActiveAlarm,
  deviceStatusText, alarmStatusText, connectionStatusText, connectionDetailText,
} = useSensorData()

const connectionBlockClass = computed(() => {
  if (wsConnected.value) return 'ok'
  if (connectionStatus.value === 'connecting' || connectionStatus.value === 'reconnecting') return 'warn'
  return 'bad'
})

const connectionDotColor = computed(() => {
  if (connectionBlockClass.value === 'ok') return 'var(--color-success)'
  if (connectionBlockClass.value === 'warn') return 'var(--color-warning)'
  return 'var(--color-danger)'
})

const isTempWarning = computed(() => {
  if (displayTemp.value === '--') return false
  const v = Number(displayTemp.value)
  return v >= 30 && v < 35
})

const isHumidityWarning = computed(() => {
  if (displayHumidity.value === '--') return false
  const v = Number(displayHumidity.value)
  return v >= 70 && v < 80
})
</script>

<style scoped>
.monitoring-page {
  padding: var(--space-6);
  min-height: 100%;
  position: relative;
}

.page-decor {
  position: absolute;
  pointer-events: none;
  z-index: 0;
  opacity: 0.4;
}

.page-decor.top-right {
  top: var(--space-4);
  right: var(--space-4);
}

.page-decor.bottom-left {
  bottom: var(--space-4);
  left: var(--space-4);
}

.monitoring-page > *:not(.page-decor) {
  position: relative;
  z-index: 1;
}

.monitoring-page.has-alarm::before {
  content: '';
  position: fixed;
  inset: 0;
  border: 1px solid var(--color-danger);
  pointer-events: none;
  animation: alarm-frame 1s ease-in-out infinite;
  z-index: 1000;
}

@keyframes alarm-frame {
  0%, 100% { opacity: 0; }
  50% { opacity: 0.4; }
}

/* ============================================
   Page Header
   ============================================ */

.page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--space-6);
  margin-bottom: var(--space-6);
  padding-bottom: var(--space-5);
  border-bottom: 1px solid var(--color-border);
  position: relative;
}

.page-header::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 0;
  width: 80px;
  height: 2px;
  background: var(--color-primary);
  box-shadow: 0 0 8px var(--color-primary);
}

.header-left {
  flex: 1;
}

.title-block {
  margin-bottom: var(--space-4);
}

.title-label {
  font-family: var(--font-mono);
  font-size: 10px;
  font-weight: 600;
  color: var(--color-primary);
  letter-spacing: 0.2em;
  margin-bottom: var(--space-1);
}

.title-main {
  font-family: var(--font-display);
  font-size: 26px;
  font-weight: 700;
  color: var(--color-text-primary);
  letter-spacing: -0.02em;
  margin: 0;
}

.status-strip {
  display: flex;
  gap: var(--space-4);
  flex-wrap: wrap;
}

.strip-item {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-1) var(--space-3);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
}

.strip-label {
  font-family: var(--font-mono);
  font-size: 9px;
  color: var(--color-text-tertiary);
  letter-spacing: 0.1em;
}

.strip-value {
  font-size: 11px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.header-right {
  display: flex;
  gap: var(--space-3);
  align-items: stretch;
}

.status-block {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  min-width: 200px;
  position: relative;
}

.status-block::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 3px;
  height: 100%;
  border-radius: var(--radius-sm) 0 0 var(--radius-sm);
}

.status-block.ok::before { background: var(--color-success); box-shadow: 0 0 8px var(--color-success); }
.status-block.warn::before { background: var(--color-warning); box-shadow: 0 0 8px var(--color-warning); }
.status-block.bad::before { background: var(--color-danger); box-shadow: 0 0 8px var(--color-danger); }

.status-pulse {
  display: flex;
  align-items: center;
  justify-content: center;
}

.status-info { flex: 1; }

.status-title {
  font-family: var(--font-mono);
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.1em;
  color: var(--color-text-primary);
}

.status-block.ok .status-title { color: var(--color-success); }
.status-block.warn .status-title { color: var(--color-warning); }
.status-block.bad .status-title { color: var(--color-danger); }

.status-meta {
  font-size: 9px;
  color: var(--color-text-tertiary);
  margin-top: 2px;
  letter-spacing: 0.1em;
}

.status-detail {
  font-size: 9px;
  color: var(--color-text-secondary);
  margin-top: 2px;
  letter-spacing: 0.1em;
}

.counter-block {
  padding: var(--space-2) var(--space-4);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  display: flex;
  flex-direction: column;
  justify-content: center;
  min-width: 90px;
  position: relative;
}

.counter-block::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 3px;
  height: 100%;
  background: var(--color-primary);
  border-radius: var(--radius-sm) 0 0 var(--radius-sm);
}

.counter-block.alarm::before { background: var(--color-accent); }

.counter-label {
  font-family: var(--font-mono);
  font-size: 9px;
  color: var(--color-text-tertiary);
  letter-spacing: 0.1em;
  margin-bottom: 2px;
}

.counter-value {
  font-size: 18px;
  font-weight: 700;
  color: var(--color-primary);
  text-shadow: 0 0 8px var(--color-primary-glow);
  line-height: 1;
}

.counter-block.alarm .counter-value { color: var(--color-accent); text-shadow: 0 0 8px var(--color-accent-soft); }

/* ============================================
   Grids
   ============================================ */

.data-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--space-4);
  margin-bottom: var(--space-6);
}

.charts-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-4);
  margin-bottom: var(--space-6);
}

.bottom-grid {
  display: grid;
  grid-template-columns: 1fr 1.5fr;
  gap: var(--space-4);
}

@media (max-width: 1280px) {
  .data-grid { grid-template-columns: repeat(2, 1fr); }
  .charts-grid { grid-template-columns: 1fr; }
  .bottom-grid { grid-template-columns: 1fr; }
}

@media (max-width: 768px) {
  .monitoring-page { padding: var(--space-4); }
  .data-grid { grid-template-columns: 1fr; }
  .page-header { flex-direction: column; }
  .header-right { width: 100%; flex-wrap: wrap; }
  .title-main { font-size: 20px; }
}
</style>
