<template>
  <div class="leaderboard-container">
    <el-page-header @back="router.back()" class="page-header">
      <template #content>
        <span>排行榜</span>
      </template>
    </el-page-header>

    <el-card class="ranking-card" shadow="never" v-if="myRanking">
      <div class="ranking-content">
        <div class="ranking-medal">
          <el-icon v-if="myRanking.rank === 1" color="#FFD700" :size="48"><Trophy /></el-icon>
          <div v-else class="rank-number large">{{ myRanking.rank }}</div>
        </div>
        <div class="ranking-info">
          <div class="ranking-name">我的排名</div>
          <div class="ranking-stars">
            <el-icon><StarFilled /></el-icon>
            <span>{{ myRanking.weeklyStars }} 星星</span>
          </div>
        </div>
      </div>
    </el-card>

    <el-card class="leaderboard-card" shadow="never" v-loading="loading">
      <template #header>
        <div class="card-header">
          <span>本周排行榜</span>
          <div class="header-actions">
            <el-tag type="primary" size="small">第{{ currentWeek }}周</el-tag>
            <el-select 
              v-model="timeRange" 
              size="small" 
              @change="loadLeaderboard"
              style="width: 100px; margin-left: 8px"
            >
              <el-option label="本周" value="week"></el-option>
              <el-option label="本月" value="month"></el-option>
              <el-option label="全部" value="all"></el-option>
            </el-select>
          </div>
        </div>
      </template>

      <div v-if="leaderboard.length > 0" class="leaderboard-list">
        <div 
          v-for="(item, index) in leaderboard" 
          :key="item.id"
          class="leaderboard-item"
          :class="{ 'top-three': index < 3, 'is-me': item.isMe }"
        >
          <div class="item-rank">
            <div v-if="index === 0" class="medal gold">
              <el-icon><Medal /></el-icon>
            </div>
            <div v-else-if="index === 1" class="medal silver">
              <el-icon><Medal /></el-icon>
            </div>
            <div v-else-if="index === 2" class="medal bronze">
              <el-icon><Medal /></el-icon>
            </div>
            <div v-else class="rank-number">{{ index + 1 }}</div>
          </div>
          
          <div class="item-avatar">
            <el-avatar :size="40" :src="item.avatar">
              {{ item.name.charAt(0) }}
            </el-avatar>
          </div>
          
          <div class="item-info">
            <div class="item-name">{{ item.name }}</div>
            <div class="item-grade">{{ item.grade }}年级</div>
          </div>
          
          <div class="item-stars">
            <el-icon color="#FFD700"><StarFilled /></el-icon>
            <span class="stars-value">{{ item.weeklyStars }}</span>
          </div>
        </div>
      </div>

      <el-empty v-else-if="!loading" description="暂无排行数据" />
    </el-card>

    <el-card class="group-info-card" shadow="never" v-if="groupInfo">
      <template #header>
        <div class="card-header">
          <span>分组信息</span>
          <el-button 
            v-if="promotionalStatus && promotionalStatus.can_switch_group" 
            type="primary" 
            link 
            size="small"
            @click="switchGroup"
          >
            切换分组
          </el-button>
        </div>
      </template>
      <template #header>
        <span>分组信息</span>
      </template>
      
      <div class="group-info-content">
        <div class="info-item">
          <div class="info-label">分组名称</div>
          <div class="info-value">{{ groupInfo.groupName }}</div>
        </div>
        <div class="info-item">
          <div class="info-label">分组人数</div>
          <div class="info-value">{{ groupInfo.memberCount }}人</div>
        </div>
        <div class="info-item">
          <div class="info-label">更新时间</div>
          <div class="info-value">{{ formatTime(groupInfo.updateTime) }}</div>
        </div>
        <div class="info-item" v-if="promotionalStatus">
          <div class="info-label">晋级状态</div>
          <div class="info-value">
            <el-tag v-if="promotionalStatus.promoted" type="success">已晋级</el-tag>
            <el-tag v-else-if="promotionalStatus.demoted" type="danger">已降级</el-tag>
            <el-tag v-else type="info">保持现状</el-tag>
          </div>
        </div>
        <div class="info-item">
          <div class="info-label">重置周期</div>
          <div class="info-value">每周一 00:00</div>
        </div>
      </div>
    </el-card>

    <el-card class="rules-card" shadow="never">
      <template #header>
        <span>排行榜规则</span>
      </template>
      
      <div class="rules-content">
        <div class="rule-item">
          <div class="rule-icon">
            <el-icon><Number /></el-icon>
          </div>
          <div class="rule-text">
            <div class="rule-title">分组排名</div>
            <div class="rule-desc">用户被随机分配到30人小组，在组内进行排名</div>
          </div>
        </div>
        
        <div class="rule-item">
          <div class="rule-icon">
            <el-icon><Timer /></el-icon>
          </div>
          <div class="rule-text">
            <div class="rule-title">周榜更新</div>
            <div class="rule-desc">排行榜每周一00:00自动重置</div>
          </div>
        </div>
        
        <div class="rule-item">
          <div class="rule-icon">
            <el-icon><StarFilled /></el-icon>
          </div>
          <div class="rule-text">
            <div class="rule-title">星星计算</div>
            <div class="rule-desc">根据本周练习获得的星星数量排行</div>
          </div>
        </div>
        
        <div class="rule-item">
          <div class="rule-icon">
            <el-icon><Trophy /></el-icon>
          </div>
          <div class="rule-text">
            <div class="rule-title">奖励机制</div>
            <div class="rule-desc">前3名将在排行榜永久留名显示</div>
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getLeaderboard } from '@/apis/leaderboards'

const route = useRoute()
const router = useRouter()

const loading = ref(false)
const childId = ref(null)
const leaderboard = ref([])
const myRanking = ref(null)
const groupInfo = ref(null)
const currentWeek = ref(new Date().getUTCWeekNumber())
const timeRange = ref('week')
const promotionalStatus = ref(null)

Date.prototype.getUTCWeekNumber = function () {
  const date = new Date(Date.UTC(this.getFullYear(), this.getMonth(), this.getDate()))
  const dayNum = date.getUTCDay() || 7
  date.setUTCDate(date.getUTCDate() + 4 - dayNum)
  const yearStart = new Date(Date.UTC(date.getUTCFullYear(), 0, 1))
  return Math.ceil((((date - yearStart) / 86400000) + 1) / 7)
}

const formatTime = (timestamp) => {
  if (!timestamp) return '-'
  const date = new Date(timestamp)
  const now = new Date()
  const diff = now - date
  
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
  const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60))
  
  if (days > 0) return `${days}天前`
  if (hours > 0) return `${hours}小时前`
  if (minutes > 0) return `${minutes}分钟前`
  return '刚刚'
}

const switchGroup = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要切换到新的分组吗？排行榜将重新计算',
      '确认切换',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    ElMessage.success('分组切换成功，将重新计算排行榜')
    loadLeaderboard()
  } catch (error) {
    if (error !== 'cancel' && error !== 'close') {
      console.error('切换分组失败:', error)
      ElMessage.error(error.response?.data?.message || '切换分组失败')
    }
  }
}

const loadLeaderboard = async () => {
  loading.value = true
  try {
    const response = await getLeaderboard(childId.value, { time_range: timeRange.value })
    
    if (response.data || response.leaderboard) {
      const data = response.data || response
      
      leaderboard.value = (data.leaderboard || []).map(item => ({
        id: item.id,
        name: item.name,
        grade: item.grade,
        avatar: item.avatar || '',
        weeklyStars: item.weekly_stars || item.weeklyStars || 0,
        isMe: item.is_me || item.isMe || false,
        promoted: item.promoted || false,
        demoted: item.demoted || false,
        rankChange: item.rank_change || 0
      }))
      
      if (data.my_ranking || data.myRanking) {
        const ranking = data.my_ranking || data.myRanking
        myRanking.value = {
          rank: ranking.rank || 0,
          weeklyStars: ranking.weekly_stars || ranking.weeklyStars || 0,
          promoted: ranking.promoted || false,
          demoted: ranking.demoted || false,
          rankChange: ranking.rank_change || 0
        }
      }
      
      promotionalStatus.value = data.promotional_status || null
      
      if (data.group_info || data.groupInfo) {
        const group = data.group_info || data.groupInfo
        groupInfo.value = {
          groupName: group.group_name || group.groupName || '未分组',
          memberCount: group.member_count || group.memberCount || 0,
          updateTime: group.update_time || group.updateTime,
          groupId: group.group_id || group.groupId
        }
      }
    }
  } catch (error) {
    console.error('加载排行榜失败:', error)
    ElMessage.error(error.response?.data?.message || '加载排行榜失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  childId.value = parseInt(route.query.childId) || parseInt(localStorage.getItem('lastSelectedChildId'))
  if (!childId.value) {
    ElMessage.error('缺少孩子ID')
    router.back()
    return
  }
  
  loadLeaderboard()
})
</script>

<style scoped lang="scss">
.leaderboard-container {
  min-height: 100vh;
  background: #f5f5f5;
  padding-bottom: 20px;
}

.page-header {
  background: white;
  padding: 16px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.ranking-card, .leaderboard-card, .group-info-card, .rules-card {
  border-radius: 12px;
  margin: 16px;
  
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  
  .header-actions {
    display: flex;
    align-items: center;
  }
}
}

.ranking-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  
  .ranking-content {
    display: flex;
    align-items: center;
    gap: 20px;
    padding: 20px;
    
    .ranking-medal {
      width: 80px;
      height: 80px;
      background: rgba(255, 255, 255, 0.2);
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      
      .rank-number {
        font-size: 36px;
        font-weight: bold;
        color: white;
        
        &.large {
          font-size: 40px;
        }
      }
    }
    
    .ranking-info {
      flex: 1;
      
      .ranking-name {
        font-size: 16px;
        opacity: 0.9;
        margin-bottom: 8px;
      }
      
      .ranking-stars {
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 24px;
        font-weight: bold;
        
        .el-icon {
          font-size: 28px;
        }
      }
    }
  }
}

.leaderboard-list {
  .leaderboard-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 16px;
    background: white;
    border-radius: 8px;
    margin-bottom: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    transition: transform 0.2s;
    
    &.top-three {
      background: linear-gradient(135deg, #fff9c4 0%, #ffecb3 100%);
      border: 2px solid #ffca28;
    }
    
    &.is-me {
      border: 2px solid #667eea;
      background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
    }
    
    .item-rank {
      width: 40px;
      text-align: center;
      flex-shrink: 0;
      
      .medal {
        .el-icon {
          font-size: 28px;
        }
        
        &.gold {
          color: #FFD700;
        }
        
        &.silver {
          color: #C0C0C0;
        }
        
        &.bronze {
          color: #CD7F32;
        }
      }
      
      .rank-number {
        font-size: 18px;
        font-weight: bold;
        color: #666;
      }
    }
    
    .item-avatar {
      flex-shrink: 0;
    }
    
    .item-info {
      flex: 1;
      
      .item-name {
        font-size: 16px;
        font-weight: bold;
        color: #333;
        margin-bottom: 4px;
      }
      
      .item-grade {
        font-size: 14px;
        color: #999;
      }
    }
    
    .item-stars {
      display: flex;
      align-items: center;
      gap: 4px;
      padding: 8px 16px;
      background: rgba(255, 215, 0, 0.1);
      border-radius: 20px;
      
      .el-icon {
        font-size: 20px;
      }
      
      .stars-value {
        font-size: 18px;
        font-weight: bold;
        color: #FFD700;
      }
    }
    
    .item-status {
      display: flex;
      align-items: center;
      gap: 4px;
      
      .el-tag {
        font-size: 10px;
        padding: 2px 6px;
      }
    }
  }
}

.group-info-content {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  
  .info-item {
    padding: 12px;
    background: #f9f9f9;
    border-radius: 8px;
    
    .info-label {
      font-size: 12px;
      color: #999;
      margin-bottom: 4px;
    }
    
    .info-value {
      font-size: 14px;
      font-weight: bold;
      color: #333;
    }
  }
}
  
  .info-item {
    padding: 12px;
    background: #f9f9f9;
    border-radius: 8px;
    
    .info-label {
      font-size: 12px;
      color: #999;
      margin-bottom: 4px;
    }
    
    .info-value {
      font-size: 14px;
      font-weight: bold;
      color: #333;
    }
  }
}

.rules-content {
  .rule-item {
    display: flex;
    gap: 12px;
    padding: 12px;
    border-bottom: 1px solid #eee;
    
    &:last-child {
      border-bottom: none;
    }
    
    .rule-icon {
      width: 40px;
      height: 40px;
      border-radius: 8px;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
      flex-shrink: 0;
    }
    
    .rule-text {
      flex: 1;
      
      .rule-title {
        font-size: 14px;
        font-weight: bold;
        color: #333;
        margin-bottom: 4px;
      }
      
      .rule-desc {
        font-size: 12px;
        color: #999;
        line-height: 1.5;
      }
    }
  }
}

@media (max-width: 768px) {
  .group-info-content {
    grid-template-columns: 1fr;
  }
}
</style>
