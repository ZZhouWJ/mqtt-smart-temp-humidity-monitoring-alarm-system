<template>
  <div class="lottie-scene">
    <!-- 主背景动画 -->
    <div class="scene-layer bg-layer">
      <LottieAnimation
        type="dataflow"
        :src="dataFlowSrc"
        :size="300"
        :speed="0.6"
        color="rgba(0, 217, 255, 0.5)"
      />
    </div>

    <!-- 浮动小图标 -->
    <div class="floating-icons" v-if="showFloaters">
      <div class="floater" style="top: 10%; left: 5%; animation-delay: 0s">
        <LottieAnimation type="wifi" :size="48" :speed="0.8" color="rgba(0, 217, 255, 0.7)" />
      </div>
      <div class="floater" style="top: 20%; right: 8%; animation-delay: 0.5s">
        <LottieAnimation type="server" :size="56" :speed="0.5" color="rgba(0, 255, 157, 0.6)" />
      </div>
      <div class="floater" style="bottom: 30%; left: 3%; animation-delay: 1s">
        <LottieAnimation type="database" :size="50" :speed="0.7" color="rgba(76, 201, 240, 0.6)" />
      </div>
      <div class="floater" style="bottom: 15%; right: 12%; animation-delay: 1.5s">
        <LottieAnimation type="cloud" :size="60" :speed="0.4" color="rgba(255, 158, 0, 0.5)" />
      </div>
      <div class="floater" style="top: 50%; left: 2%; animation-delay: 2s">
        <LottieAnimation type="pulse" :size="80" :speed="1.2" color="rgba(255, 56, 96, 0.4)" />
      </div>
      <div class="floater" style="top: 60%; right: 4%; animation-delay: 2.5s">
        <LottieAnimation type="network" :size="70" :speed="0.6" color="rgba(0, 217, 255, 0.5)" />
      </div>
    </div>

    <!-- 光晕 -->
    <div class="glow-orb glow-1"></div>
    <div class="glow-orb glow-2"></div>
    <div class="glow-orb glow-3"></div>
  </div>
</template>

<script setup>
import LottieAnimation from './LottieAnimation.vue'

defineProps({
  showFloaters: { type: Boolean, default: true },
})

// LottieFiles 公开 CDN 动画 - 从 lottiefiles.com 精选的免费 IoT 主题动画
const dataFlowSrc = 'https://assets10.lottiefiles.com/packages/lf20_qp1q7mct.json'
</script>

<style scoped>
.lottie-scene {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
  overflow: hidden;
}

.scene-layer {
  position: absolute;
  display: flex;
  align-items: center;
  justify-content: center;
}

.bg-layer {
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  opacity: 0.15;
}

.floating-icons {
  position: absolute;
  inset: 0;
}

.floater {
  position: absolute;
  opacity: 0.6;
  animation: float-anim 8s ease-in-out infinite;
}

@keyframes float-anim {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  33% { transform: translateY(-15px) rotate(2deg); }
  66% { transform: translateY(10px) rotate(-2deg); }
}

.glow-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.4;
  animation: orb-drift 15s ease-in-out infinite;
}

.glow-1 {
  top: 20%;
  left: 10%;
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, rgba(0, 217, 255, 0.4), transparent 70%);
}

.glow-2 {
  bottom: 20%;
  right: 10%;
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, rgba(0, 255, 157, 0.3), transparent 70%);
  animation-delay: -5s;
}

.glow-3 {
  top: 50%;
  left: 50%;
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, rgba(255, 158, 0, 0.2), transparent 70%);
  animation-delay: -10s;
  transform: translate(-50%, -50%);
}

@keyframes orb-drift {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(30px, -20px) scale(1.1); }
  66% { transform: translate(-20px, 20px) scale(0.95); }
}

.glow-3 {
  animation-name: orb-drift-center;
}

@keyframes orb-drift-center {
  0%, 100% { transform: translate(-50%, -50%) scale(1); }
  33% { transform: translate(calc(-50% + 30px), calc(-50% - 20px)) scale(1.1); }
  66% { transform: translate(calc(-50% - 20px), calc(-50% + 20px)) scale(0.95); }
}
</style>
