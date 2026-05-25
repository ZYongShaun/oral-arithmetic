<template>
  <div class="home-container">
    <el-card class="welcome-card" shadow="never">
      <div class="welcome-content">
        <div class="avatar-section">
          <el-avatar :size="80" :src="childAvatar" v-if="selectedChild">
            {{ selectedChild.name.charAt(0) }}
          </el-avatar>
          <el-avatar :size="80" class="default-avatar" v-else>
            <el-icon><User /></el-icon>
          </el-avatar>
        </div>
        <div class="info-section">
          <h2 v-if="selectedChild">你好，{{ selectedChild.name }}！</h2>
          <h2 v-else>欢迎回来！</h2>
          <p class="subtitle">今天也要加油哦~</p>
        </div>
      </div>
    </el-card>

    <el-card class="stats-card" shadow="never" v-if="selectedChild">
      <template #header>
        <div class="card-header">
          <span>今日数据</span>
          <el-button type="primary" link @click="goToStatistics">查看更多</el-button>
        </div>
      </template>
      <div class="stats-grid">
        <div class="stat-item">
          <div class="stat-value">{{ todayStats.practiceCount || 0 }}</div>
          <div class="stat-label">今日练习</div>
        </div>
        <div class="stat-item">
          <div class="stat-value stars">{{ todayStars || 0 }}</div>
          <div class="stat-label">今日星星</div>
        </div>
        <div class="stat-item">
          <div class="stat-value total-stars">{{ totalStars || 0 }}</div>
          <div class="stat-label">星星总数</div>
        </div>
        <div class="stat-item">
          <div class="stat-value success">{{ todayStats.correctRate || 0 }}%</div>
          <div class="stat-label">正确率</div>
        </div>
      </div>
    </el-card>

    <el-card class="tasks-card" shadow="never" v-if="selectedChild">
      <template #header>
        <div class="card-header">
          <span>每日任务</span>
          <el-tag :type="dailyTaskCompleted ? 'success' : 'info'" size="small">
            {{ dailyTaskCompleted ? '已完成' : `${dailyTaskProgress || 0}/3次` }}
          </el-tag>
        </div>
      </template>
      <div class="task-item">
        <div class="task-info">
          <el-icon><Trophy /></el-icon>
          <span>完成3次练习</span>
        </div>
        <el-button 
          v-if="dailyTaskCompleted && !dailyTaskRewardClaimed" 
          type="warning" 
          size="small" 
          @click="claimDailyTaskReward"
        >
          领取奖励
        </el-button>
        <el-icon v-else-if="dailyTaskRewardClaimed" class="task-done"><SuccessFilled /></el-icon>
      </div>
    </el-card>

    <el-card class="streak-card" shadow="never" v-if="selectedChild">
      <StreakFlame 
        :streak-count="streakInfo.currentStreak || 0" 
        :size="100"
      >
        <div class="streak-details">
          <div class="streak-icon-text">
            <div class="streak-count">{{ streakInfo.currentStreak || 0 }}</div>
            <div class="streak-label">连胜天数</div>
          </div>
        </div>
      </StreakFlame>
      <div class="streak-info">
        <div class="streak-text">
          <div class="streak-label">连续打卡</div>
          <div class="streak-shields">
            <el-icon><Shield /></el-icon>
            <span>{{ streakInfo.shields || 0 }}个保护盾</span>
          </div>
        </div>
      </div>
    </el-card>

    <el-card class="quick-actions-card" shadow="never">
      <template #header>
        <div class="card-header">
          <span>快速开始</span>
          <el-select 
            v-model="difficulty" 
            placeholder="选择难度" 
            size="small"
            @change="saveDifficulty"
            style="width: 120px"
          >
            <el-option label="简单" value="easy"></el-option>
            <el-option label="中等" value="medium"></el-option>
            <el-option label="困难" value="hard"></el-option>
          </el-select>
        </div>
      </template>
      <div class="actions-grid">
        <div class="action-item" @click="startPractice">
          <div class="action-icon primary">
            <el-icon :size="32"><Edit /></el-icon>
          </div>
          <div class="action-label">开始练习</div>
        </div>
        <div class="action-item" @click="$router.push('/wrong-questions')">
          <div class="action-icon warning">
            <el-icon :size="32"><Warning /></el-icon>
          </div>
          <div class="action-label">错题本</div>
        </div>
        <div class="action-item" @click="$router.push('/leaderboard')">
          <div class="action-icon success">
            <el-icon :size="32"><TrendCharts /></el-icon>
          </div>
          <div class="action-label">排行榜</div>
        </div>
        <div class="action-item" @click="$router.push('/star-shop')">
          <div class="action-icon danger">
            <el-icon :size="32"><ShoppingBag /></el-icon>
          </div>
          <div class="action-label">星星商城</div>
        </div>
      </div>
    </el-card>

    <el-card class="children-selector-card" shadow="never">
      <template #header>
        <div class="card-header">
          <span>选择孩子</span>
          <el-button type="primary" link @click="$router.push('/children')">管理</el-button>
        </div>
      </template>
      <el-radio-group v-model="selectedChildId" @change="selectChild">
        <el-radio 
          v-for="child in childrenList" 
          :key="child.id" 
          :label="child.id"
          class="child-radio"
        >
          <div class="child-option">
            <el-avatar :size="32">{{ child.name.charAt(0) }}</el-avatar>
            <span>{{ child.name }}</span>
          </div>
        </el-radio>
      </el-radio-group>
      <el-empty v-if="childrenList.length === 0" description="还没有添加孩子" />
    </el-card>

    <el-dialog 
      v-model="showRewardDialog" 
      title="任务奖励" 
      width="300px"
      custom-class="reward-dialog"
    >
      <div class="reward-content">
        <el-icon color="#FFD700" :size="60"><StarFilled /></el-icon>
        <div class="reward-count">+{{ dailyTaskReward }}</div>
        <p>恭喜完成每日任务</p>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/auth'
import { getChildren } from '@/apis/children'
import { getWrongQuestionsStats } from '@/apis/wrongQuestions'
import { getStreakInfo } from '@/apis/streaks'
import { getDailyTaskStatus, claimDailyTaskReward as claimReward } from '@/apis/dailyTasks'
import { getStarBalance } from '@/apis/stars'
import { ElMessage } from 'element-plus'
import StreakFlame from '@/components/StreakFlame.vue'

const router = useRouter()
const userStore = useUserStore()

const childrenList = ref([])
const selectedChildId = ref(null)
const selectedChild = computed(() => {
  return childrenList.value.find(c => c.id === selectedChildId.value) || null
})

const todayStats = ref({
  practiceCount: 0,
  correctRate: 0
})
const todayStars = ref(0)
const totalStars = ref(0)
const difficulty = ref('medium')

const dailyTaskProgress = ref(0)
const dailyTaskCompleted = ref(false)
const dailyTaskRewardClaimed = ref(false)
const dailyTaskReward = ref(10)
const showRewardDialog = ref(false)

const streakInfo = ref({
  currentStreak: 0,
  shields: 0
})

const childAvatar = computed(() => {
  return selectedChild.value?.avatar || ''
})

const loadChildren = async () => {
  try {
    const response = await getChildren()
    childrenList.value = Array.isArray(response) ? response : (response.data || [])
    const lastSelectedChildId = localStorage.getItem('lastSelectedChildId')
    if (lastSelectedChildId && childrenList.value.find(c => c.id === parseInt(lastSelectedChildId))) {
      selectedChildId.value = parseInt(lastSelectedChildId)
    } else if (childrenList.value.length > 0) {
      selectedChildId.value = childrenList.value[0].id
    }
    
    const savedDifficulty = localStorage.getItem('practice_difficulty')
    if (savedDifficulty) {
      difficulty.value = savedDifficulty
    }
    
    if (selectedChildId.value) {
      loadChildData()
    }
  } catch (error) {
    console.error('加载孩子列表失败:', error)
  }
}

const loadChildData = async () => {
  try {
    const [wrongStatsRes, streakRes, taskRes, balanceRes] = await Promise.all([
      getWrongQuestionsStats(selectedChildId.value),
      getStreakInfo(selectedChildId.value),
      getDailyTaskStatus(selectedChildId.value),
      getStarBalance(selectedChildId.value)
    ])

    const wrongStats = wrongStatsRes.data || wrongStatsRes
    const streak = streakRes.data || streakRes
    const task = taskRes.data || taskRes
    const balance = balanceRes.data || balanceRes

    if (wrongStats) {
      todayStats.value = {
        practiceCount: wrongStats.todayWrongCount || 0,
        correctRate: wrongStats.overallAccuracy || 0
      }
      todayStars.value = wrongStats.todayStars || 0
    }

    if (streak) {
      streakInfo.value = streak
    }

    if (task) {
      dailyTaskProgress.value = task.todayCount || 0
      dailyTaskCompleted.value = task.completed || false
      dailyTaskRewardClaimed.value = task.rewardClaimed || false
    }

    if (balance) {
      totalStars.value = balance.balance || 0
    }
  } catch (error) {
    console.error('加载孩子数据失败:', error)
  }
}

const selectChild = (childId) => {
  localStorage.setItem('lastSelectedChildId', childId)
  loadChildData()
}

const saveDifficulty = () => {
  localStorage.setItem('practice_difficulty', difficulty.value)
}

const startPractice = () => {
  if (!selectedChildId.value) {
    ElMessage.warning('请先选择一个孩子')
    return
  }
  router.push({
    path: '/practice',
    query: { 
      childId: selectedChildId.value,
      difficulty: difficulty.value
    }
  })
}

const goToStatistics = () => {
  if (!selectedChildId.value) {
    ElMessage.warning('请先选择一个孩子')
    return
  }
  router.push({
    path: '/statistics',
    query: { childId: selectedChildId.value }
  })
}

const claimDailyTaskReward = async () => {
  try {
    const response = await claimReward(selectedChildId.value)
    if (response.code === 0) {
      dailyTaskReward.value = response.data.reward || 10
      dailyTaskRewardClaimed.value = true
      showRewardDialog.value = true
      ElMessage.success('奖励领取成功！')
      loadChildData()
    }
  } catch (error) {
    console.error('领取奖励失败:', error)
    ElMessage.error('领取奖励失败')
  }
}

onMounted(() => {
  if (!userStore.isLoggedIn) {
    router.push('/login')
    return
  }
  loadChildren()
})
</script>

<style scoped lang="scss">
.home-container {
  padding: 16px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
}

.welcome-card {
  border-radius: 16px;
  margin-bottom: 16px;
  
  .welcome-content {
    display: flex;
    align-items: center;
    gap: 16px;
    
    .avatar-section {
      flex-shrink: 0;
    }
    
    .info-section {
      flex: 1;
      
      h2 {
        margin: 0 0 8px 0;
        color: #333;
        font-size: 20px;
      }
      
      .subtitle {
        margin: 0;
        color: #666;
        font-size: 14px;
      }
    }
  }
}

.stats-card, .tasks-card, .streak-card, .quick-actions-card, .children-selector-card {
  border-radius: 16px;
  margin-bottom: 16px;
  
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  
  .stat-item {
    text-align: center;
    
    .stat-value {
      font-size: 24px;
      font-weight: bold;
      margin-bottom: 4px;
      
      &.success {
        color: #67c23a;
      }
      
      &.stars {
        color: #FFD700;
      }
      
      &.total-stars {
        color: #FF8C00;
      }
    }
    
    .stat-label {
      font-size: 11px;
      color: #666;
    }
  }
}

.task-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  
  .task-info {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 14px;
    
    .el-icon {
      color: #e6a23c;
    }
  }
  
  .task-done {
    color: #67c23a;
    font-size: 20px;
  }
}

.streak-info {
  display: flex;
  align-items: center;
  gap: 20px;
  flex-direction: row;
  
  .streak-flame {
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    
    .streak-count {
      position: absolute;
      bottom: -2px;
      font-size: 14px;
      font-weight: bold;
      color: #FF6B6B;
    }
    
    .streak-details {
      position: absolute;
      display: flex;
      align-items: center;
      justify-content: center;
      
      .streak-icon-text {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        
        .streak-count {
          position: static;
          font-size: 18px;
          font-weight: bold;
          color: #FF6B6B;
          margin-bottom: 2px;
        }
        
        .streak-label {
          font-size: 10px;
          color: #FF6B6B;
        }
      }
    }
  }
  
  .streak-text {
    flex: 1;
    
    .streak-label {
      font-size: 16px;
      font-weight: bold;
      color: #333;
      margin-bottom: 4px;
    }
    
    .streak-shields {
      display: flex;
      align-items: center;
      gap: 4px;
      font-size: 12px;
      color: #666;
      
      .el-icon {
        color: #409eff;
      }
    }
  }
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  
  .action-item {
    text-align: center;
    cursor: pointer;
    transition: transform 0.2s;
    
    &:active {
      transform: scale(0.95);
    }
    
    .action-icon {
      width: 56px;
      height: 56px;
      border-radius: 16px;
      display: flex;
      align-items: center;
      justify-content: center;
      margin: 0 auto 8px auto;
      
      &.primary {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
      }
      
      &.warning {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
      }
      
      &.success {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
      }
      
      &.danger {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        color: white;
      }
    }
    
    .action-label {
      font-size: 12px;
      color: #666;
    }
  }
}

.child-radio {
  width: 100%;
  margin-bottom: 12px;
  display: block;
  
  .el-radio__label {
    width: calc(100% - 28px);
  }
}

.child-option {
  display: flex;
  align-items: center;
  gap: 8px;
}

:deep(.reward-dialog) {
  .reward-content {
    text-align: center;
    padding: 20px 0;
    
    .reward-count {
      font-size: 36px;
      font-weight: bold;
      color: #FFD700;
      margin: 16px 0;
    }
    
    p {
      margin: 0;
      color: #666;
      font-size: 14px;
    }
  }
}

.default-avatar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

@media (max-width: 480px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
    
    .stat-value {
      font-size: 20px;
    }
  }
}
</style>
