#!/bin/bash

# 口算练习应用 - 快速部署脚本
# 用法: ./deploy.sh [dev|prod]

set -e  # 遇到错误立即退出

COLOR_GREEN='\033[0;32m'
COLOR_RED='\033[0;31m'
COLOR_YELLOW='\033[1;33m'
COLOR_RESET='\033[0m'

MODE=$1

# 打印彩色日志
log_info() {
    echo -e "${COLOR_GREEN}[INFO]${COLOR_RESET} $1"
}

log_warn() {
    echo -e "${COLOR_YELLOW}[WARN]${COLOR_RESET} $1"
}

log_error() {
    echo -e "${COLOR_RED}[ERROR]${COLOR_RESET} $1"
}

# 检查命令是否存在
check_command() {
    if ! command -v $1 &> /dev/null; then
        log_error "未找到命令: $1，请先安装"
        exit 1
    fi
}

# 1. 检查必要工具
log_info "检查必要工具..."
check_command "docker"
check_command "docker-compose"
log_info "Docker 和 Docker Compose 已安装✓"

# 2. 停止现有容器
log_info "停止现有容器..."
docker-compose down 2>/dev/null || true
docker-compose -f docker-compose.dev.yml down 2>/dev/null || true

# 3. 检查并启动 MySQL
log_info "检查 MySQL 服务..."
if ! mysqladmin ping -h localhost -uroot -p"$MYSQL_ROOT_PASSWORD" 2>/dev/null; then
    log_warn "MySQL 未运行，尝试启动..."
    if command -v brew &> /dev/null; then
        brew services start mysql
    elif command -v systemctl &> /dev/null; then
        sudo systemctl start mysql
    else
        log_error "无法自动启动 MySQL，请手动启动"
        exit 1
    fi
    sleep 3
fi

# 4. 创建数据库
log_info "创建数据库..."
DB_NAME="oral_arithmetic"
if ! mysql -h localhost -uroot -p"$MYSQL_ROOT_PASSWORD" -e "USE $DB_NAME" 2>/dev/null; then
    mysql -h localhost -uroot -p"$MYSQL_ROOT_PASSWORD" -e "CREATE DATABASE $DB_NAME CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
    log_info "数据库 $DB_NAME 已创建"
else
    log_info "数据库 $DB_NAME 已存在"
fi

# 导入数据库结构（可选）
if [ -f "docs/database.sql" ]; then
    read -p "是否导入数据库结构？这将清空现有数据！(y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        log_info "导入数据库结构..."
        mysql -h localhost -uroot -p"$MYSQL_ROOT_PASSWORD" $DB_NAME < docs/database.sql
        log_info "数据库结构已导入"
    fi
fi

# 5. 检查 .env 文件
if [ ! -f "backend/.env" ]; then
    log_warn "未找到 backend/.env 文件，复制模板..."
    cp backend/.env.example backend/.env
    log_info "请编辑 backend/.env 文件，配置数据库密码和 JWT 密钥"
    read -p "按 Enter 键继续..."
fi

# 6. 根据模式启动服务
if [ "$MODE" = "prod" ]; then
    log_info "启动生产环境（前端+后端容器）..."
    docker-compose up -d
    
    log_info "等待服务启动..."
    sleep 5
    
    # 检查后端健康
    if curl -s http://localhost:8000/health > /dev/null; then
        log_info "✅ 后端 API 运行正常: http://localhost:8000"
    else
        log_error "❌ 后端 API 启动失败"
        docker-compose logs backend
        exit 1
    fi
    
    log_info "✅ 前端已启动: http://localhost"
    log_info "✅ 后端文档: http://localhost:8000/docs"
    
elif [ "$MODE" = "dev" ]; then
    log_info "启动开发环境（后端容器 + 本地前端）..."
    docker-compose -f docker-compose.dev.yml up -d
    
    sleep 5
    
    if curl -s http://localhost:8000/health > /dev/null; then
        log_info "✅ 后端 API 运行正常: http://localhost:8000"
    else
        log_error "❌ 后端 API 启动失败"
        docker-compose -f docker-compose.dev.yml logs backend
        exit 1
    fi
    
    # 启动前端
    log_info "启动前端开发服务器..."
    cd frontend-user
    if [ ! -d "node_modules" ]; then
        log_info "安装前端依赖..."
        npm install
    fi
    npm run dev &
    FRONTEND_PID=$!
    cd ..
    
    log_info "✅ 前端运行: http://localhost:3000"
    log_info "前端 PID: $FRONTEND_PID"
    log_info "按 Ctrl+C 停止所有服务"
    
    # 等待中断
    wait $FRONTEND_PID
    
else
    log_error "用法: $0 [dev|prod]"
    echo "  dev  - 开发环境（后端容器 + 前端本地热重载）"
    echo "  prod - 生产环境（所有服务容器化）"
    exit 1
fi

log_info "部署完成！"
