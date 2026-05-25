<template>
  <el-table :data="tableData" border v-loading="loading">
    <el-table-column prop="id" label="ID" width="80" />
    <el-table-column prop="username" label="用户名" width="120" />
    <el-table-column prop="phone" label="手机号" width="130" />
    <el-table-column prop="email" label="邮箱" min-width="180" />
    <el-table-column prop="status" label="状态" width="100">
      <template #default="{ row }">
        <el-tag :type="row.status === 1 ? 'success' : 'info'">
          {{ row.status === 1 ? '正常' : '禁用' }}
        </el-tag>
      </template>
    </el-table-column>
    <el-table-column prop="created_at" label="注册时间" width="180" />
    <el-table-column prop="total_questions" label="总答题数" width="120" />
    <el-table-column label="操作" width="180" fixed="right">
      <template #default="{ row }">
        <el-button link type="primary" @click="onView(row)">查看详情</el-button>
        <el-button link type="warning" @click="onToggleStatus(row)">
          {{ row.status === 1 ? '禁用' : '启用' }}
        </el-button>
      </template>
    </el-table-column>
  </el-table>
</template>

<script setup>
defineProps({
  tableData: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['view', 'toggle-status'])

const onView = (row) => {
  emit('view', row)
}

const onToggleStatus = (row) => {
  emit('toggle-status', row)
}
</script>
