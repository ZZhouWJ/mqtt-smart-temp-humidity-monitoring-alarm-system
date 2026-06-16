package com.example.iot.service;

import com.example.iot.model.AlarmRecord;
import com.example.iot.model.ProcessedSensorData;
import com.example.iot.model.SensorData;
import com.example.iot.websocket.SensorWebSocketHandler;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * 传感器数据业务服务。
 *
 * 工作流程：
 * MQTT 原始数据 -> 丢包检测 -> 跳变检测 -> 滤波 -> 报警判断 -> 诊断建议 -> 保存历史 -> WebSocket 推送。
 */
@Service
public class SensorDataService {

    private final FilterService filterService;
    private final AlarmService alarmService;
    private final DiagnosisService diagnosisService;
    private final SensorWebSocketHandler webSocketHandler;

    private final List<ProcessedSensorData> history = Collections.synchronizedList(new ArrayList<>());
    private final List<AlarmRecord> alarms = Collections.synchronizedList(new ArrayList<>());
    private Long lastSeq = null;

    public SensorDataService(FilterService filterService, AlarmService alarmService,
                             DiagnosisService diagnosisService, SensorWebSocketHandler webSocketHandler) {
        this.filterService = filterService;
        this.alarmService = alarmService;
        this.diagnosisService = diagnosisService;
        this.webSocketHandler = webSocketHandler;
    }

    public synchronized ProcessedSensorData handleRawData(SensorData raw) {
        boolean packetLoss = false;
        if (lastSeq != null && raw.getSeq() != null && raw.getSeq() > lastSeq + 1) {
            packetLoss = true;
        }
        lastSeq = raw.getSeq();

        boolean thresholdOutlier = filterService.isOutlier(raw);
        boolean explicitJump = "jump".equalsIgnoreCase(raw.getStatus());
        boolean explicitLimitAlarm = isLimitAlarmStatus(raw.getStatus());
        boolean outlier = explicitJump || (!explicitLimitAlarm && thresholdOutlier);

        // 超温/超湿演示样本可能在数值上也是一次大跳变，但它们应优先作为环境报警展示；
        // 同时仍不让这类单点大幅变化进入滤波窗口，避免污染后续平滑曲线。
        boolean excludeFromFilter = explicitJump || thresholdOutlier;
        double filteredTemp = filterService.filterTemperature(raw, excludeFromFilter);
        double filteredHumidity = filterService.filterHumidity(raw, excludeFromFilter);

        ProcessedSensorData processed = new ProcessedSensorData();
        processed.setDeviceId(raw.getDeviceId());
        processed.setSeq(raw.getSeq());
        processed.setTimestamp(raw.getTimestamp());
        processed.setRawTemperature(raw.getTemperature());
        processed.setRawHumidity(raw.getHumidity());
        processed.setFilteredTemperature(filteredTemp);
        processed.setFilteredHumidity(filteredHumidity);
        processed.setRawStatus(raw.getStatus());
        processed.setDeviceStatus("offline".equalsIgnoreCase(raw.getStatus()) ? "offline" : "online");
        processed.setPacketLoss(packetLoss);
        processed.setOutlier(outlier);

        alarmService.fillAlarmInfo(processed);
        processed.setDiagnosisAdvice(diagnosisService.generateAdvice(processed));

        history.add(processed);
        if (history.size() > 200) {
            history.remove(0);
        }

        if (alarmService.isAlarm(processed)) {
            alarms.add(alarmService.toAlarmRecord(processed));
            if (alarms.size() > 100) {
                alarms.remove(0);
            }
        }

        webSocketHandler.broadcast(processed);
        return processed;
    }

    private boolean isLimitAlarmStatus(String status) {
        return "temp_high".equalsIgnoreCase(status)
                || "humidity_high".equalsIgnoreCase(status)
                || "both_high".equalsIgnoreCase(status);
    }

    public ProcessedSensorData latest() {
        if (history.isEmpty()) {
            return null;
        }
        return history.get(history.size() - 1);
    }

    public List<ProcessedSensorData> history() {
        return new ArrayList<>(history);
    }

    public List<AlarmRecord> alarms() {
        return new ArrayList<>(alarms);
    }
}
