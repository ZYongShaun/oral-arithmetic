# 变更总结：简化家庭局域网认证系统

**变更日期：** 2026-04-15  
**变更类型：** 功能增强  
**影响范围：** 认证系统、前端用户端、管理后台  
**向后兼容：** 是 ✅  

---

## 📋 变更概述

本次变更将现有的用户名+密码认证系统简化为仅需用户名的快速登录，专为家庭局域网场景设计。系统现在支持无密码登录、自动创建用户、长期有效token等功能，同时保留传统登录方式以向后兼容。

### 主要目标
1. **快速登录**：用户只需输入姓名就能登录，无需密码
2. **自动创建用户**：如果用户名不存在，自动创建新用户  
3. **长期有效token**：JWT 有效期从 2 小时延长到 2 年
4. **完整管理后台**：家长可以查看所有孩子的进度和统计

---

## 🔄 数据库变更

### 用户表修改

```sql
-- 将 password_hash 字段改为可空，支持无密码用户
ALTER TABLE users MODIFY COLUMN password_hash VARCHAR(255) NULL;
```

**影响：**
- ✅ 现有用户（有密码的）完全不受影响
- ✅ password_hash 值保持不变
- ✅ 可以创建 password_hash 为 NULL 的新用户

### 性能优化索引（可选）

```sql
-- 为用户历史查询添加复合索引
CREATE INDEX idx_practices_user_date ON practices(user_id, DATE(created_at));
```

**场景：** 当 practices 表数据量大时，这可以显著提升历史查询性能

---

## ⚙️ 配置文件变更

### JWT 配置 (`backend/app/core/config.py`)

**变更前：**
```python
JWT_EXPIRE_MINUTES = 120          # 2小时
ACCESS_TOKEN_EXPIRE_MINUTES = 120 # 2小时
```

**变更后：**
```python
JWT_EXPIRE_MINUTES = 525600          # 2年 = 365 * 24 * 60 ⚠️
ACCESS_TOKEN_EXPIRE_MINUTES = 525600 # 2年 = 365 * 24 * 60 ⚠️
```

---

## 📁 新增文件列表

### 后端 API

**新增文件：**
- `backend/app/api/statistics.py` - 统计数据API端点
- `backend/app/api/admin.py` - 用户管理API端点（扩展现有模块）

**新增功能：**
- `POST /api/v1/auth/quick-login` - 快速登录
- `GET /api/v1/users/recent` - 获取最近使用用户
- `GET /api/v1/statistics/today` - 今日数据统计
- `GET /api/v1/statistics/leaderboard` - 排行榜（支持导出）
- `GET /api/v1/statistics/user/{user_id}/history` - 用户历史趋势
- `GET /api/v1/admin/users` - 用户列表（支持搜索、筛选、排序）
- `PUT /api/v1/admin/users/{user_id}/status` - 更新用户状态
- `GET /api/v1/admin/users/export` - 导出用户数据

### 前端用户端

**修改文件：**
- `frontend-user/src/views/Login.vue` - 登录页面改造
- `frontend-user/src/apis/auth.js` - 添加快速登录API
- `frontend-user/src/stores/auth.js` - 更新状态管理

**新增功能：**
- 移除密码输入框
- 添加"记住登录状态"选项
- 显示最近使用用户列表（最多5个）
- 自动更新最近用户列表逻辑

### 前端管理端

**修改的现有文件：**
- `frontend-admin/src/router/index.js` - 更新路由配置
- `frontend-admin/src/apis/admin.js` - 扩展API调用
- `frontend-admin/src/apis/statistics.js` - 新增统计API

**新增页面文件：**
- `frontend-admin/src/views/Dashboard.vue` - 管理后台首页
- `frontend-admin/src/views/Statistics.vue` - 统计页面
- `frontend-admin/src/views/UserList.vue` - 用户列表页面
- `frontend-admin/src/views/UserDetail.vue` - 用户详情页面

**新增组件文件：**
- `frontend-admin/src/components/StatCard.vue` - 统计卡片组件
- `frontend-admin/src/components/LeaderboardTable.vue` - 排行榜表格组件
- `frontend-admin/src/components/UserTable.vue` - 用户表格组件
- `frontend-admin/src/components/HistoryTrendChart.vue` - 历史趋势图表组件
- `frontend-admin/src/components/PeriodSelector.vue` - 时间范围选择器组件
- `frontend-admin/src/components/SearchBar.vue` - 搜索框组件  
- `frontend-admin/src/components/Pagination.vue` - 分页组件

---

## 📝 修改的现有文件

### 后端文件

1. **`backend/app/api/auth.py`**
   - 添加 `quick_login` 端点
   - 添加 `get_recent_users` 端点

2. **`backend/app/services/auth_service.py`**
   - 添加 `create_or_get_user` 函数
   - 修改 `get_current_user` 函数增加状态检查
   - 添加禁用用户的拒绝逻辑

3. **`backend/app/core/config.py`**
   - 修改 JWT 过期时间为 2 年

### 前端用户端文件

1. **`frontend-user/src/views/Login.vue`**
   - 完全重构登录界面
   - 实现快速登录逻辑
   - 添加最近用户列表

2. **`frontend-user/src/apis/auth.js`**
   - 添加 `quickLogin` 函数
   - 添加 `getRecentUsers` 函数

3. **`frontend-user/src/stores/auth.js`**
   - 更新 logout 逻辑清除 recent_user_ids

### 前端管理端文件

1. **`frontend-admin/src/router/index.js`**
   - 已存在路由配置（未修改）

### 文档文件

1. **`README.md`**
   - 添加快速登录功能说明
   - 添加家庭局域网场景配置指南
   - 更新功能列表

2. **`DEPLOY.md`**  
   - 添加数据库迁移步骤
   - 添加 JWT 配置更新说明
   - 添加防火墙配置建议

---

## 🧪 删除/移除的功能

无删除功能。所有现有功能保持不变并支持向下兼容。

---

## 🔐 安全注意事项

### 新的安全考虑

1. **长期有效token**
   - JWT token 现在有效期为 2 年
   - 建议仅在家庭局域网环境使用
   - 通过禁用用户功能可以立即撤销访问权限

2. **无密码登录**
   - 适用于高信任度的家庭环境
   - 不适合公网部署场景
   - 建议配置路由器限制外网访问

### 向后兼容性保证

1. **传统登录保留**
   - `POST /api/v1/auth/login` 仍然可用
   - 有密码的用户可以继续使用密码登录
   - 所有现有用户数据完全保留

2. **数据库兼容**
   - password_hash 字段变为可空（不影响现有值）
   - 所有现有的数据结构保持一致

---

## 📊 功能对比

### 认证方式对比

| 功能 | 传统登录 | 快速登录 |
|------|----------|----------|
| 用户名验证 | ✅ | ✅ |
| 密码验证 | ✅ | ❌ |
| 自动创建用户 | ❌ | ✅ |
| 用户存在检查 | ✅ | ✅ |
| JWT 过期时间 | 2年 | 2年 |
| 适合场景 | 公网/企业 | 家庭局域网 |

### 管理后台新增功能

| 功能 | 描述 | 状态 |
|------|------|------|
| 今日数据统计 | 活跃用户、答题数、用时、前5名 | ✅ |
| 排行榜 | 本周/本月/全部 ranking | ✅ |
| 用户历史趋势 | 图表展示 + 统计摘要 | ✅ |
| 用户管理 | 搜索、筛选、禁用/启用 | ✅ |
| 数据导出 | CSV/Excel 格式 | ✅ |

---

## 🚀 部署步骤

### 1. 数据库迁移
```sql
ALTER TABLE users MODIFY COLUMN password_hash VARCHAR(255) NULL;
```

### 2. 配置更新
```bash
# 确保配置文件中的JWT过期时间为2年
# backend/app/core/config.py 已自动更新
```

### 3. 启动服务
```bash
# 使用现有的部署脚本
./deploy.sh prod
```

### 4. 验证功能
```bash
# 测试快速登录
curl -X POST http://localhost:8000/api/v1/auth/quick-login \
  -H "Content-Type: application/json" \
  -d '{"username": "测试用户"}'

# 测试管理后台
# 访问 http://localhost:8000/docs 查看完整API文档
```

---

## 📝 测试建议

### 关键测试场景

1. **快速登录流程**
   - [ ] 新用户首次快速登录（自动创建）
   - [ ] 已存在用户快速登录
   - [ ] 无密码用户 password_hash 验证
   - [ ] 用户名冲突处理

2. **前端用户端**
   - [ ] 最近用户列表显示（5个）
   - [ ] 点击最近用户快速登录
   - [ ] "记住登录状态"功能
   - [ ] 最近用户列表更新逻辑

3. **管理后台**
   - [ ] 今日统计数据正确性
   - [ ] 排行榜排序准确性
   - [ ] 用户列表搜索、筛选、排序
   - [ ] 禁用/启用用户操作
   - [ ] 导出功能（CSV/Excel）

4. **向后兼容性**
   - [ ] 传统登录接口仍然可用
   - [ ] 现有用户数据未受影响
   - [ ] JWT token 2年有效期验证

---

## 🔄 回滚方案

如果需要回滚此变更：

### 1. 恢复数据库
```sql
-- 将 password_hash 改回 NOT NULL（如果不需要支持无密码用户）
ALTER TABLE users MODIFY COLUMN password_hash VARCHAR(255) NOT NULL;
```

### 2. 恢复配置
```bash
# 恢复 JWT 过期时间为 2 小时
# backend/app/core/config.py
JWT_EXPIRE_MINUTES = 120
ACCESS_TOKEN_EXPIRE_MINUTES = 120
```

### 3. 移除新功能
- 删除快速登录相关的文件和代码
- 恢复原登录界面

---

## 📞 支持与反馈

如有任何问题或建议，请：
1. 查看 `README.md` 中的家庭局域网场景配置指南
2. 检查 `DEPLOY.md` 中的部署和故障排查指南
3. 访问 API 文档：http://localhost:8000/docs

---

**变更完成时间：** 2026-04-15  
**文档版本：** 1.0  
**相关文档：** README.md, DEPLOY.md