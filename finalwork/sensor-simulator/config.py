"""模拟传感器端配置文件。

本文件支持两种运行方式：
1. 本地直接运行：使用本地 Mosquitto MQTT Broker (localhost:1883)；
2. Docker Compose 运行：通过环境变量把 MQTT_HOST 指向 emqx 容器。

这样既方便本地演示，也方便工程化一键部署。
"""

import os

MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "iot/env/node001/data")
CLIENT_ID = os.getenv("CLIENT_ID", "python-env-simulator-001")
DEVICE_ID = os.getenv("DEVICE_ID", "env-node-001")

# 采样间隔，单位：秒
PUBLISH_INTERVAL = float(os.getenv("PUBLISH_INTERVAL", "1.0"))

# 温湿度基础值
BASE_TEMPERATURE = float(os.getenv("BASE_TEMPERATURE", "26.0"))
BASE_HUMIDITY = float(os.getenv("BASE_HUMIDITY", "60.0"))

# 随机噪声范围
TEMP_NOISE_RANGE = (-0.8, 0.8)
HUMIDITY_NOISE_RANGE = (-2.0, 2.0)

# 报警阈值，与后端保持一致
TEMP_HIGH_THRESHOLD = 35.0
HUMIDITY_HIGH_THRESHOLD = 80.0

# 异常模拟概率
JUMP_PROBABILITY = 0.08    # 跳变异常概率
DROP_PROBABILITY = 0.05    # 丢包概率
OFFLINE_PROBABILITY = 0.02 # 短暂离线概率
