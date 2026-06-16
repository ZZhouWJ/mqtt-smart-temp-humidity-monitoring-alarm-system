<template>
  <div class="app-layout">
    <!-- 加载屏幕 -->
    <LoadingScreen :show="loading" />

    <!-- 背景动画场景 -->
    <LottieScene :show-floaters="true" />

    <!-- 扫描线效果 -->
    <div class="scanline"></div>

    <!-- 侧边栏 -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <div class="brand">
          <div class="brand-logo">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <circle cx="12" cy="12" r="3" />
              <circle cx="12" cy="12" r="7" opacity="0.5" />
              <circle cx="12" cy="12" r="10" opacity="0.2" />
              <line x1="12" y1="2" x2="12" y2="4" />
              <line x1="12" y1="20" x2="12" y2="22" />
              <line x1="2" y1="12" x2="4" y2="12" />
              <line x1="20" y1="12" x2="22" y2="12" />
            </svg>
          </div>
          <div class="brand-text">
            <div class="brand-title">SENTINEL<span class="brand-accent">.IoT</span></div>
            <div class="brand-subtitle">v2.0 · 监测终端</div>
          </div>
        </div>
      </div>

      <!-- 系统状态卡片 -->
      <div class="system-status">
        <div class="status-header">
          <span class="status-label">SYSTEM</span>
          <span class="status-dot" :class="wsConnected ? 'ok' : 'bad'"></span>
        </div>
        <div class="status-content">
          <div class="status-row">
            <span class="status-key">UPLINK</span>
            <span class="status-value" :class="wsConnected ? 'ok' : 'bad'">
              {{ wsConnected ? 'ONLINE' : 'OFFLINE' }}
            </span>
          </div>
          <div class="status-row">
            <span class="status-key">PACKETS</span>
            <span class="status-value mono">{{ totalReceived.toString().padStart(4, '0') }}</span>
          </div>
          <div class="status-row">
            <span class="status-key">ALARMS</span>
            <span class="status-value danger mono">{{ alarmCount.toString().padStart(3, '0') }}</span>
          </div>
        </div>
      </div>

      <nav class="sidebar-nav">
        <div class="nav-section">
          <div class="nav-section-title">— NAVIGATION</div>
          <router-link
            v-for="route in mainRoutes"
            :key="route.path"
            :to="route.path"
            class="nav-item"
            :class="{ active: isActive(route.path) }"
          >
            <span class="nav-bracket">[</span>
            <span class="nav-icon">
              <component :is="getIcon(route.meta.icon)" />
            </span>
            <span class="nav-text">{{ route.meta.title }}</span>
            <span v-if="route.name === 'alarms' && alarmCount > 0" class="nav-badge">
              {{ alarmCount }}
            </span>
            <span class="nav-bracket">]</span>
          </router-link>
        </div>
      </nav>

      <div class="sidebar-footer">
        <div class="time-display">
          <div class="time-label">UTC+8</div>
          <div class="time-value mono">{{ currentTime }}</div>
        </div>
      </div>
    </aside>

    <!-- 主内容区 -->
    <main class="main-content">
      <router-view v-slot="{ Component }">
        <transition name="page" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, h } from 'vue'
import { useRoute } from 'vue-router'
import { useSensorData } from './composables/useSensorData'
import LottieScene from './components/LottieScene.vue'
import LoadingScreen from './components/LoadingScreen.vue'

const route = useRoute()
const { alarmCount, wsConnected, totalReceived } = useSensorData()

const currentTime = ref('')
const loading = ref(true)
let timer = null

function updateTime() {
  const now = new Date()
  currentTime.value = now.toTimeString().slice(0, 8)
}

onMounted(() => {
  updateTime()
  timer = setInterval(updateTime, 1000)
  setTimeout(() => { loading.value = false }, 2200)
})

onBeforeUnmount(() => {
  if (timer) clearInterval(timer)
})

const mainRoutes = [
  { path: '/monitoring', meta: { title: '实时监测', icon: 'monitoring' }, name: 'monitoring' },
  { path: '/alarms', meta: { title: '报警历史', icon: 'alarms' }, name: 'alarms' },
  { path: '/history', meta: { title: '历史数据', icon: 'history' }, name: 'history' },
  { path: '/about', meta: { title: '系统设计', icon: 'about' }, name: 'about' },
]

function isActive(path) {
  return route.path === path
}

const icons = {
  monitoring: () => h('svg', { viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '1.5' }, [
    h('path', { d: 'M3 3v18h18' }),
    h('path', { d: 'M7 14l4-4 4 4 5-5' }),
    h('circle', { cx: 7, cy: 14, r: 1, fill: 'currentColor' }),
    h('circle', { cx: 11, cy: 10, r: 1, fill: 'currentColor' }),
    h('circle', { cx: 15, cy: 14, r: 1, fill: 'currentColor' }),
    h('circle', { cx: 20, cy: 9, r: 1, fill: 'currentColor' }),
  ]),
  alarms: () => h('svg', { viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '1.5' }, [
    h('path', { d: 'M12 2L2 22h20L12 2z' }),
    h('line', { x1: 12, y1: 9, x2: 12, y2: 14 }),
    h('circle', { cx: 12, cy: 17, r: 0.5, fill: 'currentColor' }),
  ]),
  history: () => h('svg', { viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '1.5' }, [
    h('circle', { cx: 12, cy: 12, r: 9 }),
    h('polyline', { points: '12 7 12 12 15 14' }),
    h('line', { x1: 12, y1: 3, x2: 12, y2: 5 }),
    h('line', { x1: 12, y1: 19, x2: 12, y2: 21 }),
  ]),
  about: () => h('svg', { viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '1.5' }, [
    h('rect', { x: 3, y: 3, width: 18, height: 18, rx: 1 }),
    h('line', { x1: 9, y1: 3, x2: 9, y2: 21 }),
    h('line', { x1: 15, y1: 3, x2: 15, y2: 21 }),
    h('line', { x1: 3, y1: 9, x2: 21, y2: 9 }),
    h('line', { x1: 3, y1: 15, x2: 21, y2: 15 }),
  ]),
}

function getIcon(name) {
  return icons[name] || icons.monitoring
}
</script>

<style scoped>
.app-layout {
  display: flex;
  min-height: 100vh;
  background: var(--color-bg);
  position: relative;
  z-index: 1;
}

/* 扫描线动画 */
.scanline {
  position: fixed;
  top: 0;
  left: 240px;
  right: 0;
  height: 100vh;
  pointer-events: none;
  z-index: 100;
  overflow: hidden;
}

.scanline::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, transparent, var(--color-primary), transparent);
  opacity: 0.15;
  animation: scan 8s linear infinite;
}

@keyframes scan {
  0% { transform: translateY(0); }
  100% { transform: translateY(100vh); }
}

/* ============================================
   Sidebar
   ============================================ */

.sidebar {
  width: 240px;
  background: var(--color-bg-elevated);
  border-right: 1px solid var(--color-border);
  display: flex;
  flex-direction: column;
  position: sticky;
  top: 0;
  height: 100vh;
  z-index: 10;
  flex-shrink: 0;
}

.sidebar::before {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  width: 1px;
  background: linear-gradient(180deg, transparent, var(--color-primary), transparent);
  opacity: 0.4;
}

.sidebar-header {
  padding: var(--space-5);
  border-bottom: 1px solid var(--color-border);
}

.brand {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.brand-logo {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid var(--color-primary);
  border-radius: var(--radius-sm);
  color: var(--color-primary);
  background: var(--color-primary-soft);
  box-shadow: var(--shadow-glow);
}

.brand-logo svg {
  width: 22px;
  height: 22px;
  animation: rotate-slow 20s linear infinite;
}

@keyframes rotate-slow {
  from { transform: rotate(0); }
  to { transform: rotate(360deg); }
}

.brand-text { flex: 1; min-width: 0; }

.brand-title {
  font-family: var(--font-display);
  font-size: 15px;
  font-weight: 700;
  color: var(--color-text-primary);
  letter-spacing: 0.02em;
  line-height: 1;
}

.brand-accent {
  color: var(--color-primary);
}

.brand-subtitle {
  font-family: var(--font-mono);
  font-size: 10px;
  color: var(--color-text-tertiary);
  margin-top: 4px;
  letter-spacing: 0.05em;
}

/* ============================================
   System Status
   ============================================ */

.system-status {
  margin: var(--space-4);
  padding: var(--space-3);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  position: relative;
}

.system-status::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 3px;
  height: 100%;
  background: var(--color-primary);
  border-radius: var(--radius-sm) 0 0 var(--radius-sm);
}

.status-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-2);
  padding-bottom: var(--space-2);
  border-bottom: 1px dashed var(--color-border);
}

.status-label {
  font-family: var(--font-mono);
  font-size: 9px;
  font-weight: 600;
  color: var(--color-text-tertiary);
  letter-spacing: 0.15em;
}

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
}

.status-dot.ok {
  background: var(--color-success);
  box-shadow: 0 0 8px var(--color-success);
  animation: pulse-glow 2s ease-in-out infinite;
}

.status-dot.bad {
  background: var(--color-danger);
  box-shadow: 0 0 8px var(--color-danger);
}

@keyframes pulse-glow {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(0.85); }
}

.status-content {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.status-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.status-key {
  font-family: var(--font-mono);
  font-size: 10px;
  color: var(--color-text-tertiary);
  letter-spacing: 0.05em;
}

.status-value {
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.status-value.ok { color: var(--color-success); }
.status-value.bad { color: var(--color-danger); }
.status-value.danger { color: var(--color-accent); }

/* ============================================
   Navigation
   ============================================ */

.sidebar-nav {
  flex: 1;
  padding: var(--space-4) 0;
  overflow-y: auto;
}

.nav-section { margin-bottom: var(--space-4); }

.nav-section-title {
  padding: 0 var(--space-5) var(--space-2);
  font-family: var(--font-mono);
  font-size: 9px;
  font-weight: 600;
  color: var(--color-text-tertiary);
  letter-spacing: 0.15em;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-3) var(--space-4);
  font-family: var(--font-mono);
  font-size: 12px;
  font-weight: 500;
  color: var(--color-text-secondary);
  text-decoration: none;
  transition: all var(--duration-base) var(--ease-out);
  position: relative;
  border-left: 2px solid transparent;
}

.nav-bracket {
  color: var(--color-text-tertiary);
  font-weight: 300;
  transition: color var(--duration-base);
}

.nav-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 18px;
  height: 18px;
  flex-shrink: 0;
}

.nav-icon svg {
  width: 16px;
  height: 16px;
}

.nav-text { flex: 1; }

.nav-item:hover {
  color: var(--color-primary);
  background: var(--color-primary-soft);
  border-left-color: var(--color-primary);
}

.nav-item:hover .nav-bracket { color: var(--color-primary); }

.nav-item.active {
  color: var(--color-primary);
  background: var(--color-primary-soft);
  border-left-color: var(--color-primary);
  text-shadow: 0 0 8px var(--color-primary-glow);
}

.nav-item.active .nav-bracket { color: var(--color-primary); }

.nav-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 20px;
  height: 18px;
  padding: 0 6px;
  font-family: var(--font-mono);
  font-size: 10px;
  font-weight: 700;
  color: var(--color-text-inverse);
  background: var(--color-danger);
  border-radius: var(--radius-sm);
  box-shadow: 0 0 8px rgba(255, 56, 96, 0.5);
  animation: pulse-badge 1.5s ease-in-out infinite;
}

@keyframes pulse-badge {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

/* ============================================
   Footer
   ============================================ */

.sidebar-footer {
  padding: var(--space-4);
  border-top: 1px solid var(--color-border);
}

.time-display {
  text-align: center;
  padding: var(--space-2);
  background: var(--color-bg);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
}

.time-label {
  font-family: var(--font-mono);
  font-size: 9px;
  color: var(--color-text-tertiary);
  letter-spacing: 0.1em;
}

.time-value {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-primary);
  margin-top: 2px;
  letter-spacing: 0.05em;
  text-shadow: 0 0 10px var(--color-primary-glow);
}

/* ============================================
   Main Content
   ============================================ */

.main-content {
  flex: 1;
  min-width: 0;
  overflow-x: hidden;
  position: relative;
}

/* Page transitions */
.page-enter-active {
  transition: opacity var(--duration-slow) var(--ease-out), transform var(--duration-slow) var(--ease-out);
}

.page-leave-active {
  transition: opacity var(--duration-fast) var(--ease-in-out);
}

.page-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.page-leave-to {
  opacity: 0;
}

@media (max-width: 768px) {
  .app-layout { flex-direction: column; }
  .sidebar { width: 100%; height: auto; position: relative; }
  .sidebar-nav { display: flex; overflow-x: auto; padding: var(--space-2); }
  .nav-section { margin: 0; }
  .nav-section-title { display: none; }
  .nav-item { white-space: nowrap; }
  .nav-bracket { display: none; }
  .system-status, .time-display { display: none; }
  .scanline { display: none; }
}
</style>
