# Design: 简化家庭局域网的认证系统

## 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                        认证系统架构                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   ┌────────────┐                                            │
│   │  前端用户端   │                                            │
│   │            │                                            │
│   │  Login.vue │                                            │
│   └──────┬─────┘                                            │
│          │                                                   │
│          │ POST /api/v1/auth/quick-login                     │
│          │ {username: "小明"}                                │
│          ▼                                                   │
│   ┌───────────────────────────────────────────────┐          │
│   │  FastAPI 后端                                 │          │
│   │                                               │          │
│   │  ┌─────────────────────────────────────┐    │          │
│   │  │  auth.py                             │    │          │
│   │  │  - quick_login()                   │    │          │
│   │  │  - get_recent_users()               │    │          │
│   │  │                                     │    │          │
│   │  │  逻辑：                             │    │          │
│   │  │  1. 查询用户是否存在                │    │          │
│   │  │  2. 如果不存在 → 创建新用户          │    │          │
│   │  │  3. 生成长期JWT（2年）              │    │          │
│   │  │  4. 返回token + 用户信息            │    │          │
│   │  └─────────────────────────────────────┘    │          │
│   │                                               │          │
│   │  ┌─────────────────────────────────────┐    │          │
│   │  │  auth_service.py                    │    │          │
│   │  │  - create_or_get_user()             │    │          │
│   │  │  - create_access_token()           │    │          │
│   │  └─────────────────────────────────────┘    │          │
│   │                                               │          │
│   └───────────────────┬───────────────────────────┘          │
│                       │                                          │
│                       │                                          │
│   ┌───────────────────▼───────────────────────────┐          │
│   │  MySQL 数据库                                 │          │
│   │                                               │          │
│   │  ┌─────────────────────────────────────┐    │          │
│   │  │  users                               │    │          │
│   │  │  - id, username, phone, email...     │    │          │
│   │  │  - password_hash (nullable) ✅       │    │          │
│   │  │                                     │    │          │
│   │  │  索引:                               │    │          │
│   │  │  - username (UNIQUE) ✅             │    │          │
│   │  └─────────────────────────────────────┘    │          │
│   │                                               │          │
│   └───────────────────────────────────────────────┘          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## API 设计

### 1. 快速登录接口

**端点**：`POST /api/v1/auth/quick-login`

**请求**：
```json
{
  "username": "小明"
}
```

**响应**：
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 123,
    "username": "小明",
    "total_questions": 99,
    "created_at": "2024-01-15T10:30:00"
  }
}
```

**逻辑流程**：
```
1. 接收 username
2. 查询数据库：SELECT * FROM users WHERE username = ?
3. 如果用户不存在：
   a. 创建新用户：INSERT INTO users (username, status) VALUES (?, 1)
   b. 可选：创建默认孩子档案
4. 生成 JWT token（有效期：2年）
   exp = now() + 2 years
5. 返回 token + 用户信息
```

**错误响应**：
```json
// 用户名已存在但被禁用
{
  "detail": "User account is disabled"
}
```

---

### 2. 获取最近使用用户

**端点**：`GET /api/v1/users/recent`

**请求**：
```
Authorization: Bearer {token}
```

**响应**：
```json
{
  "recent_users": [
    {
      "id": 123,
      "username": "小明",
      "total_questions": 99
    },
    {
      "id": 124,
      "username": "小红",
      "total_questions": 35
    }
  ]
}
```

**说明**：
- 从前端的 localStorage 读取已登录用户的 ID 列表
- 后端批量查询用户信息
- 用于在登录页显示"最近使用用户"选项

---

### 3. 传统登录接口（保留）

**端点**：`POST /api/v1/auth/login`

**请求**：
```
username=小明&password=123456
```

**说明**：
- 保持向后兼容
- 如果用户有密码，验证密码
- 如果用户没有密码，返回 400 错误

---

## 数据库设计

### users 表调整

```sql
-- 现有列（保持不变）
id INT PRIMARY KEY AUTO_INCREMENT
username VARCHAR(50) UNIQUE NOT NULL
phone VARCHAR(20) UNIQUE NULL
email VARCHAR(100) UNIQUE NULL
nickname VARCHAR(50) NULL
password_hash VARCHAR(255) NULL  -- 改为 NULLABLE ✅
status INT DEFAULT 1  -- 1-正常 0-禁用
created_at DATETIME
updated_at DATETIME

-- 添加索引（如果还没有）
CREATE INDEX idx_username ON users(username);  -- 需要确保存在
```

### 向后兼容数据库迁移

```sql
-- 将现有的 password_hash 改为 NULLABLE（如果之前是 NOT NULL）
ALTER TABLE users MODIFY COLUMN password_hash VARCHAR(255) NULL;
```

---

## 配置调整

### JWT 过期时间

```python
# backend/app/core/config.py
class Settings(BaseSettings):
    # JWT 配置
    JWT_SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 525600  # 2年 = 365 * 24 * 60
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 525600  # 2年
```

---

## 前端设计

### 登录页面改造

**文件**：`frontend-user/src/views/Login.vue`

**组件结构**：
```vue
<template>
  <div class="login-page">
    <div class="login-container">
      <div class="logo-section">
        <h1>口算练习</h1>
      </div>

      <!-- 最近使用用户 -->
      <div v-if="recentUsers.length > 0" class="recent-users">
        <p class="section-title">选择您的身份</p>
        <div class="user-list">
          <div
            v-for="user in recentUsers"
            :key="user.id"
            class="user-card"
            @click="selectUser(user)"
          >
            <div class="user-avatar">{{ user.username[0] }}</div>
            <div class="user-info">
              <div class="user-name">{{ user.username }}</div>
              <div class="user-stats">{{ user.total_questions }}道题</div>
            </div>
          </div>
        </div>
      </div>

      <!-- 或者使用新用户 -->
      <div class="new-user-section">
        <p class="section-title">或使用新用户</p>
        <el-form ref="formRef" :model="form" :rules="rules">
          <el-form-item prop="username">
            <el-input
              v-model="form.username"
              placeholder="请输入您的姓名"
              size="large"
            />
          </el-form-item>

          <el-form-item>
            <el-checkbox v-model="form.rememberMe">
              记住我的登录状态
            </el-checkbox>
          </el-form-item>

          <el-button
            type="primary"
            size="large"
            class="login-button"
            :loading="loading"
            @click="handleQuickLogin"
          >
            开始答题
          </el-button>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/auth'
import { authAPI } from '@/apis/auth'

const router = useRouter()
const userStore = useUserStore()

const formRef = ref(null)
const loading = ref(false)
const recentUsers = ref([])

const form = reactive({
  username: '',
  rememberMe: true  // 默认勾选
})

const rules = {
  username: [
    { required: true, message: '请输入您的姓名', trigger: 'blur' },
    { min: 2, max: 20, message: '姓名长度2-20个字符', trigger: 'blur' }
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
        user_ids: recentUserIds
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
```

---

### API 调用封装

**文件**：`frontend-user/src/apis/auth.js`

```javascript
import request from '@/utils/request'

// 快速登录
export function quickLogin(data) {
  return request({
    url: '/api/v1/auth/quick-login',
    method: 'post',
    data
  })
}

// 获取最近使用用户
export function getRecentUsers(data) {
  return request({
    url: '/api/v1/users/recent',
    method: 'get',
    params: data
  })
}

// 原有登录（保留）
export function login(data) {
  return request({
    url: '/api/v1/auth/login',
    method: 'post',
    data
  })
}

// ... 其他原有函数保持不变
```

---

### Store 持久化

**文件**：`frontend-user/src/stores/auth.js`

```javascript
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('access_token') || '',
    userInfo: JSON.parse(localStorage.getItem('user_info') || '{}'),
    currentChildId: localStorage.getItem('current_child_id') || null
  }),

  getters: {
    isLoggedIn: (state) => !!state.token
  },

  actions: {
    setToken(token) {
      this.token = token
      localStorage.setItem('access_token', token)
    },

    setUserInfo(userInfo) {
      this.userInfo = userInfo
      localStorage.setItem('user_info', JSON.stringify(userInfo))
    },

    setCurrentChildId(childId) {
      this.currentChildId = childId
      if (childId) {
        localStorage.setItem('current_child_id', childId)
      } else {
        localStorage.removeItem('current_child_id')
      }
    },

    logout() {
      this.token = ''
      this.userInfo = {}
      this.currentChildId = null
      localStorage.removeItem('access_token')
      localStorage.removeItem('user_info')
      localStorage.removeItem('current_child_id')
      localStorage.removeItem('recent_user_ids')  // 清除最近用户列表
    }
  }
})
```

---

## 管理后台 API 设计

### 1. 今日数据统计

**端点**：`GET /api/v1/statistics/today`

**响应**：
```json
{
  "active_users": 3,
  "total_questions": 144,
  "total_time_minutes": 40,
  "top_users": [
    {
      "id": 123,
      "username": "小明",
      "question_count": 99,
      "time_minutes": 20
    },
    ...
  ]
}
```

---

### 2. 本周排行榜

**端点**：`GET /api/v1/statistics/leaderboard?period=weekly`

**响应**：
```json
{
  "leaderboard": [
    {
      "rank": 1,
      "id": 123,
      "username": "小明",
      "question_count": 500,
      "score": 12500
    },
    ...
  ],
  "period": "weekly"
}
```

---

### 3. 用户历史趋势

**端点**：`GET /api/v1/statistics/user/{user_id}/history`

**响应**：
```json
{
  "user_id": 123,
  "username": "小明",
  "history": [
    {
      "date": "2024-01-15",
      "question_count": 20,
      "score": 500
    },
    ...
  ]
}
```

---

### 4. 用户列表

**端点**：`GET /api/v1/admin/users`

**查询参数**：
- `page`: 页码
- `page_size`: 每页数量
- `search`: 搜索关键词

**响应**：
```json
{
  "users": [
    {
      "id": 123,
      "username": "小明",
      "phone": "13800138000",
      "email": "xiaoming@example.com",
      "status": 1,
      "created_at": "2024-01-15T10:30:00",
      "total_questions": 99
    },
    ...
  ],
  "total": 10,
  "page": 1,
  "page_size": 20
}
```

---

### 5. 用户禁用/启用

**端点**：`PUT /api/v1/admin/users/{user_id}/status`

**请求**：
```json
{
  "status": 0  // 0-禁用 1-启用
}
```

---

## 安全考虑

### 1. JWT 安全

```python
# 使用强随机密钥
JWT_SECRET_KEY = secrets.token_urlsafe(64)

# 2 年有效期但仍需防止长期token泄露
# 建议：在部署文档中说明使用场景限制
```

---

### 2. 用户名验证

```python
# 前端验证
username: [
  { required: true, message: '请输入您的姓名', trigger: 'blur' },
  { min: 2, max: 20, message: '姓名长度2-20个字符', trigger: 'blur' },
  {
    pattern: /^[\u4e00-\u9fa5a-zA-Z0-9_]+$/,
    message: '只能输入中文、英文、数字和下划线',
    trigger: 'blur'
  }
]

# 后端验证
@validator('username')
def validate_username(cls, v):
    if len(v) < 2 or len(v) > 20:
        raise ValueError('姓名长度必须在2-20个字符之间')
    if not re.match(r'^[\u4e00-\u9fa5a-zA-Z0-9_]+$', v):
        raise ValueError('只能输入中文、英文、数字和下划线')
    return v
```

---

### 3. 用户名冲突处理

```python
# 当用户名已存在时
try:
    user = User(username=username)
    db.add(user)
    db.commit()
except IntegrityError:
    raise HTTPException(
        status_code=400,
        detail=f"用户名 '{username}' 已存在，请添加后缀重新输入（如：小明_1）"
    )
```

---

## 测试策略

### 1. 前端测试

- [ ] 测试快速登录流程（新用户）
- [ ] 测试快速登录流程（已存在用户）
- [ ] 测试最近用户列表显示
- [ ] 测试最近用户列表点击登录
- [ ] 测试"记住登录状态"功能
- [ ] 测试登录状态持久化
- [ ] 测试边界情况（空用户名、超长用户名）

---

### 2. 后端测试

- [ ] 测试 quick_login 接口
- [ ] 测试自动创建用户逻辑
- [ ] 测试 JWT token 生成和验证
- [ ] 测试 get_recent_users 接口
- [ ] 测试用户名冲突处理
- [ ] 测试向后兼容（传统登录）

---

### 3. 集成测试

- [ ] 端到端测试登录流程
- [ ] 测试多设备登录同一用户
- [ ] 测试token长期有效性

---

## 部署注意事项

1. **数据库迁移**：先执行 `ALTER TABLE` 将 `password_hash` 改为 NULLABLE
2. **配置更新**：修改 JWT 过期时间为 2 年
3. **向后兼容**：确保原有登录接口仍然可用
4. **前端部署**：同步更新前端代码
5. **防火墙规则**：在路由器中限制外网访问（如果需要）
