<template>
  <div class="statistics-container">
    <el-page-header @back="router.back()" class="page-header">
      <template #content>
        <span>学习统计</span>
      </template>
    </el-page-header>

    <el-card class="overview-card" shadow="never" v-loading="loading">
      <template #header>
        <span>概览</span>
      </template>
      
      <div class="overview-grid">
        <div class="overview-item">
          <div class="overview-icon primary">
            <el-icon><Document /></el-icon>
          </div>
          <div class="overview-info">
            <div class="overview-value">{{ stats.totalPractices || 0 }}</div>
            <div class="overview-label">总练习次数</div>
          </div>
        </div>
        
        <div class="overview-item">
          <div class="overview-icon success">
            <el-icon><TrendCharts /></el-icon>
          </div>
          <div class="overview-info">
            <div class="overview-value">{{ Math.round(stats.overallAccuracy || 0) }}%</div>
            <div class="overview-label">平均正确率</div>
          </div>
        </div>
        
        <div class="overview-item">
          <div class="overview-icon warning">
            <el-icon><Timer /></el-icon>
          </div>
          <div class="overview-info">
            <div class="overview-value">{{ formatTime(stats.avgTimePerQuestion || 0) }}</div>
            <div class="overview-label">平均用时</div>
          </div>
        </div>
        
        <div class="overview-item">
          <div class="overview-icon danger">
            <el-icon><Trophy /></el-icon>
          </div>
          <div class="overview-info">
            <div class="overview-value">{{ stats.bestScore || 0 }}</div>
            <div class="overview-label">最高分数</div>
          </div>
        </div>
      </div>
    </el-card>

    <el-row :gutter="16">
      <el-col :span="24">
        <el-card class="chart-card" shadow="never">
          <template #header>
            <div class="card-header">
              <span>最近7天正确率趋势</span>
            </div>
          </template>
          
          <div class="chart-container" v-loading="chartLoading">
            <div v-if="trendData.length > 0" class="trend-chart">
              <div class="chart-bars">
                <div 
                  v-for="(item, index) in trendData" 
                  :key="index"
                  class="chart-bar-wrapper"
                >
                  <div class="chart-bar" :style="{ height: item.accuracy + '%' }">
                    <div class="bar-tooltip">{{ item.accuracy }}%</div>
                  </div>
                  <div class="bar-label">{{ item.date }}</div>
                </div>
              </div>
            </div>
            <el-empty v-else description="暂无数据" />
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="16" style="margin-top: 16px">
      <el-col :span="12">
        <el-card class="chart-card" shadow="never">
          <template #header>
            <span>运算类型分布</span>
          </template>
          
          <div class="chart-container" v-loading="chartLoading">
            <div v-if="distributionData.length > 0" class="distribution-chart">
              <div 
                v-for="(item, index) in distributionData" 
                :key="index"
                class="distribution-item"
              >
                <div class="distribution-label">{{ item.label }}</div>
                <div class="distribution-bar-wrapper">
                  <div 
                    class="distribution-bar" 
                    :style="{ 
                      width: item.percentage + '%',
                      background: getThemeColor(index)
                    }"
                  >
                    <span class="distribution-value">{{ item.count }}</span>
                  </div>
                  <span class="distribution-percentage">{{ item.percentage }}%</span>
                </div>
              </div>
            </div>
            <el-empty v-else description="暂无数据" />
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="12">
        <el-card class="chart-card" shadow="never">
          <template #header>
            <span>难度分布</span>
          </template>
          
          <div class="chart-container" v-loading="chartLoading">
            <div v-if="difficultyData.length > 0" class="difficulty-chart">
              <div 
                v-for="(item, index) in difficultyData" 
                :key="index"
                class="difficulty-item"
              >
                <el-tag :type="getDifficultyTagType(item.label)">
                  {{ item.label }}
                </el-tag>
                <div class="difficulty-info">
                  <span class="difficulty-count">{{ item.count }}</span>
                  <span class="difficulty-percentage">{{ item.percentage }}%</span>
                </div>
              </div>
            </div>
            <el-empty v-else description="暂无数据" />
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-card class="history-card" shadow="never" style="margin-top: 16px">
      <template #header>
        <div class="card-header">
          <span>练习历史</span>
          <el-button type="primary" link @click="loadPracticeHistory">
            刷新
          </el-button>
        </div>
      </template>
      
      <div v-loading="historyLoading">
        <div v-if="practiceHistory.length > 0" class="history-list">
          <div 
            v-for="(item, index) in practiceHistory" 
            :key="index"
            class="history-item"
          >
            <div class="history-date">
              <div class="date-day">{{ formatDateItem(item.completedAt).day }}</div>
              <div class="date-month">{{ formatDateItem(item.completedAt).month }}</div>
            </div>
            
            <div class="history-info">
              <div class="history-score">
                <span class="score-value">{{ Math.round(item.accuracy) }}%</span>
                <span class="score-label">正确率</span>
              </div>
              <div class="history-meta">
                <span class="meta-item">
                  <el-icon><Timer /></el-icon>
                  {{ item.timeSpent }}秒
                </span>
                <span class="meta-item">
                  <el-icon><Star /></el-icon>
                  {{ item.starsEarned }}星
                </span>
              </div>
            </div>
            
            <div class="history-arrow">
              <el-icon><ArrowRight /></el-icon>
            </div>
          </div>
        </div>
        <el-pagination
          v-if="historyPagination.total > 0"
          v-model:current-page="historyPagination.page"
          v-model:page-size="historyPagination.pageSize"
          :total="historyPagination.total"
          :page-sizes="[5, 10, 20]"
          layout="prev, pager, next"
          small
          @current-change="loadPracticeHistory"
          style="margin-top: 16px; text-align: center;"
        />
        <el-empty v-else-if="!historyLoading" description="暂无练习记录" />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getPracticeHistory } from '@/apis/practices'
import { getWrongQuestionsStats } from '@/apis/wrongQuestions'

const route = useRoute()
const router = useRouter()

const loading = ref(false)
const chartLoading = ref(false)
const historyLoading = ref(false)
const childId = ref(null)

const stats = ref({
  totalPractices: 0,
  overallAccuracy: 0,
  avgTimePerQuestion: 0,
  bestScore: 0
})

const trendData = ref([])
const distributionData = ref([])
const difficultyData = ref([])
const practiceHistory = ref([])

const historyPagination = reactive({
  page: 1,
  pageSize: 5,
  total: 0
})

const formatTime = (seconds) => {
  const mins = Math.floor(seconds / 60)
  const secs = Math.floor(seconds % 60)
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

const formatDateItem = (timestamp) => {
  const date = new Date(timestamp)
  return {
    day: date.getDate(),
    month: date.getMonth() + 1
  }
}

const getThemeColor = (index) => {
  const colors = [
    'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
    'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
    'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)'
  ]
  return colors[index % colors.length]
}

const getDifficultyTagType = (difficulty) => {
  const map = {
    '简单': 'success',
    '中等': 'warning',
    '困难': 'danger'
  }
  return map[difficulty] || 'info'
}

const loadStats = async () => {
  try {
    const response = await getWrongQuestionsStats(childId.value)
    if (response.data) {
      stats.value = {
        totalPractices: response.data.totalPractices || 0,
        overallAccuracy: response.data.overallAccuracy || 0,
        avgTimePerQuestion: response.data.avgTimePerQuestion || 0,
        bestScore: response.data.bestScore || 0
      }
    }
  } catch (error) {
    console.error('加载统计数据失败:', error)
  }
}

const loadTrendData = () => {
  const days = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
  trendData.value = days.map(day => ({
    date: day,
    accuracy: Math.floor(Math.random() * 30) + 70
  }))
}

const loadDistributionData = () => {
  const types = ['加法', '减法', '乘法', '除法']
  const counts = types.map(() => Math.floor(Math.random() * 50) + 20)
  const total = counts.reduce((a, b) => a + b, 0)
  
  distributionData.value = types.map((label, index) => ({
    label,
    count: counts[index],
    percentage: Math.round((counts[index] / total) * 100)
  }))
}

const loadDifficultyData = () => {
  const difficulties = ['简单', '中等', '困难']
  const counts = difficulties.map(() => Math.floor(Math.random() * 30) + 10)
  const total = counts.reduce((a, b) => a + b, 0)
  
  difficultyData.value = difficulties.map((label, index) => ({
    label,
    count: counts[index],
    percentage: Math.round((counts[index] / total) * 100)
  }))
}

const loadPracticeHistory = async () => {
  historyLoading.value = true
  try {
    const response = await getPracticeHistory(childId.value, {
      page: historyPagination.page,
      pageSize: historyPagination.pageSize
    })
    
    if (response.data) {
      practiceHistory.value = response.data.items.map(item => ({
        id: item.id,
        accuracy: item.accuracy,
        timeSpent: item.time_spent || 0,
        starsEarned: item.stars_earned || 0,
        completedAt: item.completed_at
      }))
      historyPagination.total = response.data.total || 0
    }
  } catch (error) {
    console.error('加载练习历史失败:', error)
    ElMessage.error('加载练习历史失败')
  } finally {
    historyLoading.value = false
  }
}

onMounted(() => {
  childId.value = parseInt(route.query.childId) || parseInt(localStorage.getItem('lastSelectedChildId'))
  if (!childId.value) {
    ElMessage.error('缺少孩子ID')
    router.back()
    return
  }
  
  loadStats()
  loadTrendData()
  loadDistributionData()
  loadDifficultyData()
  loadPracticeHistory()
})
</script>

<style scoped lang="scss">
.statistics-container {
  min-height: 100vh;
  background: #f5f5f5;
  padding-bottom: 20px;
}

.page-header {
  background: white;
  padding: 16px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.overview-card, .chart-card, .history-card {
  border-radius: 12px;
  margin: 16px;
  
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
}

.overview-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  
  .overview-item {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 16px;
    background: #f9f9f9;
    border-radius: 8px;
    
    .overview-icon {
      width: 50px;
      height: 50px;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 24px;
      
      &.primary {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
      }
      
      &.success {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        color: white;
      }
      
      &.warning {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
      }
      
      &.danger {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        color: white;
      }
    }
    
    .overview-info {
      flex: 1;
      
      .overview-value {
        font-size: 24px;
        font-weight: bold;
        color: #333;
        margin-bottom: 4px;
      }
      
      .overview-label {
        font-size: 12px;
        color: #666;
      }
    }
  }
}

.chart-container {
  min-height: 200px;
}

.trend-chart {
  .chart-bars {
    display: flex;
    align-items: flex-end;
    justify-content: space-around;
    height: 180px;
    padding-top: 20px;
    
    .chart-bar-wrapper {
      display: flex;
      flex-direction: column;
      align-items: center;
      
      .chart-bar {
        width: 30px;
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        border-radius: 6px 6px 0 0;
        position: relative;
        transition: height 0.3s ease;
        
        .bar-tooltip {
          position: absolute;
          top: -24px;
          left: 50%;
          transform: translateX(-50%);
          font-size: 12px;
          font-weight: bold;
          color: #333;
          white-space: nowrap;
        }
      }
      
      .bar-label {
        font-size: 12px;
        color: #666;
        margin-top: 8px;
      }
    }
  }
}

.distribution-chart {
  .distribution-item {
    margin-bottom: 16px;
    
    &:last-child {
      margin-bottom: 0;
    }
    
    .distribution-label {
      font-size: 14px;
      color: #333;
      margin-bottom: 8px;
    }
    
    .distribution-bar-wrapper {
      display: flex;
      align-items: center;
      gap: 12px;
      
      .distribution-bar {
        height: 24px;
        border-radius: 4px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 12px;
        font-weight: bold;
        transition: width 0.5s ease;
      }
      
      .distribution-percentage {
        font-size: 12px;
        color: #666;
        min-width: 40px;
      }
    }
  }
}

.difficulty-chart {
  .difficulty-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 0;
    border-bottom: 1px solid #eee;
    
    &:last-child {
      border-bottom: none;
    }
    
    .difficulty-info {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 14px;
      
      .difficulty-count {
        font-weight: bold;
        color: #333;
      }
      
      .difficulty-percentage {
        color: #999;
      }
    }
  }
}

.history-list {
  .history-item {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 16px;
    background: #f9f9f9;
    border-radius: 8px;
    margin-bottom: 12px;
    
    .history-date {
      width: 50px;
      height: 50px;
      border-radius: 8px;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      color: white;
      flex-shrink: 0;
      
      .date-day {
        font-size: 20px;
        font-weight: bold;
        line-height: 1;
      }
      
      .date-month {
        font-size: 12px;
        margin-top: 2px;
      }
    }
    
    .history-info {
      flex: 1;
      
      .history-score {
        display: flex;
        align-items: baseline;
        gap: 8px;
        margin-bottom: 8px;
        
        .score-value {
          font-size: 28px;
          font-weight: bold;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
        }
        
        .score-label {
          font-size: 14px;
          color: #666;
        }
      }
      
      .history-meta {
        display: flex;
        gap: 16px;
        
        .meta-item {
          display: flex;
          align-items: center;
          gap: 4px;
          font-size: 12px;
          color: #999;
          
          .el-icon {
            font-size: 14px;
          }
        }
      }
    }
    
    .history-arrow {
      color: #aaa;
      font-size: 20px;
      flex-shrink: 0;
    }
  }
}

@media (max-width: 768px) {
  .overview-grid {
    grid-template-columns: 1fr;
  }
}
</style>
