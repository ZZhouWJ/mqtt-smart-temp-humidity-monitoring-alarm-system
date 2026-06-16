@echo off
set MQTT_BROKER=tcp://localhost:1883
C:\apache-maven-3.9.6\bin\mvn.cmd spring-boot:run -f iot-backend\pom.xml
