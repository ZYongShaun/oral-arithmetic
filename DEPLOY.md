# 快速部署指南

## 新电脑部署步骤

### 1️⃣ 环境准备
```bash
# 安装 Docker Desktop (https://www.docker.com/products/docker-desktop)
# 安装 Git
# 确保 MySQL 已安装并运行
```

### 2️⃣ 传输代码
```bash
# 克隆仓库或复制文件到新电脑
git clone <仓库地址>
cd oral-arithmetic
```

### 3️⃣ 修改配置
编辑 `backend/.env`:
```bash
DATABASE_PASSWORD=你的MySQL密码
JWT_SECRET_KEY=任意密钥（至少32位）
```

### 6️⃣ 一键部署

### 5️⃣ 访问应用
- 开发模式：前端 http://localhost:3000，后端 http://localhost:8000
- 生产模式：前端 http://localhost，后端 http://localhost:8000

## 数据库迁移步骤

### 快速登录功能所需的数据库变更

本项目的简化认证系统（快速登录）需要对现有数据库进行以下迁移：

#### 1. 修改用户表密码字段
```sql
-- 连接到数据库
mysql -u root -p oral_arithmetic

-- 将 password_hash 字段改为可空，以支持无密码的快速登录用户
ALTER TABLE users MODIFY COLUMN password_hash VARCHAR(255) NULL;

-- 验证更改
DESCRIBE users;
```

#### 2. 验证现有数据不受影响
```sql
-- 检查现有用户的 password_hash 是否仍然有效
SELECT id, username, password_hash IS NOT NULL as has_password, status
FROM users;

-- 确认现有有密码的用户的 password_hash 没有变化
SELECT COUNT(*) as users_with_password FROM users WHERE password_hash IS NOT NULL;
```

#### 3. 添加性能优化索引（可选）
```sql
-- 为用户历史查询添加复合索引
-- 如果表中的数据量很大，这可以显著提高查询性能
--
-- practices 表索引（用户历史统计）
CREATE INDEX idx_practices_user_date ON practices(user_id, DATE(created_at));

-- 验证索引创建
SHOW INDEX FROM practices;
```

### JWT 配置更新说明

**重要变更：**
- JWT 过期时间从 2 小时延长到 2 年
- 这是为了简化家庭局域网场景的用户体验
- 仍然保留了 token 撤销能力（通过禁用用户）

**配置文件位置：** `backend/app/core/config.py`
```python
# JWT 配置（已更新）
JWT_SECRET_KEY: str = "your-secret-key-change-in-production"
JWT_ALGORITHM: str = "HS256"
JWT_EXPIRE_MINUTES: int = 525600  # 2年 = 365 * 24 * 60 ⚠️ 新值
ACCESS_TOKEN_EXPIRE_MINUTES: int = 525600  # 2年 ⚠️ 新值
```

### 向后兼容性保证

**确认事项：**
1. ✅ 现有用户（有密码的用户）仍然可以正常登录
2. ✅ password_hash 字段不会丢失，只是变为可空
3. ✅ 传统登录接口 `/api/v1/auth/login` 仍然可用
4. ✅ 所有现有功能不受影响

**测试步骤：**
1. 使用现有的用户名和密码登录，确认成功
2. 验证数据库中的 password_hash 没有变化
3. 检查现有的用户权限和配置仍然有效

### 防火墙配置建议

**对于家庭局域网场景：**
```bash
# 建议：限制外网访问管理后台
# 在路由器配置中添加规则，仅允许局域网IP访问
#
# 示例：仅允许 192.168.1.0/24 网段访问
# - 允许局域网IP访问端口8000和80
# - 阻止外部IP访问这些端口
#
# 具体配置取决于你使用的路由器型号和网络环境
```

**生产环境注意事项：**
- 如果部署到公网，必须使用 HTTPS
- 考虑实施额外的访问控制
- 定期审查用户权限和访问日志

## 常见问题

### MySQL 连接失败
- 确认 MySQL 已启动: `mysqladmin ping -uroot`
- 检查密码是否正确
- Docker 访问宿主机 MySQL 使用 `host.docker.internal`

### 端口占用
```bash
# 查看端口占用
lsof -i :8000
lsof -i :80

# 停止现有服务
docker-compose down
```

### 停止所有服务
```bash
# 开发模式
./deploy.sh dev  # 按 Ctrl+C

# 生产模式
docker-compose down

# 强制停止
docker-compose down -v
```

## 文件说明

- `deploy.sh` - 自动化部署脚本
- `docker-compose.yml` - 生产环境配置
- `docker-compose.dev.yml` - 开发环境配置
- `backend/Dockerfile` - 后端容器配置
- `frontend-user/Dockerfile` - 前端容器配置
- `frontend-user/nginx.conf` - 前端 Nginx 配置

详细文档请参考 README-DOCKER.md
