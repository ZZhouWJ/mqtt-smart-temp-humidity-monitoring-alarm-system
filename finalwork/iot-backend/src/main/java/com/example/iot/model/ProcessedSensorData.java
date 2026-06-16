package com.example.iot.model;

/**
 * 后端处理后的数据，用于推送给前端展示。
 */
public class ProcessedSensorData {
    private String deviceId;
    private Long seq;
    private String timestamp;
    private Double rawTemperature;
    private Double filteredTemperature;
    private Double rawHumidity;
    private Double filteredHumidity;
    private String rawStatus;
    private String deviceStatus;
    private Boolean outlier;
    private Boolean packetLoss;
    private String alarmType;
    private String alarmMessage;
    private String diagnosisAdvice;

    public String getDeviceId() { return deviceId; }
    public void setDeviceId(String deviceId) { this.deviceId = deviceId; }
    public Long getSeq() { return seq; }
    public void setSeq(Long seq) { this.seq = seq; }
    public String getTimestamp() { return timestamp; }
    public void setTimestamp(String timestamp) { this.timestamp = timestamp; }
    public Double getRawTemperature() { return rawTemperature; }
    public void setRawTemperature(Double rawTemperature) { this.rawTemperature = rawTemperature; }
    public Double getFilteredTemperature() { return filteredTemperature; }
    public void setFilteredTemperature(Double filteredTemperature) { this.filteredTemperature = filteredTemperature; }
    public Double getRawHumidity() { return rawHumidity; }
    public void setRawHumidity(Double rawHumidity) { this.rawHumidity = rawHumidity; }
    public Double getFilteredHumidity() { return filteredHumidity; }
    public void setFilteredHumidity(Double filteredHumidity) { this.filteredHumidity = filteredHumidity; }
    public String getRawStatus() { return rawStatus; }
    public void setRawStatus(String rawStatus) { this.rawStatus = rawStatus; }
    public String getDeviceStatus() { return deviceStatus; }
    public void setDeviceStatus(String deviceStatus) { this.deviceStatus = deviceStatus; }
    public Boolean getOutlier() { return outlier; }
    public void setOutlier(Boolean outlier) { this.outlier = outlier; }
    public Boolean getPacketLoss() { return packetLoss; }
    public void setPacketLoss(Boolean packetLoss) { this.packetLoss = packetLoss; }
    public String getAlarmType() { return alarmType; }
    public void setAlarmType(String alarmType) { this.alarmType = alarmType; }
    public String getAlarmMessage() { return alarmMessage; }
    public void setAlarmMessage(String alarmMessage) { this.alarmMessage = alarmMessage; }
    public String getDiagnosisAdvice() { return diagnosisAdvice; }
    public void setDiagnosisAdvice(String diagnosisAdvice) { this.diagnosisAdvice = diagnosisAdvice; }
}
