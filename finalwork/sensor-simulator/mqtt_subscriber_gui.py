"""MQTT 订阅端 - 实时可视化界面

功能：
- 订阅 MQTT 温湿度数据
- 实时绘制动态曲线
- 显示连接状态和报警信息
- 断线重连自动处理

运行方式：
    python mqtt_subscriber_gui.py
"""

import json
import signal
import sys
import threading
from collections import deque
from datetime import datetime
from typing import Optional

import paho.mqtt.client as mqtt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import config

# ============================================
# 颜色主题（深色专业风格）
# ============================================
COLORS = {
    'bg': '#1a1a2e',
    'surface': '#16213e',
    'surface_light': '#1f3460',
    'primary': '#4cc9f0',
    'success': '#06d6a0',
    'warning': '#ffd166',
    'danger': '#ef476f',
    'text': '#edf2f4',
    'text_dim': '#8d99ae',
    'chart_temp': '#4cc9f0',
    'chart_humi': '#06d6a0',
    'chart_grid': '#2a2a4a',
}

# ============================================
# MQTT 客户端
# ============================================

class MqttSubscriber:
    """MQTT 订阅客户端"""

    def __init__(self, on_message_callback, on_connect_callback, on_disconnect_callback):
        self.client = mqtt.Client(client_id=f"gui_subscriber_{id(self)}")
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_message = self._on_message
        self.client.on_log = self._on_log

        self._on_message_callback = on_message_callback
        self._on_connect_callback = on_connect_callback
        self._on_disconnect_callback = on_disconnect_callback

        self.connected = False
        self.reconnect_attempts = 0

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.connected = True
            self.reconnect_attempts = 0
            self._on_connect_callback()
        else:
            self._on_connect_callback(rc)

    def _on_disconnect(self, client, userdata, rc):
        self.connected = False
        self._on_disconnect_callback(rc)

    def _on_message(self, client, userdata, msg):
        try:
            data = json.loads(msg.payload.decode())
            self._on_message_callback(data)
        except Exception as e:
            print(f"消息解析错误: {e}")

    def _on_log(self, client, userdata, level, buf):
        pass  # 静默日志

    def connect(self):
        """连接 MQTT Broker"""
        try:
            self.client.connect(config.MQTT_HOST, config.MQTT_PORT, keepalive=60)
            self.client.loop_start()
        except Exception as e:
            print(f"连接失败: {e}")
            self._schedule_reconnect()

    def _schedule_reconnect(self):
        """调度重连"""
        self.reconnect_attempts += 1
        delay = min(2 ** self.reconnect_attempts, 60)
        threading.Timer(delay, self.connect).start()

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()


# ============================================
# 数据管理器
# ============================================

class DataManager:
    """管理实时数据缓冲区"""

    def __init__(self, max_points=60):
        self.max_points = max_points
        self.timestamps = deque(maxlen=max_points)
        self.temperatures = deque(maxlen=max_points)
        self.humidities = deque(maxlen=max_points)
        self.raw_temps = deque(maxlen=max_points)
        self.raw_humis = deque(maxlen=max_points)

        self.latest_temp = None
        self.latest_humi = None
        self.alarm_type = None
        self.seq = 0

    def add(self, data: dict):
        """添加新数据点"""
        self.seq += 1
        timestamp = data.get('timestamp', datetime.now().strftime("%H:%M:%S"))
        temp = data.get('temperature', 0)
        humi = data.get('humidity', 0)

        self.timestamps.append(timestamp)
        self.temperatures.append(temp)
        self.humidities.append(humi)
        self.raw_temps.append(temp)
        self.raw_humis.append(humi)

        self.latest_temp = temp
        self.latest_humi = humi
        self.alarm_type = data.get('status', 'normal')

    def get_data(self) -> dict:
        """获取绘图数据"""
        return {
            'timestamps': list(self.timestamps),
            'temperatures': list(self.temperatures),
            'humidities': list(self.humidities),
            'raw_temps': list(self.raw_temps),
            'raw_humis': list(self.raw_humis),
        }


# ============================================
# 主界面
# ============================================

class SensorDashboard(tk.Tk):
    """温湿度监测仪表盘"""

    def __init__(self):
        super().__init__()

        self.title("温湿度环境监测系统 - MQTT Subscriber")
        self.geometry("1200x800")
        self.configure(bg=COLORS['bg'])
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # 数据管理
        self.data_manager = DataManager(max_points=60)

        # MQTT 客户端
        self.mqtt = MqttSubscriber(
            on_message_callback=self.on_mqtt_message,
            on_connect_callback=self.on_connect,
            on_disconnect_callback=self.on_disconnect,
        )

        # 创建界面
        self.create_widgets()

        # 启动 MQTT
        self.mqtt.connect()

        # 启动动画
        self.ani = animation.FuncAnimation(
            self.fig, self.update_plot, interval=500, blit=True
        )

    def create_widgets(self):
        """创建界面组件"""
        # 主容器
        main_frame = tk.Frame(self, bg=COLORS['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # 顶部状态栏
        self.create_status_bar(main_frame)

        # 数值卡片区
        self.create_value_cards(main_frame)

        # 图表区
        self.create_charts(main_frame)

        # 报警信息区
        self.create_alarm_panel(main_frame)

    def create_status_bar(self, parent):
        """创建状态栏"""
        status_frame = tk.Frame(parent, bg=COLORS['surface'], pady=10, padx=15)
        status_frame.pack(fill=tk.X)

        # 标题
        title = tk.Label(
            status_frame,
            text="环境监测系统",
            font=("Microsoft YaHei UI", 18, "bold"),
            fg=COLORS['text'],
            bg=COLORS['surface']
        )
        title.pack(side=tk.LEFT)

        # 连接状态
        self.status_label = tk.Label(
            status_frame,
            text="● 正在连接...",
            font=("Microsoft YaHei UI", 12),
            fg=COLORS['warning'],
            bg=COLORS['surface']
        )
        self.status_label.pack(side=tk.RIGHT)

    def create_value_cards(self, parent):
        """创建数值卡片"""
        cards_frame = tk.Frame(parent, bg=COLORS['bg'])
        cards_frame.pack(fill=tk.X, pady=(20, 10))

        # 温度卡片
        self.temp_card = self.create_single_card(
            cards_frame, "当前温度", "℃", COLORS['chart_temp'], 0
        )

        # 湿度卡片
        self.humi_card = self.create_single_card(
            cards_frame, "当前湿度", "%RH", COLORS['chart_humi'], 1
        )

        # 状态卡片
        self.state_card = self.create_state_card(cards_frame, 2)

    def create_single_card(self, parent, title: str, unit: str, color: str, col: int):
        """创建单个数值卡片"""
        card = tk.Frame(parent, bg=COLORS['surface'], padx=30, pady=20)
        card.grid(row=0, column=col, padx=10, sticky="nsew")

        label = tk.Label(
            card, text=title,
            font=("Microsoft YaHei UI", 11),
            fg=COLORS['text_dim'],
            bg=COLORS['surface']
        )
        label.pack(anchor="w")

        value_frame = tk.Frame(card, bg=COLORS['surface'])
        value_frame.pack(fill=tk.X, pady=(5, 0))

        value_label = tk.Label(
            value_frame,
            text="--",
            font=("JetBrains Mono", 36, "bold"),
            fg=color,
            bg=COLORS['surface']
        )
        value_label.pack(side=tk.LEFT)

        unit_label = tk.Label(
            value_frame,
            text=unit,
            font=("Microsoft YaHei UI", 14),
            fg=COLORS['text_dim'],
            bg=COLORS['surface']
        )
        unit_label.pack(side=tk.LEFT, padx=(5, 0))

        return value_label

    def create_state_card(self, parent, col: int):
        """创建设备状态卡片"""
        card = tk.Frame(parent, bg=COLORS['surface'], padx=30, pady=20)
        card.grid(row=0, column=col, padx=10, sticky="nsew")

        label = tk.Label(
            card, text="设备状态",
            font=("Microsoft YaHei UI", 11),
            fg=COLORS['text_dim'],
            bg=COLORS['surface']
        )
        label.pack(anchor="w")

        state_label = tk.Label(
            card,
            text="等待数据...",
            font=("Microsoft YaHei UI", 18, "bold"),
            fg=COLORS['success'],
            bg=COLORS['surface']
        )
        state_label.pack(anchor="w", pady=(5, 0))

        return state_label

    def create_charts(self, parent):
        """创建图表区域"""
        charts_frame = tk.Frame(parent, bg=COLORS['bg'])
        charts_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.fig = Figure(figsize=(10, 5), facecolor=COLORS['surface'])
        self.fig.subplots_adjust(hspace=0.3)

        # 温度子图
        self.ax_temp = self.fig.add_subplot(211)
        self.ax_temp.set_facecolor(COLORS['bg'])
        self.ax_temp.set_title("温度曲线 (°C)", color=COLORS['text'], fontsize=10, pad=5)
        self.ax_temp.tick_params(colors=COLORS['text_dim'], labelsize=8)
        self.ax_temp.spines['bottom'].set_color(COLORS['chart_grid'])
        self.ax_temp.spines['left'].set_color(COLORS['chart_grid'])
        self.ax_temp.spines['top'].set_visible(False)
        self.ax_temp.spines['right'].set_visible(False)
        self.ax_temp.grid(True, color=COLORS['chart_grid'], alpha=0.3)

        # 湿度子图
        self.ax_humi = self.fig.add_subplot(212)
        self.ax_humi.set_facecolor(COLORS['bg'])
        self.ax_humi.set_title("湿度曲线 (%RH)", color=COLORS['text'], fontsize=10, pad=5)
        self.ax_humi.tick_params(colors=COLORS['text_dim'], labelsize=8)
        self.ax_humi.spines['bottom'].set_color(COLORS['chart_grid'])
        self.ax_humi.spines['left'].set_color(COLORS['chart_grid'])
        self.ax_humi.spines['top'].set_visible(False)
        self.ax_humi.spines['right'].set_visible(False)
        self.ax_humi.grid(True, color=COLORS['chart_grid'], alpha=0.3)

        # 初始化空曲线
        self.line_temp, = self.ax_temp.plot([], [], color=COLORS['chart_temp'], linewidth=2)
        self.line_humi, = self.ax_humi.plot([], [], color=COLORS['chart_humi'], linewidth=2)

        # 阈值线
        self.ax_temp.axhline(y=35, color=COLORS['danger'], linestyle='--', alpha=0.5, linewidth=1)
        self.ax_humi.axhline(y=80, color=COLORS['danger'], linestyle='--', alpha=0.5, linewidth=1)

        self.canvas = FigureCanvasTkAgg(self.fig, master=charts_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def create_alarm_panel(self, parent):
        """创建报警面板"""
        alarm_frame = tk.Frame(parent, bg=COLORS['surface'], padx=15, pady=10)
        alarm_frame.pack(fill=tk.X, pady=(10, 0))

        # 报警标题
        title = tk.Label(
            alarm_frame,
            text="报警记录",
            font=("Microsoft YaHei UI", 12, "bold"),
            fg=COLORS['text'],
            bg=COLORS['surface']
        )
        title.pack(anchor="w")

        # 报警内容
        self.alarm_label = tk.Label(
            alarm_frame,
            text="系统运行正常，无报警",
            font=("Microsoft YaHei UI", 11),
            fg=COLORS['success'],
            bg=COLORS['surface']
        )
        self.alarm_label.pack(anchor="w", pady=(5, 0))

    def update_plot(self, frame):
        """更新图表"""
        data = self.data_manager.get_data()

        if not data['timestamps']:
            return self.line_temp, self.line_humi

        # 更新数据
        self.line_temp.set_data(range(len(data['temperatures'])), data['temperatures'])
        self.line_humi.set_data(range(len(data['humidities'])), data['humidities'])

        # 调整坐标轴
        self.ax_temp.set_xlim(0, max(60, len(data['temperatures'])))
        self.ax_humi.set_xlim(0, max(60, len(data['humidities'])))

        if data['temperatures']:
            self.ax_temp.set_ylim(
                min(data['temperatures']) - 5,
                max(data['temperatures']) + 5
            )
        if data['humidities']:
            self.ax_humi.set_ylim(
                min(data['humidities']) - 10,
                max(data['humidities']) + 10
            )

        return self.line_temp, self.line_humi

    def on_mqtt_message(self, data: dict):
        """处理 MQTT 消息"""
        self.data_manager.add(data)

        # 更新界面
        self.update_display(data)

    def update_display(self, data: dict):
        """更新显示"""
        temp = data.get('temperature', 0)
        humi = data.get('humidity', 0)
        status = data.get('status', 'normal')

        # 更新数值
        self.temp_card.config(text=f"{temp:.1f}")
        self.humi_card.config(text=f"{humi:.1f}")

        # 检查报警状态
        is_alarm = temp > 35 or humi > 80 or status != 'normal'

        if status == 'temp_high' or temp > 35:
            self.temp_card.config(fg=COLORS['danger'])
            self.state_card.config(text="高温报警！", fg=COLORS['danger'])
            self.alarm_label.config(
                text=f"⚠ 高温报警！当前温度: {temp:.1f}°C (阈值: 35°C)",
                fg=COLORS['danger']
            )
        elif status == 'humidity_high' or humi > 80:
            self.humi_card.config(fg=COLORS['danger'])
            self.state_card.config(text="高湿报警！", fg=COLORS['danger'])
            self.alarm_label.config(
                text=f"⚠ 高湿报警！当前湿度: {humi:.1f}% (阈值: 80%)",
                fg=COLORS['danger']
            )
        elif status == 'both_high':
            self.temp_card.config(fg=COLORS['danger'])
            self.humi_card.config(fg=COLORS['danger'])
            self.state_card.config(text="复合报警！", fg=COLORS['danger'])
            self.alarm_label.config(
                text=f"⚠ 复合报警！温度: {temp:.1f}°C 湿度: {humi:.1f}%",
                fg=COLORS['danger']
            )
        elif status == 'jump':
            self.state_card.config(text="数据跳变", fg=COLORS['warning'])
            self.alarm_label.config(
                text=f"⚡ 检测到数据跳变异常，seq={data.get('seq')}",
                fg=COLORS['warning']
            )
        elif status == 'offline':
            self.state_card.config(text="设备离线", fg=COLORS['danger'])
            self.alarm_label.config(
                text="⚠ 设备离线，数据中断",
                fg=COLORS['danger']
            )
        else:
            self.temp_card.config(fg=COLORS['chart_temp'])
            self.humi_card.config(fg=COLORS['chart_humi'])
            self.state_card.config(text="正常", fg=COLORS['success'])
            self.alarm_label.config(
                text=f"✓ 系统运行正常 | seq: {data.get('seq', '-')}",
                fg=COLORS['success']
            )

    def on_connect(self, rc: int = 0):
        """连接成功回调"""
        if rc == 0:
            self.status_label.config(
                text=f"● 已连接 {config.MQTT_HOST}:{config.MQTT_PORT}",
                fg=COLORS['success']
            )
            self.mqtt.client.subscribe(config.MQTT_TOPIC, qos=1)
        else:
            self.status_label.config(
                text=f"● 连接失败 (rc={rc})",
                fg=COLORS['danger']
            )

    def on_disconnect(self, rc: int):
        """断开连接回调"""
        self.status_label.config(
            text=f"◐ 正在重连... (第 {self.mqtt.reconnect_attempts} 次)",
            fg=COLORS['warning']
        )
        self.state_card.config(text="重连中...", fg=COLORS['warning'])

    def on_close(self):
        """关闭窗口"""
        self.mqtt.disconnect()
        self.destroy()


# ============================================
# 入口
# ============================================

def main():
    print("=" * 60)
    print("MQTT 温湿度监测系统 - Python GUI 订阅端")
    print(f"目标: {config.MQTT_HOST}:{config.MQTT_PORT}")
    print(f"主题: {config.MQTT_TOPIC}")
    print("=" * 60)

    app = SensorDashboard()
    app.mainloop()


if __name__ == "__main__":
    main()
