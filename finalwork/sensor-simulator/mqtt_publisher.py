"""MQTT 发布端。

运行方式：
    python mqtt_publisher.py --mode normal
    python mqtt_publisher.py --mode demo

normal 模式：按概率随机生成正常、跳变、丢包、离线数据。
demo 模式：按固定顺序生成正常、跳变、超温、超湿、丢包等数据，方便课堂演示。
"""

from __future__ import annotations

import argparse
import json
import random
import signal
import sys
import time
from typing import Iterable, Optional

import paho.mqtt.client as mqtt

import config
from simulator import EnvironmentSimulator, SensorPacket


class RobustMqttPublisher:
    """带断线自动重连能力的 MQTT 发布客户端。"""

    def __init__(self) -> None:
        self.client = mqtt.Client(client_id=config.CLIENT_ID, clean_session=True)
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_publish = self.on_publish
        self.connected = False
        self._stop = False

    def on_connect(self, client, userdata, flags, rc):
        """连接成功回调。rc=0 表示连接成功。"""
        if rc == 0:
            self.connected = True
            print(f"[MQTT] 已连接 Broker: {config.MQTT_HOST}:{config.MQTT_PORT}")
        else:
            print(f"[MQTT] 连接失败，返回码 rc={rc}")

    def on_disconnect(self, client, userdata, rc):
        """断线回调。非主动断开时，进入自动重连。"""
        self.connected = False
        if not self._stop:
            print(f"[MQTT] 连接断开，rc={rc}，准备自动重连")

    def on_publish(self, client, userdata, mid):
        """发布成功回调。"""
        pass

    def connect_with_retry(self) -> None:
        """指数退避重连。

        当公共 MQTT Broker 临时不可用或网络断开时，客户端不会立刻失败退出，
        而是按照 1s、2s、4s、8s、16s、30s 的间隔逐步重试，避免频繁重连造成网络压力。
        """
        delay = 1
        while not self._stop:
            try:
                self.client.connect(config.MQTT_HOST, config.MQTT_PORT, keepalive=60)
                self.client.loop_start()
                return
            except Exception as exc:
                print(f"[MQTT] 连接异常：{exc}，{delay}s 后重试")
                time.sleep(delay)
                delay = min(delay * 2, 30)

    def publish_packet(self, packet: SensorPacket) -> None:
        """发布一条 JSON 数据。"""
        if not self.connected:
            print("[MQTT] 当前未连接，跳过本次发送")
            return

        payload = json.dumps(packet.to_dict(), ensure_ascii=False)
        result = self.client.publish(config.MQTT_TOPIC, payload=payload, qos=1)
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print(f"[PUB] topic={config.MQTT_TOPIC} payload={payload}")
        else:
            print(f"[PUB] 发布失败，rc={result.rc}")

    def stop(self) -> None:
        self._stop = True
        self.client.loop_stop()
        self.client.disconnect()


def demo_status_sequence() -> Iterable[Optional[str]]:
    """演示模式的状态序列。

    让前端和后端能稳定看到：正常数据、跳变异常、超温报警、超湿报警、丢包。
    """
    seq = [
        "normal", "normal", "normal", "jump", "normal",
        "temp_high", "normal", "humidity_high", "normal",
        "both_high", "lost", "normal", "offline", "normal",
    ]
    while True:
        for item in seq:
            yield item


def main() -> None:
    parser = argparse.ArgumentParser(description="模拟温湿度传感器 MQTT 发布端")
    parser.add_argument("--mode", choices=["normal", "demo"], default="normal", help="运行模式")
    parser.add_argument("--interval", type=float, default=config.PUBLISH_INTERVAL, help="发送间隔，单位秒")
    args = parser.parse_args()

    simulator = EnvironmentSimulator()
    publisher = RobustMqttPublisher()
    publisher.connect_with_retry()

    def handle_signal(signum, frame):
        print("\n[SYS] 收到退出信号，正在关闭 MQTT 客户端")
        publisher.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    status_iter = demo_status_sequence() if args.mode == "demo" else None

    while True:
        force_status = next(status_iter) if status_iter else None
        packet = simulator.next_packet(force_status=force_status)

        if packet is None:
            print("[SIM] 本次模拟丢包：未发布数据")
        else:
            publisher.publish_packet(packet)

        # 模拟离线状态：短暂休眠，后端可据此判断数据间隔异常
        if packet and packet.status == "offline":
            print("[SIM] 模拟设备短暂离线 3 秒")
            time.sleep(3)
        else:
            time.sleep(args.interval)


if __name__ == "__main__":
    main()
