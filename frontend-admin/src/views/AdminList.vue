<template>
  <div class="admin-list">
    <el-card>
      <template #header>
        <div style="display: flex; justify-content: space-between; align-items: center">
          <span>管理员列表</span>
          <el-button type="primary" @click="handleAdd">添加管理员</el-button>
        </div>
      </template>

      <el-table :data="tableData" border v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="username" label="用户名" width="150" />
        <el-table-column prop="role" label="角色" width="120">
          <template #default="{ row }">
            {{ { admin: '管理员', super: '超级管理员', readonly: '只读' }[row.role] }}
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 'active' ? 'success' : 'info'">
              {{ row.status === 'active' ? '正常' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="lastLoginAt" label="最后登录" width="180" />
        <el-table-column prop="createdAt" label="创建时间" width="180" />
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" @click="handleEdit(row)" v-if="row.role !== 'super'">编辑</el-button>
            <el-button link type="danger" @click="handleDelete(row)" v-if="row.role !== 'super'">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="500px">
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="密码" prop="password" v-if="!isEdit">
          <el-input v-model="form.password" type="password" placeholder="请输入密码" show-password />
        </el-form-item>
        <el-form-item label="角色" prop="role">
          <el-select v-model="form.role" placeholder="请选择角色">
            <el-option label="管理员" value="admin" />
            <el-option label="只读" value="readonly" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="form.status">
            <el-radio value="active">正常</el-radio>
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
const dialogTitle = computed(() => isEdit.value ? '编辑管理员' : '添加管理员')
const formRef = ref(null)
const isEdit = ref(false)
const editingId = ref(null)

const form = reactive({
  username: '',
  password: '',
  role: 'admin',
  status: 'active'
})

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
  role: [{ required: true, message: '请选择角色', trigger: 'change' }]
}

const fetchAdmins = async () => {
  loading.value = true
  try {
    const res = await adminAPI.getAdmins()
    tableData.value = res.data
  } finally {
    loading.value = false
  }
}

const handleAdd = () => {
  isEdit.value = false
  Object.assign(form, { username: '', password: '', role: 'admin', status: 'active' })
  dialogVisible.value = true
}

const handleEdit = (row) => {
  isEdit.value = true
  editingId.value = row.id
  Object.assign(form, {
    username: row.username,
    role: row.role,
    status: row.status
  })
  dialogVisible.value = true
}

const handleDelete = async (row) => {
  await ElMessageBox.confirm('确定删除该管理员吗？', '警告', { type: 'warning' })
  await adminAPI.deleteAdmin(row.id)
  ElMessage.success('删除成功')
  fetchAdmins()
}

const handleSubmit = async () => {
  await formRef.value.validate()
  if (isEdit.value) {
    await adminAPI.updateAdmin(editingId.value, form)
  } else {
    await adminAPI.createAdmin(form)
  }
  ElMessage.success('保存成功')
  dialogVisible.value = false
  fetchAdmins()
}

onMounted(fetchAdmins)
</script>
