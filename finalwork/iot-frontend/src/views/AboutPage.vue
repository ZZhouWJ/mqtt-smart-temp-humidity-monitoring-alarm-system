<template>
  <div class="about-page">
    <div class="page-decoration">
      <LottieAnimation
        type="rocket"
        :size="120"
        :speed="0.5"
        color="rgba(0, 217, 255, 0.5)"
      />
    </div>

    <header class="page-header">
      <div class="title-label mono">SYSTEM_DESIGN / 系统设计</div>
      <h1 class="title-main">ARCHITECTURE BLUEPRINT</h1>
      <p class="subtitle">MQTT 环境监测系统架构与考核点说明</p>
    </header>

    <section class="arch-section">
      <div class="section-header">
        <span class="section-num mono">01</span>
        <h2 class="section-title">SYSTEM FLOW</h2>
        <span class="section-sub">四层架构数据流</span>
      </div>

      <div class="arch-diagram">
        <div class="arch-step">
          <div class="step-icon" style="--c: var(--color-primary)">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <rect x="2" y="3" width="20" height="14" rx="2" />
              <line x1="8" y1="21" x2="16" y2="21" />
              <line x1="12" y1="17" x2="12" y2="21" />
            </svg>
          </div>
          <div class="step-num mono">01</div>
          <div class="step-title">采集层</div>
          <div class="step-desc">Python 脚本生成带噪声、跳变、丢包的温湿度数据</div>
          <div class="step-tech">Python 3.10 · Paho-MQTT</div>
        </div>

        <div class="arch-flow">
          <div class="flow-line"></div>
          <div class="flow-arrow">→</div>
        </div>

        <div class="arch-step">
          <div class="step-icon" style="--c: var(--color-info)">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M22 12h-4l-3 9L9 3l-3 9H2" />
            </svg>
          </div>
          <div class="step-num mono">02</div>
          <div class="step-title">通信层</div>
          <div class="step-desc">EMQX 公共 Broker 处理消息路由与发布订阅</div>
          <div class="step-tech">MQTT 3.1.1 · QoS 1</div>
        </div>

        <div class="arch-flow">
          <div class="flow-line"></div>
          <div class="flow-arrow">→</div>
        </div>

        <div class="arch-step">
          <div class="step-icon" style="--c: var(--color-success)">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <ellipse cx="12" cy="5" rx="9" ry="3" />
              <path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3" />
              <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5" />
            </svg>
          </div>
          <div class="step-num mono">03</div>
          <div class="step-title">处理层</div>
          <div class="step-desc">Spring Boot 完成丢包检测、滑动平均滤波、报警判断</div>
          <div class="step-tech">Java 17 · Spring Boot 3</div>
        </div>

        <div class="arch-flow">
          <div class="flow-line"></div>
          <div class="flow-arrow">→</div>
        </div>

        <div class="arch-step">
          <div class="step-icon" style="--c: var(--color-accent)">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <rect x="3" y="3" width="18" height="18" rx="2" />
              <line x1="3" y1="9" x2="21" y2="9" />
              <line x1="9" y1="21" x2="9" y2="9" />
            </svg>
          </div>
          <div class="step-num mono">04</div>
          <div class="step-title">展示层</div>
          <div class="step-desc">Vue 3 + ECharts 实时展示曲线、报警记录与诊断建议</div>
          <div class="step-tech">Vue 3 · ECharts · Vite</div>
        </div>
      </div>
    </section>

    <section class="assessment-section">
      <div class="section-header">
        <span class="section-num mono">02</span>
        <h2 class="section-title">ASSESSMENT MATRIX</h2>
        <span class="section-sub">考核重点对应</span>
      </div>

      <div class="assessment-grid">
        <div class="assessment-card">
          <div class="card-header">
            <span class="card-num mono">#01</span>
            <h3>MQTT vs TCP</h3>
          </div>
          <div class="comparison-table">
            <div class="table-head mono">
              <span>ITEM</span>
              <span style="color: var(--color-primary)">MQTT</span>
              <span>TCP</span>
            </div>
            <div class="table-row" v-for="row in mqttComparison" :key="row.key">
              <span class="row-key">{{ row.key }}</span>
              <span class="row-mqtt">{{ row.mqtt }}</span>
              <span class="row-tcp">{{ row.tcp }}</span>
            </div>
          </div>
          <div class="card-reason">
            <span class="reason-label mono">REASON</span>
            <p>MQTT 专为物联网场景设计，发布/订阅模型解耦设备和后端，Topic 机制自动路由，QoS 保障消息可靠传输。</p>
          </div>
        </div>

        <div class="assessment-card">
          <div class="card-header">
            <span class="card-num mono">#02</span>
            <h3>JSON 数据格式</h3>
          </div>
          <pre class="code-block"><code>{
  <span class="key">"deviceId"</span>: <span class="str">"env-node-001"</span>,
  <span class="key">"seq"</span>: <span class="num">1001</span>,
  <span class="key">"timestamp"</span>: <span class="str">"2026-06-16 20:35:01"</span>,
  <span class="key">"temperature"</span>: <span class="num">25.4</span>,
  <span class="key">"humidity"</span>: <span class="num">60.1</span>,
  <span class="key">"status"</span>: <span class="str">"normal"</span>
}</code></pre>
          <div class="card-reason">
            <span class="reason-label mono">REASON</span>
            <p>JSON 可读性强便于调试；Python、Java、JS 跨语言原生支持；字段自描述；<code class="inline-code">seq</code> 字段用于丢包检测。</p>
          </div>
        </div>

        <div class="assessment-card">
          <div class="card-header">
            <span class="card-num mono">#03</span>
            <h3>断线自动重连</h3>
          </div>
          <pre class="code-block"><code><span class="kw">def</span> <span class="fn">on_disconnect</span>(self, client, rc):
    delay = <span class="num">1</span>
    <span class="kw">while</span> <span class="bool">True</span>:
        time.sleep(delay)
        <span class="kw">try</span>:
            client.reconnect()
            <span class="kw">break</span>
        <span class="kw">except</span>:
            delay = <span class="fn">min</span>(delay * <span class="num">2</span>, <span class="num">60</span>)</code></pre>
          <div class="card-reason">
            <span class="reason-label mono">REASON</span>
            <p>采用指数退避算法，初始延迟 1s 翻倍递增，最大 60s；后端使用 Eclipse Paho 内置自动重连。</p>
          </div>
        </div>

        <div class="assessment-card">
          <div class="card-header">
            <span class="card-num mono">#04</span>
            <h3>异常数据处理</h3>
          </div>
          <ul class="strategy-list">
            <li>
              <span class="strategy-tag warning">JUMP</span>
              <span class="strategy-text">差值阈值检测（±10℃），标记 outlier，不进入滤波窗口</span>
            </li>
            <li>
              <span class="strategy-tag danger">LOST</span>
              <span class="strategy-text">seq 序号连续性检测，丢失数据点用特殊标记</span>
            </li>
            <li>
              <span class="strategy-tag info">NOISE</span>
              <span class="strategy-text">滑动平均滤波（窗口 5），平滑随机波动</span>
            </li>
            <li>
              <span class="strategy-tag accent">OFFLINE</span>
              <span class="strategy-text">状态字段标记 offline，前端灰色提示</span>
            </li>
          </ul>
        </div>
      </div>
    </section>

    <section class="stats-section">
      <div class="section-header">
        <span class="section-num mono">03</span>
        <h2 class="section-title">RUNTIME STATS</h2>
        <span class="section-sub">运行统计</span>
      </div>
      <div class="stats-grid">
        <div class="stat-block">
          <div class="stat-corner tl"></div><div class="stat-corner tr"></div>
          <div class="stat-corner bl"></div><div class="stat-corner br"></div>
          <div class="stat-key mono">PACKETS_RX</div>
          <div class="stat-val mono">{{ totalReceived.toString().padStart(5, '0') }}</div>
        </div>
        <div class="stat-block">
          <div class="stat-corner tl"></div><div class="stat-corner tr"></div>
          <div class="stat-corner bl"></div><div class="stat-corner br"></div>
          <div class="stat-key mono">ALARMS</div>
          <div class="stat-val danger mono">{{ alarmCount.toString().padStart(3, '0') }}</div>
        </div>
        <div class="stat-block">
          <div class="stat-corner tl"></div><div class="stat-corner tr"></div>
          <div class="stat-corner bl"></div><div class="stat-corner br"></div>
          <div class="stat-key mono">UPLINK</div>
          <div class="stat-val" :class="wsConnected ? 'success' : 'danger'">
            {{ wsConnected ? 'ONLINE' : 'OFFLINE' }}
          </div>
        </div>
        <div class="stat-block">
          <div class="stat-corner tl"></div><div class="stat-corner tr"></div>
          <div class="stat-corner bl"></div><div class="stat-corner br"></div>
          <div class="stat-key mono">FREQ</div>
          <div class="stat-val mono">1.0 Hz</div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import LottieAnimation from '../components/LottieAnimation.vue'
import { useSensorData } from '../composables/useSensorData'
const { totalReceived, alarmCount, wsConnected } = useSensorData()

const mqttComparison = [
  { key: '通信模式', mqtt: '发布/订阅', tcp: '点对点' },
  { key: '心跳机制', mqtt: '内置 KeepAlive', tcp: '需自行实现' },
  { key: '消息路由', mqtt: 'Topic 主题', tcp: '需自行实现' },
  { key: '带宽开销', mqtt: '2 字节头部', tcp: '较大' },
  { key: '断线重连', mqtt: '自动重连', tcp: '需自行实现' },
]
</script>

<style scoped>
.about-page {
  padding: var(--space-6);
  max-width: 1400px;
  margin: 0 auto;
  position: relative;
}

.page-decoration {
  position: absolute;
  top: var(--space-4);
  right: var(--space-4);
  opacity: 0.6;
  pointer-events: none;
  z-index: 0;
}

.about-page > *:not(.page-decoration) {
  position: relative;
  z-index: 1;
}

.page-header {
  margin-bottom: var(--space-8);
  padding-bottom: var(--space-5);
  border-bottom: 1px solid var(--color-border);
  position: relative;
}

.page-header::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 0;
  width: 80px;
  height: 2px;
  background: var(--color-primary);
  box-shadow: 0 0 8px var(--color-primary);
}

.title-label {
  font-size: 10px;
  font-weight: 600;
  color: var(--color-primary);
  letter-spacing: 0.2em;
  margin-bottom: var(--space-1);
}

.title-main {
  font-family: var(--font-display);
  font-size: 28px;
  font-weight: 700;
  color: var(--color-text-primary);
  letter-spacing: -0.02em;
  margin: 0 0 var(--space-1) 0;
}

.subtitle {
  font-size: 13px;
  color: var(--color-text-tertiary);
}

/* ============================================
   Section Header
   ============================================ */

.section-header {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  margin-bottom: var(--space-5);
  padding-bottom: var(--space-3);
  border-bottom: 1px dashed var(--color-border);
}

.section-num {
  font-size: 10px;
  font-weight: 700;
  color: var(--color-primary);
  letter-spacing: 0.1em;
  padding: 2px 8px;
  background: var(--color-primary-soft);
  border: 1px solid var(--color-primary);
  border-radius: var(--radius-sm);
}

.section-title {
  font-family: var(--font-display);
  font-size: 18px;
  font-weight: 700;
  color: var(--color-text-primary);
  letter-spacing: 0.02em;
  margin: 0;
}

.section-sub {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--color-text-tertiary);
}

/* ============================================
   Architecture
   ============================================ */

.arch-section { margin-bottom: var(--space-8); }

.arch-diagram {
  display: flex;
  align-items: stretch;
  gap: 0;
  padding: var(--space-5);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  overflow-x: auto;
  position: relative;
}

.arch-diagram::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--color-primary), transparent);
  opacity: 0.5;
}

.arch-step {
  flex: 1;
  min-width: 180px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: var(--space-4);
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  transition: all var(--duration-base);
}

.arch-step:hover {
  border-color: var(--c);
  transform: translateY(-4px);
  box-shadow: 0 0 20px color-mix(in srgb, var(--c) 30%, transparent);
}

.step-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  background: color-mix(in srgb, var(--c) 15%, transparent);
  border: 1px solid var(--c);
  border-radius: var(--radius-md);
  color: var(--c);
  margin-bottom: var(--space-3);
  box-shadow: 0 0 12px color-mix(in srgb, var(--c) 40%, transparent);
}

.step-icon svg { width: 24px; height: 24px; }

.step-num {
  font-size: 10px;
  font-weight: 700;
  color: var(--color-text-tertiary);
  letter-spacing: 0.1em;
  margin-bottom: var(--space-1);
}

.step-title {
  font-family: var(--font-display);
  font-size: 14px;
  font-weight: 700;
  color: var(--color-text-primary);
  margin-bottom: var(--space-1);
}

.step-desc {
  font-size: 11px;
  color: var(--color-text-secondary);
  line-height: 1.5;
  margin-bottom: var(--space-2);
}

.step-tech {
  font-family: var(--font-mono);
  font-size: 9px;
  color: var(--color-text-tertiary);
  letter-spacing: 0.05em;
  padding: 2px 6px;
  background: var(--color-bg);
  border-radius: var(--radius-sm);
}

.arch-flow {
  display: flex;
  align-items: center;
  padding: 0 var(--space-2);
  position: relative;
}

.flow-line {
  position: absolute;
  left: 0;
  right: 0;
  top: 50%;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--color-primary), transparent);
  opacity: 0.4;
}

.flow-arrow {
  position: relative;
  font-size: 20px;
  color: var(--color-primary);
  text-shadow: 0 0 8px var(--color-primary-glow);
  z-index: 1;
  background: var(--color-surface);
  padding: 0 var(--space-1);
}

/* ============================================
   Assessment
   ============================================ */

.assessment-section { margin-bottom: var(--space-8); }

.assessment-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--space-4);
}

.assessment-card {
  position: relative;
  padding: var(--space-5);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  transition: all var(--duration-base);
}

.assessment-card:hover {
  border-color: var(--color-primary);
  box-shadow: 0 0 20px rgba(0, 217, 255, 0.1);
}

.card-header {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  margin-bottom: var(--space-4);
  padding-bottom: var(--space-3);
  border-bottom: 1px dashed var(--color-border);
}

.card-num {
  font-size: 10px;
  font-weight: 700;
  color: var(--color-primary);
  letter-spacing: 0.1em;
  padding: 2px 8px;
  background: var(--color-primary-soft);
  border: 1px solid var(--color-primary);
  border-radius: var(--radius-sm);
}

.card-header h3 {
  font-family: var(--font-display);
  font-size: 15px;
  font-weight: 700;
  color: var(--color-text-primary);
  margin: 0;
  letter-spacing: 0.02em;
}

.comparison-table {
  font-size: 11px;
  margin-bottom: var(--space-3);
}

.table-head, .table-row {
  display: grid;
  grid-template-columns: 80px 1fr 1fr;
  gap: var(--space-2);
  padding: var(--space-2);
  align-items: center;
}

.table-head {
  font-size: 9px;
  color: var(--color-text-tertiary);
  letter-spacing: 0.1em;
  border-bottom: 1px solid var(--color-border);
}

.table-row {
  border-bottom: 1px solid var(--color-border-subtle);
  transition: background var(--duration-base);
}

.table-row:hover { background: var(--color-bg-elevated); }
.table-row:last-child { border-bottom: none; }

.row-key { color: var(--color-text-tertiary); }
.row-mqtt { color: var(--color-primary); font-weight: 600; }
.row-tcp { color: var(--color-text-tertiary); }

.code-block {
  background: #0a0e1a;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  padding: var(--space-3);
  font-family: var(--font-mono);
  font-size: 11px;
  line-height: 1.6;
  margin-bottom: var(--space-3);
  overflow-x: auto;
  color: var(--color-text-secondary);
}

.code-block .key { color: #4cc9f0; }
.code-block .str { color: #00ff9d; }
.code-block .num { color: #ff9e00; }
.code-block .kw { color: #ff3860; font-weight: 600; }
.code-block .fn { color: #4cc9f0; }
.code-block .bool { color: #ff9e00; }

.card-reason {
  padding: var(--space-3);
  background: var(--color-bg-elevated);
  border-left: 2px solid var(--color-primary);
  border-radius: var(--radius-sm);
}

.reason-label {
  display: block;
  font-size: 9px;
  color: var(--color-primary);
  letter-spacing: 0.15em;
  margin-bottom: var(--space-1);
}

.card-reason p {
  font-size: 12px;
  color: var(--color-text-secondary);
  line-height: 1.5;
  margin: 0;
}

.inline-code {
  font-family: var(--font-mono);
  font-size: 11px;
  padding: 1px 4px;
  background: var(--color-bg);
  color: var(--color-primary);
  border-radius: 3px;
}

.strategy-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.strategy-list li {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3);
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  transition: all var(--duration-base);
}

.strategy-list li:hover {
  border-color: var(--color-border-strong);
  transform: translateX(2px);
}

.strategy-tag {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 4px 10px;
  font-family: var(--font-mono);
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.05em;
  border-radius: var(--radius-sm);
  flex-shrink: 0;
  min-width: 80px;
}

.strategy-tag.warning { background: var(--color-warning-soft); color: var(--color-warning); border: 1px solid var(--color-warning); }
.strategy-tag.danger { background: var(--color-danger-soft); color: var(--color-danger); border: 1px solid var(--color-danger); }
.strategy-tag.info { background: var(--color-info-soft); color: var(--color-info); border: 1px solid var(--color-info); }
.strategy-tag.accent { background: var(--color-accent-soft); color: var(--color-accent); border: 1px solid var(--color-accent); }

.strategy-text {
  font-size: 12px;
  color: var(--color-text-secondary);
  line-height: 1.4;
}

/* ============================================
   Stats
   ============================================ */

.stats-section { margin-bottom: var(--space-6); }

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--space-4);
}

.stat-block {
  position: relative;
  padding: var(--space-5);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
}

.stat-corner {
  position: absolute;
  width: 8px;
  height: 8px;
  border-color: var(--color-primary);
  opacity: 0.4;
}

.stat-corner.tl { top: 4px; left: 4px; border-top: 1px solid; border-left: 1px solid; }
.stat-corner.tr { top: 4px; right: 4px; border-top: 1px solid; border-right: 1px solid; }
.stat-corner.bl { bottom: 4px; left: 4px; border-bottom: 1px solid; border-left: 1px solid; }
.stat-corner.br { bottom: 4px; right: 4px; border-bottom: 1px solid; border-right: 1px solid; }

.stat-key {
  font-size: 9px;
  color: var(--color-text-tertiary);
  letter-spacing: 0.15em;
  margin-bottom: var(--space-2);
}

.stat-val {
  font-size: 32px;
  font-weight: 700;
  color: var(--color-primary);
  text-shadow: 0 0 12px var(--color-primary-glow);
  line-height: 1;
}

.stat-val.danger {
  color: var(--color-danger);
  text-shadow: 0 0 12px rgba(255, 56, 96, 0.4);
}

.stat-val.success {
  color: var(--color-success);
  text-shadow: 0 0 12px var(--color-success-soft);
}

@media (max-width: 1024px) {
  .assessment-grid { grid-template-columns: 1fr; }
  .stats-grid { grid-template-columns: repeat(2, 1fr); }
  .arch-diagram { flex-wrap: wrap; }
  .arch-flow { width: 100%; transform: rotate(90deg); }
}
</style>
