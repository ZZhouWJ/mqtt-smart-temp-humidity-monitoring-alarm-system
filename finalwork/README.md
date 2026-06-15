# 基于 MQTT 与 Spring Boot 的智能温湿度环境监测与异常报警系统

本项目为物联网技术开发课程设计题目一的工程化实现。系统使用 Python 模拟温湿度采集节点，通过 MQTT 发布 JSON 数据，Spring Boot 后端订阅并完成滤波、丢包检测、报警判断和本地规则诊断，Vue + ECharts 前端实时展示曲线、设备状态和报警记录。

## 项目结构

```text
sensor-simulator/  Python 模拟温湿度传感器与 MQTT 发布端
iot-backend/       Spring Boot 后端：MQTT 订阅、滤波、报警、WebSocket 推送
iot-frontend/      Vue + ECharts 前端大屏
docs/              系统设计、接口协议、运行说明、测试说明、答辩防守说明
PPT/               白色背景项目汇报 PPT
docker-compose.yml Docker 一键部署文件
```

## 推荐运行方式一：Docker 一键启动

```bash
docker compose up -d --build
```

启动后访问：

- 前端页面：http://localhost:5173
- 后端健康检查：http://localhost:8080/api/health
- EMQX 管理后台：http://localhost:18083，账号 admin，密码 public

## 运行方式二：本地分别启动

后端：

```bash
cd iot-backend
mvn spring-boot:run
```

前端：

```bash
cd iot-frontend
npm install
npm run dev
```

模拟器：

```bash
cd sensor-simulator
pip install -r requirements.txt
python mqtt_publisher.py --mode demo
```

## 核心考核点对应

1. MQTT 与 TCP 对比：见 `docs/系统设计说明.md` 和 PPT。
2. JSON 数据格式设计：见 `docs/接口协议说明.md`。
3. 断线自动重连：Python 发布端指数退避重连；Spring Boot 后端 Paho 自动重连并重订阅。
4. 异常数据处理：模拟跳变、丢包、离线；后端通过滑动平均、阈值判断和 seq 序号处理。
