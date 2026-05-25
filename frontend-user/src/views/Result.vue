<template>
  <div class="result-container">
    <el-card class="result-card" shadow="never">
      <div class="result-header">
        <div class="result-icon" :class="getResultIconType()">
          <el-icon :size="60">
            <component :is="getResultIcon()" />
          </el-icon>
        </div>
        <h2 class="result-title">{{ getResultTitle() }}</h2>
        <p class="result-subtitle">{{ getResultSubtitle() }}</p>
      </div>

      <div class="score-display">
        <div class="score-number">{{ correctRate }}%</div>
        <div class="score-label">正确率</div>
      </div>

      <div class="stars-earned">
        <div class="stars-label">获得星星</div>
        <div class="stars-display">
          <el-icon 
            v-for="i in 3" 
            :key="i" 
            class="star-icon" 
            :style="{ color: i <= starsEarned ? '#FFD700' : '#d9d9d9' }"
          >
            <StarFilled />
          </el-icon>
          <span class="stars-count">+{{ starsEarned }}</span>
        </div>
      </div>

      <div class="stats-grid">
        <div class="stat-item">
          <div class="stat-value">{{ totalQuestions }}</div>
          <div class="stat-label">总题数</div>
        </div>
        <div class="stat-item">
          <div class="stat-value success">{{ correctCount }}</div>
          <div class="stat-label">正确</div>
        </div>
        <div class="stat-item">
          <div class="stat-value error">{{ wrongCount }}</div>
          <div class="stat-label">错误</div>
        </div>
      </div>

      <div class="action-buttons">
        <el-button 
          type="primary" 
          size="large" 
          class="action-btn"
          @click="newPractice"
        >
          <el-icon><RefreshRight /></el-icon>
          新一轮练习
        </el-button>
        <el-button 
          v-if="wrongCount > 0" 
          type="warning" 
          size="large" 
          class="action-btn"
          @click="reviewWrongQuestions"
        >
          <el-icon><Warning /></el-icon>
          查看错题
        </el-button>
        <el-button 
          type="default" 
          size="large" 
          class="action-btn"
          @click="backToHome"
        >
          <el-icon><HomeFilled /></el-icon>
          返回首页
        </el-button>
      </div>
    </el-card>

    <el-card class="wrong-questions-card" shadow="never" v-if="wrongCount > 0">
      <template #header>
        <div class="card-header">
          <span>错题回顾</span>
          <el-button type="primary" link @click="reviewWrongQuestions">
            查看全部
          </el-button>
        </div>
      </template>
      
      <div v-for="(wrongItem, index) in wrongQuestions.slice(0, 3)" :key="index" class="wrong-item">
        <div class="wrong-content">
          <div class="wrong-text">{{ wrongItem.questionText }}</div>
          <div class="wrong-answers">
            <span class="user-answer error">你的答案：{{ wrongItem.userAnswer }}</span>
            <span class="correct-answer success">正确答案：{{ wrongItem.correctAnswer }}</span>
          </div>
        </div>
      </div>
      
      <el-empty 
        v-if="wrongQuestions.length === 0" 
        description="没有错题，太棒了！" 
      />
    </el-card>

    <el-dialog
      v-model="showCelebrationDialog"
      width="320px"
      custom-class="celebration-dialog"
      :show-close="false"
    >
      <div class="celebration-content">
        <el-icon color="#FFD700" :size="80"><Trophy /></el-icon>
        <h3>恭喜你！</h3>
        <p>获得了 {{ starsEarned }} 颗星星</p>
      </div>
      <template #footer>
        <el-button type="primary" @click="showCelebrationDialog = false">
          太棒了！
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getWrongQuestions } from '@/apis/wrongQuestions'

const route = useRoute()
const router = useRouter()

const childId = ref(null)
const correctRate = ref(0)
const starsEarned = ref(0)
const wrongQuestions = ref([])
const showCelebrationDialog = ref(false)

const totalQuestions = computed(() => 20)
const correctCount = computed(() => Math.round(totalQuestions.value * (correctRate.value / 100)))
const wrongCount = computed(() => totalQuestions.value - correctCount.value)

const getResultIcon = () => {
  if (correctRate.value === 100) return 'Trophy'
  if (correctRate.value >= 80) return 'CircleCheckFilled'
  if (correctRate.value >= 60) return 'CircleCheck'
  return 'WarningFilled'
}

const getResultIconType = () => {
  if (correctRate.value === 100) return 'gold'
  if (correctRate.value >= 80) return 'silver'
  if (correctRate.value >= 60) return 'bronze'
  return 'normal'
}

const getResultTitle = () => {
  if (correctRate.value === 100) return '完美表现！'
  if (correctRate.value >= 80) return '做得很好！'
  if (correctRate.value >= 60) return '继续加油！'
  return '需要努力！'
}

const getResultSubtitle = () => {
  if (correctRate.value === 100) return '全部正确，太棒了！'
  if (correctRate.value >= 80) return '正确率很高，继续保持！'
  if (correctRate.value >= 60) return '掌握了大部分知识点！'
  return '多加练习，你一定能做到！'
}

const loadWrongQuestions = async () => {
  try {
    const response = await getWrongQuestions(childId.value, {
      page: 1,
      pageSize: 3
    })
    if (response.data && response.data.items) {
      wrongQuestions.value = response.data.items.map(item => ({
        questionText: item.question_text,
        userAnswer: item.user_answer,
        correctAnswer: item.correct_answer
      }))
    }
  } catch (error) {
    console.error('加载错题失败:', error)
  }
}

const newPractice = () => {
  router.push({
    path: '/practice',
    query: { childId: childId.value }
  })
}

const reviewWrongQuestions = () => {
  router.push({
    path: '/wrong-questions',
    query: { childId: childId.value }
  })
}

const backToHome = () => {
  router.push('/')
}

onMounted(() => {
  childId.value = parseInt(route.query.childId) || parseInt(localStorage.getItem('lastSelectedChildId'))
  correctRate.value = parseInt(route.query.correctRate) || 0
  starsEarned.value = parseInt(route.query.starsEarned) || 0
  
  if (correctRate.value > 0) {
    loadWrongQuestions()
    
    if (starsEarned.value > 0 && correctRate.value >= 80) {
      showCelebrationDialog.value = true
    }
  }
})
</script>

<style scoped lang="scss">
.result-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 16px;
}

.result-card, .wrong-questions-card {
  border-radius: 20px;
  margin-bottom: 16px;
  
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
}

.result-header {
  text-align: center;
  padding: 20px 0;
  
  .result-icon {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 16px auto;
    
    &.gold {
      background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
      color: white;
    }
    
    &.silver {
      background: linear-gradient(135deg, #C0C0C0 0%, #A9A9A9 100%);
      color: white;
    }
    
    &.bronze {
      background: linear-gradient(135deg, #CD7F32 0%, #8B4513 100%);
      color: white;
    }
    
    &.normal {
      background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
      color: white;
    }
  }
  
  .result-title {
    margin: 0 0 8px 0;
    font-size: 24px;
    font-weight: bold;
    color: #333;
  }
  
  .result-subtitle {
    margin: 0;
    color: #666;
    font-size: 14px;
  }
}

.score-display {
  text-align: center;
  padding: 32px 0;
  background: linear-gradient(135deg, #f0f9ff 0%, #e6f7ff 100%);
  border-radius: 16px;
  margin-bottom: 24px;
  
  .score-number {
    font-size: 64px;
    font-weight: bold;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 8px;
  }
  
  .score-label {
    font-size: 16px;
    color: #666;
  }
}

.stars-earned {
  text-align: center;
  padding: 24px 0;
  margin-bottom: 24px;
  
  .stars-label {
    font-size: 16px;
    color: #666;
    margin-bottom: 12px;
  }
  
  .stars-display {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    
    .star-icon {
      font-size: 40px;
      transition: transform 0.3s;
      
      &:hover {
        transform: scale(1.2);
      }
    }
    
    .stars-count {
      font-size: 28px;
      font-weight: bold;
      color: #FFD700;
      margin-left: 8px;
    }
  }
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 32px;
  
  .stat-item {
    text-align: center;
    padding: 16px;
    background: #f9f9f9;
    border-radius: 12px;
    
    .stat-value {
      font-size: 32px;
      font-weight: bold;
      margin-bottom: 8px;
      
      &.success {
        color: #67c23a;
      }
      
      &.error {
        color: #f56c6c;
      }
    }
    
    .stat-label {
      font-size: 14px;
      color: #666;
    }
  }
}

.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 12px;
  
  .action-btn {
    height: 50px;
    font-size: 16px;
    border-radius: 12px;
    
    .el-icon {
      font-size: 18px;
      margin-right: 8px;
    }
  }
}

.wrong-questions-card {
  .wrong-item {
    padding: 16px;
    background: #fef0f0;
    border-radius: 8px;
    margin-bottom: 12px;
    border-left: 4px solid #f56c6c;
    
    &:last-child {
      margin-bottom: 0;
    }
    
    .wrong-content {
      .wrong-text {
        font-size: 16px;
        font-weight: bold;
        margin-bottom: 8px;
        color: #333;
      }
      
      .wrong-answers {
        display: flex;
        flex-direction: column;
        gap: 4px;
        font-size: 14px;
        
        .user-answer {
          &.error {
            color: #f56c6c;
          }
        }
        
        .correct-answer {
          &.success {
            color: #67c23a;
          }
        }
      }
    }
  }
}

:deep(.celebration-dialog) {
  .el-dialog__body {
    text-align: center;
    padding: 32px 20px;
  }
  
  .celebration-content {
    h3 {
      margin: 16px 0 8px 0;
      color: #333;
      font-size: 20px;
    }
    
    p {
      margin: 0;
      color: #666;
      font-size: 14px;
    }
  }
}
</style>
