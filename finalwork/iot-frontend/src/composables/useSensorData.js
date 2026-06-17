import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { createSensorSocket } from '../websocket/sensorSocket'
import { fetchAlarms, fetchHistory } from '../api/sensor'

const latest = ref(null)
const history = ref([])
const alarms = ref([])
const wsConnected = ref(false)
const connectionStatus = ref('disconnected')
const reconnectAttempts = ref(0)
const lastUpdateTime = ref('--')
const totalReceived = ref(0)
const alarmCount = ref(0)
let socket = null
let reconnectTimer = null
let isInitialized = false
let activeConsumers = 0
let shouldReconnect = false

const MAX_POINTS = 60
const RECONNECT_DELAY_MS = 2000

function formatDisplayTime(timestamp) {
  if (!timestamp) return new Date().toLocaleTimeString('zh-CN', { hour12: false })
  const text = String(timestamp)
  return text.length >= 19 ? text.slice(11, 19) : text
}

function pushData(data) {
  totalReceived.value++
  latest.value = data
  lastUpdateTime.value = formatDisplayTime(data.timestamp)
  history.value.push(data)
  if (history.value.length > MAX_POINTS) history.value.shift()

  if (data.alarmType && data.alarmType !== 'NORMAL') {
    alarmCount.value++
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

function scheduleReconnect() {
  clearTimeout(reconnectTimer)
  reconnectAttempts.value++
  connectionStatus.value = 'reconnecting'
  reconnectTimer = setTimeout(connectWs, RECONNECT_DELAY_MS)
}

function connectWs() {
  clearTimeout(reconnectTimer)
  connectionStatus.value = reconnectAttempts.value > 0 ? 'reconnecting' : 'connecting'

  socket = createSensorSocket({
    onOpen: () => {
      wsConnected.value = true
      connectionStatus.value = 'connected'
      reconnectAttempts.value = 0
    },
    onMessage: pushData,
    onClose: () => {
      wsConnected.value = false
      socket = null
      if (shouldReconnect) {
        scheduleReconnect()
      } else {
        connectionStatus.value = 'disconnected'
      }
    },
    onError: () => {
      wsConnected.value = false
      connectionStatus.value = shouldReconnect ? 'reconnecting' : 'disconnected'
    },
  })
}

async function init() {
  if (isInitialized) return
  isInitialized = true
  shouldReconnect = true
  connectionStatus.value = 'connecting'
  try {
    history.value = (await fetchHistory()).slice(-MAX_POINTS)
    alarms.value = await fetchAlarms()
    alarmCount.value = alarms.value.length
    totalReceived.value = history.value.length
    latest.value = history.value[history.value.length - 1] || null
    if (latest.value) lastUpdateTime.value = formatDisplayTime(latest.value.timestamp)
  } catch (err) {
    console.warn('初始化历史数据失败', err)
  }
  connectWs()
}

function cleanup() {
  shouldReconnect = false
  clearTimeout(reconnectTimer)
  reconnectTimer = null
  socket?.close()
  socket = null
  wsConnected.value = false
  connectionStatus.value = 'disconnected'
  isInitialized = false
}

export function useSensorData() {
  onMounted(() => {
    activeConsumers++
    init()
  })
  onBeforeUnmount(() => {
    activeConsumers = Math.max(0, activeConsumers - 1)
    if (activeConsumers === 0) cleanup()
  })

  const timeLabels = computed(() => history.value.map(x => (x.timestamp || '').slice(11)))
  const rawTemps = computed(() => history.value.map(x => x.rawTemperature))
  const filteredTemps = computed(() => history.value.map(x => x.filteredTemperature))
  const rawHumidities = computed(() => history.value.map(x => x.rawHumidity))
  const filteredHumidities = computed(() => history.value.map(x => x.filteredHumidity))

  const displayTemp = computed(() => latest.value?.rawTemperature ?? '--')
  const displayHumidity = computed(() => latest.value?.rawHumidity ?? '--')
  const isTempAlarm = computed(() => ['TEMP_HIGH', 'BOTH_HIGH'].includes(latest.value?.alarmType))
  const isHumidityAlarm = computed(() => ['HUMIDITY_HIGH', 'BOTH_HIGH'].includes(latest.value?.alarmType))
  const isActiveAlarm = computed(() => latest.value?.alarmType && latest.value?.alarmType !== 'NORMAL')
  const hasActiveAlarm = computed(() => isTempAlarm.value || isHumidityAlarm.value)

  const deviceStatusText = computed(() => {
    const status = latest.value?.deviceStatus
    if (status === 'offline') return '离线'
    if (status === 'online') return '在线'
    return '--'
  })

  const alarmStatusText = computed(() => {
    const type = latest.value?.alarmType
    const map = {
      'TEMP_HIGH': '高温告警',
      'HUMIDITY_HIGH': '高湿告警',
      'BOTH_HIGH': '复合告警',
      'DATA_OUTLIER': '数据异常',
      'PACKET_LOSS': '丢包',
      'DEVICE_OFFLINE': '设备离线',
      'NORMAL': '正常',
    }
    return map[type] || '--'
  })

  const connectionStatusText = computed(() => {
    const map = {
      connected: 'CONNECTED',
      connecting: 'CONNECTING',
      reconnecting: 'RECONNECTING',
      disconnected: 'DISCONNECTED',
    }
    return map[connectionStatus.value] || 'DISCONNECTED'
  })

  const connectionDetailText = computed(() => {
    if (connectionStatus.value === 'connected') return `LAST ${lastUpdateTime.value}`
    if (connectionStatus.value === 'reconnecting') return `RETRY ${reconnectAttempts.value} · ${RECONNECT_DELAY_MS / 1000}S`
    if (connectionStatus.value === 'connecting') return 'OPENING SOCKET'
    return 'WAITING BACKEND'
  })

  return {
    latest, history, alarms, wsConnected, connectionStatus, reconnectAttempts, lastUpdateTime, totalReceived, alarmCount,
    timeLabels, rawTemps, filteredTemps, rawHumidities, filteredHumidities,
    displayTemp, displayHumidity, isTempAlarm, isHumidityAlarm, isActiveAlarm, hasActiveAlarm,
    deviceStatusText, alarmStatusText, connectionStatusText, connectionDetailText,
  }
}
