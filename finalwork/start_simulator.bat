@echo off
set MQTT_HOST=localhost
set MQTT_PORT=1883
set MQTT_TOPIC=iot/env/node001/data
python sensor-simulator\mqtt_publisher.py --mode demo
