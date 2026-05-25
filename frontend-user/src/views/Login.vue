<template>
  <div class="login-page">
    <div class="login-container">
      <div class="logo-section">
        <h1>口算练习</h1>
        <p>让孩子爱上数学</p>
      </div>

      <!-- 最近使用用户列表 -->
      <div v-if="recentUsers.length > 0" class="recent-users-section">
        <p class="section-title">选择您的身份</p>
        <div class="recent-users-grid">
          <div
            v-for="user in recentUsers"
            :key="user.id"
            class="user-card"
            @click="selectUser(user)"
          >
            <div class="user-avatar">{{ user.username.charAt(0) }}</div>
            <div class="user-name">{{ user.username }}</div>
            <div class="user-stats">{{ user.total_questions }}道题</div>
          </div>
        </div>
      </div>

      <!-- 快速登录表单 -->
      <div class="new-user-section">
        <p class="section-title">或使用新用户</p>
        <el-form
          ref="formRef"
          :model="form"
          :rules="rules"
          label-width="0"
          class="login-form"
        >
          <el-form-item prop="username">
            <el-input
              v-model="form.username"
              placeholder="请输入您的姓名"
              size="large"
            >
              <template #prefix>
                <el-icon><User /></el-icon>
              </template>
            </el-input>
          </el-form-item>

          <el-form-item>
            <el-checkbox v-model="form.rememberMe">
              记住我的登录状态
            </el-checkbox>
          </el-form-item>

          <el-form-item>
            <el-button
              type="primary"
              size="large"
              class="login-button"
              :loading="loading"
              @click="handleQuickLogin"
            >
              开始答题
            </el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/auth'
import { authAPI } from '@/apis/auth'

const router = useRouter()
const userStore = useUserStore()

const formRef = ref(null)
const loading = ref(false)
const recentUsers = ref([])

const form = reactive({
  username: '',
  rememberMe: true  // 默认选中
})

const rules = {
  username: [
    { required: true, message: '请输入您的姓名', trigger: 'blur' },
    { min: 2, max: 20, message: '姓名长度2-20个字符', trigger: 'blur' },
    {
      pattern: /^[\u4e00-\u9fa5a-zA-Z0-9_]+$/,
      message: '只能输入中文、英文、数字和下划线',
      trigger: 'blur'
    }
  ]
}

// 组件挂载时加载最近使用用户
onMounted(async () => {
  await loadRecentUsers()
})

const loadRecentUsers = async () => {
  try {
    const recentUserIds = JSON.parse(
      localStorage.getItem('recent_user_ids') || '[]'
    )
    if (recentUserIds.length > 0) {
      const response = await authAPI.getRecentUsers({
        user_ids: recentUserIds.join(',')
      })
      recentUsers.value = response.recent_users || []
    }
  } catch (error) {
    console.error('加载最近用户失败:', error)
  }
}

const selectUser = async (user) => {
  loading.value = true
  try {
    const response = await authAPI.quickLogin({
      username: user.username
    })
    userStore.setToken(response.access_token)
    userStore.setUserInfo(response.user)
    updateUserRecentList(user.id)
    ElMessage.success('登录成功')
    router.push('/home')
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '登录失败')
  } finally {
    loading.value = false
  }
}

const handleQuickLogin = async () => {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return

  loading.value = true
  try {
    const response = await authAPI.quickLogin({
      username: form.username
    })
    userStore.setToken(response.access_token)
    userStore.setUserInfo(response.user)

    // 更新最近使用列表
    updateUserRecentList(response.user.id)

    ElMessage.success('登录成功')
    router.push('/home')
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '登录失败')
  } finally {
    loading.value = false
  }
}

const updateUserRecentList = (userId) => {
  let recentIds = JSON.parse(localStorage.getItem('recent_user_ids') || '[]')
  recentIds = recentIds.filter(id => id !== userId)
  recentIds.unshift(userId)
  recentIds = recentIds.slice(0, 5)  // 只保留最近5个
  localStorage.setItem('recent_user_ids', JSON.stringify(recentIds))
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.login-container {
  width: 100%;
  max-width: 400px;
  background: white;
  border-radius: 16px;
  padding: 40px 30px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
}

.logo-section {
  text-align: center;
  margin-bottom: 30px;
}

.logo-section h1 {
  font-size: 28px;
  color: #333;
  margin-bottom: 8px;
}

.logo-section p {
  font-size: 14px;
  color: #999;
}

.section-title {
  text-align: center;
  margin-bottom: 15px;
  color: #666;
  font-size: 14px;
}

.recent-users-section {
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px dashed #ddd;
}

.recent-users-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

.user-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 15px 10px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.user-card:hover {
  border-color: #667eea;
  background-color: #f5f7ff;
  transform: translateY(-2px);
}

.user-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 8px;
}

.user-name {
  font-size: 14px;
  color: #333;
  margin-bottom: 4px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 100%;
}

.user-stats {
  font-size: 12px;
  color: #999;
}

.new-user-section {
  margin-top: 10px;
}

.login-form {
  margin-top: 10px;
}

.login-button {
  width: 100%;
  margin-top: 10px;
}

.footer-links {
  text-align: center;
  margin-top: 20px;
}

.footer-links a {
  color: #667eea;
  text-decoration: none;
  font-size: 14px;
}
</style>
