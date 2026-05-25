<template>
  <div class="achievements-container">
    <el-page-header @back="router.back()" class="page-header">
      <template #content>
        <span>成就系统</span>
      </template>
    </el-page-header>

    <el-card class="overview-card" shadow="never" v-loading="loading">
      <template #header>
        <span>成就概览</span>
      </template>
      
      <div class="overview-content">
        <div class="total-count">
          <div class="count-value">{{ unlockedCount }}/{{ totalCount }}</div>
          <div class="count-label">已解锁</div>
        </div>
        <div class="progress-bar">
          <div 
            class="progress-fill" 
            :style="{ width: unlockProgress + '%' }"
          ></div>
        </div>
        <div class="progress-text">{{ unlockProgress }}%</div>
      </div>
    </el-card>

    <el-tabs v-model="activeTab" class="achievement-tabs">
      <el-tab-pane label="全部成就" name="all">
        <div class="achievements-list" v-loading="listLoading">
           <div 
             v-for="achievement in allAchievements" 
             :key="achievement.id"
             class="achievement-item"
             :class="{ locked: !achievement.unlocked }"
           >
             <div class="achievement-icon">
               <el-icon :size="40">
                 <component :is="getAchievementIcon(achievement.type)" />
               </el-icon>
             </div>
             <div class="achievement-info">
               <div class="achievement-title">
                 {{ achievement.title }}
                 <el-tag 
                   v-if="achievement.unlocked" 
                   type="success" 
                   size="small"
                 >
                   已解锁
                 </el-tag>
                 <el-tag v-else type="info" size="small">未解锁</el-tag>
               </div>
               <div class="achievement-desc">{{ achievement.description }}</div>
               <div class="achievement-progress" v-if="!achievement.unlocked">
                 <el-progress
                   :percentage="getAchievementProgress(achievement)"
                   :format="() => `${achievement.current}/${achievement.target}`"
                   :stroke-width="8"
                 />
               </div>
               <div class="achievement-reward" v-if="achievement.stars > 0">
                 <el-icon><StarFilled /></el-icon>
                 <span>{{ achievement.stars }} 星星</span>
               </div>
               <div class="achievement-time" v-if="achievement.unlocked && achievement.unlockedAt">
                 <el-icon><Calendar /></el-icon>
                 {{ formatDate(achievement.unlockedAt) }}
               </div>
             </div>
           </div>
          
          <el-empty 
            v-if="!listLoading && allAchievements.length === 0" 
            description="暂无成就" 
          />
        </div>
      </el-tab-pane>

      <el-tab-pane label="已解锁" name="unlocked">
        <div class="achievements-list" v-loading="listLoading">
           <div 
             v-for="achievement in unlockedAchievements" 
             :key="achievement.id"
             class="achievement-item unlocked"
           >
             <div class="achievement-icon">
               <el-icon :size="40">
                 <component :is="getAchievementIcon(achievement.type)" />
               </el-icon>
             </div>
             <div class="achievement-info">
               <div class="achievement-title">
                 {{ achievement.title }}
                 <el-tag type="success" size="small">已解锁</el-tag>
               </div>
               <div class="achievement-desc">{{ achievement.description }}</div>
               <div class="achievement-time" v-if="achievement.unlockedAt">
                 <el-icon><Calendar /></el-icon>
                 {{ formatDate(achievement.unlockedAt) }}
               </div>
               <div class="achievement-reward" v-if="achievement.stars > 0">
                 <el-icon><StarFilled /></el-icon>
                 <span>{{ achievement.stars }} 星星</span>
               </div>
             </div>
           </div>
          
          <el-empty 
            v-if="!listLoading && unlockedAchievements.length === 0" 
            description="还没有解锁任何成就" 
          />
        </div>
      </el-tab-pane>

      <el-tab-pane label="未解锁" name="locked">
        <div class="achievements-list" v-loading="listLoading">
          <div 
            v-for="achievement in lockedAchievements" 
            :key="achievement.id"
            class="achievement-item locked"
          >
            <div class="achievement-icon">
              <el-icon :size="40">
                <component :is="getAchievementIcon(achievement.type)" />
              </el-icon>
            </div>
            <div class="achievement-info">
              <div class="achievement-title">
                {{ achievement.title }}
                <el-tag type="info" size="small">未解锁</el-tag>
              </div>
              <div class="achievement-desc">{{ achievement.description }}</div>
              <div class="achievement-progress">
                <el-progress
                  :percentage="getAchievementProgress(achievement)"
                  :format="() => `${achievement.current}/${achievement.target}`"
                  :stroke-width="8"
                />
              </div>
            </div>
          </div>
          
          <el-empty 
            v-if="!listLoading && lockedAchievements.length === 0" 
            description="所有成就都已解锁！" 
          />
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getAchievements } from '@/apis/achievements'

const route = useRoute()
const router = useRouter()

const loading = ref(false)
const listLoading = ref(false)
const childId = ref(null)
const activeTab = ref('all')

const achievements = ref([])

const totalCount = computed(() => achievements.value.length)
const unlockedCount = computed(() => achievements.value.filter(a => a.unlocked).length)
const unlockProgress = computed(() => {
  if (totalCount.value === 0) return 0
  return Math.round((unlockedCount.value / totalCount.value) * 100)
})

const allAchievements = computed(() => achievements.value)
const unlockedAchievements = computed(() => achievements.value.filter(a => a.unlocked))
const lockedAchievements = computed(() => achievements.value.filter(a => !a.unlocked))

const getAchievementIcon = (type) => {
  const icons = {
    'practice_count': 'Document',
    'accuracy': 'TrendCharts',
    'streak': 'Fire',
    'stars': 'StarFilled',
    'practice_time': 'Timer',
    'difficulty': 'Medal'
  }
  return icons[type] || 'Trophy'
}

const getAchievementProgress = (achievement) => {
  if (achievement.target === 0) return 0
  return Math.min(100, Math.round((achievement.current / achievement.target) * 100))
}

const getAchievementColor = (type) => {
  const colors = {
    'practice_count': '#667eea',
    'accuracy': '#764ba2',
    'streak': '#FF6B6B',
    'stars': '#FFD700',
    'practice_time': '#4facfe',
    'difficulty': '#00f2fe'
  }
  return colors[type] || '#999'
}

const formatDate = (timestamp) => {
  const date = new Date(timestamp)
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

const loadAchievements = async () => {
  listLoading.value = true
  try {
    const response = await getAchievements(childId.value)
    if (response.data || Array.isArray(response)) {
      const data = response.data || response
      achievements.value = data.map(item => ({
        id: item.id,
        title: item.title,
        description: item.description,
        type: item.type,
        unlocked: item.unlocked || false,
        current: item.current || 0,
        target: item.target || 0,
        stars: item.stars || 0,
        unlockedAt: item.unlocked_at
      }))
    }
  } catch (error) {
    console.error('加载成就列表失败:', error)
    ElMessage.error(error.response?.data?.message || '加载成就列表失败')
  } finally {
    listLoading.value = false
  }
}

onMounted(() => {
  childId.value = parseInt(route.query.childId) || parseInt(localStorage.getItem('lastSelectedChildId'))
  if (!childId.value) {
    ElMessage.error('缺少孩子ID')
    router.back()
    return
  }
  
  loadAchievements()
})
</script>

<style scoped lang="scss">
.achievements-container {
  min-height: 100vh;
  background: #f5f5f5;
  padding-bottom: 20px;
}

.page-header {
  background: white;
  padding: 16px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.overview-card {
  border-radius: 12px;
  margin: 16px;
  
  .overview-content {
    text-align: center;
    padding: 24px 0;
    
    .total-count {
      margin-bottom: 20px;
      
      .count-value {
        font-size: 48px;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
      }
      
      .count-label {
        font-size: 14px;
        color: #999;
        margin-top: 4px;
      }
    }
    
    .progress-bar {
      height: 12px;
      background: #e9ecef;
      border-radius: 6px;
      overflow: hidden;
      margin: 0 auto 12px auto;
      max-width: 300px;
      
      .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        transition: width 0.5s ease;
      }
    }
    
    .progress-text {
      font-size: 18px;
      font-weight: bold;
      color: #667eea;
    }
  }
}

.achievement-tabs {
  background: white;
  margin: 16px;
  border-radius: 12px;
  padding: 16px;
  
  :deep(.el-tabs__header) {
    margin-bottom: 20px;
  }
  
  :deep(.el-tabs__nav-wrap::after) {
    display: none;
  }
}

.achievements-list {
  .achievement-item {
    display: flex;
    gap: 16px;
    padding: 16px;
    background: white;
    border-radius: 12px;
    margin-bottom: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    transition: transform 0.2s, box-shadow 0.2s;
    
    &:active {
      transform: scale(0.98);
    }
    
    &.unlocked {
      background: linear-gradient(135deg, #f0f9ff 0%, #e6f7ff 100%);
      border: 2px solid #4facfe;
    }
    
    &.locked {
      opacity: 0.7;
      
      .achievement-icon {
        color: #ccc;
        background: #f5f5f5;
      }
    }
    
    .achievement-icon {
      width: 60px;
      height: 60px;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      flex-shrink: 0;
    }
    
    .achievement-info {
      flex: 1;
      
      .achievement-title {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 8px;
        margin-bottom: 8px;
        font-size: 16px;
        font-weight: bold;
        color: #333;
      }
      
      .achievement-desc {
        font-size: 14px;
        color: #666;
        margin-bottom: 12px;
        line-height: 1.5;
      }
      
      .achievement-progress {
        margin-bottom: 12px;
        
        :deep(.el-progress__text) {
          font-size: 12px;
        }
      }
      
      .achievement-reward {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        padding: 6px 12px;
        background: rgba(255, 215, 0, 0.1);
        border-radius: 16px;
        color: #f0ad4e;
        font-size: 14px;
        font-weight: bold;
      }
      
      .achievement-time {
        display: flex;
        align-items: center;
        gap: 4px;
        font-size: 12px;
        color: #999;
        margin-top: 8px;
        
        .el-icon {
          font-size: 14px;
        }
      }

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
}

@media (max-width: 768px) {
  .achievement-item {
    .achievement-icon {
      width: 50px;
      height: 50px;
      
      .el-icon {
        font-size: 24px !important;
      }
    }
    
    .achievement-info {
      .achievement-title {
        font-size: 14px;
      }
      
      .achievement-desc {
        font-size: 13px;
      }
    }
  }
}
</style>
