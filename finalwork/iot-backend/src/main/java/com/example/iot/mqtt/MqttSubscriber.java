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
 * MQTT 订阅端 - 优化版控制台输出
 *
 * 功能：
 * 1. 订阅 MQTT 温湿度数据
 * 2. 实时打印数据处理过程
 * 3. 断线重连状态显示
 */
@Component
public class MqttSubscriber {

    private static final String RESET = "\033[0m";
    private static final String BOLD = "\033[1m";
    private static final String DIM = "\033[2m";

    // 颜色
    private static final String RED = "\033[91m";
    private static final String GREEN = "\033[92m";
    private static final String YELLOW = "\033[93m";
    private static final String BLUE = "\033[94m";
    private static final String CYAN = "\033[96m";
    private static final String MAGENTA = "\033[95m";

    @Value("${mqtt.broker}")
    private String broker;

    @Value("${mqtt.clientId}")
    private String clientId;

    @Value("${mqtt.topic}")
    private String topic;

    private final SensorDataService sensorDataService;
    private final ObjectMapper objectMapper = new ObjectMapper();
    private MqttClient client;

    // 统计
    private int reconnectCount = 0;
    private int totalReceived = 0;
    private int alarmCount = 0;

    public MqttSubscriber(SensorDataService sensorDataService) {
        this.sensorDataService = sensorDataService;
    }

    @PostConstruct
    public void start() {
        printBanner();
        Thread mqttThread = new Thread(this::connectWithRetry, "mqtt-connect-retry-thread");
        mqttThread.setDaemon(true);
        mqttThread.start();
    }

    private void printBanner() {
        System.out.println();
        System.out.println(BOLD + CYAN + "╔══════════════════════════════════════════════════════════╗" + RESET);
        System.out.println(BOLD + CYAN + "║" + RESET + "        IoT 后端服务 - MQTT 订阅端 v2.0" + BOLD + CYAN + "            ║" + RESET);
        System.out.println(BOLD + CYAN + "║" + RESET + "        Broker: " + broker + "  Topic: " + topic + BOLD + CYAN + " ║" + RESET);
        System.out.println(BOLD + CYAN + "╚══════════════════════════════════════════════════════════╝" + RESET);
        System.out.println();
    }

    private void connectWithRetry() {
        int delaySeconds = 1;
        reconnectCount = 0;

        while (true) {
            try {
                String uniqueClientId = clientId + "-" + System.currentTimeMillis();
                client = new MqttClient(broker, uniqueClientId);
                client.setCallback(buildCallback());

                MqttConnectOptions options = new MqttConnectOptions();
                options.setAutomaticReconnect(true);
                options.setCleanSession(true);
                options.setConnectionTimeout(10);
                options.setKeepAliveInterval(30);

                client.connect(options);
                reconnectCount = 0;
                System.out.println(GREEN + "[OK] " + RESET + "已连接 MQTT Broker: " + broker);
                System.out.println(DIM + "      开始监听数据流..." + RESET);
                System.out.println();
                return;
            } catch (Exception e) {
                reconnectCount++;
                System.out.println(YELLOW + "[WARN] " + RESET + "连接失败: " + e.getMessage());
                System.out.println(DIM + "      " + delaySeconds + " 秒后重试 (第 " + reconnectCount + " 次)" + RESET);
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
                    if (reconnect) {
                        reconnectCount++;
                        System.out.println();
                        System.out.println(GREEN + "[RECONNECT] " + RESET + "重连成功！Broker: " + serverURI);
                        System.out.println(DIM + "           重连次数: " + reconnectCount + RESET);
                        System.out.println();
                    } else {
                        System.out.println(GREEN + "[OK] " + RESET + "已订阅 Topic: " + topic + " (QoS=1)");
                    }
                } catch (MqttException e) {
                    System.err.println(RED + "[ERROR] " + RESET + "订阅失败: " + e.getMessage());
                }
            }

            @Override
            public void connectionLost(Throwable cause) {
                System.out.println();
                System.out.println(YELLOW + "[WARN] " + RESET + "连接丢失，等待自动重连...");
                if (cause != null) {
                    System.out.println(DIM + "       原因: " + cause.getMessage() + RESET);
                }
            }

            @Override
            public void messageArrived(String topic, MqttMessage message) {
                totalReceived++;
                try {
                    String payload = new String(message.getPayload());
                    SensorData raw = objectMapper.readValue(payload, SensorData.class);

                    // 打印接收到的原始数据
                    printReceivedData(raw);

                    // 处理数据
                    var processed = sensorDataService.handleRawData(raw);

                    // 打印处理结果
                    printProcessedData(processed);

                } catch (Exception e) {
                    System.err.println(RED + "[ERROR] " + RESET + "数据解析失败: " + e.getMessage());
                }
            }

            @Override
            public void deliveryComplete(IMqttDeliveryToken token) {
                // 不使用发布功能
            }
        };
    }

    private void printReceivedData(SensorData raw) {
        String status = raw.getStatus();
        String statusColor = getStatusColor(status);
        String statusText = getStatusText(status);

        System.out.printf(
            DIM + "[%s] " + RESET + CYAN + "[MQTT] " + RESET +
            "设备: %s | Seq: %d | Temp: " + statusColor + "%6.1f°C" + RESET + " | Humi: " +
            statusColor + "%5.1f%%" + RESET + " | Status: " + statusColor + "%s" + RESET + "\n",
            java.time.LocalDateTime.now().format(java.time.format.DateTimeFormatter.ofPattern("HH:mm:ss")),
            raw.getDeviceId(),
            raw.getSeq() != null ? raw.getSeq() : 0,
            raw.getTemperature() != null ? raw.getTemperature() : 0.0,
            raw.getHumidity() != null ? raw.getHumidity() : 0.0,
            statusText
        );
    }

    private void printProcessedData(var processed) {
        if (processed == null) return;

        String alarmType = processed.getAlarmType();
        if (alarmType != null && !"NORMAL".equals(alarmType)) {
            alarmCount++;
            String alarmColor = RED;
            String alarmText = getAlarmText(alarmType);

            System.out.println(
                "           └─> " + alarmColor + BOLD + "[ALARM] " + alarmType + RESET +
                " | " + alarmColor + alarmText + RESET
            );

            // 诊断建议
            if (processed.getDiagnosisAdvice() != null) {
                System.out.println(
                    "              " + DIM + "建议: " + processed.getDiagnosisAdvice() + RESET
                );
            }
        }

        // 打印滤波结果
        System.out.printf(
            "           " + DIM + "└─> 滤波: Temp=%.1f°C Humi=%.1f%% | %s" + RESET + "\n",
            processed.getFilteredTemperature(),
            processed.getFilteredHumidity(),
            processed.getOutlier() != null && processed.getOutlier() ?
                YELLOW + "异常点" + RESET : GREEN + "正常" + RESET
        );

        // 打印统计信息
        System.out.println(
            DIM + "           [统计] 累计接收: " + totalReceived +
            " | 报警次数: " + alarmCount +
            " | 重连次数: " + reconnectCount + RESET
        );
        System.out.println();
    }

    private String getStatusColor(String status) {
        if (status == null) return GREEN;
        return switch (status.toLowerCase()) {
            case "temp_high", "humidity_high", "both_high" -> RED;
            case "jump" -> YELLOW;
            case "offline" -> MAGENTA;
            case "lost" -> YELLOW;
            default -> GREEN;
        };
    }

    private String getStatusText(String status) {
        if (status == null) return "NORMAL";
        return switch (status.toLowerCase()) {
            case "temp_high" -> "HIGH TEMP";
            case "humidity_high" -> "HIGH HUMI";
            case "both_high" -> "ALARM!";
            case "jump" -> "JUMP!";
            case "offline" -> "OFFLINE";
            case "lost" -> "LOST";
            default -> "NORMAL";
        };
    }

    private String getAlarmText(String alarmType) {
        return switch (alarmType) {
            case "TEMP_HIGH" -> "温度超过阈值";
            case "HUMIDITY_HIGH" -> "湿度超过阈值";
            case "BOTH_HIGH" -> "温湿度同时超标";
            case "DATA_OUTLIER" -> "数据跳变异常";
            case "PACKET_LOSS" -> "检测到丢包";
            case "DEVICE_OFFLINE" -> "设备离线";
            default -> alarmType;
        };
    }

    @PreDestroy
    public void stop() throws Exception {
        if (client != null && client.isConnected()) {
            client.disconnect();
            client.close();
        }
        System.out.println();
        System.out.println(BLUE + "[INFO] " + RESET + "后端服务已停止");
        System.out.println(DIM + "      总计接收: " + totalReceived + " 条 | 触发报警: " + alarmCount + " 次" + RESET);
    }
}
