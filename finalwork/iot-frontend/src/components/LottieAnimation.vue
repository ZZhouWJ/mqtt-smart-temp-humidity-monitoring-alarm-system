<template>
  <div class="lottie-wrapper" :style="wrapperStyle">
    <component v-if="fallbackAnim" :is="fallbackAnim" />
    <div v-else class="static-fallback">
      <div class="static-dot"></div>
    </div>
  </div>
</template>

<script setup>
import { computed, h } from 'vue'

const props = defineProps({
  type: {
    type: String,
    default: 'loading',
  },
  src: { type: String, default: '' },
  size: { type: Number, default: 120 },
  loop: { type: Boolean, default: true },
  autoplay: { type: Boolean, default: true },
  speed: { type: Number, default: 1 },
  color: { type: String, default: '#00d9ff' },
})

const wrapperStyle = computed(() => ({
  width: props.size + 'px',
  height: props.size + 'px',
}))

// 自绘 SVG 动画，避免演示时依赖外部 Lottie CDN。
const fallbackAnim = computed(() => {
  const c = props.color
  const animations = {
    loading: () => h('svg', { viewBox: '0 0 50 50', class: 'spin-anim' }, [
      h('circle', { cx: 25, cy: 25, r: 20, fill: 'none', stroke: c, 'stroke-width': 3, 'stroke-dasharray': '80 30', 'stroke-linecap': 'round', opacity: 0.6 }),
    ]),
    dataflow: () => h('svg', { viewBox: '0 0 100 60' }, [
      h('circle', { cx: 15, cy: 30, r: 6, fill: c, class: 'pulse-anim' }),
      h('circle', { cx: 50, cy: 30, r: 6, fill: c, class: 'pulse-anim', style: 'animation-delay: 0.3s' }),
      h('circle', { cx: 85, cy: 30, r: 6, fill: c, class: 'pulse-anim', style: 'animation-delay: 0.6s' }),
      h('line', { x1: 21, y1: 30, x2: 44, y2: 30, stroke: c, 'stroke-width': 1, 'stroke-dasharray': '2 2', class: 'flow-anim' }),
      h('line', { x1: 56, y1: 30, x2: 79, y2: 30, stroke: c, 'stroke-width': 1, 'stroke-dasharray': '2 2', class: 'flow-anim', style: 'animation-delay: 0.3s' }),
    ]),
    success: () => h('svg', { viewBox: '0 0 50 50' }, [
      h('circle', { cx: 25, cy: 25, r: 20, fill: 'none', stroke: c, 'stroke-width': 3, class: 'draw-circle' }),
      h('path', { d: 'M15 25 L22 32 L35 18', fill: 'none', stroke: c, 'stroke-width': 3, 'stroke-linecap': 'round', 'stroke-linejoin': 'round', class: 'draw-check' }),
    ]),
    alert: () => h('svg', { viewBox: '0 0 50 50' }, [
      h('path', { d: 'M25 8 L45 42 L5 42 Z', fill: 'none', stroke: c, 'stroke-width': 3, 'stroke-linejoin': 'round', class: 'pulse-alert' }),
      h('line', { x1: 25, y1: 18, x2: 25, y2: 30, stroke: c, 'stroke-width': 3, 'stroke-linecap': 'round' }),
      h('circle', { cx: 25, cy: 35, r: 2, fill: c }),
    ]),
    bell: () => h('svg', { viewBox: '0 0 50 50', class: 'shake-anim' }, [
      h('path', { d: 'M25 8 C20 8 16 12 16 18 L16 28 L12 32 L38 32 L34 28 L34 18 C34 12 30 8 25 8 Z', fill: c, opacity: 0.8 }),
      h('path', { d: 'M22 36 C22 39 24 41 25 41 C26 41 28 39 28 36', fill: 'none', stroke: c, 'stroke-width': 2 }),
    ]),
    thermometer: () => h('svg', { viewBox: '0 0 50 50' }, [
      h('rect', { x: 21, y: 8, width: 8, height: 26, rx: 4, fill: 'none', stroke: c, 'stroke-width': 2 }),
      h('circle', { cx: 25, cy: 38, r: 7, fill: c, class: 'pulse-anim' }),
      h('rect', { x: 23, y: 22, width: 4, height: 16, rx: 2, fill: c, class: 'fill-up' }),
    ]),
    droplet: () => h('svg', { viewBox: '0 0 50 50' }, [
      h('path', { d: 'M25 8 C18 20 14 26 14 32 C14 38 18 42 25 42 C32 42 36 38 36 32 C36 26 32 20 25 8 Z', fill: c, opacity: 0.8, class: 'drop-bounce' }),
    ]),
    cpu: () => h('svg', { viewBox: '0 0 50 50' }, [
      h('rect', { x: 12, y: 12, width: 26, height: 26, rx: 2, fill: 'none', stroke: c, 'stroke-width': 2 }),
      h('rect', { x: 20, y: 20, width: 10, height: 10, fill: c, class: 'pulse-anim' }),
      [10, 18, 26, 34, 42].flatMap(y => [12, 20, 28, 36, 44].map(x => h('line', { x1: x, y1: y, x2: x + (x < 25 ? -2 : 2), y2: y, stroke: c, 'stroke-width': 1.5 })))
    ]),
    wifi: () => h('svg', { viewBox: '0 0 50 50' }, [
      h('path', { d: 'M10 22 Q25 8 40 22', fill: 'none', stroke: c, 'stroke-width': 2, 'stroke-linecap': 'round', class: 'wave-1' }),
      h('path', { d: 'M15 28 Q25 18 35 28', fill: 'none', stroke: c, 'stroke-width': 2, 'stroke-linecap': 'round', class: 'wave-2' }),
      h('path', { d: 'M20 34 Q25 30 30 34', fill: 'none', stroke: c, 'stroke-width': 2, 'stroke-linecap': 'round', class: 'wave-3' }),
      h('circle', { cx: 25, cy: 40, r: 2, fill: c, class: 'pulse-anim' }),
    ]),
    network: () => h('svg', { viewBox: '0 0 100 60' }, [
      h('circle', { cx: 20, cy: 30, r: 8, fill: 'none', stroke: c, 'stroke-width': 2, class: 'pulse-anim' }),
      h('circle', { cx: 80, cy: 30, r: 8, fill: 'none', stroke: c, 'stroke-width': 2, class: 'pulse-anim', style: 'animation-delay: 0.5s' }),
      h('circle', { cx: 50, cy: 30, r: 4, fill: c }),
      h('path', { d: 'M28 30 L46 30 M54 30 L72 30', stroke: c, 'stroke-width': 1, 'stroke-dasharray': '3 2', class: 'flow-anim' }),
    ]),
    pulse: () => h('svg', { viewBox: '0 0 100 50' }, [
      h('path', { d: 'M0 25 L20 25 L25 10 L30 40 L35 25 L50 25 L55 15 L60 35 L65 25 L100 25', fill: 'none', stroke: c, 'stroke-width': 2, 'stroke-linejoin': 'round', 'stroke-linecap': 'round', class: 'ecg-anim' }),
    ]),
    default: () => h('div', { class: 'static-dot' }),
  }
  return animations[props.type] || animations.default
})
</script>

<style scoped>
.lottie-wrapper {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.static-fallback {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.static-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--color-primary, #00d9ff);
  box-shadow: 0 0 8px var(--color-primary, #00d9ff);
  animation: pulse-dot 1.5s ease-in-out infinite;
}

@keyframes pulse-dot {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(0.7); }
}

@keyframes spin { to { transform: rotate(360deg); } }
.spin-anim { animation: spin 1.2s linear infinite; }

@keyframes pulse-anim {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(0.8); }
}
.pulse-anim { animation: pulse-anim 1.4s ease-in-out infinite; transform-origin: center; transform-box: fill-box; }

@keyframes flow-anim {
  to { stroke-dashoffset: -20; }
}
.flow-anim { animation: flow-anim 1.5s linear infinite; }

@keyframes pulse-alert {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.05); opacity: 0.85; }
}
.pulse-alert { animation: pulse-alert 1s ease-in-out infinite; transform-origin: center; transform-box: fill-box; }

@keyframes shake {
  0%, 100% { transform: rotate(0); }
  25% { transform: rotate(-15deg); }
  75% { transform: rotate(15deg); }
}
.shake-anim { animation: shake 0.5s ease-in-out infinite; transform-origin: 50% 10%; transform-box: fill-box; }

@keyframes drop-bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(4px); }
}
.drop-bounce { animation: drop-bounce 2s ease-in-out infinite; transform-origin: center; transform-box: fill-box; }

@keyframes fill-up {
  0%, 100% { transform: scaleY(0.4); }
  50% { transform: scaleY(1); }
}
.fill-up { animation: fill-up 3s ease-in-out infinite; transform-origin: 25px 38px; }

@keyframes wave {
  0%, 100% { opacity: 0.3; }
  50% { opacity: 1; }
}
.wave-1 { animation: wave 1.5s ease-in-out infinite; }
.wave-2 { animation: wave 1.5s ease-in-out infinite; animation-delay: 0.2s; }
.wave-3 { animation: wave 1.5s ease-in-out infinite; animation-delay: 0.4s; }

@keyframes draw-circle {
  from { stroke-dasharray: 0 130; }
  to { stroke-dasharray: 130 0; }
}
.draw-circle { stroke-dasharray: 130; stroke-dashoffset: 0; }

@keyframes draw-check {
  from { stroke-dasharray: 0 30; }
  to { stroke-dasharray: 30 0; }
}
.draw-check { stroke-dasharray: 30; }

@keyframes ecg-anim {
  0% { stroke-dasharray: 0 300; }
  100% { stroke-dasharray: 300 0; }
}
.ecg-anim { stroke-dasharray: 300; animation: ecg-anim 2s linear infinite; }
</style>
