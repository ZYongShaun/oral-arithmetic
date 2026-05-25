# Docker 部署指南

## 前提条件
- 安装 Docker Desktop
- 安装 Docker Compose

## 项目结构
```
oral-arithmetic/
├── backend/                  # 后端 FastAPI 应用
│   └── Dockerfile
├── frontend-user/           # 前端 Vue 3 应用  
│   ├── Dockerfile
│   └── nginx.conf
├── docker-compose.yml       # 生产环境部署
└── docker-compose.dev.yml   # 开发环境部署
```

## 快速开始

### 1. 开发环境（推荐）
```bash
# 启动后端 + MySQL（不含前端容器）
docker-compose -f docker-compose.dev.yml up

# 或者后台运行
docker-compose -f docker-compose.dev.yml up -d
```

前端需要单独运行：
```bash
cd frontend-user
npm install
npm run dev
```

### 2. 生产环境
```bash
# 启动所有服务（前端 + 后端 + MySQL）
docker-compose up -d

# 启动完成
访问 http://localhost 即可看到前端界面
```

## 服务说明
- **MySQL** (端口 3306): 数据库服务
- **Backend** (端口 8000): FastAPI API 服务
- **Frontend** (端口 80): Vue 3 静态文件服务

## 访问地址
- 前端界面: http://localhost
- 后端 API: http://localhost:8000
- API 文档: http://localhost:8000/docs
- 数据库: localhost:3306

## 常用命令

```bash
# 启动服务
docker-compose up -d

# 停止服务
docker-compose stop

# 重启服务
docker-compose restart

# 查看日志
docker-compose logs -f [service_name]

# 进入容器
docker-compose exec backend /bin/bash
docker-compose exec mysql mysql -uroot -p

# 删除所有容器和网络
docker-compose down

# 删除容器、网络、数据卷
docker-compose down -v
```

## 开发环境说明
开发环境配置文件 `docker-compose.dev.yml` 只包含 MySQL 和 Backend 服务，前端需要单独本地运行，便于实时查看代码修改效果。

## 生产环境说明
生产环境配置文件 `docker-compose.yml` 包含完整的三个服务，前端使用 Nginx 托管静态文件，适合部署到生产服务器。

## 环境变量
可以在 `docker-compose.yml` 中修改以下配置：
- MySQL 密码
- JWT 密钥
- 数据库连接信息

## 故障排查

### 数据库连接失败
```bash
# 检查 MySQL 是否正常运行
docker-compose ps mysql
docker-compose logs mysql
```

### 前端无法访问后端
检查前端 nginx.conf 中的 proxy_pass 配置是否正确

### 容器无法启动
```bash
# 查看详细日志
docker-compose logs [service_name]
```

## 数据持久化
MySQL 数据存储在 Docker volume 中，即使删除容器数据也不会丢失。如需完全清理，使用 `docker-compose down -v`。
