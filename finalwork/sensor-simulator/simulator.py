"""温湿度模拟器。

功能：
1. 使用电脑模拟一个温湿度采集节点；
2. 周期性生成温度、湿度数据；
3. 主动加入白噪声，模拟真实传感器误差；
4. 主动注入跳变异常、丢包异常、短暂离线状态，便于后端测试异常处理策略。
"""

from __future__ import annotations

import math
import random
import time
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional, Tuple

import config


@dataclass
class SensorPacket:
    """单条传感器数据包。"""

    deviceId: str
    seq: int
    timestamp: str
    temperature: float
    humidity: float
    status: str

    def to_dict(self) -> dict:
        return asdict(self)


class EnvironmentSimulator:
    """温湿度数据生成器。

    通过正弦波 + 随机噪声生成更接近真实环境的温湿度变化：
    - 正弦波：模拟环境缓慢变化趋势；
    - 随机噪声：模拟传感器测量误差；
    - 跳变异常：模拟传感器故障或采样干扰。
    """

    def __init__(self, device_id: str = config.DEVICE_ID) -> None:
        self.device_id = device_id
        self.seq = 0
        self.start_time = time.time()

    def _normal_value(self) -> Tuple[float, float]:
        """生成正常温湿度。

        返回：
            temperature: 温度
            humidity: 湿度
        """
        elapsed = time.time() - self.start_time

        # 缓慢周期变化，让曲线更自然
        temp_trend = math.sin(elapsed / 30.0) * 2.0
        humidity_trend = math.cos(elapsed / 35.0) * 5.0

        temp_noise = random.uniform(*config.TEMP_NOISE_RANGE)
        humidity_noise = random.uniform(*config.HUMIDITY_NOISE_RANGE)

        temperature = config.BASE_TEMPERATURE + temp_trend + temp_noise
        humidity = config.BASE_HUMIDITY + humidity_trend + humidity_noise

        return round(temperature, 2), round(humidity, 2)

    def next_packet(self, force_status: Optional[str] = None) -> Optional[SensorPacket]:
        """生成下一条数据。

        Args:
            force_status: 强制指定数据状态，可用于演示模式。

        Returns:
            SensorPacket 或 None。None 表示本次模拟丢包。
        """
        self.seq += 1

        # 演示或随机丢包：直接不返回数据，让 MQTT 发布端跳过本次发送
        status = force_status or self._random_status()
        if status == "lost":
            return None

        temperature, humidity = self._normal_value()

        # 跳变异常：人为制造明显离谱的温湿度，后端用于异常检测与滤波
        if status == "jump":
            temperature += random.choice([18.0, 25.0, -15.0])
            humidity += random.choice([25.0, -30.0])

        # 报警演示：制造超温、超湿数据
        if status == "temp_high":
            temperature = random.uniform(36.0, 42.0)
        elif status == "humidity_high":
            humidity = random.uniform(82.0, 95.0)
        elif status == "both_high":
            temperature = random.uniform(36.0, 42.0)
            humidity = random.uniform(82.0, 95.0)

        return SensorPacket(
            deviceId=self.device_id,
            seq=self.seq,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            temperature=round(temperature, 2),
            humidity=round(humidity, 2),
            status=status,
        )

    def _random_status(self) -> str:
        """按概率生成当前数据状态。"""
        r = random.random()
        if r < config.DROP_PROBABILITY:
            return "lost"
        if r < config.DROP_PROBABILITY + config.OFFLINE_PROBABILITY:
            return "offline"
        if r < config.DROP_PROBABILITY + config.OFFLINE_PROBABILITY + config.JUMP_PROBABILITY:
            return "jump"
        return "normal"


# ============================================
# 数据状态枚举（供文档参考）
# ============================================
"""
数据状态说明：

| 状态 | 说明 | 触发条件 |
|------|------|----------|
| normal | 正常数据 | 无异常时 |
| jump | 跳变异常 | 传感器故障、采样干扰 |
| temp_high | 高温报警 | 温度 > 35°C |
| humidity_high | 高湿报警 | 湿度 > 80% |
| both_high | 复合报警 | 温湿度同时超标 |
| lost | 丢包 | 本次不发送数据 |
| offline | 设备离线 | 短暂断开连接 |
"""
