package com.example.iot.controller;

import com.example.iot.model.AlarmRecord;
import com.example.iot.model.ProcessedSensorData;
import com.example.iot.service.SensorDataService;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * 前端可调用的 REST 接口。
 */
@RestController
@RequestMapping("/api")
@CrossOrigin
public class SensorDataController {

    private final SensorDataService sensorDataService;

    public SensorDataController(SensorDataService sensorDataService) {
        this.sensorDataService = sensorDataService;
    }

    @GetMapping("/latest")
    public ProcessedSensorData latest() {
        return sensorDataService.latest();
    }

    @GetMapping("/history")
    public List<ProcessedSensorData> history() {
        return sensorDataService.history();
    }

    @GetMapping("/alarms")
    public List<AlarmRecord> alarms() {
        return sensorDataService.alarms();
    }

    @GetMapping("/health")
    public String health() {
        return "iot-backend is running";
    }
}
