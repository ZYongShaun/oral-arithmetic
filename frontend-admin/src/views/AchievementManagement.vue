<template>
  <div class="achievement-management">
    <el-card>
      <template #header>
        <div style="display: flex; justify-content: space-between; align-items: center">
          <span>成就管理</span>
          <el-button type="primary" @click="handleAdd">添加成就</el-button>
        </div>
      </template>

      <el-table :data="tableData" border v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="成就名称" width="150" />
        <el-table-column prop="icon" label="图标" width="100">
          <template #default="{ row }">
            <el-icon v-if="row.icon" :size="30">{{ row.icon }}</el-icon>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column prop="type" label="类型" width="120">
          <template #default="{ row }">
            {{ { daily: '每日', weekly: '每周', lifetime: '终身' }[row.type] }}
          </template>
        </el-table-column>
        <el-table-column prop="description" label="描述" min-width="200" show-overflow-tooltip />
        <el-table-column prop="rewardStars" label="星星奖励" width="100" />
        <el-table-column prop="condition" label="达成条件" min-width="150" />
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
    </el-card>

    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="600px">
      <el-form :model="form" :rules="rules" ref="formRef" label-width="120px">
        <el-form-item label="成就名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入成就名称" />
        </el-form-item>
        <el-form-item label="类型" prop="type">
          <el-select v-model="form.type" placeholder="请选择类型">
            <el-option label="每日成就" value="daily" />
            <el-option label="每周成就" value="weekly" />
            <el-option label="终身成就" value="lifetime" />
          </el-select>
        </el-form-item>
        <el-form-item label="图标" prop="icon">
          <el-input v-model="form.icon" placeholder="请输入图标名" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="form.description" type="textarea" :rows="3" placeholder="请输入描述" />
        </el-form-item>
        <el-form-item label="星星奖励" prop="rewardStars">
          <el-input-number v-model="form.rewardStars" :min="0" />
        </el-form-item>
        <el-form-item label="达成条件" prop="condition">
          <el-input v-model="form.condition" type="textarea" :rows="3" placeholder="请输入达成条件" />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="form.status">
            <el-radio value="active">启用</el-radio>
            <el-radio value="disabled">禁用</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessageBox, ElMessage } from 'element-plus'
import { adminAPI } from '@/apis/admin'

const loading = ref(false)
const tableData = ref([])
const dialogVisible = ref(false)
const dialogTitle = computed(() => isEdit.value ? '编辑成就' : '添加成就')
const formRef = ref(null)
const isEdit = ref(false)
const editingId = ref(null)

const form = reactive({
  name: '',
  type: 'daily',
  icon: '',
  description: '',
  rewardStars: 0,
  condition: '',
  status: 'active'
})

const rules = {
  name: [{ required: true, message: '请输入成就名称', trigger: 'blur' }],
  type: [{ required: true, message: '请选择类型', trigger: 'change' }],
  description: [{ required: true, message: '请输入描述', trigger: 'blur' }],
  condition: [{ required: true, message: '请输入达成条件', trigger: 'blur' }]
}

const fetchAchievements = async () => {
  loading.value = true
  try {
    const res = await adminAPI.getStatistics('achievements')
    tableData.value = res.data.list || []
  } finally {
    loading.value = false
  }
}

const handleAdd = () => {
  isEdit.value = false
  Object.assign(form, { name: '', type: 'daily', icon: '', description: '', rewardStars: 0, condition: '', status: 'active' })
  dialogVisible.value = true
}

const handleEdit = (row) => {
  isEdit.value = true
  editingId.value = row.id
  Object.assign(form, row)
  dialogVisible.value = true
}

const handleDelete = async (row) => {
  await ElMessageBox.confirm('确定删除该成就吗？', '警告', { type: 'warning' })
  await adminAPI.updateConfig('achievements', { action: 'delete', id: row.id })
  ElMessage.success('删除成功')
  fetchAchievements()
}

const handleSubmit = async () => {
  await formRef.value.validate()
  const action = isEdit.value ? 'update' : 'create'
  const data = isEdit.value ? { ...form, id: editingId.value } : form
  await adminAPI.updateConfig('achievements', { action, data })
  ElMessage.success('保存成功')
  dialogVisible.value = false
  fetchAchievements()
}

onMounted(fetchAchievements)
</script>
