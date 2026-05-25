<template>
  <div class="children-container">
    <el-page-header @back="$router.back()" class="page-header">
      <template #content>
        <div class="header-content">
          <span>孩子管理</span>
          <el-button type="primary" size="small" @click="showAddDialog">
            <el-icon><Plus /></el-icon>
            添加
          </el-button>
        </div>
      </template>
    </el-page-header>

    <div class="children-list" v-loading="loading">
      <div 
        v-for="child in childrenList" 
        :key="child.id" 
        class="child-card"
      >
        <div class="child-info">
          <el-avatar :size="60" :src="child.avatar">
            {{ child.name.charAt(0) }}
          </el-avatar>
          <div class="child-details">
            <h3>{{ child.name }}</h3>
            <p>年级: {{ child.grade }}</p>
            <p>星星: {{ child.stars }}</p>
          </div>
        </div>
        <div class="child-actions">
          <el-button 
            type="primary" 
            link 
            @click="editChild(child)"
          >
            编辑
          </el-button>
          <el-button 
            type="danger" 
            link 
            @click="deleteChild(child)"
          >
            删除
          </el-button>
        </div>
      </div>

      <el-empty 
        v-if="!loading && childrenList.length === 0" 
        description="还没有添加孩子，点击右上角添加"
      />
    </div>

    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑孩子' : '添加孩子'"
      width="90%"
      :close-on-click-modal="false"
    >
      <el-form
        ref="childFormRef"
        :model="childForm"
        :rules="childRules"
        label-width="80px"
      >
        <el-form-item label="姓名" prop="name">
          <el-input 
            v-model="childForm.name" 
            placeholder="请输入孩子的姓名"
            maxlength="10"
          />
        </el-form-item>

        <el-form-item label="年级" prop="grade">
          <el-select 
            v-model="childForm.grade" 
            placeholder="请选择年级"
            style="width: 100%"
          >
            <el-option label="一年级" value="1" />
            <el-option label="二年级" value="2" />
            <el-option label="三年级" value="3" />
            <el-option label="四年级" value="4" />
            <el-option label="五年级" value="5" />
            <el-option label="六年级" value="6" />
          </el-select>
        </el-form-item>

        <el-form-item label="头像" prop="avatar">
          <el-upload
            class="avatar-uploader"
            :show-file-list="false"
            :on-success="handleAvatarSuccess"
            :before-upload="beforeAvatarUpload"
            :action="uploadUrl"
            :headers="uploadHeaders"
          >
            <img v-if="childForm.avatar" :src="childForm.avatar" class="avatar" />
            <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
          </el-upload>
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitForm" :loading="submitLoading">
          确定
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getChildren, createChild, updateChild, deleteChild as deleteChildApi } from '@/apis/children'

const loading = ref(false)
const childrenList = ref([])
const dialogVisible = ref(false)
const submitLoading = ref(false)
const isEdit = ref(false)
const childFormRef = ref(null)

const childForm = reactive({
  id: null,
  name: '',
  grade: '1',
  avatar: ''
})

const childRules = {
  name: [
    { required: true, message: '请输入孩子的姓名', trigger: 'blur' },
    { min: 1, max: 10, message: '姓名长度为1-10个字符', trigger: 'blur' }
  ],
  grade: [
    { required: true, message: '请选择年级', trigger: 'change' }
  ]
}

const uploadUrl = computed(() => {
  return `${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'}/upload`
})

const uploadHeaders = computed(() => {
  const token = localStorage.getItem('token')
  return {
    'Authorization': `Bearer ${token}`
  }
})

const loadChildren = async () => {
  loading.value = true
  try {
    const response = await getChildren()
    childrenList.value = response
  } catch (error) {
    console.error('加载孩子列表失败:', error)
    ElMessage.error('加载孩子列表失败')
  } finally {
    loading.value = false
  }
}

const showAddDialog = () => {
  isEdit.value = false
  Object.assign(childForm, {
    id: null,
    name: '',
    grade: '1',
    avatar: ''
  })
  dialogVisible.value = true
}

const editChild = (child) => {
  isEdit.value = true
  Object.assign(childForm, {
    id: child.id,
    name: child.name,
    grade: child.grade,
    avatar: child.avatar || ''
  })
  dialogVisible.value = true
}

const deleteChild = async (child) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除"${child.name}"吗？`,
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    await deleteChildApi(child.id)
    ElMessage.success('删除成功')
    loadChildren()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败:', error)
      ElMessage.error('删除失败')
    }
  }
}

const submitForm = async () => {
  if (!childFormRef.value) return

  try {
    await childFormRef.value.validate()

    submitLoading.value = true
    const data = {
      name: childForm.name,
      grade: childForm.grade,
      avatar: childForm.avatar
    }

    if (isEdit.value) {
      await updateChild(childForm.id, data)
      ElMessage.success('更新成功')
    } else {
      await createChild(data)
      ElMessage.success('添加成功')
    }

    dialogVisible.value = false
    loadChildren()
  } catch (error) {
    if (error !== false) {
      console.error('提交失败:', error)
      ElMessage.error('提交失败')
    }
  } finally {
    submitLoading.value = false
  }
}

const handleAvatarSuccess = (response) => {
  if (response.code === 0) {
    childForm.avatar = response.data.url
    ElMessage.success('头像上传成功')
  } else {
    ElMessage.error(response.message || '头像上传失败')
  }
}

const beforeAvatarUpload = (file) => {
  const isJPG = file.type === 'image/jpeg' || file.type === 'image/png'
  const isLt2M = file.size / 1024 / 1024 < 2

  if (!isJPG) {
    ElMessage.error('头像图片只能是 JPG 或 PNG 格式!')
  }
  if (!isLt2M) {
    ElMessage.error('头像图片大小不能超过 2MB!')
  }
  return isJPG && isLt2M
}

loadChildren()
</script>

<style scoped lang="scss">
.children-container {
  min-height: 100vh;
  background: #f5f5f5;
  padding-bottom: 20px;
}

.page-header {
  background: white;
  padding: 16px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.header-content {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 18px;
  font-weight: bold;
}

.children-list {
  padding: 16px;
}

.child-card {
  background: white;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  
  .child-info {
    display: flex;
    gap: 16px;
    margin-bottom: 12px;
    
    .child-details {
      flex: 1;
      
      h3 {
        margin: 0 0 8px 0;
        font-size: 18px;
        color: #333;
      }
      
      p {
        margin: 4px 0;
        color: #666;
        font-size: 14px;
      }
    }
  }
  
  .child-actions {
    display: flex;
    justify-content: flex-end;
    gap: 8px;
    border-top: 1px solid #eee;
    padding-top: 12px;
  }
}

.avatar-uploader {
  :deep(.el-upload) {
    border: 1px dashed #d9d9d9;
    border-radius: 50%;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s;
    
    &:hover {
      border-color: #409eff;
    }
  }
}

.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 100px;
  height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
  display: block;
}

:deep(.el-dialog__body) {
  padding: 20px;
}
</style>
