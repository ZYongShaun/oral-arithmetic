<template>
  <div class="profile-container">
    <el-page-header @back="router.back()" class="page-header">
      <template #content>
        <span>个人中心</span>
      </template>
    </el-page-header>

    <el-card class="profile-card" shadow="never">
      <div class="profile-content">
        <div class="avatar-section">
          <el-avatar :size="80" :src="userProfile.avatar">
            {{ userProfile.name.charAt(0) }}
          </el-avatar>
        </div>
        <div class="info-section">
          <h2>{{ userProfile.name }}</h2>
          <p class="phone">{{ formatPhone(userProfile.phone) }}</p>
        </div>
      </div>
    </el-card>

    <el-card class="stats-card" shadow="never">
      <template #header>
        <span>使用统计</span>
      </template>
      
      <div class="stats-grid">
        <div class="stat-item">
          <div class="stat-icon primary">
            <el-icon><User /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.childrenCount || 0 }}</div>
            <div class="stat-label">孩子数</div>
          </div>
        </div>
        
        <div class="stat-item">
          <div class="stat-icon success">
            <el-icon><Document /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.totalPractices || 0 }}</div>
            <div class="stat-label">总练习次数</div>
          </div>
        </div>
        
        <div class="stat-item">
          <div class="stat-icon warning">
            <el-icon><StarFilled /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.totalStars || 0 }}</div>
            <div class="stat-label">累计星星</div>
          </div>
        </div>
      </div>
    </el-card>

    <el-card class="menu-card" shadow="never">
      <div class="menu-list">
        <div class="menu-item" @click="$router.push('/children')">
          <div class="menu-left">
            <el-icon class="menu-icon"><User /></el-icon>
            <span>孩子管理</span>
          </div>
          <el-icon class="menu-arrow"><ArrowRight /></el-icon>
        </div>
        
        <div class="menu-item" @click="showEditDialog = true">
          <div class="menu-left">
            <el-icon class="menu-icon"><Edit /></el-icon>
            <span>编辑资料</span>
          </div>
          <el-icon class="menu-arrow"><ArrowRight /></el-icon>
        </div>
        
        <div class="menu-item" @click="$router.push({ path: '/statistics', query: { childId: lastChildId } })">
          <div class="menu-left">
            <el-icon class="menu-icon"><TrendCharts /></el-icon>
            <span>学习统计</span>
          </div>
          <el-icon class="menu-arrow"><ArrowRight /></el-icon>
        </div>
        
        <div class="menu-item" @click="$router.push({ path: '/achievements', query: { childId: lastChildId } })">
          <div class="menu-left">
            <el-icon class="menu-icon"><Trophy /></el-icon>
            <span>成就系统</span>
          </div>
          <el-icon class="menu-arrow"><ArrowRight /></el-icon>
        </div>
      </div>
    </el-card>

    <el-card class="settings-card" shadow="never">
      <template #header>
        <span>设置</span>
      </template>
      
      <div class="menu-list">
        <div class="menu-item" @click="showAboutDialog = true">
          <div class="menu-left">
            <el-icon class="menu-icon"><InfoFilled /></el-icon>
            <span>关于我们</span>
          </div>
          <el-icon class="menu-arrow"><ArrowRight /></el-icon>
        </div>
        
        <div class="menu-item" @click="handleLogout">
          <div class="menu-left">
            <el-icon class="menu-icon danger"><SwitchButton /></el-icon>
            <span class="danger">退出登录</span>
          </div>
          <el-icon class="menu-arrow"><ArrowRight /></el-icon>
        </div>
      </div>
    </el-card>

    <el-dialog
      v-model="showEditDialog"
      title="编辑资料"
      width="90%"
      :close-on-click-modal="false"
    >
      <el-form
        ref="editFormRef"
        :model="editForm"
        :rules="editRules"
        label-width="80px"
      >
        <el-form-item label="姓名" prop="name">
          <el-input 
            v-model="editForm.name" 
            placeholder="请输入姓名"
            maxlength="20"
          />
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
            <img v-if="editForm.avatar" :src="editForm.avatar" class="avatar" />
            <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
          </el-upload>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="showEditDialog = false">取消</el-button>
        <el-button type="primary" :loading="editLoading" @click="updateProfile">
          保存
        </el-button>
      </template>
    </el-dialog>

    <el-dialog
      v-model="showAboutDialog"
      title="关于我们"
      width="90%"
    >
      <div class="about-content">
        <div class="about-logo">
          <el-icon color="#667eea" :size="60"><TrendCharts /></el-icon>
        </div>
        <h3>口算练习</h3>
        <p class="version">版本 1.0.0</p>
        <p class="description">
          专为小学生设计的口算练习应用，帮助孩子提高计算能力，培养数学兴趣。
        </p>
        <div class="features">
          <div class="feature-item">
            <el-icon><Document /></el-icon>
            <span>智能出题</span>
          </div>
          <div class="feature-item">
            <el-icon><TrendCharts /></el-icon>
            <span>学习统计</span>
          </div>
          <div class="feature-item">
            <el-icon><Trophy /></el-icon>
            <span>成就系统</span>
          </div>
          <div class="feature-item">
            <el-icon><StarFilled /></el-icon>
            <span>星星奖励</span>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getUserProfile, updateUserProfile } from '@/apis/auth'
import { useUserStore } from '@/stores/auth'

const router = useRouter()
const userStore = useUserStore()

const userProfile = ref({
  name: '',
  phone: '',
  avatar: ''
})

const stats = ref({
  childrenCount: 0,
  totalPractices: 0,
  totalStars: 0
})

const showEditDialog = ref(false)
const showAboutDialog = ref(false)
const editLoading = ref(false)
const editFormRef = ref(null)

const editForm = reactive({
  name: '',
  avatar: ''
})

const editRules = {
  name: [
    { required: true, message: '请输入姓名', trigger: 'blur' },
    { min: 1, max: 20, message: '姓名长度为1-20个字符', trigger: 'blur' }
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

const lastChildId = computed(() => {
  return localStorage.getItem('lastSelectedChildId') || ''
})

const formatPhone = (phone) => {
  if (!phone) return ''
  return phone.replace(/(\d{3})\d{4}(\d{4})/, '$1****$2')
}

const loadUserProfile = async () => {
  try {
    const response = await getUserProfile()
    if (response.data) {
      userProfile.value = {
        name: response.data.name || '',
        phone: response.data.phone || '',
        avatar: response.data.avatar || ''
      }
      
      Object.assign(editForm, {
        name: response.data.name || '',
        avatar: response.data.avatar || ''
      })
      
      stats.value = {
        childrenCount: response.data.children_count || 0,
        totalPractices: response.data.total_practices || 0,
        totalStars: response.data.total_stars || 0
      }
    }
  } catch (error) {
    console.error('加载用户资料失败:', error)
    ElMessage.error('加载用户资料失败')
  }
}

const updateProfile = async () => {
  if (!editFormRef.value) return
  
  try {
    await editFormRef.value.validate()
    
    editLoading.value = true
    const response = await updateUserProfile({
      name: editForm.name,
      avatar: editForm.avatar
    })
    
    if (response.code === 0) {
      ElMessage.success('更新成功')
      showEditDialog.value = false
      loadUserProfile()
    } else {
      ElMessage.error(response.message || '更新失败')
    }
  } catch (error) {
    if (error !== false) {
      console.error('更新失败:', error)
      ElMessage.error('更新失败')
    }
  } finally {
    editLoading.value = false
  }
}

const handleAvatarSuccess = (response) => {
  if (response.code === 0) {
    editForm.avatar = response.data.url
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

const handleLogout = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要退出登录吗？',
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    userStore.logout()
    router.push('/login')
    ElMessage.success('已退出登录')
  } catch (error) {
    if (error !== 'cancel') {
      console.error('退出登录失败:', error)
    }
  }
}

onMounted(() => {
  loadUserProfile()
})
</script>

<style scoped lang="scss">
.profile-container {
  min-height: 100vh;
  background: #f5f5f5;
  padding-bottom: 20px;
}

.page-header {
  background: white;
  padding: 16px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.profile-card {
  border-radius: 12px;
  margin: 16px;
  
  .profile-content {
    display: flex;
    align-items: center;
    gap: 20px;
    padding: 20px;
    
    .avatar-section {
      flex-shrink: 0;
    }
    
    .info-section {
      flex: 1;
      
      h2 {
        margin: 0 0 8px 0;
        color: #333;
        font-size: 20px;
      }
      
      .phone {
        margin: 0;
        color: #666;
        font-size: 14px;
      }
    }
  }
}

.stats-card, .menu-card, .settings-card {
  border-radius: 12px;
  margin: 16px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  
  .stat-item {
    text-align: center;
    padding: 16px 8px;
    
    .stat-icon {
      width: 50px;
      height: 50px;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      margin: 0 auto 12px auto;
      font-size: 24px;
      
      &.primary {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
      }
      
      &.success {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        color: white;
      }
      
      &.warning {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        color: white;
      }
    }
    
    .stat-info {
      .stat-value {
        font-size: 24px;
        font-weight: bold;
        color: #333;
        margin-bottom: 4px;
      }
      
      .stat-label {
        font-size: 12px;
        color: #999;
      }
    }
  }
}

.menu-list {
  .menu-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px;
    border-bottom: 1px solid #eee;
    cursor: pointer;
    transition: background 0.2s;
    
    &:hover {
      background: #f9f9f9;
    }
    
    &:last-child {
      border-bottom: none;
    }
    
    .menu-left {
      display: flex;
      align-items: center;
      gap: 12px;
      font-size: 16px;
      color: #333;
      
      .menu-icon {
        font-size: 20px;
        color: #667eea;
        
        &.danger {
          color: #f56c6c;
        }
      }
      
      .danger {
        color: #f56c6c;
      }
    }
    
    .menu-arrow {
      color: #ccc;
      font-size: 18px;
    }
  }
}

.avatar-uploader {
  :deep(.el-upload) {
    border: 1px dashed #d9d9d9;
    border-radius: 8px;
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
  border-radius: 8px;
  object-fit: cover;
  display: block;
}

.about-content {
  text-align: center;
  padding: 20px 0;
  
  .about-logo {
    margin-bottom: 16px;
  }
  
  h3 {
    margin: 0 0 8px 0;
    color: #333;
    font-size: 20px;
  }
  
  .version {
    margin: 0 0 16px 0;
    color: #999;
    font-size: 12px;
  }
  
  .description {
    margin: 0 0 24px 0;
    color: #666;
    font-size: 14px;
    line-height: 1.6;
  }
  
  .features {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
    
    .feature-item {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      padding: 12px;
      background: #f9f9f9;
      border-radius: 8px;
      font-size: 14px;
      color: #666;
      
      .el-icon {
        color: #667eea;
      }
    }
  }
}

:deep(.el-dialog__body) {
  padding: 20px;
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
    
    .stat-item {
      flex-direction: row;
      padding: 12px;
      background: #f9f9f9;
      border-radius: 8px;
      display: flex;
      align-items: center;
      text-align: left;
      
      .stat-icon {
        margin: 0 12px 0 0;
      }
      
      .stat-info {
        flex: 1;
      }
    }
  }
  
  .about-content .features {
    grid-template-columns: 1fr;
  }
}
</style>
