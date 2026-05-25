<template>
  <div class="practice-container">
    <div class="practice-header">
      <div class="header-back" @click="handleBack">
        <el-icon><ArrowLeft /></el-icon>
      </div>
      <div class="header-info">
        <div class="progress-text">
          第 {{ currentQuestionIndex + 1 }} / {{ questions.length }} 题
        </div>
        <div class="timer" :class="{ warning: timeLeft <= 30 }">
          <el-icon><Timer /></el-icon>
          {{ formatTime(timeLeft) }}
        </div>
      </div>
      <div class="header-score">
        连胜: <StreakFlame :count="currentStreak" />
      </div>
    </div>

    <div class="progress-bar">
      <div 
        class="progress-fill" 
        :style="{ width: progressPercent + '%' }"
      ></div>
    </div>

    <div class="question-card" v-if="currentQuestion && !practiceComplete">
      <div class="question-number">
        <el-tag type="primary" size="large">{{ currentQuestionIndex + 1 }}</el-tag>
      </div>
      
      <div class="question-content">
        <div class="question-text">
          {{ currentQuestion.questionText }}
        </div>
        <div class="question-difficulty">
          <el-tag 
            :type="getDifficultyType(currentQuestion.difficultyLevel)" 
            size="small"
          >
            {{ getDifficultyLabel(currentQuestion.difficultyLevel) }}
          </el-tag>
        </div>
      </div>

      <div v-if="showFeedback" class="feedback-bar" :class="feedbackType">
        <div class="feedback-icon">
          {{ feedbackType === 'correct' ? '✓' : '✗' }}
        </div>
        <div class="feedback-text">
          {{ feedbackText }}
        </div>
        <div v-if="feedbackType === 'incorrect'" class="correct-answer">
          正确答案: {{ currentQuestion.expectedAnswer }}
        </div>
      </div>

      <div class="answer-input">
        <el-input
          ref="answerInputRef"
          v-model="userAnswer"
          type="number"
          placeholder="输入答案"
          size="large"
          :disabled="showFeedback"
          clearable
          @keyup.enter="submitAnswer"
          @focus="onInputFocus"
        >
          <template #prepend>
            <el-button 
              :disabled="currentQuestionIndex === 0" 
              @click="previousQuestion"
            >
              上一题
            </el-button>
          </template>
        </el-input>
        <div class="answer-actions">
          <el-button
            class="action-button"
            type="primary"
            @click="submitAnswer"
            :loading="submitting"
          >
            {{ submitButtonText }}
          </el-button>
        </div>
      </div>
    </div>

    <div class="practice-complete" v-if="practiceComplete">
      <el-result
        icon="success"
        title="练习完成！"
        :sub-title="`正确率：${correctRate}%, 用时：${formatUsedTime()}`"
      >
        <template #extra>
          <div class="result-stars">
            获得星星: <el-tag type="warning" size="large">{{ earnedStars }} ⭐</el-tag>
          </div>
          <div class="result-actions">
            <el-button type="primary" size="large" @click="viewResult">
              查看详情
            </el-button>
            <el-button size="large" @click="backToHome">
              返回首页
            </el-button>
          </div>
        </template>
      </el-result>
    </div>

    <el-dialog
      v-model="showExitConfirm"
      title="退出练习"
      width="300px"
      :close-on-click-modal="false"
    >
      <p>当前练习尚未完成，确定要退出吗？您的进度将不会保存，且会中断当前连胜。</p>
      <div v-if="currentStreak > 0" class="warning-text">
        <el-alert type="warning" :closable="false">
          当前连胜 {{ currentStreak }} 次，退出将清零
        </el-alert>
      </div>
      <template #footer>
        <el-button @click="showExitConfirm = false">取消</el-button>
        <el-button type="danger" @click="confirmExit">确定退出</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, nextTick, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getRandomQuestions, submitPractice } from '@/apis/practices'
import { useUserStore } from '@/stores/auth'
import StreakFlame from '@/components/StreakFlame.vue'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const childId = ref(null)
const questions = ref([])
const currentQuestionIndex = ref(0)
const userAnswer = ref('')
const answers = ref([])
const timeLeft = ref(600)
const timer = ref(null)
const practiceComplete = ref(false)
const showExitConfirm = ref(false)
const answerInputRef = ref(null)
const startTime = ref(null)
const hasUnsavedChanges = ref(false)
const submitting = ref(false)
const showFeedback = ref(false)
const feedbackType = ref('')
const feedbackText = ref('')
const currentStreak = ref(0)
const earnedStars = ref(0)

const currentQuestion = computed(() => {
  return questions.value[currentQuestionIndex.value] || null
})

const submitButtonText = computed(() => {
  return showFeedback.value && feedbackType.value === 'incorrect' ? '下一题' : '提交'
})

const difficultyQueryToGradeLevel = {
  easy: 10,
  medium: 20,
  hard: 50
}

const gradeLevelToDifficultyLevel = {
  10: 1,
  20: 2,
  50: 3,
  100: 4
}

const progressPercent = computed(() => {
  if (questions.value.length === 0) return 0
  return Math.round(((currentQuestionIndex.value + 1) / questions.value.length) * 100)
})

const correctRate = computed(() => {
  if (answers.value.length === 0) return 0
  const correctCount = answers.value.filter(a => a.isCorrect).length
  return Math.round((correctCount / answers.value.length) * 100)
})

const formatTime = (seconds) => {
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
}

const formatUsedTime = () => {
  if (!startTime.value) return '00:00'
  const used = Math.floor((Date.now() - startTime.value) / 1000)
  return formatTime(used)
}

const getDifficultyType = (difficulty) => {
  const map = {
    1: 'success',
    2: 'warning',
    3: 'danger',
    4: 'danger'
  }
  return map[difficulty] || 'info'
}

const getDifficultyLabel = (difficulty) => {
  const labels = {
    1: '10以内',
    2: '20以内',
    3: '50以内',
    4: '100以内'
  }
  return labels[difficulty] || ''
}

const loadQuestions = async () => {
  try {
    const response = await getRandomQuestions({
      grade_level: difficultyQueryToGradeLevel[route.query.difficulty] || 20,
      count: 20
    })
    questions.value = (response || []).map((question) => ({
      ...question,
      questionText: question.questionText ?? question.question_text,
      expectedAnswer: question.expectedAnswer ?? question.expected_answer ?? question.answer,
      difficultyLevel:
        question.difficultyLevel ??
        question.difficulty_level ??
        gradeLevelToDifficultyLevel[question.grade_level] ??
        1
    }))
    if (questions.value.length === 0) {
      ElMessage.warning('暂时没有题目可供练习')
      router.back()
      return
    }
    startTime.value = Date.now()
    startTimer()
  } catch (error) {
    console.error('加载题目失败:', error)
    ElMessage.error('加载题目失败')
    router.back()
  }
}

const startTimer = () => {
  timer.value = setInterval(() => {
    timeLeft.value--
    if (timeLeft.value <= 0) {
      stopTimer()
      finishPractice()
    }
  }, 1000)
}

const stopTimer = () => {
  if (timer.value) {
    clearInterval(timer.value)
    timer.value = null
  }
}

const onInputFocus = () => {
  nextTick(() => {
    if (answerInputRef.value) {
      answerInputRef.value.focus()
    }
  })
}

const submitAnswer = async () => {
  if (showFeedback.value) {
    nextQuestion()
    return
  }

  if (!userAnswer.value.trim()) {
    ElMessage.warning('请输入答案')
    return
  }

  const answer = parseInt(userAnswer.value)
  const expected = parseInt(currentQuestion.value.expectedAnswer)
  const isCorrect = answer === expected

  answers.value.push({
    questionId: currentQuestion.value.id,
    questionText: currentQuestion.value.questionText,
    correctAnswer: expected,
    userAnswer: answer,
    isCorrect: isCorrect,
    timeSpent: Math.floor((Date.now() - startTime.value) / 1000)
  })

  hasUnsavedChanges.value = true

  if (isCorrect) {
    showFeedback.value = false
    feedbackType.value = ''
    feedbackText.value = ''
    userAnswer.value = ''
    nextQuestion()
    return
  }

  showFeedback.value = true
  feedbackType.value = 'incorrect'
  feedbackText.value = '回答错误'
  userAnswer.value = ''
}

const nextQuestion = () => {
  if (showFeedback.value) {
    showFeedback.value = false
  }

  if (currentQuestionIndex.value < questions.value.length - 1) {
    currentQuestionIndex.value++
    onInputFocus()
  } else {
    finishPractice()
  }
}

const previousQuestion = () => {
  if (currentQuestionIndex.value > 0) {
    currentQuestionIndex.value--
    const prevAnswer = answers.value.find(a => a.questionId === currentQuestion.value.id)
    userAnswer.value = prevAnswer ? prevAnswer.userAnswer.toString() : ''
    onInputFocus()
  }
}

const finishPractice = async () => {
  stopTimer()
  
  if (answers.value.length < questions.value.length) {
    const remaining = questions.value.length - answers.value.length
    ElMessageBox.confirm(
      `还有 ${remaining} 道题未完成，确定要提前结束吗？正确率可能受到影响。`,
      '确认结束',
      {
        confirmButtonText: '确定结束',
        cancelButtonText: '继续答题',
        type: 'warning'
      }
    ).then(async () => {
      await submitPracticeData()
    }).catch(() => {
      showFeedback.value = false
      onInputFocus()
    })
  } else {
    await submitPracticeData()
  }
}

const submitPracticeData = async () => {
  submitting.value = true
  
  try {
    const response = await submitPractice({
      childId: childId.value,
      time_spent: Math.floor((Date.now() - startTime.value) / 1000),
      answers: answers.value.reduce((acc, a) => {
        acc[a.questionId] = a.userAnswer
        return acc
      }, {}),
      answer_details: answers.value
    })

    if (response && response.practice_id) {
      earnedStars.value = response.stars_earned || 0
      currentStreak.value = response.streak_info?.current_streak || 0
      practiceComplete.value = true
      hasUnsavedChanges.value = false
    } else {
      ElMessage.error('提交练习失败')
      router.back()
    }
  } catch (error) {
    console.error('提交练习失败:', error)
    ElMessage.error('提交练习失败')
    router.back()
  } finally {
    submitting.value = false
  }
}

const handleBack = () => {
  if (hasUnsavedChanges.value && !practiceComplete.value) {
    showExitConfirm.value = true
  } else {
    router.back()
  }
}

const confirmExit = async () => {
  showExitConfirm.value = false
  stopTimer()
  
  try {
    await submitPractice({
      childId: childId.value,
      answers: {},
      exited: true
    })
  } catch (error) {
    console.log('退出练习记录失败:', error)
  }
  
  router.back()
}

const viewResult = () => {
  router.push({
    path: '/result',
    query: { 
      childId: childId.value,
      practiceId: answers.value[0]?.practiceId
    }
  })
}

const backToHome = () => {
  router.push('/home')
}

watch(currentQuestionIndex, (newIndex) => {
  if (newIndex < answers.value.length) {
    const prevAnswer = answers.value.find(a => a.questionId === currentQuestion.value?.id)
    userAnswer.value = prevAnswer ? prevAnswer.userAnswer.toString() : ''
  } else {
    userAnswer.value = ''
  }
  showFeedback.value = false
})

onMounted(async () => {
  childId.value = parseInt(route.query.childId)
  if (!childId.value) {
    ElMessage.error('缺少孩子ID')
    router.back()
    return
  }

  await loadQuestions()
  onInputFocus()
})

onBeforeUnmount(() => {
  stopTimer()
})
</script>

<style scoped lang="scss">
.practice-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 16px;
}

.practice-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 16px;
  
  .header-back {
    width: 40px;
    height: 40px;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    backdrop-filter: blur(10px);
    
    .el-icon {
      color: white;
      font-size: 20px;
    }
  }
  
  .header-info {
    flex: 1;
    display: flex;
    justify-content: space-between;
    align-items: center;
    
    .progress-text {
      color: white;
      font-size: 16px;
      font-weight: bold;
    }
    
    .timer {
      display: flex;
      align-items: center;
      gap: 4px;
      color: white;
      font-size: 18px;
      font-weight: bold;
      padding: 8px 16px;
      background: rgba(255, 255, 255, 0.2);
      border-radius: 20px;
      backdrop-filter: blur(10px);
      
      &.warning {
        background: rgba(245, 108, 108, 0.8);
        animation: pulse 1s infinite;
      }
    }
  }
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.progress-bar {
  height: 4px;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 2px;
  margin-bottom: 24px;
  overflow: hidden;
  
  .progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
    transition: width 0.3s ease;
  }
}

.question-card {
  background: white;
  border-radius: 20px;
  padding: 32px 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  
  .question-number {
    text-align: center;
    margin-bottom: 24px;
  }
  
  .question-content {
    text-align: center;
    margin-bottom: 32px;
    
    .question-text {
      font-size: 48px;
      font-weight: bold;
      color: #333;
      margin-bottom: 16px;
      letter-spacing: 2px;
    }
    
    .question-difficulty {
      display: flex;
      justify-content: center;
    }
  }
  
  .feedback-bar {
    margin-bottom: 24px;
    padding: 16px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    gap: 12px;
    animation: fadeIn 0.3s ease;
    
    &.correct {
      background: #f0f9ff;
      border: 2px solid #67c23a;
      
      .feedback-icon {
        color: #67c23a;
        font-size: 24px;
        font-weight: bold;
      }
      
      .feedback-text {
        color: #67c23a;
        font-weight: bold;
      }
    }
    
    &.incorrect {
      background: #fef0f0;
      border: 2px solid #f56c6c;
      
      .feedback-icon {
        color: #f56c6c;
        font-size: 24px;
        font-weight: bold;
      }
      
      .feedback-text {
        color: #f56c6c;
        font-weight: bold;
      }
      
      .correct-answer {
        margin-left: auto;
        color: #f56c6c;
        font-weight: bold;
        padding: 4px 12px;
        background: rgba(245, 108, 108, 0.1);
        border-radius: 8px;
      }
    }
  }
  
  .answer-input {
    margin-top: 24px;
    
    .el-input {
      :deep(.el-input__wrapper) {
        border-radius: 12px;
        padding: 12px 16px;
        font-size: 20px;
      }
      
      :deep(.el-input-group__prepend),
      :deep(.el-input-group__append) {
        border-radius: 12px;
        padding: 0 16px;
        
        .el-button {
          font-size: 14px;
        }
      }
    }

    .answer-actions {
      display: grid;
      grid-template-columns: minmax(0, 1fr);
      margin-top: 12px;
    }

    .action-button {
      width: 100%;
      min-width: 0;
    }
  }
}

.practice-complete {
  background: white;
  border-radius: 20px;
  padding: 32px;
  margin-top: 80px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  text-align: center;
  
  .result-stars {
    margin: 24px 0;
    font-size: 24px;
    font-weight: bold;
    
    .el-tag {
      font-size: 28px;
      padding: 12px 24px;
      margin-left: 16px;
    }
  }
  
  .result-actions {
    display: flex;
    justify-content: center;
    gap: 16px;
    margin-top: 24px;
  }
}

.warning-text {
  margin-top: 16px;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.practice-complete {
  background: white;
  border-radius: 20px;
  padding: 32px;
  margin-top: 80px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

:deep(.el-dialog__body) {
  text-align: center;
  
  p {
    margin: 0;
    color: #666;
    font-size: 14px;
  }
}
</style>
