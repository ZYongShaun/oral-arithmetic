<template>
  <div class="statistics">
    <el-card>
      <template #header>
        <div style="display: flex; justify-content: space-between; align-items: center">
          <span>排行榜</span>
          <div style="display: flex; gap: 12px; align-items: center">
            <PeriodSelector v-model="period" />
            <el-button @click="handleExport">导出 CSV</el-button>
          </div>
        </div>
      </template>

      <el-table :data="leaderboardData" border v-loading="loading">
        <el-table-column prop="rank" label="排名" width="80">
          <template #default="{ row }">
            <span v-if="row.icon">{{ row.icon }}</span>
            <span v-else>{{ row.rank }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="username" label="用户名" />
        <el-table-column prop="question_count" label="答题数" width="120" />
        <el-table-column prop="score" label="得分" width="120" />
      </el-table>

      <Pagination
        v-model:modelValue="pagination"
        :total="total"
        @change="fetchLeaderboard"
      />
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getLeaderboard, exportLeaderboard } from '@/apis/statistics'
import PeriodSelector from '@/components/PeriodSelector.vue'
import Pagination from '@/components/Pagination.vue'

const period = ref('weekly')
const leaderboardData = ref([])
const loading = ref(false)
const total = ref(0)
const pagination = reactive({
  page: 1,
  pageSize: 20
})

const fetchLeaderboard = async () => {
  loading.value = true
  try {
    const res = await getLeaderboard({
      period: period.value,
      page: pagination.page,
      page_size: pagination.pageSize
    })
    leaderboardData.value = res.data.leaderboard
    total.value = res.data.total
  } catch (error) {
    ElMessage.error('加载排行榜失败')
  } finally {
    loading.value = false
  }
}

const handleExport = async () => {
  try {
    const res = await exportLeaderboard(period.value)
    const url = URL.createObjectURL(new Blob([res]))
    const link = document.createElement('a')
    link.href = url
    link.download = `leaderboard_${period.value}_${new Date().toISOString().split('T')[0]}.csv`
    link.click()
    ElMessage.success('导出成功')
  } catch (error) {
    ElMessage.error('导出失败')
  }
}

onMounted(() => {
  fetchLeaderboard()
})
</script>

