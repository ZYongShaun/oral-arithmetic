<template>
  <div 
    class="badge-display" 
    :class="[`badge-${size}`, { 'badge-locked': !isUnlocked }]"
    @click="handleClick"
  >
    <div class="badge-wrapper">
      <div class="badge-icon">
        <el-icon v-if="!isUnlocked" :size="iconSize"></el-icon>
        <el-icon v-else :size="iconSize">
          <component :is="badge.icon" />
        </el-icon>
      </div>
      
      <div class="badge-overlay" v-if="!isUnlocked">
        <el-icon><Lock /></el-icon>
        <span class="lock-text">未解锁</span>
      </div>
      
      <div class="badge-glow" v-if="isUnlocked" :style="{ background: badge.color }"></div>
    </div>
    
    <div class="badge-info">
      <div class="badge-name">{{ badge.name }}</div>
      <div class="badge-desc">{{ badge.description }}</div>
      <div class="badge-time" v-if="isUnlocked && unlockedTime">
        <el-icon><Clock /></el-icon>
        {{ formatTime(unlockedTime) }}
      </div>
      <div class="badge-requirement" v-else-if="!isUnlocked">
        {{ badge.requirement }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Lock, Clock } from '@element-plus/icons-vue'

const props = defineProps({
  badge: {
    type: Object,
    required: true
  },
  isUnlocked: {
    type: Boolean,
    default: false
  },
  unlockedTime: {
    type: String,
    default: null
  },
  size: {
    type: String,
    default: 'medium',
    validator: (value) => ['small', 'medium', 'large'].includes(value)
  }
})

const emit = defineEmits(['click'])

const iconSize = computed(() => {
  const sizes = {
    small: 24,
    medium: 32,
    large: 48
  }
  return sizes[props.size]
})

const formatTime = (time) => {
  if (!time) return ''
  const date = new Date(time)
  const now = new Date()
  const diff = now - date
  
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  if (days === 0) return '今天'
  if (days === 1) return '昨天'
  if (days < 7) return `${days}天前`
  if (days < 30) return `${Math.floor(days / 7)}周前`
  return `${Math.floor(days / 30)}月前`
}

const handleClick = () => {
  emit('click', props.badge)
}
</script>

<style scoped lang="scss">
.badge-display {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  border-radius: 16px;
  background: white;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  
  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
  }
  
  &.badge-locked {
    opacity: 0.6;
    filter: grayscale(0.5);
    
    &:hover {
      transform: translateY(-2px);
    }
  }
}

.badge-wrapper {
  position: relative;
  flex-shrink: 0;
}

.badge-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  color: #666;
  transition: all 0.3s ease;
}

.badge-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: white;
  
  .el-icon {
    font-size: 20px;
    margin-bottom: 2px;
  }
  
  .lock-text {
    font-size: 10px;
    line-height: 1;
  }
}

.badge-glow {
  position: absolute;
  top: -4px;
  left: -4px;
  right: -4px;
  bottom: -4px;
  border-radius: 50%;
  filter: blur(8px);
  opacity: 0.3;
  animation: glow-pulse 2s ease-in-out infinite;
}

.badge-info {
  flex: 1;
  min-width: 0;
}

.badge-name {
  font-size: 16px;
  font-weight: bold;
  color: #333;
  margin-bottom: 4px;
}

.badge-desc {
  font-size: 13px;
  color: #666;
  margin-bottom: 6px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.badge-time {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: #409eff;
}

.badge-requirement {
  font-size: 12px;
  color: #999;
  font-style: italic;
}

@keyframes glow-pulse {
  0%, 100% {
    opacity: 0.3;
    transform: scale(1);
  }
  50% {
    opacity: 0.5;
    transform: scale(1.05);
  }
}

.badge-small {
  padding: 12px;
  
  .badge-icon {
    width: 48px;
    height: 48px;
  }
  
  .badge-name {
    font-size: 14px;
  }
  
  .badge-desc {
    font-size: 12px;
  }
}

.badge-large {
  padding: 20px;
  
  .badge-icon {
    width: 80px;
    height: 80px;
  }
  
  .badge-name {
    font-size: 18px;
  }
  
  .badge-desc {
    font-size: 14px;
  }
}

@media (max-width: 480px) {
  .badge-display {
    padding: 12px;
    gap: 12px;
  }
  
  .badge-icon {
    width: 48px;
    height: 48px;
  }
  
  .badge-name {
    font-size: 14px;
  }
  
  .badge-desc {
    font-size: 12px;
  }
}
</style>
