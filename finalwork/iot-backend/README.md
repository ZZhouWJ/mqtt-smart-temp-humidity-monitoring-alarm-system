# iot-backend：Spring Boot 后端服务

## 核心功能

- **MQTT 订阅**：订阅模拟器发布的主题，接收传感器数据
- **数据解析**：解析 JSON 格式的传感器数据
- **丢包检测**：通过 seq 序号检测丢包情况
- **跳变检测**：判断数据是否发生异常跳变
- **滤波处理**：滑动平均滤波算法去除噪声
- **报警判断**：温度/湿度超阈值时触发报警
- **WebSocket 推送**：实时推送数据到前端
- **REST 接口**：提供历史数据和报警记录查询

## 运行环境

- JDK 17+
- Maven 3.8+

## 启动方式

```bash
cd iot-backend
mvn spring-boot:run
```

## API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/health` | GET | 健康检查 |
| `/api/latest` | GET | 获取最新数据 |
| `/api/history` | GET | 获取历史数据（最近 60 条） |
| `/api/alarms` | GET | 获取报警记录 |

## WebSocket 地址

```
ws://localhost:8080/ws/sensor
```

## 数据处理流程

```
MQTT 消息接收
    ↓
JSON 解析
    ↓
丢包检测（seq 序号）
    ↓
跳变检测（阈值判断）
    ↓
滑动平均滤波
    ↓
报警判断（阈值比较）
    ↓
数据存储
    ↓
WebSocket 推送
```

## 滤波算法

采用**滑动平均滤波**，窗口大小为 5：

```java
public double filter(double newValue) {
    window.add(newValue);
    if (window.size() > WINDOW_SIZE) {
        window.remove();
    }
    return window.stream()
        .mapToDouble(Double::doubleValue)
        .average()
        .orElse(newValue);
}
```

## 报警阈值

| 类型 | 阈值 | 说明 |
|------|------|------|
| TEMP_HIGH | > 35℃ | 高温报警 |
| TEMP_LOW | < 10℃ | 低温报警 |
| HUMIDITY_HIGH | > 80% | 高湿报警 |
| HUMIDITY_LOW | < 20% | 低湿报警 |
| BOTH_HIGH | 温湿度同时超标 | 复合报警 |

## 断线重连

后端使用 Eclipse Paho MQTT 客户端，配置自动重连：
- 自动重连：已启用
- 重连间隔：Paho 默认指数退避
- QoS 级别：1（至少一次）

## 配置说明

在 `application.yml` 中配置 MQTT 连接：

```yaml
spring:
  application:
    name: iot-backend

mqtt:
  broker:
    url: tcp://broker.emqx.io:1883
    client-id: springboot_subscriber
    topic: iot/env/node001/data
```
