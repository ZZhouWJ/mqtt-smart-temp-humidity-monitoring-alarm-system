package com.example.iot.model;

/**
 * 报警记录。
 */
public class AlarmRecord {
    private String deviceId;
    private String timestamp;
    private String alarmType;
    private String alarmMessage;
    private String diagnosisAdvice;
    private Double temperature;
    private Double humidity;

    public AlarmRecord() {}

    public AlarmRecord(String deviceId, String timestamp, String alarmType, String alarmMessage,
                       String diagnosisAdvice, Double temperature, Double humidity) {
        this.deviceId = deviceId;
        this.timestamp = timestamp;
        this.alarmType = alarmType;
        this.alarmMessage = alarmMessage;
        this.diagnosisAdvice = diagnosisAdvice;
        this.temperature = temperature;
        this.humidity = humidity;
    }

    public String getDeviceId() { return deviceId; }
    public void setDeviceId(String deviceId) { this.deviceId = deviceId; }
    public String getTimestamp() { return timestamp; }
    public void setTimestamp(String timestamp) { this.timestamp = timestamp; }
    public String getAlarmType() { return alarmType; }
    public void setAlarmType(String alarmType) { this.alarmType = alarmType; }
    public String getAlarmMessage() { return alarmMessage; }
    public void setAlarmMessage(String alarmMessage) { this.alarmMessage = alarmMessage; }
    public String getDiagnosisAdvice() { return diagnosisAdvice; }
    public void setDiagnosisAdvice(String diagnosisAdvice) { this.diagnosisAdvice = diagnosisAdvice; }
    public Double getTemperature() { return temperature; }
    public void setTemperature(Double temperature) { this.temperature = temperature; }
    public Double getHumidity() { return humidity; }
    public void setHumidity(Double humidity) { this.humidity = humidity; }
}
