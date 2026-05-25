<template>
  <div class="dashboard">
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card shadow="hover">
          <el-statistic title="活跃用户" :value="stats.active_users">
            <template #suffix>人</template>
          </el-statistic>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <el-statistic title="答题总数" :value="stats.total_questions">
            <template #suffix>题</template>
          </el-statistic>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <el-statistic title="总用时" :value="stats.total_time_minutes">
            <template #suffix>分钟</template>
          </el-statistic>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <el-statistic title="今日前5名" :value="stats.top_users.length">
            <template #suffix>位</template>
          </el-statistic>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>今日前5名用户</span>
          </template>
          <el-table :data="stats.top_users" border>
            <el-table-column prop="username" label="姓名" />
            <el-table-column prop="question_count" label="答题数" />
            <el-table-column prop="time_minutes" label="用时（分钟）" />
          </el-table>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>快捷入口</span>
          </template>
          <div class="quick-links">
            <el-button type="primary" @click="$router.push('/users')">用户管理</el-button>
            <el-button type="success" @click="$router.push('/children')">孩子管理</el-button>
            <el-button type="warning" @click="$router.push('/statistics')">数据统计</el-button>
            <el-button type="info" @click="$router.push('/questions')">题目管理</el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getTodayStats } from '@/apis/statistics'

const stats = ref({
  active_users: 0,
  total_questions: 0,
  total_time_minutes: 0,
  top_users: []
})

onMounted(async () => {
  try {
    const res = await getTodayStats()
    stats.value = res.data
  } catch (error) {
    console.error('加载今日统计失败:', error)
  }
})
</script>

<style scoped>
.dashboard .quick-links {
  display: flex;
  gap: 12px;
}
</style>
