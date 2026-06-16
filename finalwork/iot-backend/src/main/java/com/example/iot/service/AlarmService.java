package com.example.iot.service;

import com.example.iot.model.AlarmRecord;
import com.example.iot.model.ProcessedSensorData;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

/**
 * 超温、超湿、异常数据报警服务。
 */
@Service
public class AlarmService {

    @Value("${alarm.temperatureHigh:35.0}")
    private double temperatureHigh;

    @Value("${alarm.humidityHigh:80.0}")
    private double humidityHigh;

    public void fillAlarmInfo(ProcessedSensorData data) {
        boolean explicitJump = "jump".equalsIgnoreCase(data.getRawStatus());
        boolean outlier = Boolean.TRUE.equals(data.getOutlier());
        boolean explicitTempHigh = "temp_high".equalsIgnoreCase(data.getRawStatus())
                || "both_high".equalsIgnoreCase(data.getRawStatus());
        boolean explicitHumidityHigh = "humidity_high".equalsIgnoreCase(data.getRawStatus())
                || "both_high".equalsIgnoreCase(data.getRawStatus());
        boolean measuredTempHigh = isAbove(data.getRawTemperature(), temperatureHigh)
                || isAbove(data.getFilteredTemperature(), temperatureHigh);
        boolean measuredHumidityHigh = isAbove(data.getRawHumidity(), humidityHigh)
                || isAbove(data.getFilteredHumidity(), humidityHigh);
        boolean tempHigh = !explicitJump && (explicitTempHigh || (!outlier && measuredTempHigh));
        boolean humHigh = !explicitJump && (explicitHumidityHigh || (!outlier && measuredHumidityHigh));
        boolean packetLoss = Boolean.TRUE.equals(data.getPacketLoss());
        boolean offline = "offline".equalsIgnoreCase(data.getDeviceStatus());

        if (tempHigh && humHigh) {
            data.setAlarmType("BOTH_HIGH");
            data.setAlarmMessage("温度和湿度均超过阈值");
        } else if (tempHigh) {
            data.setAlarmType("TEMP_HIGH");
            data.setAlarmMessage("温度超过阈值");
        } else if (humHigh) {
            data.setAlarmType("HUMIDITY_HIGH");
            data.setAlarmMessage("湿度超过阈值");
        } else if (outlier) {
            data.setAlarmType("DATA_OUTLIER");
            data.setAlarmMessage("检测到传感器跳变异常");
        } else if (packetLoss) {
            data.setAlarmType("PACKET_LOSS");
            data.setAlarmMessage("检测到 MQTT 数据序号不连续，可能发生丢包");
        } else if (offline) {
            data.setAlarmType("DEVICE_OFFLINE");
            data.setAlarmMessage("设备上报离线状态或采集暂停");
        } else {
            data.setAlarmType("NORMAL");
            data.setAlarmMessage("环境状态正常");
        }
    }

    private boolean isAbove(Double value, double threshold) {
        return value != null && value >= threshold;
    }

    public boolean isAlarm(ProcessedSensorData data) {
        return data.getAlarmType() != null && !"NORMAL".equals(data.getAlarmType());
    }

    public AlarmRecord toAlarmRecord(ProcessedSensorData data) {
        return new AlarmRecord(
                data.getDeviceId(),
                data.getTimestamp(),
                data.getAlarmType(),
                data.getAlarmMessage(),
                data.getDiagnosisAdvice(),
                data.getFilteredTemperature(),
                data.getFilteredHumidity()
        );
    }
}
