# iot-frontend：Vue + ECharts 前端

## 功能

- WebSocket 实时接收后端数据；
- 展示当前温度、湿度、设备状态、报警状态；
- 使用 ECharts 绘制原始值与滤波值曲线；
- 显示报警记录；
- 显示最近数据和异常状态。

## 运行环境

- Node.js 18+
- npm 9+

## 启动

```bash
npm install
npm run dev
```

浏览器打开：

```text
http://localhost:5173
```

## 注意

前端默认连接：

```text
REST: http://localhost:8080
WebSocket: ws://localhost:8080/ws/sensor
```
