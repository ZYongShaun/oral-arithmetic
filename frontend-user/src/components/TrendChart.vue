<template>
  <div class="trend-chart">
    <div class="chart-header">
      <div class="chart-title">{{ title }}</div>
      
      <div class="chart-controls">
        <el-radio-group v-model="timeRange" size="small">
          <el-radio-button label="7">7天</el-radio-button>
          <el-radio-button label="30">30天</el-radio-button>
        </el-radio-group>
      </div>
    </div>
    
    <div class="chart-content">
      <div class="chart-legend">
        <div class="legend-item">
          <div class="legend-color practice-color"></div>
          <span>练习次数</span>
        </div>
        <div class="legend-item">
          <div class="legend-color accuracy-color"></div>
          <span>正确率</span>
        </div>
      </div>
      
      <div class="chart-canvas-container" ref="chartContainer">
        <canvas ref="chartCanvas"></canvas>
      </div>
    </div>
    
    <div class="chart-stats" v-if="stats">
      <div class="stat-item">
        <div class="stat-label">总练习</div>
        <div class="stat-value">{{ stats.totalPractices }}次</div>
      </div>
      <div class="stat-item">
        <div class="stat-label">平均正确率</div>
        <div class="stat-value">{{ stats.avgAccuracy }}%</div>
      </div>
      <div class="stat-item">
        <div class="stat-label">最高正确率</div>
        <div class="stat-value">{{ stats.maxAccuracy }}%</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onBeforeUnmount, nextTick } from 'vue'

const props = defineProps({
  data: {
    type: Array,
    default: () => []
  },
  title: {
    type: String,
    default: '练习趋势'
  }
})

const emit = defineEmits(['range-change'])

const timeRange = ref('7')
const chartContainer = ref(null)
const chartCanvas = ref(null)
const resizeObserver = ref(null)

const stats = computed(() => {
  if (!props.data || props.data.length === 0) return null
  
  const totalPractices = props.data.reduce((sum, item) => sum + item.practices, 0)
  const avgAccuracy = Math.round(props.data.reduce((sum, item) => sum + item.accuracy, 0) / props.data.length)
  const maxAccuracy = Math.max(...props.data.map(item => item.accuracy))
  
  return {
    totalPractices,
    avgAccuracy,
    maxAccuracy
  }
})

const filteredData = computed(() => {
  const days = parseInt(timeRange.value)
  return props.data.slice(-days)
})

const drawChart = () => {
  if (!chartCanvas.value || !chartContainer.value) return
  
  const canvas = chartCanvas.value
  const container = chartContainer.value
  const ctx = canvas.getContext('2d')
  
  const rect = container.getBoundingClientRect()
  canvas.width = rect.width * 2
  canvas.height = rect.height * 2
  ctx.scale(2, 2)
  
  const width = rect.width
  const height = rect.height
  const padding = { top: 40, right: 40, bottom: 40, left: 50 }
  const chartWidth = width - padding.left - padding.right
  const chartHeight = height - padding.top - padding.bottom
  
  ctx.clearRect(0, 0, width, height)
  
  const data = filteredData.value
  if (data.length === 0) return
  
  const maxPractices = Math.max(...data.map(d => d.practices), 1)
  const maxAccuracy = 100
  
  const days = data.map(d => d.date.substring(5).replace('-', '/'))
  
  ctx.fillStyle = '#666'
  ctx.font = '11px Arial'
  ctx.textAlign = 'center'
  ctx.textBaseline = 'middle'
  
  const xStep = chartWidth / (data.length - 1 || 1)
  
  for (let i = 0; i < data.length && i < 7; i++) {
    const x = padding.left + i * xStep
    ctx.fillText(days[i], x, height - padding.bottom / 2)
  }
  
  ctx.save()
  ctx.translate(padding.left / 2, padding.top + chartHeight / 2)
  ctx.rotate(-Math.PI / 2)
  ctx.textAlign = 'center'
  ctx.fillText('次数 / 正确率', 0, 0)
  ctx.restore()
  
  ctx.strokeStyle = '#ddd'
  ctx.lineWidth = 1
  
  for (let i = 0; i <= 5; i++) {
    const y = padding.top + (chartHeight / 5) * i
    ctx.beginPath()
    ctx.moveTo(padding.left, y)
    ctx.lineTo(padding.left + chartWidth, y)
    ctx.stroke()
    
    const value = Math.round(100 - (i * 20))
    ctx.fillStyle = '#999'
    ctx.textAlign = 'right'
    ctx.fillText(value.toString(), padding.left - 10, y)
  }
  
  drawPracticeLine(ctx, data, padding, chartWidth, chartHeight, maxPractices, xStep)
  drawAccuracyLine(ctx, data, padding, chartWidth, chartHeight, maxAccuracy, xStep)
}

const drawPracticeLine = (ctx, data, padding, chartWidth, chartHeight, maxValue, xStep) => {
  ctx.beginPath()
  ctx.strokeStyle = '#409eff'
  ctx.lineWidth = 2
  
  data.forEach((item, index) => {
    const x = padding.left + index * xStep
    const normalizedValue = item.practices / maxValue
    const y = padding.top + chartHeight * (1 - normalizedValue)
    
    if (index === 0) {
      ctx.moveTo(x, y)
    } else {
      ctx.lineTo(x, y)
    }
  })
  
  ctx.stroke()
  
  data.forEach((item, index) => {
    const x = padding.left + index * xStep
    const normalizedValue = item.practices / maxValue
    const y = padding.top + chartHeight * (1 - normalizedValue)
    
    ctx.beginPath()
    ctx.arc(x, y, 4, 0, Math.PI * 2)
    ctx.fillStyle = 'white'
    ctx.fill()
    ctx.strokeStyle = '#409eff'
    ctx.lineWidth = 2
    ctx.stroke()
  })
}

const drawAccuracyLine = (ctx, data, padding, chartWidth, chartHeight, maxValue, xStep) => {
  ctx.beginPath()
  ctx.strokeStyle = '#67c23a'
  ctx.lineWidth = 2
  
  data.forEach((item, index) => {
    const x = padding.left + index * xStep
    const normalizedValue = item.accuracy / maxValue
    const y = padding.top + chartHeight * (1 - normalizedValue)
    
    if (index === 0) {
      ctx.moveTo(x, y)
    } else {
      ctx.lineTo(x, y)
    }
  })
  
  ctx.stroke()
  
  data.forEach((item, index) => {
    const x = padding.left + index * xStep
    const normalizedValue = item.accuracy / maxValue
    const y = padding.top + chartHeight * (1 - normalizedValue)
    
    ctx.beginPath()
    ctx.arc(x, y, 4, 0, Math.PI * 2)
    ctx.fillStyle = 'white'
    ctx.fill()
    ctx.strokeStyle = '#67c23a'
    ctx.lineWidth = 2
    ctx.stroke()
  })
}

const initResizeObserver = () => {
  if (!chartContainer.value) return
  
  resizeObserver.value = new ResizeObserver(() => {
    nextTick(() => {
      drawChart()
    })
  })
  
  resizeObserver.value.observe(chartContainer.value)
}

const cleanupResizeObserver = () => {
  if (resizeObserver.value) {
    resizeObserver.value.disconnect()
    resizeObserver.value = null
  }
}

watch([timeRange, () => props.data], () => {
  emit('range-change', timeRange.value)
  nextTick(() => {
    drawChart()
  })
})

watch(chartContainer, (newContainer) => {
  if (newContainer) {
    initResizeObserver()
  }
})

onMounted(() => {
  nextTick(() => {
    drawChart()
  })
})

onBeforeUnmount(() => {
  cleanupResizeObserver()
})
</script>

<style scoped lang="scss">
.trend-chart {
  background: white;
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  
  .chart-title {
    font-size: 18px;
    font-weight: bold;
    color: #333;
  }
}

.chart-content {
  margin-bottom: 20px;
}

.chart-legend {
  display: flex;
  justify-content: center;
  gap: 24px;
  margin-bottom: 16px;
  
  .legend-item {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 13px;
    color: #666;
  }
  
  .legend-color {
    width: 12px;
    height: 12px;
    border-radius: 2px;
    
    &.practice-color {
      background: #409eff;
    }
    
    &.accuracy-color {
      background: #67c23a;
    }
  }
}

.chart-canvas-container {
  width: 100%;
  height: 300px;
  
  canvas {
    width: 100%;
    height: 100%;
  }
}

.chart-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  padding-top: 16px;
  border-top: 1px solid #eee;
  
  .stat-item {
    text-align: center;
    
    .stat-label {
      font-size: 12px;
      color: #999;
      margin-bottom: 4px;
    }
    
    .stat-value {
      font-size: 20px;
      font-weight: bold;
      color: #333;
    }
  }
}

@media (max-width: 768px) {
  .trend-chart {
    padding: 16px;
  }
  
  .chart-header {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }
  
  .chart-canvas-container {
    height: 250px;
  }
  
  .chart-stats {
    grid-template-columns: 1fr;
    gap: 12px;
  }
}

@media (max-width: 480px) {
  .trend-chart {
    padding: 12px;
  }
  
  .chart-canvas-container {
    height: 200px;
  }
}
</style>
