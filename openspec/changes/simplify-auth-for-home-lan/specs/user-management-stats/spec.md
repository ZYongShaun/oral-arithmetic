# Spec: User Management and Statistics Dashboard

## 新增需求

### 需求：管理后台必须提供今日数据统计
系统必须提供今日数据统计接口，显示当天活跃用户数、答题总数和用时统计。

#### 场景：获取今日统计概览
- **当** 管理员访问今日统计页面
- **那么** 系统必须显示以下指标：
  - 今日活跃用户数（去重）
  - 今日答题总数
  - 今日总用时（分钟）
- **并且** 数据必须实时计算（缓存时间不超过5分钟）

#### 场景：今日统计显示前5名用户
- **当** 管理员访问今日统计页面
- **那么** 系统必须显示今日答题数前5名的用户列表
- **并且** 每个条目必须显示：
  - 用户ID
  - 用户名
  - 答题数量
  - 用时（分钟）
- **并且** 列表必须按答题数降序排列

---

### 需求：管理后台必须提供本周排行榜
系统必须提供本周排行榜功能，按答题数量对用户进行排名。

#### 场景：获取本周排行榜
- **当** 管理员请求本周排行榜
- **那么** 系统必须返回本周（周一至当前时间）的排行榜数据
- **并且** 排行榜必须包含：
  - 用户排名（1, 2, 3...）
  - 用户ID
  - 用户名
  - 本周答题数量
  - 本周得分
- **并且** 列表必须按答题数降序排列
- **并且** 支持分页（每页最多50条）

#### 场景：本周排行榜前3名高亮显示
- **当** 管理员查看本周排行榜
- **那么** 前3名用户必须使用特殊样式高亮显示
- **并且** 第1名显示 🥇 图标
- **并且** 第2名显示 🥈 图标
- **并且** 第3名显示 🥉 图标

#### 场景：排行榜筛选时间范围
- **当** 管理员选择不同时间范围（本周、本月、全部）
- **那么** 系统必须根据选择重新计算排行榜数据
- **并且** 排行榜标题必须显示当前时间范围

---

### 需求：管理后台必须提供单个用户历史趋势
系统必须提供单个用户的答题历史趋势分析，支持图表展示。

#### 场景：查看用户历史趋势
- **当** 管理员点击某个用户查看详情
- **那么** 系统必须显示该用户的答题历史趋势图
- **并且** 趋势图必须包含：
  - 时间轴（日期）
  - 每日答题数量
  - 每日得分
- **并且** 图表必须支持至少30天的历史数据

#### 场景：历史趋势图支持时间筛选
- **当** 管理员选择不同时间范围（7天、30天、90天）
- **那么** 趋势图必须更新显示对应时间范围的数据
- **并且** X轴时间间隔必须自动调整以适应数据密度

#### 场景：用户历史统计摘要
- **当** 管理员查看用户历史页面
- **那么** 系统必须显示统计摘要卡片：
  - 总答题数
  - 总得分
  - 平均每日答题数
  - 最高单日答题数
  - 注册日期

---

### 需求：管理后台必须提供用户列表管理功能
系统必须提供完整的用户列表管理功能，支持搜索、分页和状态切换。

#### 场景：查看用户列表
- **当** 管理员访问用户列表页面
- **那么** 系统必须显示完整的用户列表
- **并且** 每行必须显示：
  - 用户ID
  - 用户名
  - 手机号码（如果存在）
  - 邮箱（如果存在）
  - 状态（正常/禁用）
  - 注册时间
  - 总答题数
- **并且** 列表必须支持分页（每页20条）

#### 场景：搜索用户
- **当** 管理员在搜索框输入关键词
- **那么** 系统必须实时过滤用户列表
- **并且** 搜索范围必须包括：
  - 用户名（模糊匹配）
  - 手机号码（精确匹配）
  - 邮箱（模糊匹配）
- **并且** 结果必须即时更新（无需点击搜索按钮）

#### 场景：禁用用户账户
- **当** 管理员点击用户列表中的"禁用"按钮
- **那么** 系统必须显示确认对话框
- **并且** 确认后系统必须将该用户 status 更新为 0
- **并且** 该用户的长期 token 必须立即失效
- **并且** 列表必须更新显示用户状态为"禁用"

#### 场景：启用用户账户
- **当** 管理员点击已禁用用户的"启用"按钮
- **那么** 系统必须将该用户 status 更新为 1
- **并且** 列表必须更新显示用户状态为"正常"
- **并且** 用户必须可以重新登录

---

### 需求：管理后台必须提供数据导出功能
系统必须支持导出统计数据为 CSV 或 Excel 格式。

#### 场景：导出本周排行榜
- **当** 管理员点击"导出排行榜"按钮
- **那么** 系统必须生成 CSV 文件
- **并且** 文件必须包含完整的排行榜数据
- **并且** 文件必须自动下载到用户设备
- **并且** 文件名格式为：`leaderboard_YYYY-MM-DD.csv`

#### 场景：导出用户详细数据
- **当** 管理员点击"导出用户数据"按钮
- **那么** 系统必须生成 Excel 文件
- **并且** 文件必须包含所有用户的完整信息
- **并且** 文件必须自动下载
- **并且** 文件名格式为：`users_export_YYYY-MM-DD.xlsx`

---

## 修改需求

### 需求：用户列表必须显示总答题数
原有的用户列表需要增加总答题数列，用于快速查看用户活跃程度。

#### 场景：用户列表显示答题统计
- **当** 管理员查看用户列表
- **那么** 每个用户条目必须显示"总答题数"列
- **并且** 该列必须显示该用户累计完成的所有题目数量
- **并且** 该列必须支持点击排序（升序/降序）

---

### 需求：用户详情页必须显示孩子档案关联
原有的用户详情需要显示关联的孩子档案信息。

#### 场景：查看用户关联的孩子档案
- **当** 管理员点击用户详情
- **那么** 详情页必须显示该用户关联的所有孩子档案
- **并且** 每个孩子档案必须显示：
  - 孩子ID
  - 孩子姓名
  - 年级
  - 总星星数
  - 该孩子的答题统计

---

## 移除需求

无移除需求。

---

## 规格说明

### API 端点定义

#### GET /api/v1/statistics/today
**描述**: 获取今日数据统计

**认证**: 需要管理员权限

**响应 (200 OK)**:
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
    {
      "id": 124,
      "username": "小红",
      "question_count": 35,
      "time_minutes": 15
    }
  ]
}
```

---

#### GET /api/v1/statistics/leaderboard
**描述**: 获取排行榜

**认证**: 需要管理员权限

**查询参数**:
- `period`: 时间范围 (`weekly`, `monthly`, `all`)
- `page`: 页码（默认1）
- `page_size`: 每页数量（默认20，最大50）

**响应 (200 OK)**:
```json
{
  "period": "weekly",
  "leaderboard": [
    {
      "rank": 1,
      "id": 123,
      "username": "小明",
      "question_count": 500,
      "score": 12500
    },
    {
      "rank": 2,
      "id": 124,
      "username": "小红",
      "question_count": 420,
      "score": 10500
    }
  ],
  "total": 50,
  "page": 1,
  "page_size": 20
}
```

---

#### GET /api/v1/statistics/user/{user_id}/history
**描述**: 获取单个用户历史趋势

**认证**: 需要管理员权限

**路径参数**:
- `user_id`: 用户ID

**查询参数**:
- `days`: 天数范围（默认30，最大90）

**响应 (200 OK)**:
```json
{
  "user_id": 123,
  "username": "小明",
  "summary": {
    "total_questions": 500,
    "total_score": 12500,
    "avg_daily_questions": 16.7,
    "max_daily_questions": 45,
    "created_at": "2024-01-15T10:30:00"
  },
  "history": [
    {
      "date": "2024-01-15",
      "question_count": 20,
      "score": 500
    },
    {
      "date": "2024-01-16",
      "question_count": 30,
      "score": 750
    }
  ]
}
```

---

#### GET /api/v1/admin/users
**描述**: 获取用户列表

**认证**: 需要管理员权限

**查询参数**:
- `page`: 页码（默认1）
- `page_size`: 每页数量（默认20）)
- `search`: 搜索关键词
- `status`: 状态筛选（`all`, `1`-启用, `0`-禁用）
- `sort_by`: 排序字段（`created_at`, `question_count`, `username`）
- `order`: 排序方向（`asc`, `desc`）

**响应 (200 OK)**:
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
    }
  ],
  "total": 10,
  "page": 1,
  "page_size": 20
}
```

---

#### PUT /api/v1/admin/users/{user_id}/status
**描述**: 更新用户状态（启用/禁用）

**认证**: 需要管理员权限

**路径参数**:
- `user_id`: 用户ID

**请求体**:
```json
{
  "status": 0
}
```

**响应 (200 OK)**:
```json
{
  "id": 123,
  "status": 0,
  "message": "用户已禁用"
}
```

---

#### GET /api/v1/statistics/leaderboard/export
**描述**: 导出排行榜为 CSV

**认证**: 需要管理员权限

**查询参数**:
- `period`: 时间范围

**响应 (200 OK)**:
```csv
rank,username,question_count,score
1,小明,500,12500
2,小红,420,10500
```

**Content-Type**: `text/csv; charset=utf-8`

---

#### GET /api/v1/admin/users/export
**描述**: 导出用户数据为 Excel

**认证**: 需要管理员权限

**响应 (200 OK)**:
返回 Excel 文件下载

**Content-Type**: `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`

---

### 前端页面结构

#### Dashboard.vue（管理后台首页）
```vue
<template>
  <div class="dashboard">
    <!-- 今日统计卡片 -->
    <div class="stats-cards">
      <StatCard title="今日活跃用户" :value="todayStats.active_users" />
      <StatCard title="今日答题总数" :value="todayStats.total_questions" />
      <StatCard title="今日总用时" :value="todayStats.total_time_minutes" unit="分钟" />
    </div>

    <!-- 今日前5名 -->
    <TopUsersList :users="todayStats.top_users" />

    <!-- 快速导航 -->
    <QuickNav />
  </div>
</template>
```

---

#### Statistics.vue（统计页面）
```vue
<template>
  <div class="statistics">
    <!-- 时间范围选择器 -->
    <PeriodSelector v-model="period" @change="loadData" />

    <!-- 排行榜表格 -->
    <LeaderboardTable
      :period="period"
      :data="leaderboard"
      @export="exportLeaderboard"
    />

    <!-- 分页 -->
    <Pagination :total="total" :page="page" :size="pageSize" @change="handlePageChange" />
  </div>
</template>
```

---

#### UserList.vue（用户列表）
```vue
<template>
  <div class="user-list">
    <!-- 搜索栏 -->
    <SearchBar v-model="searchQuery" @search="handleSearch" />

    <!-- 筛选器 -->
    <FilterBar v-model:status="statusFilter" v-model:sort="sortBy" @change="loadUsers" />

    <!-- 用户表格 -->
    <UserTable
      :users="users"
      :loading="loading"
      @toggle-status="handleToggleStatus"
      @view-detail="goToUserDetail"
    />

    <!-- 分页 -->
    <Pagination :total="total" :page="page" :size="pageSize" @change="handlePageChange" />
  </div>
</template>
```

---

#### UserDetail.vue（用户详情）
```vue
<template>
  <div class="user-detail">
    <!-- 用户基本信息 -->
    <UserInfoCard :user="userInfo" @toggle-status="handleToggleStatus" />

    <!-- 孩子档案列表 -->
    <ChildProfilesList :children="userChildren" />

    <!-- 历史趋势图 -->
    <HistoryTrendChart :data="userHistory" :days="selectedDays" />

    <!-- 统计摘要 -->
    <StatsSummary :summary="userSummary" />
  </div>
</template>
```

---

### 数据库查询优化

#### 今日统计查询
```sql
-- 获取今日活跃用户数
SELECT COUNT(DISTINCT user_id)
FROM practices
WHERE DATE(created_at) = CURRENT_DATE;

-- 获取今日答题总数
SELECT COUNT(*)
FROM practices
WHERE DATE(created_at) = CURRENT_DATE;

-- 获取今日总用时（分钟）
SELECT SUM(time_used)
FROM practices
WHERE DATE(created_at) = CURRENT_DATE;

-- 获取今日前5名用户
SELECT
    p.user_id,
    u.username,
    COUNT(*) as question_count,
    SUM(p.time_used) as time_minutes
FROM practices p
JOIN users u ON p.user_id = u.id
WHERE DATE(p.created_at) = CURRENT_DATE
GROUP BY p.user_id, u.username
ORDER BY question_count DESC
LIMIT 5;
```

---

#### 排行榜查询
```sql
-- 获取本周排行榜
SELECT
    ROW_NUMBER() OVER (ORDER BY question_count DESC) as rank,
    user_id,
    username,
    question_count,
    SUM(score) as score
FROM (
    SELECT
        p.user_id,
        u.username,
        COUNT(*) as question_count
    FROM practices p
    JOIN users u ON p.user_id = u.id
    WHERE YEARWEEK(p.created_at, 1) = YEARWEEK(CURDATE(), 1)
    GROUP BY p.user_id, u.username
) ranked_users
ORDER BY question_count DESC
LIMIT ? OFFSET ?;
```

---

#### 用户历史查询
```sql
-- 获取用户历史按天统计
SELECT
    DATE(created_at) as date,
    COUNT(*) as question_count,
    SUM(score) as score
FROM practices
WHERE
    user_id = ?
    AND created_at >= DATE_SUB(CURDATE(), INTERVAL ? DAY)
GROUP BY DATE(created_at)
ORDER BY date DESC
LIMIT ?;
```

---

### 前端组件要求

#### StatCard 组件
- 显示统计数值
- 支持单位显示
- 支持趋势指示（上升/下降）

#### LeaderboardTable 组件
- 表格显示
- 排名列带图标（🥇🥈🥉）
- 支持排序
- 导出按钮

#### UserTable 组件
- 表格显示
- 状态标签（正常/禁用）
- 操作按钮（查看详情、启用/禁用）
- 搜索过滤

#### HistoryTrendChart 组件
- 使用 ECharts 实现趋势图
- 支持多数据系列（答题数、得分）
- 支持时间范围切换

---

### 性能要求

- 今日统计数据查询：< 200ms
- 排行榜查询（每页20条）：< 300ms
- 用户历史查询（30天）：< 500ms
- 用户列表查询（每页20条）：< 300ms

建议使用数据库索引优化查询性能。

---

### 缓存策略

#### Redis 缓存
```
# 今日统计（5分钟过期）
stats:today:TTL=300

# 本周排行榜（10分钟过期）
leaderboard:weekly:TTL=600

# 用户历史数据（1小时过期）
user:history:{user_id}:TTL=3600
```

---

### 权限控制

只有管理员角色才能访问管理后台统计接口。

检查方式：
```python
async def get_current_admin(
    current_user: User = Depends(get_current_user)
) -> Admin:
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="需要管理员权限")
    return current_user
```

---

### 安全考虑

1. **数据隐藏**：普通用户看不到其他用户的统计数据
2. **频率限制**：导出功能需要频率限制（每分钟最多1次）
3. **日志记录**：所有管理操作必须记录到审计日志
4. **敏感信息**：导出文件不得包含密码哈希等信息

---

## 实施检查清单

### 后端 API
- [ ] 实现 `GET /api/v1/statistics/today` 接口
- [ ] 实现 `GET /api/v1/statistics/leaderboard` 接口
- [ ] 实现 `GET /api/v1/statistics/user/{user_id}/history` 接口
- [ ] 实现 `GET /api/v1/admin/users` 接口
- [ ] 实现 `PUT /api/v1/admin/users/{user_id}/status` 接口
- [ ] 实现 `GET /api/v1/statistics/leaderboard/export` 接口
- [ ] 实现 `GET /api/v1/admin/users/export` 接口
- [ ] 添加管理员权限检查依赖项
- [ ] 优化数据库查询性能（添加索引）
- [ ] 实现 Redis 缓存层

### 前端管理后台
- [ ] 创建 `Dashboard.vue` 页面
- [ ] 创建 `Statistics.vue` 页面
- [ ] 创建 `UserList.vue` 页面
- [ ] 创建 `UserDetail.vue` 页面
- [ ] 创建 `StatCard.vue` 组件
- [ ] 创建 `LeaderboardTable.vue` 组件
- [ ] 创建 `UserTable.vue` 组件
- [ ] 创建 `HistoryTrendChart.vue` 组件（使用 ECharts）
- [ ] 实现 API 调用封装
- [ ] 添加路由配置

### 测试
- [ ] 测试今日统计数据准确性
- [ ] 测试排行榜排序和时间范围筛选
- [ ] 测试用户历史趋势图渲染
- [ ] 测试用户列表搜索和分页
- [ ] 测试用户启用/禁用功能
- [ ] 测试数据导出功能
- [ ] 测试权限控制（非管理员无法访问）
- [ ] 性能测试（所有接口响应时间）
