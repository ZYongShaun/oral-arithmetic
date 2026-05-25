<template>
  <div ref="chartRef" style="height: 400px; width: 100%"></div>
</template>

<script setup>
import { ref, onMounted, watch, onBeforeUnmount } from 'vue'
import * as echarts from 'echarts'

const props = defineProps({
  history: {
    type: Array,
    default: () => []
  }
})

const chartRef = ref(null)
let chartInstance = null

const initChart = () => {
  if (!chartRef.value) return
  chartInstance = echarts.init(chartRef.value)
  updateChart()
}

const updateChart = () => {
  if (!chartInstance) return
  const dates = props.history.map(item => item.date).reverse()
  const values = props.history.map(item => item.question_count).reverse()
  const option = {
    title: {
      text: '历史趋势',
      left: 'center'
    },
    tooltip: {
      trigger: 'axis'
    },
    xAxis: {
      type: 'category',
      data: dates
    },
    yAxis: {
      type: 'value',
      name: '题数'
    },
    series: [{
      data: values,
      type: 'line',
      smooth: true,
      areaStyle: {}
    }]
  }
  chartInstance.setOption(option)
}

watch(() => props.history, () => {
  updateChart()
}, { deep: true })

onMounted(() => {
  initChart()
})

onBeforeUnmount(() => {
  if (chartInstance) {
    chartInstance.dispose()
  }
})
</script>
