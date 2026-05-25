<template>
  <div class="wrong-questions-container">
    <el-page-header @back="router.back()" class="page-header">
      <template #content>
        <span>错题本</span>
      </template>
    </el-page-header>

    <el-card class="stats-card" shadow="never" v-if="stats">
      <div class="stats-grid">
        <div class="stat-item">
          <div class="stat-value">{{ stats.totalCount || 0 }}</div>
          <div class="stat-label">总错题数</div>
        </div>
        <div class="stat-item">
          <div class="stat-value">{{ stats.todayWrongCount || 0 }}</div>
          <div class="stat-label">今日错题</div>
        </div>
        <div class="stat-item">
          <div class="stat-value warning">{{ Math.round(stats.overallAccuracy || 0) }}%</div>
          <div class="stat-label">当前正确率</div>
        </div>
      </div>
    </el-card>

    <el-card class="questions-card" shadow="never" v-loading="loading">
      <template #header>
        <div class="card-header">
          <span>错题列表</span>
          <el-button 
            v-if="selectedIds.length > 0" 
            type="danger" 
            size="small" 
            @click="batchDelete"
          >
            删除选中
          </el-button>
        </div>
      </template>

      <div v-if="wrongQuestions.length > 0" class="questions-list">
        <div 
          v-for="item in wrongQuestions" 
          :key="item.id" 
          class="question-item"
        >
          <div class="question-header">
            <el-checkbox 
              v-model="selectedIds" 
              :label="item.id"
              @change="updateSelected"
            />
            <div class="question-info">
              <div class="question-text">{{ item.questionText }}</div>
              <div class="question-meta">
                <el-tag size="small" type="warning">{{ item.operationType }}</el-tag>
                <span class="wrong-time">{{ formatTime(item.wrongAt) }}</span>
              </div>
            </div>
          </div>
          
          <div class="question-detail">
            <div class="answer-row error">
              <span class="label">你的答案：</span>
              <span class="value">{{ item.userAnswer }}</span>
            </div>
            <div class="answer-row success">
              <span class="label">正确答案：</span>
              <span class="value">{{ item.correctAnswer }}</span>
            </div>
          </div>

          <div class="question-actions">
            <el-button type="primary" link size="small" @click="reviewQuestion(item)">
              查看
            </el-button>
            <el-button type="danger" link size="small" @click="deleteWrongQuestion(item)">
              删除
            </el-button>
          </div>
        </div>
      </div>

      <el-empty 
        v-if="!loading && wrongQuestions.length === 0" 
        description="没有错题，继续加油！"
      />

      <div class="pagination" v-if="pagination.total > 0">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.pageSize"
          :total="pagination.total"
          :page-sizes="[10, 20, 50]"
          layout="total, sizes, prev, pager, next"
          @current-change="loadWrongQuestions"
          @size-change="loadWrongQuestions"
        />
      </div>
    </el-card>

    <el-dialog
      v-model="showReviewDialog"
      title="错题详情"
      width="90%"
      custom-class="review-dialog"
    >
      <div v-if="currentQuestion" class="review-content">
        <div class="review-question">
          <div class="question-display">{{ currentQuestion.questionText }}</div>
        </div>
        
        <div class="review-answers">
          <div class="answer-row error">
            <span class="label">你的答案：</span>
            <span class="value large">{{ currentQuestion.userAnswer }}</span>
          </div>
          <div class="answer-row success">
            <span class="label">正确答案：</span>
            <span class="value large">{{ currentQuestion.correctAnswer }}</span>
          </div>
        </div>

        <div class="review-hint">
          <el-alert
            title="提示：仔细审题，按照正确的运算步骤计算哦！"
            type="warning"
            :closable="false"
            show-icon
          />
        </div>
      </div>

      <template #footer>
        <el-button @click="showReviewDialog = false">关闭</el-button>
        <el-button type="primary" @click="retryQuestion">
          重新练习
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getWrongQuestions, deleteWrongQuestion as deleteWrongQuestionApi, getWrongQuestionsStats } from '@/apis/wrongQuestions'

const route = useRoute()
const router = useRouter()

const loading = ref(false)
const childId = ref(null)
const wrongQuestions = ref([])
const selectedIds = ref([])
const showReviewDialog = ref(false)
const currentQuestion = ref(null)
const stats = ref(null)

const pagination = reactive({
  page: 1,
  pageSize: 10,
  total: 0
})

const loadStats = async () => {
  try {
    const response = await getWrongQuestionsStats(childId.value)
    stats.value = response.data
  } catch (error) {
    console.error('加载统计数据失败:', error)
  }
}

const loadWrongQuestions = async () => {
  loading.value = true
  try {
    const response = await getWrongQuestions(childId.value, {
      page: pagination.page,
      pageSize: pagination.pageSize
    })
    
    if (response.data) {
      wrongQuestions.value = response.data.items.map(item => ({
        id: item.id,
        questionText: item.question_text,
        correctAnswer: item.correct_answer,
        userAnswer: item.user_answer,
        operationType: item.operation_type,
        wrongAt: item.wrong_at
      }))
      pagination.total = response.data.total || 0
    }
  } catch (error) {
    console.error('加载错题失败:', error)
    ElMessage.error('加载错题失败')
  } finally {
    loading.value = false
  }
}

const updateSelected = () => {
  console.log('Selected IDs:', selectedIds.value)
}

const reviewQuestion = (question) => {
  currentQuestion.value = question
  showReviewDialog.value = true
}

const deleteWrongQuestion = async (question) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除这道错题吗？`,
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    await deleteWrongQuestionApi(question.id)
    ElMessage.success('删除成功')
    
    selectedIds.value = selectedIds.value.filter(id => id !== question.id)
    loadWrongQuestions()
    loadStats()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败:', error)
      ElMessage.error('删除失败')
    }
  }
}

const batchDelete = async () => {
  if (selectedIds.value.length === 0) {
    ElMessage.warning('请选择要删除的错题')
    return
  }

  try {
    await ElMessageBox.confirm(
      `确定要删除选中的 ${selectedIds.value.length} 道错题吗？`,
      '批量删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    await Promise.all(
      selectedIds.value.map(id => deleteWrongQuestionApi(id))
    )
    
    ElMessage.success('批量删除成功')
    selectedIds.value = []
    loadWrongQuestions()
    loadStats()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('批量删除失败:', error)
      ElMessage.error('批量删除失败')
    }
  }
}

const retryQuestion = () => {
  showReviewDialog.value = false
  router.push({
    path: '/practice',
    query: { childId: childId.value }
  })
}

const formatTime = (timestamp) => {
  const date = new Date(timestamp)
  const now = new Date()
  const diff = now - date
  
  if (diff < 60000) {
    return '刚刚'
  } else if (diff < 3600000) {
    return `${Math.floor(diff / 60000)}分钟前`
  } else if (diff < 86400000) {
    return `${Math.floor(diff / 3600000)}小时前`
  } else {
    return `${Math.floor(diff / 86400000)}天前`
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
  loadWrongQuestions()
})
</script>

<style scoped lang="scss">
.wrong-questions-container {
  min-height: 100vh;
  background: #f5f5f5;
  padding-bottom: 20px;
}

.page-header {
  background: white;
  padding: 16px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.stats-card, .questions-card {
  border-radius: 12px;
  margin: 16px;
  
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  
  .stat-item {
    text-align: center;
    
    .stat-value {
      font-size: 28px;
      font-weight: bold;
      margin-bottom: 4px;
      
      &.warning {
        color: #e6a23c;
      }
    }
    
    .stat-label {
      font-size: 12px;
      color: #666;
    }
  }
}

.questions-list {
  .question-item {
    background: white;
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    
    .question-header {
      display: flex;
      gap: 12px;
      margin-bottom: 12px;
      
      .question-info {
        flex: 1;
        
        .question-text {
          font-size: 18px;
          font-weight: bold;
          color: #333;
          margin-bottom: 8px;
        }
        
        .question-meta {
          display: flex;
          align-items: center;
          gap: 8px;
          
          .wrong-time {
            font-size: 12px;
            color: #999;
          }
        }
      }
    }
    
    .question-detail {
      background: #fef0f0;
      border-radius: 6px;
      padding: 12px;
      margin-bottom: 12px;
      
      .answer-row {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 8px;
        font-size: 14px;
        
        &:last-child {
          margin-bottom: 0;
        }
        
        &.error {
          .label {
            color: #f56c6c;
          }
          
          .value {
            color: #f56c6c;
            font-weight: bold;
          }
        }
        
        &.success {
          .label {
            color: #67c23a;
          }
          
          .value {
            color: #67c23a;
            font-weight: bold;
          }
        }
      }
    }
    
    .question-actions {
      display: flex;
      justify-content: flex-end;
      gap: 8px;
      border-top: 1px solid #eee;
      padding-top: 12px;
    }
  }
}

.pagination {
  margin-top: 16px;
  text-align: center;
}

:deep(.review-dialog) {
  .review-content {
    padding: 20px 0;
    
    .review-question {
      text-align: center;
      margin-bottom: 24px;
      
      .question-display {
        font-size: 32px;
        font-weight: bold;
        color: #333;
        padding: 24px;
        background: #f9f9f9;
        border-radius: 12px;
      }
    }
    
    .review-answers {
      max-width: 400px;
      margin: 0 auto 24px auto;
      
      .answer-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 16px;
        border-radius: 8px;
        margin-bottom: 12px;
        font-size: 16px;
        
        &:last-child {
          margin-bottom: 0;
        }
        
        &.error {
          background: #fef0f0;
          
          .label, .value.large {
            color: #f56c6c;
            font-size: 24px;
            font-weight: bold;
          }
        }
        
        &.success {
          background: #f0f9ff;
          
          .label, .value.large {
            color: #67c23a;
            font-size: 24px;
            font-weight: bold;
          }
        }
      }
    }
    
    .review-hint {
      margin-top: 16px;
    }
  }
}
</style>
