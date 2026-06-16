# iot-frontend：Vue 3 前端大屏

## 核心功能

- **实时数据展示**：温度、湿度、设备状态、报警状态卡片
- **曲线绘制**：ECharts 实时绘制原始值和滤波值对比曲线
- **报警记录**：展示报警历史和诊断建议
- **数据表格**：显示最近采集记录
- **WebSocket 连接**：实时接收后端推送数据
- **状态指示**：连接状态实时显示

## 技术栈

- Vue 3 Composition API
- ECharts 5
- 原生 WebSocket
- CSS Variables 设计系统

## 运行环境

- Node.js 18+
- npm 9+

## 启动方式

```bash
cd iot-frontend
npm install
npm run dev
```

访问：http://localhost:5173

## 界面布局

```
┌─────────────────────────────────────────────────────┐
│  智能温湿度环境监测系统                    [连接状态] │
├────────┬────────┬────────┬────────────────────────┤
│  温度  │  湿度  │ 设备状态│       报警状态         │
├────────┴────────┴────────┴────────────────────────┤
│                                                   │
│           温度实时曲线                             │
│                                                   │
├─────────────────────────┬─────────────────────────┤
│                         │    报警记录             │
│     湿度实时曲线         │    · 报警 1            │
│                         │    · 报警 2            │
├─────────────────────────┴─────────────────────────┤
│                   最近采集记录表格                  │
└───────────────────────────────────────────────────┘
```

## 通信接口

### WebSocket

```
ws://localhost:8080/ws/sensor
```

接收实时数据推送。

### REST API

```
http://localhost:8080/api/latest     # 最新数据
http://localhost:8080/api/history    # 历史数据
http://localhost:8080/api/alarms     # 报警记录
```

## 数据字段

| 字段 | 类型 | 说明 |
|------|------|------|
| deviceId | String | 设备编号 |
| timestamp | String | 时间戳 |
| seq | Integer | 数据序号 |
| rawTemperature | Double | 原始温度 |
| rawHumidity | Double | 原始湿度 |
| filteredTemperature | Double | 滤波温度 |
| filteredHumidity | Double | 滤波湿度 |
| outlier | Boolean | 是否异常值 |
| packetLoss | Boolean | 是否丢包 |
| alarmType | String | 报警类型 |
| alarmMessage | String | 报警信息 |
| diagnosisAdvice | String | 诊断建议 |

## 组件说明

| 组件 | 功能 |
|------|------|
| `DataCard.vue` | 数据卡片，展示单个指标 |
| `LineChart.vue` | ECharts 曲线图 |
| `AlarmPanel.vue` | 报警记录面板 |
| `LoadingState.vue` | 加载状态 |
| `LottieAnimation.vue` | 动画组件 |

## 设计特点

- **商业级 UI**：参考 Notion/飞书风格
- **8px 间距系统**：统一间距节奏
- **灰度配色**：Indigo 主色调 + 灰度体系
- **响应式布局**：适配多种屏幕尺寸
