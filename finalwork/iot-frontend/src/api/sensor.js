import axios from 'axios'

const http = axios.create({
  baseURL: 'http://localhost:8080',
  timeout: 5000,
})

export async function fetchHistory() {
  const res = await http.get('/api/history')
  return res.data || []
}

export async function fetchAlarms() {
  const res = await http.get('/api/alarms')
  return res.data || []
}
