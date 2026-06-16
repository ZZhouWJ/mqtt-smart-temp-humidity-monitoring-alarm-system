# iot-backend：Spring Boot 后端

## 功能

- 订阅 MQTT 数据；
- 解析 JSON；
- 丢包检测；
- 跳变异常检测；
- 滑动平均滤波；
- 超温、超湿报警；
- WebSocket 推送；
- REST 接口查询历史数据和报警记录。

## 运行环境

- JDK 17+
- Maven 3.8+

## 启动

```bash
mvn spring-boot:run
```

启动成功后：

```text
http://localhost:8080/api/health
```

## WebSocket 地址

```text
ws://localhost:8080/ws/sensor
```

## REST 接口

```text
GET http://localhost:8080/api/latest
GET http://localhost:8080/api/history
GET http://localhost:8080/api/alarms
GET http://localhost:8080/api/health
```
