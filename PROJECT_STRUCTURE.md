# 项目架构说明

## 目录结构

```
oral-arithmetic/
├── backend/                      # FastAPI 后端服务
│   ├── app/
│   │   ├── api/                 # API 路由模块
│   │   │   ├── __init__.py
│   │   │   ├── auth.py          # 认证接口
│   │   │   ├── users.py         # 用户接口
│   │   │   ├── children.py      # 孩子档案接口
│   │   │   ├── questions.py     # 题目接口
│   │   │   ├── practices.py     # 练习接口
│   │   │   ├── wrong_questions.py  # 错题接口
│   │   │   ├── streaks.py       # 连胜接口
│   │   │   ├── achievements.py  # 成就接口
│   │   │   ├── leaderboards.py  # 排行榜接口
│   │   │   ├── stars.py         # 星星接口
│   │   │   └── admin.py         # 管理接口
│   │   ├── models/              # SQLAlchemy 数据模型
│   │   │   ├── __init__.py
│   │   │   ├── user.py          # 用户相关模型
│   │   │   ├── question.py      # 题目模型
│   │   │   ├── practice.py      # 练习模型
│   │   │   ├── streak.py        # 连胜模型
│   │   │   ├── achievement.py   # 成就模型
│   │   │   ├── leaderboard.py   # 排行榜模型
│   │   │   └── star.py          # 星星模型
│   │   ├── schemas/             # Pydantic 请求/响应模型
│   │   ├── services/            # 业务逻辑层
│   │   ├── utils/               # 工具函数
│   │   ├── core/                # 核心配置
│   │   │   ├── __init__.py
│   │   │   ├── config.py        # 配置管理
│   │   │   ├── security.py      # 安全工具
│   │   │   └── database.py      # 数据库连接
│   │   └── main.py              # FastAPI 应用入口
│   ├── requirements.txt         # Python 依赖
│   ├── .env.example             # 环境配置示例
│   └── venv/                    # 虚拟环境（需自行创建）
├── frontend-user/               # 用户端（移动端 H5）
│   ├── src/
│   │   ├── views/               # 页面组件
│   │   │   ├── Login.vue
│   │   │   ├── Register.vue
│   │   │   ├── Home.vue
│   │   │   ├── Practice.vue
│   │   │   ├── WrongQuestions.vue
│   │   │   ├── Statistics.vue
│   │   │   ├── Children.vue
│   │   │   └── Profile.vue
│   │   ├── components/          # 公共组件
│   │   ├── router/              # 路由配置
│   │   ├── stores/              # Pinia 状态管理
│   │   ├── utils/               # 工具函数
│   │   ├── apis/                # API 调用封装
│   │   ├── assets/              # 静态资源
│   │   └── style.css            # 全局样式
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
├── frontend-admin/              # 管理端（PC 端）
│   ├── src/
│   │   ├── views/               # 页面组件
│   │   │   ├── Login.vue
│   │   │   ├── Dashboard.vue
│   │   │   ├── UserList.vue
│   │   │   ├── QuestionList.vue
│   │   │   ├── Statistics.vue
│   │   │   └── ...
│   │   ├── components/
│   │   ├── router/
│   │   ├── stores/
│   │   ├── utils/
│   │   ├── apis/
│   │   └── assets/
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
├── docs/
│   └── database.sql             # 数据库建表脚本
├── scripts/
│   └── setup.sh                 # 初始化脚本
└── README.md                    # 项目说明
```

## 已完成的文件清单

### 后端
✅ requirements.txt
✅ app/__init__.py
✅ app/core/config.py
✅ app/core/security.py
✅ app/core/database.py
✅ app/models/user.py
✅ app/main.py
✅ .env.example

### 数据库
✅ docs/database.sql - 完整的建表 SQL（14 张表）

### 前端用户端
✅ package.json
✅ vite.config.js
✅ index.html
✅ src/main.js
✅ src/App.vue
✅ src/router/index.js
✅ (页面组件待继续创建)

### 前端管理端
✅ package.json
✅ vite.config.js
✅ src/main.js
✅ (其他文件待继续创建)

### 工具
✅ scripts/setup.sh - 自动初始化脚本

## 下一步开发任务

### 优先级 1 - 后端核心 API（必需）
1. 创建完整的数据模型（models/）
   - question.py
   - practice.py
   - streak.py
   - achievement.py
   - leaderboard.py
   - star.py
2. 实现认证模块（api/auth.py）
3. 实现用户管理（api/users.py, api/children.py）
4. 实现题目生成算法（services/question_generator.py）
5. 实现练习流程（api/practices.py）
6. 实现错题本（api/wrong_questions.py）
7. 实现趣味化模块（streaks, achievements, leaderboards, stars）

### 优先级 2 - 前端用户端页面（必需）
1. 创建所有页面组件（views/）
   - Login.vue, Register.vue
   - Home.vue（首页，包含难度选择）
   - Practice.vue（答题页）
   - WrongQuestions.vue（错题本）
   - Statistics.vue（统计）
   - Children.vue（孩子管理）
   - Profile.vue（个人中心）
2. 创建 API 调用层（apis/）
3. 创建状态管理（stores/）
4. 创建公共组件（components/）

### 优先级 3 - 前端管理端（可选，可后续补充）
1. 创建管理页面（views/）
2. 创建管理 API（apis/）
3. 创建管理状态（stores/）

### 优先级 4 - 测试和部署
1. 单元测试
2. 集成测试
3. 部署文档
4. 用户手册

## 快速启动指南

```bash
# 1. 数据库初始化
mysql -u root -p < docs/database.sql

# 2. 配置环境
cp backend/.env.example backend/.env
# 编辑 backend/.env，设置正确的数据库密码

# 3. 安装依赖
bash scripts/setup.sh

# 4. 启动后端
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 5. 启动前端（新开终端）
cd frontend-user
npm run dev

# 6. 访问应用
# 后端 API: http://localhost:8000
# API 文档: http://localhost:8000/docs
# 用户前端: http://localhost:3000
```

## 数据库连接配置

后端使用配置文件中定义的数据库连接：

```python
# backend/app/core/config.py
DATABASE_HOST=localhost
DATABASE_PORT=3306
DATABASE_NAME=oral_arithmetic
DATABASE_USER=root
DATABASE_PASSWORD=你的密码
```

确保：
1. MySQL 服务已启动
2. 数据库 oral_arithmetic 已创建（sql 脚本会自动创建）
3. 用户有读写权限

## 默认管理员账号

执行 database.sql 后会创建：
- 用户名：`admin`
- 密码：`admin123`（bcrypt 加密）

管理后台地址（待开发）：http://localhost:3001

## 技术要点

### 后端
- FastAPI 提供 RESTful API
- SQLAlchemy ORM 操作数据库
- JWT 认证（2小时有效期）
- 密码 bcrypt 加密
- Pydantic 数据验证

### 前端
- Vue 3 Composition API
- Vue Router 4 路由管理
- Pinia 状态管理
- Element Plus UI 组件库
- Axios HTTP 客户端
- Vite 构建工具

## 注意事项

1. **数据库版本**：要求 MySQL 8.0+
2. **Python 版本**：要求 3.9+
3. **Node 版本**：要求 16+
4. **跨域**：后端已配置 CORS，允许所有来源（仅开发环境）
5. **环境变量**：请勿将 .env 文件提交到版本控制

## 后续扩展

1. 完善趣味化功能（连胜、成就、排行榜）
2. 实现智能出题算法
3. 添加单元测试
4. 性能优化
5. PWA 支持（离线可用）
6. 微信小程序版本

---

**开发进行中...**
