-- 迁移脚本：修改 users 表 password_hash 字段为 NULLABLE
-- 版本：v1
-- 日期：2026-04-15
-- 说明：支持简化认证，允许无密码用户

-- 将 password_hash 字段从 NOT NULL 修改为 NULL
ALTER TABLE users MODIFY COLUMN password_hash VARCHAR(255) NULL;

-- 验证迁移成功
SELECT 
    COLUMN_NAME,
    IS_NULLABLE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'oral_arithmetic'
    AND TABLE_NAME = 'users'
    AND COLUMN_NAME = 'password_hash';