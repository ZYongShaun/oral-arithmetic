<template>
  <div class="streak-flame" :style="{ width: size + 'px', height: size + 'px' }">
    <div class="flame-container" :class="{ 'super-flame': isSuperFlame }">
      <div class="flame-outer" :style="{ borderColor: flameColor }">
        <div class="flame-inner" :style="{ borderColor: flameColor }">
          <div class="flame-core">
            <div class="flame-icon">
              🔥
            </div>
            <div class="streak-count" :style="{ color: flameColor }">
              {{ streakCount }}
            </div>
          </div>
        </div>
      </div>
      
      <div class="flame-particles" v-if="isSuperFlame">
        <div class="particle" v-for="i in 6" :key="i" :style="{ animationDelay: (i * 0.3) + 's' }"></div>
      </div>
    </div>
    
    <div class="streak-label" :style="{ color: flameColor }">
      <span v-if="streakCount === 0">开始连胜</span>
      <span v-else-if="streakCount < 3">连胜{{ streakCount }}次</span>
      <span v-else-if="streakCount < 7">连胜{{ streakCount }}次🔥</span>
      <span v-else>超级连胜{{ streakCount }}次}}次🔥🔥</span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  streakCount: {
    type: Number,
    default: 0
  },
  size: {
    type: Number,
    default: 80
  },
  color: {
    type: String,
    default: null
  }
})

const isSuperFlame = computed(() => props.streakCount >= 7)

const flameColor = computed(() => {
  if (props.color) return props.color
  
  if (props.streakCount === 0) return '#ccc'
  if (props.streakCount < 3) return '#ffa500'
  if (props.streakCount < 7) return '#ff6b35'
  return '#ff0055'
})
</script>

<style scoped lang="scss">
.streak-flame {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.flame-container {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.flame-outer {
  position: relative;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  border: 3px solid var(--flame-color, #ffa500);
  animation: flame-pulse 2s ease-in-out infinite;
  display: flex;
  align-items: center;
  justify-content: center;
}

.flame-inner {
  width: 80%;
  height: 80%;
  border-radius: 50%;
  border: 2px solid var(--flame-color, #ffa500);
  animation: flame-pulse 1.5s ease-in-out infinite reverse;
  display: flex;
  align-items: center;
  justify-content: center;
}

.flame-core {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.flame-icon {
  font-size: 24px;
  color: var(--flame-color, #ffa500);
  animation: flame-flicker 0.5s ease-in-out infinite alternate;
}

.streak-count {
  font-size: 20px;
  font-weight: bold;
  line-height: 1;
}

.streak-label {
  font-size: 14px;
  font-weight: bold;
  text-align: center;
}

.super-flame {
  .flame-outer {
    animation: super-flame-pulse 1s ease-in-out infinite;
  }
  
  .flame-icon {
    font-size: 28px;
    animation: super-flame-flicker 0.3s ease-in-out infinite alternate;
  }
}

.flame-particles {
  position: absolute;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.particle {
  position: absolute;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--flame-color, #ffa500);
  top: 50%;
  left: 50%;
  opacity: 0;
  animation: particle-rise 1.5s ease-out infinite;
}

@keyframes flame-pulse {
  0%, 100% {
    transform: scale(1);
    opacity: 0.8;
  }
  50% {
    transform: scale(1.05);
    opacity: 1;
  }
}

@keyframes super-flame-pulse {
  0%, 100% {
    transform: scale(1) rotate(0deg);
    opacity: 0.9;
  }
  25% {
    transform: scale(1.1) rotate(5deg);
    opacity: 1;
  }
  75% {
    transform: scale(1.1) rotate(-5deg);
    opacity: 1;
  }
}

@keyframes flame-flicker {
  0% {
    transform: scale(1);
  }
  100% {
    transform: scale(1.1);
  }
}

@keyframes super-flame-flicker {
  0% {
    transform: scale(1) rotate(-5deg);
  }
  100% {
    transform: scale(1.2) rotate(5deg);
  }
}

@keyframes particle-rise {
  0% {
    transform: translate(-50%, -50%) scale(1);
    opacity: 0.8;
  }
  100% {
    transform: translate(-50%, -150%) scale(0.3);
    opacity: 0;
  }
}

@media (max-width: 480px) {
  .streak-label {
    font-size: 12px;
  }
}
</style>
