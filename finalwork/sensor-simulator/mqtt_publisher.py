"""MQTT 发布端 - 优化版控制台输出

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
from datetime import datetime
from typing import Iterable, Optional

import paho.mqtt.client as mqtt

import config
from simulator import EnvironmentSimulator, SensorPacket


class ColoredPrinter:
    """终端彩色输出工具"""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

    # 颜色
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'

    @classmethod
    def timestamp(cls) -> str:
        return datetime.now().strftime("%H:%M:%S")

    @classmethod
    def info(cls, msg: str) -> str:
        return f"{cls.DIM}[{cls.timestamp()}]{cls.RESET} {cls.BLUE}[INFO]{cls.RESET} {msg}"

    @classmethod
    def success(cls, msg: str) -> str:
        return f"{cls.DIM}[{cls.timestamp()}]{cls.RESET} {cls.GREEN}[OK]{cls.RESET} {msg}"

    @classmethod
    def warn(cls, msg: str) -> str:
        return f"{cls.DIM}[{cls.timestamp()}]{cls.RESET} {cls.YELLOW}[WARN]{cls.RESET} {msg}"

    @classmethod
    def error(cls, msg: str) -> str:
        return f"{cls.DIM}[{cls.timestamp()}]{cls.RESET} {cls.RED}[ERROR]{cls.RESET} {msg}"

    @classmethod
    def data(cls, temp: float, humi: float, status: str) -> str:
        status_colors = {
            'normal': cls.GREEN,
            'jump': cls.YELLOW,
            'temp_high': cls.RED,
            'humidity_high': cls.RED,
            'both_high': cls.RED,
            'offline': cls.MAGENTA,
        }
        color = status_colors.get(status, cls.GREEN)
        status_text = {
            'normal': 'NORMAL',
            'jump': 'JUMP!',
            'temp_high': 'TEMP HIGH',
            'humidity_high': 'HUMI HIGH',
            'both_high': 'ALARM!',
            'offline': 'OFFLINE',
        }
        return (
            f"{cls.DIM}[{cls.timestamp()}]{cls.RESET} "
            f"{cls.CYAN}[DATA]{cls.RESET} "
            f"Temp: {color}{temp:>6.1f}°C{cls.RESET}  "
            f"Humi: {color}{humi:>5.1f}%{cls.RESET}  "
            f"Status: {color}{status_text.get(status, status):<10}{cls.RESET}"
        )


class RobustMqttPublisher:
    """带断线自动重连能力的 MQTT 发布客户端。"""

    def __init__(self) -> None:
        self.client = mqtt.Client(client_id=config.CLIENT_ID, clean_session=True)
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_publish = self.on_publish
        self.connected = False
        self._stop = False
        self.reconnect_count = 0
        self.total_sent = 0

    def on_connect(self, client, userdata, flags, rc):
        """连接成功回调。rc=0 表示连接成功。"""
        if rc == 0:
            self.connected = True
            if self.reconnect_count > 0:
                print(ColoredPrinter.success(
                    f"重连成功！Broker: {config.MQTT_HOST}:{config.MQTT_PORT} "
                    f"(第 {self.reconnect_count} 次重连)"
                ))
            else:
                print(ColoredPrinter.success(
                    f"已连接 Broker: {config.MQTT_HOST}:{config.MQTT_PORT}"
                ))
            self.reconnect_count = 0
        else:
            print(ColoredPrinter.error(f"连接失败，返回码 rc={rc}"))
            self._print_broker_tips()

    def _print_broker_tips(self):
        """打印 Broker 连接失败提示"""
        print(ColoredPrinter.info("请确保 MQTT Broker 已启动："))
        print(ColoredPrinter.info("  - Docker: docker compose up -d"))
        print(ColoredPrinter.info("  - 本地: mosquitto -v"))

    def on_disconnect(self, client, userdata, rc):
        """断线回调。非主动断开时，进入自动重连。"""
        self.connected = False
        if not self._stop:
            if rc == 0:
                print(ColoredPrinter.info("主动断开连接"))
            else:
                print(ColoredPrinter.warn(
                    f"连接异常断开 (rc={rc})，正在尝试重连..."
                ))

    def on_publish(self, client, userdata, mid):
        """发布成功回调。"""
        pass

    def connect_with_retry(self) -> None:
        """指数退避重连。"""
        delay = 1
        while not self._stop:
            try:
                print(ColoredPrinter.info(
                    f"正在连接 {config.MQTT_HOST}:{config.MQTT_PORT}..."
                ))
                self.client.connect(config.MQTT_HOST, config.MQTT_PORT, keepalive=60)
                self.client.loop_start()
                return
            except Exception as exc:
                self.reconnect_count += 1
                print(ColoredPrinter.warn(
                    f"连接失败: {exc}，{delay}s 后重试 "
                    f"(第 {self.reconnect_count} 次尝试)"
                ))
                time.sleep(delay)
                delay = min(delay * 2, 30)

    def publish_packet(self, packet: SensorPacket) -> None:
        """发布一条 JSON 数据。"""
        if not self.connected:
            print(ColoredPrinter.warn("当前未连接，跳过本次发送"))
            return

        payload = json.dumps(packet.to_dict(), ensure_ascii=False)
        result = self.client.publish(config.MQTT_TOPIC, payload=payload, qos=1)
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            self.total_sent += 1
            print(ColoredPrinter.data(
                packet.temperature,
                packet.humidity,
                packet.status
            ))
        else:
            print(ColoredPrinter.error(f"发布失败，rc={result.rc}"))

    def stop(self) -> None:
        self._stop = True
        self.client.loop_stop()
        self.client.disconnect()
        print(ColoredPrinter.info(
            f"已停止运行，共发送 {self.total_sent} 条数据"
        ))


def demo_status_sequence() -> Iterable[Optional[str]]:
    """演示模式的状态序列。"""
    seq = [
        "normal", "normal", "normal",           # 3条正常数据
        "jump", "normal",                        # 1条跳变
        "temp_high", "normal",                   # 高温报警
        "humidity_high", "normal",                # 高湿报警
        "both_high", "normal",                   # 复合报警
        "lost", "normal",                         # 丢包
        "offline", "normal",                     # 离线
    ]
    while True:
        for item in seq:
            yield item


def print_banner():
    """打印欢迎横幅"""
    banner = f"""
{ColoredPrinter.BOLD}{ColoredPrinter.CYAN}╔══════════════════════════════════════════════════════════╗
║        MQTT 环境监测传感器模拟器 v2.0                 ║
║        环境: {config.MQTT_HOST}:{config.MQTT_PORT}  主题: {config.MQTT_TOPIC:<25}  ║
╚══════════════════════════════════════════════════════════╝{ColoredPrinter.RESET}
    """
    print(banner)


def print_usage(mode: str):
    """打印使用说明"""
    if mode == "demo":
        print(ColoredPrinter.info("演示模式：按固定顺序生成各种状态数据"))
        print(ColoredPrinter.info("  → 正常 → 跳变 → 高温 → 高湿 → 复合报警 → 丢包 → 离线"))
    else:
        print(ColoredPrinter.info("普通模式：按概率随机生成异常数据"))
        print(ColoredPrinter.info(
            f"  → 跳变概率: {config.JUMP_PROBABILITY*100:.0f}%  "
            f"丢包概率: {config.DROP_PROBABILITY*100:.0f}%  "
            f"离线概率: {config.OFFLINE_PROBABILITY*100:.0f}%"
        ))
    print()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="MQTT 环境监测传感器模拟器",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--mode",
        choices=["normal", "demo"],
        default="normal",
        help="运行模式: normal(随机异常) / demo(固定序列)"
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=config.PUBLISH_INTERVAL,
        help="发送间隔，单位秒"
    )
    args = parser.parse_args()

    print_banner()
    print_usage(args.mode)

    simulator = EnvironmentSimulator()
    publisher = RobustMqttPublisher()
    publisher.connect_with_retry()

    def handle_signal(signum, frame):
        print(f"\n{ColoredPrinter.warn('收到退出信号，正在关闭...')}")
        publisher.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    status_iter = demo_status_sequence() if args.mode == "demo" else None

    print(ColoredPrinter.success("开始模拟数据发送...\n"))

    while True:
        force_status = next(status_iter) if status_iter else None
        packet = simulator.next_packet(force_status=force_status)

        if packet is None:
            print(ColoredPrinter.warn("丢包：本次未发送数据"))
        else:
            # 根据状态打印不同的警告信息
            if packet.status == "jump":
                print(ColoredPrinter.warn(
                    f"检测到传感器跳变异常！seq={packet.seq}"
                ))
            elif packet.status == "temp_high":
                print(ColoredPrinter.warn(
                    f"触发高温报警！温度={packet.temperature}°C"
                ))
            elif packet.status == "humidity_high":
                print(ColoredPrinter.warn(
                    f"触发高湿报警！湿度={packet.humidity}%"
                ))
            elif packet.status == "both_high":
                print(ColoredPrinter.error(
                    f"⚠ 复合报警！温度={packet.temperature}°C 湿度={packet.humidity}%"
                ))
            elif packet.status == "offline":
                print(ColoredPrinter.warn(
                    f"设备离线模拟 (seq={packet.seq})"
                ))
                publisher.publish_packet(packet)
                time.sleep(3)
                continue

            publisher.publish_packet(packet)

        time.sleep(args.interval)


if __name__ == "__main__":
    main()
