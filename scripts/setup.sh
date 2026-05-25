#!/bin/bash

# 小学口算应用 - 初始化脚本
# 使用方法：bash scripts/setup.sh

set -e

echo "========== 口算练习应用初始化 =========="

# 检查 Python
echo "1. 检查 Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | awk '{print $2}')
    echo "   Python 版本: $PYTHON_VERSION"
else
    echo "   未找到 Python3，请先安装 Python 3.9+"
    exit 1
fi

# 检查 Node.js
echo "2. 检查 Node.js..."
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo "   Node.js 版本: $NODE_VERSION"
else
    echo "   未找到 Node.js，请先安装 Node.js 16+"
    exit 1
fi

# 检查 MySQL
echo "3. 检查 MySQL..."
if command -v mysql &> /dev/null; then
    echo "   MySQL 已安装"
    echo "   请确保 MySQL 8.0+ 正在运行"
else
    echo "   未找到 MySQL，请先安装 MySQL 8.0+"
    exit 1
fi

# 创建虚拟环境
echo "4. 创建 Python 虚拟环境..."
cd backend
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "   虚拟环境已创建"
else
    echo "   虚拟环境已存在"
fi

# 激活虚拟环境并安装依赖
echo "5. 安装后端依赖..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
deactivate

cd ..

# 安装前端依赖
echo "6. 安装前端依赖..."
cd frontend-user
if [ ! -d "node_modules" ]; then
    npm install
else
    echo "   node_modules 已存在"
fi
cd ..

cd frontend-admin
if [ ! -d "node_modules" ]; then
    npm install
else
    echo "   node_modules 已存在"
fi
cd ..

echo ""
echo "========== 初始化完成 =========="
echo ""
echo "接下来请按以下步骤操作："
echo ""
echo "【数据库初始化】"
echo "1. 登录 MySQL: mysql -u root -p"
echo "2. 执行建表脚本: source docs/database.sql"
echo ""
echo "【配置修改】"
echo "1. 复制后端配置: cp backend/.env.example backend/.env"
echo "2. 修改 backend/.env 中的数据库密码"
echo ""
echo "【启动应用】"
echo "启动后端服务："
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "启动用户前端："
echo "  cd frontend-user"
echo "  npm run dev"
echo ""
echo "启动管理前端："
echo "  cd frontend-admin"
echo "  npm run dev"
echo ""
echo "访问地址："
echo "  后端 API: http://localhost:8000"
echo "  API 文档: http://localhost:8000/docs"
echo "  用户前端: http://localhost:3000"
echo "  管理前端: http://localhost:3001"
echo ""
