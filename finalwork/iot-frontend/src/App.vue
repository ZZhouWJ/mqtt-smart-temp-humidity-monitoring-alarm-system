<template>
  <main class="dashboard">
    <header class="header">
      <div>
        <h1>基于 MQTT 的智能温湿度环境监测与异常报警系统</h1>
        <p>Python 模拟采集节点 · MQTT 公共 Broker · Spring Boot 后端 · Vue + ECharts 前端</p>
      </div>
      <div class="status-pill" :class="wsConnected ? 'ok' : 'bad'">
        {{ wsConnected ? 'WebSocket 已连接' : 'WebSocket 未连接' }}
      </div>
    </header>

    <section class="cards">
      <DataCard label="当前温度" :value="displayTemp" sub="原始实时温度 / ℃" :danger="isTempAlarm" />
      <DataCard label="当前湿度" :value="displayHumidity" sub="原始实时湿度 / %RH" :danger="isHumidityAlarm" />
      <DataCard label="设备状态" :value="latest?.deviceStatus || 'waiting'" :sub="latest?.rawStatus || '等待数据'" :danger="latest?.deviceStatus === 'offline'" />
      <DataCard label="报警状态" :value="latest?.alarmType || 'WAITING'" :sub="latest?.alarmMessage || '等待后端推送'" :danger="latest?.alarmType && latest?.alarmType !== 'NORMAL'" />
    </section>

    <section class="main-grid">
      <div class="charts">
        <LineChart title="温度实时曲线" :xData="timeLabels" :rawData="rawTemps" :filteredData="filteredTemps" unit="℃" />
        <LineChart title="湿度实时曲线" :xData="timeLabels" :rawData="rawHumidities" :filteredData="filteredHumidities" unit="%RH" />
      </div>
      <AlarmPanel :alarms="alarms" />
    </section>

    <section class="log-panel">
      <div class="panel-title">最近数据</div>
      <table>
        <thead>
          <tr>
            <th>序号</th><th>时间</th><th>原始温度</th><th>滤波温度</th><th>原始湿度</th><th>滤波湿度</th><th>异常</th><th>丢包</th><th>诊断建议</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in history.slice().reverse().slice(0, 8)" :key="item.seq">
            <td>{{ item.seq }}</td>
            <td>{{ item.timestamp }}</td>
            <td>{{ item.rawTemperature }}</td>
            <td>{{ item.filteredTemperature }}</td>
            <td>{{ item.rawHumidity }}</td>
            <td>{{ item.filteredHumidity }}</td>
            <td>{{ item.outlier ? '是' : '否' }}</td>
            <td>{{ item.packetLoss ? '是' : '否' }}</td>
            <td class="advice-cell">{{ item.diagnosisAdvice }}</td>
          </tr>
        </tbody>
      </table>
    </section>
  </main>
</template>

<script setup>
import { computed, onMounted, onBeforeUnmount, ref } from 'vue'
import DataCard from './components/DataCard.vue'
import LineChart from './components/LineChart.vue'
import AlarmPanel from './components/AlarmPanel.vue'
import { createSensorSocket } from './websocket/sensorSocket'
import { fetchAlarms, fetchHistory } from './api/sensor'

const latest = ref(null)
const history = ref([])
const alarms = ref([])
const wsConnected = ref(false)
let socket = null
let reconnectTimer = null

const MAX_POINTS = 60

const timeLabels = computed(() => history.value.map(x => (x.timestamp || '').slice(11)))
const rawTemps = computed(() => history.value.map(x => x.rawTemperature))
const filteredTemps = computed(() => history.value.map(x => x.filteredTemperature))
const rawHumidities = computed(() => history.value.map(x => x.rawHumidity))
const filteredHumidities = computed(() => history.value.map(x => x.filteredHumidity))

const displayTemp = computed(() => latest.value?.rawTemperature ?? '--')
const displayHumidity = computed(() => latest.value?.rawHumidity ?? '--')
const isTempAlarm = computed(() => ['TEMP_HIGH', 'BOTH_HIGH'].includes(latest.value?.alarmType))
const isHumidityAlarm = computed(() => ['HUMIDITY_HIGH', 'BOTH_HIGH'].includes(latest.value?.alarmType))

function pushData(data) {
  latest.value = data
  history.value.push(data)
  if (history.value.length > MAX_POINTS) history.value.shift()
  if (data.alarmType && data.alarmType !== 'NORMAL') {
    alarms.value.push({
      deviceId: data.deviceId,
      timestamp: data.timestamp,
      alarmType: data.alarmType,
      alarmMessage: data.alarmMessage,
      temperature: data.filteredTemperature,
      humidity: data.filteredHumidity,
      diagnosisAdvice: data.diagnosisAdvice,
    })
  }
}

function connectWs() {
  socket = createSensorSocket({
    onOpen: () => { wsConnected.value = true },
    onMessage: pushData,
    onClose: () => {
      wsConnected.value = false
      reconnectTimer = setTimeout(connectWs, 2000)
    },
    onError: () => { wsConnected.value = false },
  })
}

onMounted(async () => {
  try {
    history.value = (await fetchHistory()).slice(-MAX_POINTS)
    alarms.value = await fetchAlarms()
    latest.value = history.value[history.value.length - 1] || null
  } catch (err) {
    console.warn('初始化历史数据失败，等待 WebSocket 实时数据')
  }
  connectWs()
})

onBeforeUnmount(() => {
  clearTimeout(reconnectTimer)
  socket?.close()
})
</script>
