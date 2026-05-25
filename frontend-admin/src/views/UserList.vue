<template>
  <div class="user-list">
    <el-card>
      <div style="margin-bottom: 16px; display: flex; gap: 12px; align-items: center">
        <SearchBar v-model="search" @search="onSearch" />
        <el-select v-model="statusFilter" placeholder="状态" clearable style="width: 120px" @change="onFilterChange">
          <el-option label="全部" value="all" />
          <el-option label="正常" value="1" />
          <el-option label="禁用" value="0" />
        </el-select>
        <el-select v-model="sortBy" placeholder="排序" style="width: 120px" @change="onSortChange">
          <el-option label="注册时间" value="created_at" />
          <el-option label="用户名" value="username" />
          <el-option label="答题数" value="question_count" />
        </el-select>
        <el-select v-model="sortOrder" placeholder="方向" style="width: 80px" @change="onSortChange">
          <el-option label="降序" value="desc" />
          <el-option label="升序" value="asc" />
        </el-select>
        <el-button type="primary" @click="fetchUsers">刷新</el-button>
        <el-button @click="handleExport">导出</el-button>
      </div>

      <UserTable
        :table-data="tableData"
        :loading="loading"
        @view="onViewUser"
        @toggle-status="onToggleStatus"
      />

      <Pagination
        v-model:modelValue="pagination"
        :total="total"
        @change="fetchUsers"
      />
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getParentUsers, updateParentUserStatus, exportParentUsers } from '@/apis/admin'
import SearchBar from '@/components/SearchBar.vue'
import UserTable from '@/components/UserTable.vue'
import Pagination from '@/components/Pagination.vue'

const router = useRouter()
const search = ref('')
const statusFilter = ref('all')
const sortBy = ref('created_at')
const sortOrder = ref('desc')
const loading = ref(false)
const tableData = ref([])
const total = ref(0)
const pagination = reactive({
  page: 1,
  pageSize: 20
})

const fetchUsers = async () => {
  loading.value = true
  try {
    const res = await getParentUsers({
      page: pagination.page,
      page_size: pagination.pageSize,
      search: search.value || undefined,
      status: statusFilter.value,
      sort_by: sortBy.value,
      order: sortOrder.value
    })
    tableData.value = res.data.users
    total.value = res.data.total
  } catch (error) {
    ElMessage.error('加载用户列表失败')
  } finally {
    loading.value = false
  }
}

const onSearch = () => {
  pagination.page = 1
  fetchUsers()
}

const onFilterChange = () => {
  pagination.page = 1
  fetchUsers()
}

const onSortChange = () => {
  pagination.page = 1
  fetchUsers()
}

const onViewUser = (row) => {
  router.push(`/users/${row.id}`)
}

const onToggleStatus = async (row) => {
  const newStatus = row.status === 1 ? 0 : 1
  try {
    await ElMessageBox.confirm(
      `确定要${newStatus === 1 ? '启用' : '禁用'}用户 "${row.username}" 吗？`,
      '提示',
      { type: 'warning' }
    )
    await updateParentUserStatus(row.id, { status: newStatus })
    ElMessage.success('状态已更新')
    fetchUsers()
  } catch {
    // 用户取消
  }
}

const handleExport = async () => {
  try {
    const res = await exportParentUsers()
    const url = URL.createObjectURL(new Blob([res]))
    const link = document.createElement('a')
    link.href = url
    link.download = `users_export_${new Date().toISOString().split('T')[0]}.csv`
    link.click()
    ElMessage.success('导出成功')
  } catch (error) {
    ElMessage.error('导出失败')
  }
}

onMounted(fetchUsers)
</script>
