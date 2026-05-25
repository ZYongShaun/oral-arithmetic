<template>
  <div class="user-detail">
    <el-card>
      <template #header>
        <div style="display: flex; justify-content: space-between; align-items: center">
          <el-button link @click="$router.back()">返回</el-button>
          <span>用户详情</span>
        </div>
      </template>

      <el-descriptions :column="2" border v-if="userData">
        <el-descriptions-item label="用户ID">{{ userData.id }}</el-descriptions-item>
        <el-descriptions-item label="用户名">{{ userData.username }}</el-descriptions-item>
        <el-descriptions-item label="手机号">{{ userData.phone || '-' }}</el-descriptions-item>
        <el-descriptions-item label="邮箱">{{ userData.email || '-' }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="userData.status === 1 ? 'success' : 'info'">
            {{ userData.status === 1 ? '正常' : '禁用' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="注册时间">{{ formatDate(userData.created_at) }}</el-descriptions-item>
        <el-descriptions-item label="总答题数">{{ userData.total_questions }}</el-descriptions-item>
        <el-descriptions-item label="操作">
          <el-button
            :type="userData.status === 1 ? 'warning' : 'success'"
            size="small"
            @click="handleToggleStatus"
          >
            {{ userData.status === 1 ? '禁用用户' : '启用用户' }}
          </el-button>
        </el-descriptions-item>
      </el-descriptions>
    </el-card>

    <el-card style="margin-top: 20px">
      <template #header>
        <span>关联孩子档案列表</span>
      </template>
      <el-table :data="userData?.children || []" border>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="姓名" width="120" />
        <el-table-column prop="grade" label="年级" width="100" />
        <el-table-column prop="is_active" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.is_active === 1 ? 'success' : 'info'">
              {{ row.is_active === 1 ? '正常' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="total_questions" label="总答题数" width="120" />
      </el-table>
      <el-empty v-if="!userData?.children?.length" description="暂无孩子档案" />
    </el-card>

    <el-card style="margin-top: 20px">
      <template #header>
        <div style="display: flex; justify-content: space-between; align-items: center">
          <span>历史趋势</span>
          <el-select v-model="days" placeholder="选择天数" style="width: 120px" @change="fetchHistory">
            <el-option label="7天" :value="7" />
            <el-option label="30天" :value="30" />
            <el-option label="90天" :value="90" />
          </el-select>
        </div>
      </template>
      <div v-if="historySummary" style="margin-bottom: 16px; display: flex; gap: 24px">
        <div>总答题数: {{ historySummary.total_questions }}</div>
        <div>总练习次数: {{ historySummary.total_practices }}</div>
        <div>平均每日答题: {{ historySummary.avg_questions_per_day }}</div>
      </div>
      <HistoryTrendChart v-if="history.length" :history="history" />
      <el-empty v-else description="暂无历史数据" />
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getParentUserDetail, updateParentUserStatus, getUserHistory } from '@/apis/admin'
import HistoryTrendChart from '@/components/HistoryTrendChart.vue'

const route = useRoute()
const userData = ref(null)
const history = ref([])
const historySummary = ref(null)
const days = ref(30)
const loading = ref(false)

const fetchUserDetail = async () => {
  loading.value = true
  try {
    const res = await getParentUserDetail(route.params.id)
    userData.value = res.data
  } catch (error) {
    ElMessage.error('加载用户详情失败')
  } finally {
    loading.value = false
  }
}

const fetchHistory = async () => {
  try {
    const res = await getUserHistory(route.params.id, days.value)
    history.value = res.data.history
    historySummary.value = res.data.summary
  } catch (error) {
    ElMessage.error('加载历史数据失败')
  }
}

const handleToggleStatus = async () => {
  if (!userData.value) return
  const newStatus = userData.value.status === 1 ? 0 : 1
  try {
    await ElMessageBox.confirm(
      `确定要${newStatus === 1 ? '启用' : '禁用'}用户 "${userData.value.username}" 吗？`,
      '提示',
      { type: 'warning' }
    )
    await updateParentUserStatus(userData.value.id, { status: newStatus })
    ElMessage.success('状态已更新')
    userData.value.status = newStatus
  } catch {
    // 用户取消
  }
}

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleString()
}

onMounted(() => {
  fetchUserDetail()
  fetchHistory()
})
</script>

