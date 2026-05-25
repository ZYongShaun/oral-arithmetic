# Spec: Long-lived JWT Tokens

## 新增需求

### 需求：系统必须支持2年有效期的 JWT token
系统必须将所有认证接口生成的 JWT token 过期时间延长到至少2年。

#### 场景：快速登录生成2年有效期token
- **当** 用户通过快速登录成功验证
- **那么** 系统必须生成 JWT token
- **并且** token 的 exp（过期时间）claim 必须设置为当前时间加上2年
- **并且** token 必须包含用户ID作为 sub claim

#### 场景：传统登录生成2年有效期token
- **当** 用户通过传统用户名+密码登录成功
- **那么** 系统必须生成 JWT token
- **并且** token 的 exp（过期时间）claim 必须设置为当前时间加上2年

---

### 需求：系统必须验证长期 token 的有效性
系统必须能够验证2年期 JWT token，并在未过期时通过验证。

#### 场景：验证1年前颁发的2年期token
- **当** 用户在1年前登录并现在访问受保护资源
- **并且** 提供的 JWT token 尚未过期
- **那么** 系统必须接受该 token
- **并且** 系统必须从 token 中解码出用户ID
- **并且** 系统不得返回 401 Unauthorized 错误

#### 场景：拒绝已过期的2年期token
- **当** 用户在2年1天后访问受保护资源
- **并且** 提供的 JWT token 已经过期
- **那么** 系统必须拒绝该 token
- **并且** 系统必须返回 401 Unauthorized 状态码
- **并且** 系统必须在响应头中包含 `WWW-Authenticate: Bearer`

---

### 需求：系统必须允许管理员禁用用户以撤销其访问权限
即使 JWT token 有效期未到，管理员仍应能通过禁用用户账户来撤销其访问权限。

#### 场景：管理员禁用用户
- **当** 管理员调用用户禁用接口，将用户 status 设置为 0
- **并且** 该用户持有有效的2年期 JWT token
- **那么** 系统必须立即更新用户 status 字段为 0
- **并且** 用户下次使用该 token 访问时必须被拒绝

#### 场景：被禁用用户尝试访问
- **当** status=0（禁用）的用户使用有效 JWT token 访问受保护资源
- **那么** 系统必须拒绝该请求
- **并且** 系统必须返回 401 Unauthorized 状态码
- **并且** 系统必须在响应中包含错误详情"User account is disabled"

---

## 修改需求

### 需求：JWT 配置必须更新为长期有效期
系统的 JWT 配置参数必须从短有效期（2小时）更新为长期有效期（2年）。

#### 场景：JWT 配置参数更新
- **当** 系统加载配置文件
- **那么** `JWT_EXPIRE_MINUTES` 配置项必须设置为 525600（2年 = 365 × 24 × 60）
- **并且** `ACCESS_TOKEN_EXPIRE_MINUTES` 配置项必须设置相同的值
- **当** 快速登录或传统登录生成 token 时
- **那么** 系统必须使用上述配置项计算过期时间

---

### 需求：token 验证逻辑必须检查用户状态
系统在验证 JWT token 时，除了检查 token 签名和过期时间，还必须检查用户账户状态。

#### 场景：验证token时检查用户状态
- **当** 系统验证提供的 JWT token
- **那么** 系统必须验证 token 签名
- **并且** 系统必须验证 token 未过期
- **并且** 系统必须从数据库查询该用户记录
- **并且** 系统必须检查用户 status 字段是否为 1（启用）
- **并且** 如果 status 不为 1，系统必须拒绝访问

---

### 需求：前端必须持久化长期 token
前端必须将收到的长期 JWT token 无限期存储在 localStorage 中，不设置自动清除。

#### 场景：保存长期token到localStorage
- **当** 前端收到登录成功响应
- **那么** 前端必须将 `access_token` 保存到 localStorage
- **并且** 前端不得设置任何过期时间或定时清除机制
- **并且** 前端必须在每次页面加载时检查 localStorage 中的 token

#### 场景：长期token失败时的处理
- **当** 前端使用 localStorage 中的 token 发起请求
- **并且** 服务器返回 401 Unauthorized
- **那么** 前端必须清除 localStorage 中的 token 和用户信息
- **并且** 前端必须跳转到登录页面

---

### 需求：数据库密码字段必须允许 NULL
数据库 users 表的 password_hash 字段必须从 NOT NULL 修改为 NULLABLE，以支持无密码用户。

#### 场景：数据库密码字段允许NULL
- **当** 快速登录创建新用户时
- **那么** 系统必须在 users 表中插入记录，password_hash 字段值为 NULL
- **当** 传统登录创建用户时
- **那么** 系统必须将 password_hash 设置为 bcrypt 加密的密码字符串

#### 场景：修改密码字段约束
- **当** 执行数据库迁移脚本
- **那么** 脚本必须执行 `ALTER TABLE users MODIFY COLUMN password_hash VARCHAR(255) NULL`
- **并且** 现有记录的 password_hash 值必须保持不变

---

## 移除需求

### 需求：短有效期 JWT token（2小时）
**Reason**: 为了支持家庭局域网的简化使用场景，将JWT有效期从2小时延长到2年，避免频繁重新登录。
**Migration**: 修改配置文件中的 `JWT_EXPIRE_MINUTES` 从 120 改为 525600，同时修改 `ACCESS_TOKEN_EXPIRE_MINUTES` 为相同值。所有用户下次登录时将自动获得新的2年期token。

---

## 规格说明

### 配置参数

#### 新的 JWT 配置值
```python
# backend/app/core/config.py
class Settings(BaseSettings):
    # JWT 配置
    JWT_SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 525600  # 2年 = 365 * 24 * 60
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 525600  # 2年
```

#### 计算逻辑
```
2年 = 365天 × 24小时 × 60分钟 = 525,600 分钟
```

---

### Token Payload 结构

#### JWT Claims
```json
{
  "sub": 123,              // 用户ID (subject)
  "exp": 1735897200,      // 过期时间戳 (Unix timestamp)
  "iat": 1672735200       // 签发时间戳 (可选)
}
```

#### 示例：2年期 token 的 exp 值
```javascript
// 签发时间：2024年1月1日 00:00:00 UTC
// 过期时间：2026年1月1日 00:00:00 UTC
const now = Math.floor(Date.now() / 1000);  // 1704067200
const exp = now + (2 * 365 * 24 * 60 * 60); // 1704067200 + 63072000 = 1767139200
```

---

### 数据库迁移脚本

#### MySQL 迁移命令
```sql
-- 将 password_hash 字段从 NOT NULL 修改为 NULLABLE
ALTER TABLE users
MODIFY COLUMN password_hash VARCHAR(255) NULL;
```

#### 适用场景
- 现有系统的数据库升级
- 从有密码模式迁移到密码可选模式

---

### API 行为变化

#### 登录接口响应时间（无变化）
- 响应时间：< 500ms
- Token 生成时间：< 10ms

#### Token 验证性能（略有增加）
- 每次验证需要额外的数据库查询：`SELECT * FROM users WHERE id = ?`
- 预期额外延迟：< 50ms
- 建议添加用户缓存以优化性能

---

### 安全考虑

#### 长期 token 的风险缓解
1. **用户状态检查**：每次验证时检查 status 字段，允许管理员撤销
2. **密钥轮换**：建议定期更换 JWT_SECRET_KEY（需要通知用户重新登录）
3. **设备指纹**：如需要，可添加设备指纹限制 token 使用范围

#### 数据库查询优化
```python
# 当前实现（每次验证都查询数据库）
user = db.query(User).filter(User.id == user_id).first()

# 优化建议（可选）：添加Redis缓存
cached_user = redis.get(f"user:{user_id}")
if not cached_user:
    cached_user = db.query(User).filter(User.id == user_id).first()
    redis.set(f"user:{user_id}", json.dumps(cached_user), ex=300)  # 5分钟缓存
```

---

### 实施检查清单

- [ ] 修改 `backend/app/core/config.py` 中的 `JWT_EXPIRE_MINUTES` 为 525600
- [ ] 修改 `backend/app/core/config.py` 中的 `ACCESS_TOKEN_EXPIRE_MINUTES` 为 525600
- [ ] 更新 `backend/app/services/auth_service.py` 中的 `get_current_user()` 函数检查用户 status
- [ ] 执行数据库迁移脚本，将 password_hash 字段改为 NULLABLE
- [ ] 验证 fast_login 生成的 token 过期时间为2年
- [ ] 验证传统 login 生成的 token 过期时间为2年
- [ ] 测试2年期token在未过期时有效
- [ ] 测试2年期token在过期时被拒绝
- [ ] 测试管理员禁用用户后，token立即失效
- [ ] 验证前端 localStorage 不自动清除 token

---

### 性能测试场景

1. **Token 生成性能**
   - 输入：1000次并发登录请求
   - 预期：平均响应时间 < 200ms

2. **Token 验证性能**
   - 输入：1000次并发API请求（携带token）
   - 预期：平均响应时间 < 300ms（含用户状态查询）

3. **长期token有效性**
   - 输入：生成token，等待1个月
   - 预期：token 仍然有效

---

### 兼容性保证

#### 向后兼容
- 旧用户（有密码）可以继续使用传统登录
- 已存在的 password_hash 值不受影响
- 旧的2小时 token 过期后自动失效

#### 向前兼容
- 新用户（无密码）必须使用快速登录
- password_hash 为 NULL 的用户无法使用传统密码登录
