<template>
  <div class="number-keyboard">
    <div class="keyboard-display" v-if="modelValue">
      {{ modelValue }}
    </div>
    
    <div class="keyboard-grid">
      <button 
        v-for="num in numbers" 
        :key="num"
        class="keyboard-btn number-btn"
        @click="handleNumber(num)"
      >
        {{ num }}
      </button>
      
      <button 
        class="keyboard-btn delete-btn"
        @click="handleDelete"
        :disabled="!modelValue"
      >
        <el-icon><Delete /></el-icon>
      </button>
      
      <button 
        class="keyboard-btn number-btn"
        @click="handleNumber(0)"
      >
        0
      </button>
      
      <button 
        class="keyboard-btn confirm-btn"
        @click="handleConfirm"
        :disabled="!modelValue"
      >
        <el-icon><Check /></el-icon>
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Delete, Check } from '@element-plus/icons-vue'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  maxLength: {
    type: Number,
    default: 10
  }
})

const emit = defineEmits(['update:modelValue', 'confirm', 'delete'])

const numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]

const handleNumber = (num) => {
  const currentValue = props.modelValue || ''
  if (currentValue.length < props.maxLength) {
    emit('update:modelValue', currentValue + num)
  }
}

const handleDelete = () => {
  const currentValue = props.modelValue || ''
  if (currentValue.length > 0) {
    emit('update:modelValue', currentValue.slice(0, -1))
    emit('delete')
  }
}

const handleConfirm = () => {
  if (props.modelValue) {
    emit('confirm', props.modelValue)
  }
}
</script>

<style scoped lang="scss">
.number-keyboard {
  width: 100%;
  max-width: 360px;
  margin: 0 auto;
}

.keyboard-display {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-size: 48px;
  font-weight: bold;
  text-align: center;
  padding: 20px;
  border-radius: 16px;
  margin-bottom: 20px;
  min-height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  letter-spacing: 4px;
}

.keyboard-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.keyboard-btn {
  aspect-ratio: 1;
  border: none;
  border-radius: 16px;
  font-size: 32px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  user-select: none;
  
  &:active {
    transform: scale(0.95);
  }
  
  &:disabled {
    opacity: 0.4;
    cursor: not-allowed;
  }
}

.number-btn {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(79, 172, 254, 0.4);
  
  &:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(79, 172, 254, 0.6);
  }
}

.delete-btn {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(245, 87, 108, 0.4);
  font-size: 28px;
  
  &:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(245, 87, 108, 0.6);
  }
}

.confirm-btn {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(67, 233, 123, 0.4);
  font-size: 28px;
  
  &:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(67, 233, 123, 0.6);
  }
}

@media (max-width: 480px) {
  .keyboard-display {
    font-size: 36px;
    padding: 16px;
    min-height: 64px;
  }
  
  .keyboard-btn {
    font-size: 28px;
  }
}
</style>
