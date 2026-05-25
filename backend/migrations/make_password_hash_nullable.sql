-- Migration: Make password_hash nullable for quick login support
-- Description: Allows users to log in without password while maintaining backward compatibility

-- Modify password_hash column to accept NULL values
ALTER TABLE users MODIFY COLUMN password_hash VARCHAR(255) NULL;

-- Verify the change
DESCRIBE users;

-- Note: This migration is safe for existing users:
-- - Users with existing passwords will keep their password_hash
-- - New users created via quick_login will have password_hash = NULL
