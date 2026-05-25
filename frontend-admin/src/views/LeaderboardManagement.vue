<template>
  <div class="leaderboard-management">
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card shadow="hover">
          <el-statistic title="活跃星星榜" :value="leaderboardStats.starCount">
            <template #suffix>人</template>
          </el-statistic>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <el-statistic title="答题榜" :value="leaderboardStats.questionCount">
            <template #suffix>人</template>
          </el-statistic>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <el-statistic title="连胜榜" :value="leaderboardStats.streakCount">
            <template #suffix>人</template>
          </el-statistic>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <el-statistic title="今日练习" :value="leaderboardStats.todayCount">
            <template #suffix>人</template>
          </el-statistic>
        </el-card>
      </el-col>
    </el-row>

    <el-card style="margin-top: 20px">
      <template #header>
        <el-tabs v-model="activeTab" @tab-change="handleTabChange">
          <el-tab-pane label="星星榜" name="stars" />
          <el-tab-pane label="答题榜" name="questions" />
          <el-tab-pane label="连胜榜" name="streaks" />
          <el-tab-pane label="今日榜" name="today" />
        </el-tabs>
      </template>

      <el-table :data="tableData" border v-loading="loading">
        <el-table-column prop="rank" label="排名" width="80">
          <template #default="{ row }">
            <el-tag v-if="row.rank === 1" type="danger" effect="dark">NO.1</el-tag>
            <el-tag v-else-if="row.rank === 2" type="warning" effect="dark">NO.2</el-tag>
            <el-tag v-else-if="row.rank === 3" type="success" effect="dark">NO.3</el-tag>
            <span v-else>{{ row.rank }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="avatar" label="头像" width="80">
          <template #default="{ row }">
            <el-avatar :size="50" :src="row.avatar">{{ row.name?.[0] }}</el-avatar>
          </template>
        </el-table-column>
        <el-table-column prop="name" label="姓名" width="120" />
        <el-table-column prop="grade" label="年级" width="80" />
        <el-table-column prop="score" label="分数" width="100" v-if="activeTab === 'stars'">
          <template #default="{ row }">{{ row.score }} ⭐</template>
        </el-table-column>
        <el-table-column prop="score" label="题目数" width="100" v-if="activeTab === 'questions'" />
        <el-table-column prop="score" label="连胜次数" width="100" v-if="activeTab === 'streaks'" />
        <el-table-column prop="score" label="今日练习" width="100" v-if="activeTab === 'today'" />
        <el-table-column prop="parentPhone" label="家长手机号" width="130" />
        <el-table-column prop="updatedAt" label="更新时间" width="180" />
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" @click="handleViewDetail(row)">详情</el-button>
            <el-button link type="warning" @click="handleRefresh">刷新</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        v-model:current-page="pagination.page"
        v-model:page-size="pagination.pageSize"
        :total="pagination.total"
        :page-sizes="[20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        @current-change="fetchLeaderboard"
        @size-change="fetchLeaderboard"
        style="margin-top: 20px; justify-content: flex-end"
      />
    </el-card>

    <el-dialog v-model="detailVisible" title="排行榜详情" width="800px">
      <el-descriptions :column="2" border v-if="currentData">
        <el-descriptions-item label="排名">{{ currentData.rank }}</el-descriptions-item>
        <el-descriptions-item label="姓名">{{ currentData.name }}</el-descriptions-item>
        <el-descriptions-item label="年级">{{ currentData.grade }}年级</el-descriptions-item>
        <el-descriptions-item label="分数">{{ currentData.score }}</el-descriptions-item>
        <el-descriptions-item label="家长手机号">{{ currentData.parentPhone }}</el-descriptions-item>
        <el-descriptions-item label="更新时间">{{ currentData.updatedAt }}</el-descriptions-item>
        <el-descriptions-item label="头像">
          <el-avatar :size="60" :src="currentData.avatar">{{ currentData.name?.[0] }}</el-avatar>
        </el-descriptions-item>
      </el-descriptions>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { adminAPI } from '@/apis/admin'

const activeTab = ref('stars')
const loading = ref(false)
const tableData = ref([])
const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0
})
const leaderboardStats = ref({
  starCount: 0,
  questionCount: 0,
  streakCount: 0,
  todayCount: 0
})
const detailVisible = ref(false)
const currentData = ref(null)

const fetchLeaderboard = async () => {
  loading.value = true
  try {
    const res = await adminAPI.getStatistics('leaderboard', {
      type: activeTab.value,
      page: pagination.page,
      pageSize: pagination.pageSize
    })
    tableData.value = res.data.list
    pagination.total = res.data.total
  } finally {
    loading.value = false
  }
}

const fetchStats = async () => {
  const res = await adminAPI.getStatistics('leaderboard-stats')
  leaderboardStats.value = res.data
}

const handleTabChange = () => {
  pagination.page = 1
  fetchLeaderboard()
}

const handleViewDetail = (row) => {
  currentData.value = row
  detailVisible.value = true
}

const handleRefresh = async () => {
  await fetchLeaderboard()
  ElMessage.success('刷新成功')
}

onMounted(async () => {
  await fetchLeaderboard()
  await fetchStats()
})
</script>
