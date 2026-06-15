/**
 * 创建 WebSocket 连接，用于接收后端实时推送的温湿度数据。
 */
export function createSensorSocket({ onMessage, onOpen, onClose, onError }) {
  const socket = new WebSocket('ws://localhost:8080/ws/sensor')

  socket.onopen = () => {
    onOpen && onOpen()
  }

  socket.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data)
      onMessage && onMessage(data)
    } catch (err) {
      console.error('WebSocket 数据解析失败', err)
    }
  }

  socket.onclose = () => {
    onClose && onClose()
  }

  socket.onerror = (err) => {
    onError && onError(err)
  }

  return socket
}
