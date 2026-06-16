package com.example.iot.mqtt;

import com.example.iot.model.SensorData;
import com.example.iot.service.SensorDataService;
import com.fasterxml.jackson.databind.ObjectMapper;
import jakarta.annotation.PostConstruct;
import jakarta.annotation.PreDestroy;
import org.eclipse.paho.client.mqttv3.*;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

/**
 * MQTT 订阅端。
 *
 * 后端启动后自动连接 MQTT Broker，并订阅模拟传感器发布的数据。
 * 改进点：
 * 1. 开启 Paho 自动重连；
 * 2. 后端首次连接失败时使用指数退避重试，避免 Docker 中 EMQX 尚未完全启动导致后端退出；
 * 3. 每次连接恢复后自动重新订阅 Topic。
 */
@Component
public class MqttSubscriber {

    @Value("${mqtt.broker}")
    private String broker;

    @Value("${mqtt.clientId}")
    private String clientId;

    @Value("${mqtt.topic}")
    private String topic;

    private final SensorDataService sensorDataService;
    private final ObjectMapper objectMapper = new ObjectMapper();
    private MqttClient client;

    public MqttSubscriber(SensorDataService sensorDataService) {
        this.sensorDataService = sensorDataService;
    }

    @PostConstruct
    public void start() {
        // 不在主线程阻塞 Spring Boot 启动，后台线程负责连接 MQTT。
        Thread mqttThread = new Thread(this::connectWithRetry, "mqtt-connect-retry-thread");
        mqttThread.setDaemon(true);
        mqttThread.start();
    }

    private void connectWithRetry() {
        int delaySeconds = 1;
        while (true) {
            try {
                client = new MqttClient(broker, clientId + "-" + System.currentTimeMillis());
                client.setCallback(buildCallback());

                MqttConnectOptions options = new MqttConnectOptions();
                options.setAutomaticReconnect(true);
                options.setCleanSession(true);
                options.setConnectionTimeout(10);
                options.setKeepAliveInterval(30);

                client.connect(options);
                System.out.println("[MQTT] 后端已连接 Broker: " + broker);
                return;
            } catch (Exception e) {
                System.err.println("[MQTT] 后端连接失败: " + e.getMessage() + "，" + delaySeconds + " 秒后重试");
                try {
                    Thread.sleep(delaySeconds * 1000L);
                } catch (InterruptedException interruptedException) {
                    Thread.currentThread().interrupt();
                    return;
                }
                delaySeconds = Math.min(delaySeconds * 2, 30);
            }
        }
    }

    private MqttCallbackExtended buildCallback() {
        return new MqttCallbackExtended() {
            @Override
            public void connectComplete(boolean reconnect, String serverURI) {
                try {
                    client.subscribe(topic, 1);
                    System.out.println("[MQTT] 已订阅 Topic: " + topic + " reconnect=" + reconnect);
                } catch (MqttException e) {
                    System.err.println("[MQTT] 订阅失败: " + e.getMessage());
                }
            }

            @Override
            public void connectionLost(Throwable cause) {
                System.err.println("[MQTT] 连接丢失，Paho 将自动重连: " + (cause == null ? "unknown" : cause.getMessage()));
            }

            @Override
            public void messageArrived(String topic, MqttMessage message) {
                try {
                    String payload = new String(message.getPayload());
                    SensorData raw = objectMapper.readValue(payload, SensorData.class);
                    sensorDataService.handleRawData(raw);
                    System.out.println("[MQTT] 收到数据: " + payload);
                } catch (Exception e) {
                    System.err.println("[MQTT] 数据解析失败: " + e.getMessage());
                }
            }

            @Override
            public void deliveryComplete(IMqttDeliveryToken token) {
                // 当前后端只订阅数据，不主动发布，因此这里无需处理。
            }
        };
    }

    @PreDestroy
    public void stop() throws Exception {
        if (client != null && client.isConnected()) {
            client.disconnect();
            client.close();
        }
    }
}
