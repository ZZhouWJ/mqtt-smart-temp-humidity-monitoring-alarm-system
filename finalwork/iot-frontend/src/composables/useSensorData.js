import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { createSensorSocket } from '../websocket/sensorSocket'
import { fetchAlarms, fetchHistory } from '../api/sensor'

const latest = ref(null)
const history = ref([])
const alarms = ref([])
const wsConnected = ref(false)
const totalReceived = ref(0)
const alarmCount = ref(0)
let socket = null
let reconnectTimer = null
let isInitialized = false

const MAX_POINTS = 60

function pushData(data) {
  totalReceived.value++
  latest.value = data
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

async function init() {
  if (isInitialized) return
  isInitialized = true
  try {
    history.value = (await fetchHistory()).slice(-MAX_POINTS)
    alarms.value = await fetchAlarms()
    alarmCount.value = alarms.value.length
    totalReceived.value = history.value.length
    latest.value = history.value[history.value.length - 1] || null
  } catch (err) {
    console.warn('初始化历史数据失败', err)
  }
  connectWs()
}

function cleanup() {
  clearTimeout(reconnectTimer)
  socket?.close()
  socket = null
  isInitialized = false
}

export function useSensorData() {
  onMounted(init)
  onBeforeUnmount(cleanup)

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

  return {
    latest, history, alarms, wsConnected, totalReceived, alarmCount,
    timeLabels, rawTemps, filteredTemps, rawHumidities, filteredHumidities,
    displayTemp, displayHumidity, isTempAlarm, isHumidityAlarm, isActiveAlarm, hasActiveAlarm,
    deviceStatusText, alarmStatusText,
  }
}
