# sensor-simulator：模拟温湿度采集节点

## 功能

- 生成温度、湿度、时间戳、设备编号、数据序号；
- 加入随机白噪声；
- 模拟跳变异常、丢包、短暂离线；
- 使用 JSON 数据格式；
- 通过 MQTT 发布到公共 Broker；
- 实现断线自动重连。

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行

普通模式：

```bash
python mqtt_publisher.py --mode normal
```

演示模式：

```bash
python mqtt_publisher.py --mode demo
```

## 重要配置

配置文件：`config.py`

```text
MQTT_HOST = "broker.emqx.io"
MQTT_PORT = 1883
MQTT_TOPIC = "iot/env/node001/data"
```
