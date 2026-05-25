<template>
  <div class="question-list">
    <el-card>
      <el-form :inline="true">
        <el-form-item label="类型">
          <el-select v-model="filters.type" clearable placeholder="请选择">
            <el-option label="加法" value="addition" />
            <el-option label="减法" value="subtraction" />
            <el-option label="乘法" value="multiplication" />
            <el-option label="除法" value="division" />
          </el-select>
        </el-form-item>
        <el-form-item label="年级">
          <el-select v-model="filters.grade" clearable placeholder="请选择">
            <el-option v-for="g in 6" :key="g" :label="`${g}年级`" :value="g" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="filters.status" clearable placeholder="请选择">
            <el-option label="启用" value="active" />
            <el-option label="禁用" value="disabled" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
        <el-form-item>
          <el-button type="success" @click="$router.push('/questions/new')">新建题目</el-button>
          <el-button @click="$router.push('/questions/import')">批量导入</el-button>
        </el-form-item>
      </el-form>

      <el-table :data="tableData" border v-loading="loading" @selection-change="handleSelectionChange">
        <el-table-column type="selection" width="55" />
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="type" label="类型" width="100">
          <template #default="{ row }">
            {{ { addition: '加法', subtraction: '减法', multiplication: '乘法', division: '除法' }[row.type] }}
          </template>
        </el-table-column>
        <el-table-column prop="grade" label="年级" width="80" />
        <el-table-column prop="a" label="数字A" width="100" />
        <el-table-column prop="b" label="数字B" width="100" />
        <el-table-column prop="answer" label="答案" width="100" />
        <el-table-column prop="difficulty" label="难度" width="100">
          <template #default="{ row }">
            <el-rate v-model="row.difficulty" disabled />
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 'active' ? 'success' : 'info'">
              {{ row.status === 'active' ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="createdAt" label="创建时间" width="180" />
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" @click="handleEdit(row)">编辑</el-button>
            <el-button link type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        v-model:current-page="pagination.page"
        v-model:page-size="pagination.pageSize"
        :total="pagination.total"
        :page-sizes="[20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        @current-change="fetchQuestions"
        @size-change="fetchQuestions"
        style="margin-top: 20px; justify-content: flex-end"
      />
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessageBox, ElMessage } from 'element-plus'
import { adminAPI } from '@/apis/admin'

const router = useRouter()
const loading = ref(false)
const tableData = ref([])
const filters = reactive({
  type: '',
  grade: null,
  status: ''
})
const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0
})
const selectedIds = ref([])

const fetchQuestions = async () => {
  loading.value = true
  try {
    const res = await adminAPI.getQuestions({
      ...filters,
      page: pagination.page,
      pageSize: pagination.pageSize
    })
    tableData.value = res.data.list
    pagination.total = res.data.total
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  pagination.page = 1
  fetchQuestions()
}

const handleReset = () => {
  filters.type = ''
  filters.grade = null
  filters.status = ''
  fetchQuestions()
}

const handleEdit = (row) => {
  router.push(`/questions/${row.id}`)
}

const handleDelete = async (row) => {
  await ElMessageBox.confirm('确定删除该题目吗？', '警告', { type: 'warning' })
  await adminAPI.deleteQuestion(row.id)
  ElMessage.success('删除成功')
  fetchQuestions()
}

const handleSelectionChange = (selection) => {
  selectedIds.value = selection.map(item => item.id)
}

onMounted(fetchQuestions)
</script>
