package com.example.iot.service;

import com.example.iot.model.SensorData;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.util.ArrayDeque;
import java.util.Deque;

/**
 * 滤波与异常点处理服务。
 *
 * 策略：
 * 1. 滑动平均滤波：保留最近 N 个有效值，计算均值，降低随机噪声影响；
 * 2. 跳变异常检测：如果当前值与上一有效值差距过大，则认为是跳变异常；
 * 3. 异常点不直接进入滑动窗口，避免污染后续平滑曲线。
 */
@Service
public class FilterService {

    @Value("${filter.windowSize:5}")
    private int windowSize;

    @Value("${filter.maxTemperatureJump:8.0}")
    private double maxTemperatureJump;

    @Value("${filter.maxHumidityJump:15.0}")
    private double maxHumidityJump;

    private final Deque<Double> tempWindow = new ArrayDeque<>();
    private final Deque<Double> humidityWindow = new ArrayDeque<>();
    private Double lastValidTemp = null;
    private Double lastValidHumidity = null;

    public synchronized boolean isOutlier(SensorData data) {
        if (data.getTemperature() == null || data.getHumidity() == null) {
            return true;
        }
        if (lastValidTemp == null || lastValidHumidity == null) {
            return false;
        }
        double tempDiff = Math.abs(data.getTemperature() - lastValidTemp);
        double humidityDiff = Math.abs(data.getHumidity() - lastValidHumidity);
        return tempDiff > maxTemperatureJump || humidityDiff > maxHumidityJump;
    }

    public synchronized double filterTemperature(SensorData data, boolean outlier) {
        if (!outlier) {
            lastValidTemp = data.getTemperature();
            push(tempWindow, data.getTemperature());
        }
        return average(tempWindow, data.getTemperature());
    }

    public synchronized double filterHumidity(SensorData data, boolean outlier) {
        if (!outlier) {
            lastValidHumidity = data.getHumidity();
            push(humidityWindow, data.getHumidity());
        }
        return average(humidityWindow, data.getHumidity());
    }

    private void push(Deque<Double> window, double value) {
        window.addLast(value);
        while (window.size() > windowSize) {
            window.removeFirst();
        }
    }

    private double average(Deque<Double> window, double defaultValue) {
        if (window.isEmpty()) {
            return defaultValue;
        }
        double sum = 0.0;
        for (Double value : window) {
            sum += value;
        }
        return Math.round((sum / window.size()) * 100.0) / 100.0;
    }
}
