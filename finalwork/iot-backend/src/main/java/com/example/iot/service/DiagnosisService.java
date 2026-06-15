package com.example.iot.service;

import com.example.iot.model.ProcessedSensorData;
import org.springframework.stereotype.Service;

/**
 * 本地规则诊断服务。
 *
 * 说明：Gemini 建议接入 LLM API 生成异常解释。为了保证课堂演示稳定，
 * 本项目采用“规则驱动的轻量诊断建议”，不依赖外部 API Key 和网络请求。
 * 后续可把本服务替换为 DeepSeek、Kimi 等大模型 API 调用。
 */
@Service
public class DiagnosisService {

    public String generateAdvice(ProcessedSensorData data) {
        String type = data.getAlarmType();
        if ("TEMP_HIGH".equals(type)) {
            return "建议检查设备是否靠近热源、机房散热是否正常，并确认温度传感器未被遮挡。";
        }
        if ("HUMIDITY_HIGH".equals(type)) {
            return "建议检查是否存在漏水、潮湿积水或通风不足，并确认湿度传感器探头状态。";
        }
        if ("BOTH_HIGH".equals(type)) {
            return "温湿度同时升高，建议优先排查环境通风、空调制冷与设备散热状态。";
        }
        if ("DATA_OUTLIER".equals(type)) {
            return "数据出现突变，可能是传感器接触不良、电磁干扰或采样瞬时异常，建议复测并检查线路。";
        }
        if ("PACKET_LOSS".equals(type)) {
            return "检测到数据序号不连续，建议检查网络质量、MQTT Broker 连接状态和采样端运行日志。";
        }
        if ("DEVICE_OFFLINE".equals(type)) {
            return "设备离线或暂停上报，建议检查采集程序是否运行、网络是否断开以及 MQTT 重连日志。";
        }
        return "当前数据处于正常范围，保持持续监测即可。";
    }
}
