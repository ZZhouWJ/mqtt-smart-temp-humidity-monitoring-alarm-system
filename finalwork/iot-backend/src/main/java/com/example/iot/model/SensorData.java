package com.example.iot.model;

/**
 * MQTT 原始传感器数据。
 * 字段名称与 Python 端发布的 JSON 保持一致。
 */
public class SensorData {
    private String deviceId;
    private Long seq;
    private String timestamp;
    private Double temperature;
    private Double humidity;
    private String status;

    public String getDeviceId() { return deviceId; }
    public void setDeviceId(String deviceId) { this.deviceId = deviceId; }
    public Long getSeq() { return seq; }
    public void setSeq(Long seq) { this.seq = seq; }
    public String getTimestamp() { return timestamp; }
    public void setTimestamp(String timestamp) { this.timestamp = timestamp; }
    public Double getTemperature() { return temperature; }
    public void setTemperature(Double temperature) { this.temperature = temperature; }
    public Double getHumidity() { return humidity; }
    public void setHumidity(Double humidity) { this.humidity = humidity; }
    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }
}
