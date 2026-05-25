# 小学一年级口算练习应用

> 一款融入多邻国式趣味化机制的口算练习应用

## 项目简介

为小学一年级学生打造的口算练习应用，通过连胜系统、排行榜、成就徽章等趣味化设计，提升孩子学习兴趣和粘性。

## 技术栈

- **后端**: Python FastAPI
- **前端用户端**: Vue.js 3 + Vite + Element Plus（移动端 H5）
- **前端管理端**: Vue.js 3 + Vite + Element Plus（PC 端）
- **数据库**: MySQL 8.0+

## 项目结构

```
oral-arithmetic/
├── backend/              # 后端服务
│   ├── app/
│   │   ├── api/         # API 路由
│   │   ├── models/      # 数据模型
│   │   ├── schemas/     # Pydantic 模型
│   │   ├── services/    # 业务逻辑
│   │   ├── utils/       # 工具函数
│   │   ├── core/        # 核心配置
│   │   └── main.py      # 应用入口
│   ├── requirements.txt
│   └── .env.example
├── frontend-user/       # 前端用户端（移动端）
├── frontend-admin/      # 前端管理端（PC 端）
├── docs/                # 文档
│   └── database.sql     # 数据库脚本
└── README.md
```

## 快速开始

### 1. 数据库初始化

```bash
# 登录 MySQL
mysql -u root -p

# 执行建表脚本
source /path/to/oral-arithmetic/docs/database.sql
```

### 2. 启动后端服务

```bash
cd backend

# 安装依赖
pip install -r requirements.txt

# 复制环境配置
cp .env.example .env

# 修改 .env 中的数据库配置

# 启动服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

访问 http://localhost:8000 查看 API 文档

### 3. 启动前端（待创建）

```bash
# 用户端
cd frontend-user
npm install
npm run dev

# 管理端
cd frontend-admin
npm install
npm run dev
```

### 4. 使用 Docker 部署（推荐）

#### 开发环境（前端热重载 + 后端容器）

```bash
# 1. 停止本地已启动的服务（如果有）
# 2. 启动后端容器
docker-compose -f docker-compose.dev.yml up -d

# 3. 在新终端启动前端（热重载）
cd frontend-user
npm install
npm run dev
```

#### 生产环境（所有服务容器化）

```bash
# 一键启动所有服务
docker-compose up -d
```

详细 Docker 部署说明请查看 [README-DOCKER.md](README-DOCKER.md)。

## 服务器管理命令

### 本地开发环境（非 Docker）

#### 启动服务

```bash
# 终端1: 启动后端
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 终端2: 启动前端用户端
cd frontend-user
npm install
npm run dev

# （可选）终端3: 启动前端管理端
cd frontend-admin
npm install
npm run dev
```

#### 停止服务

```bash
# 在运行服务的终端按 Ctrl+C

# 或者强制停止
pkill -f "uvicorn"
pkill -f "vite"
```

### Docker 环境

#### 开发模式（dev）

```bash
# 停止所有容器
docker-compose -f docker-compose.dev.yml down

# 启动（后台）
docker-compose -f docker-compose.dev.yml up -d

# 查看日志
docker-compose -f docker-compose.dev.yml logs -f

# 停止
docker-compose -f docker-compose.dev.yml down

# 重启
docker-compose -f docker-compose.dev.yml restart
```

#### 生产模式（prod）

```bash
# 启动
docker-compose up -d

# 停止
docker-compose down

# 重启
docker-compose restart

# 查看日志
docker-compose logs -f [服务名]  # 服务名: backend, frontend

# 进入容器
docker-compose exec backend /bin/bash
```

#### 容器管理

```bash
# 查看运行状态
docker-compose ps
docker-compose -f docker-compose.dev.yml ps

# 查看所有容器（包括未在 compose 中定义的）
docker ps -a

# 停止特定容器
docker stop oral_arithmetic_backend_dev  # 开发环境
docker stop oral_arithmetic_backend      # 生产环境

# 启动特定容器
docker start oral_arithmetic_backend_dev

# 删除容器
docker-compose down          # 保留数据卷
docker-compose down -v       # 删除所有数据（包括数据库）
docker rm [容器名]

# 清理未使用的资源
docker system prune -a
```

#### Docker 快速部署脚本

```bash
# 使用提供的自动化脚本
chmod +x deploy.sh
./deploy.sh dev   # 开发环境
./deploy.sh prod  # 生产环境
```

### 服务端口对照表

| 服务       | 本地模式                   | Docker 开发                | Docker 生产                |
| ---------- | -------------------------- | -------------------------- | -------------------------- |
| 前端用户端 | http://localhost:3000      | 需本地运行                 | http://localhost           |
| 后端 API   | http://localhost:8000      | http://localhost:8000      | http://localhost:8000      |
| API 文档   | http://localhost:8000/docs | http://localhost:8000/docs | http://localhost:8000/docs |
| MySQL      | localhost:3306             | host.docker.internal:3306  | 需外部提供                 |

### 故障排查

#### 端口占用

```bash
# 查看端口占用
lsof -i :8000
lsof -i :3000
lsof -i :80

# 杀死占用进程
kill -9 <PID>
```

#### 数据库连接失败

```bash
# 检查 MySQL 是否运行
mysqladmin ping -uroot

# 检查 Docker 内是否能访问宿主机 MySQL
docker-compose exec backend ping host.docker.internal

# 查看后端日志
docker-compose logs backend
```

#### 容器无法启动

```bash
# 查看详细错误日志
docker-compose logs [服务名]

# 重建容器
docker-compose up -d --build
```

### 停止所有服务

```bash
# 本地开发
pkill -f "uvicorn"
pkill -f "vite"

# Docker
docker-compose down
docker-compose -f docker-compose.dev.yml down

# 全部清理（包括数据卷）
docker-compose down -v
```

## 访问地址

- **本地模式**:
  - 前端: http://localhost:3000
  - 后端: http://localhost:8000
  - API 文档: http://localhost:8000/docs

- **Docker 生产模式**:
  - 前端: http://localhost
  - 后端: http://localhost:8000
  - API 文档: http://localhost:8000/docs

## 更多信息

- [Docker 部署详细文档](README-DOCKER.md)
- [部署脚本说明](DEPLOY.md)

## 核心功能

### 用户端

- ✅ 快速登录（家庭局域网场景）⚡
- ✅ 最近用户列表（快速切换）👥
- ✅ 长期有效登录（2年有效期）⏰
- ✅ 孩子档案管理
- ✅ 口算练习（10/20/50/100 以内）
- ✅ 每日任务系统
- ✅ 错题本
- ✅ 数据统计
- ✅ 闯关连胜系统 🔥
- ✅ 分组排名系统 🏆
- ✅ 成就徽章系统 🎖️
- ✅ 星星经济系统 ⭐

### 管理端

- ✅ 今日数据统计（活跃用户、答题数等）📊
- ✅ 排行榜管理（本周、本月、全部）🏆
- ✅ 用户历史趋势分析 📈
- ✅ 用户管理（搜索、筛选、禁用/启用）👥
- ✅ 题库管理（手动出题 + 批量导入）
- ✅ 出题规则配置
- ✅ 系统配置
- ✅ 成就管理

## 默认账号

**管理后台：**

- 用户名：`admin`
- 密码：`admin123`

## 家庭局域网场景配置指南

本应用提供简化的认证系统，专为家庭局域网场景设计，让孩子们可以轻松登录并使用口算练习功能。

### 快速登录功能

**特点：**

- 只需输入姓名即可登录，无需密码
- 自动创建新用户，首次使用即可进入
- 显示最近使用用户，快速切换账户
- 登录状态持久化2年，无需频繁重新登录

**适用场景：**

- 家庭 WiFi 环境
- 多个孩子共用一台设备（平板等）
- 需要快速切换不同孩子的账户
- 信任度高，无需复杂密码验证

### 使用方法

**1. 首次登录新用户**

```
1. 打开应用
2. 输入孩子姓名（如"小明"）
3. 勾选"记住我的登录状态"
4. 点击"开始答题"
5. 系统自动创建新用户并登录
```

**2. 使用历史用户快速登录**

```
1. 打开应用，显示最近使用列表（最多5个）
2. 点击用户头像或输入新姓名
3. 如果选择历史用户，直接登录
4. 如果是新用户，按首次登录流程
```

**3. 管理员查看统计**

```
1. 使用管理员账号登录后台
2. 进入"今日统计"查看当天数据
3. 进入"排行榜"查看本周/本月排名
4. 进入"用户管理"查看所有孩子进度
5. 可以禁用用户或查看详细历史
```

### 安全建议

**家庭局域网场景：**

- 仅在家庭 WiFi 环境下使用此简化认证
- 通过路由器限制外网访问管理后台
- 定期检查和清理不需要的用户账户
- 教育孩子保护个人隐私

**如果需要更高安全性：**

- 可以在管理后台禁用快速登录用户
- 使用传统用户名+密码方式登录
- 配置更复杂的访问控制策略

### 向后兼容性

**旧用户（有密码的用户）：**

- 仍然可以使用传统的用户名+密码登录
- password_hash 字段保持不变
- 登录流程和功能完全不受影响
- 可以选择性启用快速能登录以简化使用

### 配置文件变更

**JWT 配置更新** (`backend/app/core/config.py`):

```python
JWT_EXPIRE_MINUTES = 525600  # 2年 = 365 * 24 * 60
ACCESS_TOKEN_EXPIRE_MINUTES = 525600  # 2年
```

**数据库变更**:

```sql
-- 将 password_hash 字段改为可空（支持无密码用户）
ALTER TABLE users MODIFY COLUMN password_hash VARCHAR(255) NULL;
```

### 防火墙配置建议

**限制局域网外部的访问：**

```bash
# 仅允许局域网访问（假设局域网网段为 192.168.1.0/24）
# 在路由器防火墙配置中添加规则：

# 允许局域网访问应用端口
iptables -A INPUT -s 192.168.1.0/24 -p tcp --dport 8000 -j ACCEPT
iptables -A INPUT -s 192.168.1.0/24 -p tcp --dport 80 -j ACCEPT

# 拒绝其他外部访问（可选）
iptables -A INPUT -p tcp --dport 8000 -j DROP
iptables -A INPUT -p tcp --dport 80 -j DROP
```

**注意：**

- 根据实际网络环境调整网段和端口
- 在生产环境中建议使用更严格的访问控制
- 可以结合 HTTPS 和额外的认证机制

## API 文档

启动后端后访问：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 开发计划

- [x] 项目初始化
- [x] 数据库设计
- [ ] 用户认证模块
- [ ] 题目管理模块
- [ ] 练习模块
- [ ] 错题本模块
- [ ] 每日任务系统
- [ ] 连胜系统
- [ ] 成就系统
- [ ] 排行榜系统
- [ ] 前端用户端
- [ ] 前端管理端

## 许可证

MIT License
