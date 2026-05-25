-- 小学一年级口算练习应用 - 数据库建表脚本
-- 数据库：oral_arithmetic
-- 版本：v5.0
-- 创建时间：2026-04-13

-- 创建数据库
CREATE DATABASE IF NOT EXISTS oral_arithmetic DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE oral_arithmetic;

-- 1. 用户表（家长）
CREATE TABLE users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL COMMENT '用户名',
    phone VARCHAR(20) UNIQUE COMMENT '手机号',
    password_hash VARCHAR(255) NOT NULL COMMENT '密码哈希',
    nickname VARCHAR(50) COMMENT '昵称',
    status TINYINT DEFAULT 1 COMMENT '状态：1-正常 0-禁用',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_username (username),
    INDEX idx_phone (phone)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

-- 2. 孩子档案表
CREATE TABLE children (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL COMMENT '家长用户 ID',
    name VARCHAR(50) NOT NULL COMMENT '孩子姓名',
    gender TINYINT COMMENT '性别：1-男 2-女',
    birth_date DATE COMMENT '出生日期',
    grade VARCHAR(20) DEFAULT '一年级' COMMENT '年级',
    is_active TINYINT DEFAULT 1 COMMENT '是否激活',
    total_stars INT DEFAULT 0 COMMENT '累计星星数',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='孩子档案表';

-- 3. 管理员表
CREATE TABLE admins (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL COMMENT '用户名',
    password_hash VARCHAR(255) NOT NULL COMMENT '密码哈希',
    real_name VARCHAR(50) COMMENT '真实姓名',
    role TINYINT DEFAULT 1 COMMENT '角色：1-普通 2-超级',
    status TINYINT DEFAULT 1 COMMENT '状态',
    last_login_at TIMESTAMP COMMENT '最后登录时间',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='管理员表';

-- 4. 系统配置表
CREATE TABLE system_configs (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    config_key VARCHAR(50) UNIQUE NOT NULL COMMENT '配置键',
    config_value VARCHAR(255) NOT NULL COMMENT '配置值',
    description VARCHAR(255) COMMENT '描述',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='系统配置表';

-- 初始化系统配置
INSERT INTO system_configs (config_key, config_value, description) VALUES
('daily_task_target', '3', '每日任务目标次数'),
('daily_task_stars', '10', '完成每日任务获得星星数'),
('practice_stars_rule', '3,2,1', '星星奖励规则：100% 正确得 3 星，80% 得 2 星，60% 得 1 星'),
('streak_shield_cost', '50', '连胜保护罩价格（星星）');

-- 5. 题目录
CREATE TABLE questions (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    level TINYINT NOT NULL COMMENT '难度等级：10/20/50/100',
    type TINYINT NOT NULL COMMENT '题型：1-加法 2-减法 3-混合',
    question_text VARCHAR(100) NOT NULL COMMENT '题目文本',
    answer INT NOT NULL COMMENT '正确答案',
    source TINYINT DEFAULT 1 COMMENT '来源：1-系统生成 2-人工录入',
    status TINYINT DEFAULT 1 COMMENT '状态：1-启用 0-禁用',
    difficulty FLOAT DEFAULT 0.5 COMMENT '难度系数 0-1',
    usage_count INT DEFAULT 0 COMMENT '使用次数',
    correct_count INT DEFAULT 0 COMMENT '正确次数',
    created_by BIGINT COMMENT '创建人 ID',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_level (level),
    INDEX idx_type (type),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='题目录';

-- 6. 练习记录表
CREATE TABLE practices (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    child_id BIGINT NOT NULL COMMENT '孩子 ID',
    level TINYINT NOT NULL COMMENT '难度等级',
    total_questions INT DEFAULT 20 COMMENT '题目总数',
    correct_count INT DEFAULT 0 COMMENT '正确题数',
    wrong_count INT DEFAULT 0 COMMENT '错误题数',
    total_time INT COMMENT '总用时（秒）',
    avg_time FLOAT COMMENT '平均用时（秒）',
    accuracy FLOAT COMMENT '正确率',
    stars_earned INT DEFAULT 0 COMMENT '本关获得星星',
    start_time TIMESTAMP NOT NULL COMMENT '开始时间',
    end_time TIMESTAMP COMMENT '结束时间',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (child_id) REFERENCES children(id) ON DELETE CASCADE,
    INDEX idx_child_id (child_id),
    INDEX idx_start_time (start_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='练习记录表';

-- 7. 练习详情表
CREATE TABLE practice_details (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    practice_id BIGINT NOT NULL COMMENT '练习记录 ID',
    question_id BIGINT NOT NULL COMMENT '题目 ID',
    question_text VARCHAR(100) NOT NULL COMMENT '题目文本',
    user_answer INT COMMENT '用户答案',
    correct_answer INT NOT NULL COMMENT '正确答案',
    is_correct TINYINT DEFAULT 0 COMMENT '是否正确',
    answer_time INT COMMENT '答题用时（秒）',
    question_order INT COMMENT '题目序号',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (practice_id) REFERENCES practices(id) ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES questions(id),
    INDEX idx_practice_id (practice_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='练习详情表';

-- 8. 错题表
CREATE TABLE wrong_questions (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    child_id BIGINT NOT NULL COMMENT '孩子 ID',
    question_id BIGINT NOT NULL COMMENT '题目 ID',
    question_text VARCHAR(100) NOT NULL COMMENT '题目文本',
    correct_answer INT NOT NULL COMMENT '正确答案',
    level TINYINT NOT NULL COMMENT '难度等级',
    wrong_count INT DEFAULT 1 COMMENT '错误次数',
    last_wrong_time TIMESTAMP COMMENT '最后错误时间',
    is_mastered TINYINT DEFAULT 0 COMMENT '是否已掌握',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (child_id) REFERENCES children(id) ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES questions(id),
    UNIQUE KEY uk_child_question (child_id, question_id),
    INDEX idx_child_id (child_id),
    INDEX idx_mastered (is_mastered)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='错题表';

-- 9. 每日任务表
CREATE TABLE daily_tasks (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    child_id BIGINT NOT NULL COMMENT '孩子 ID',
    task_date DATE NOT NULL COMMENT '任务日期',
    target_count INT DEFAULT 3 COMMENT '目标次数',
    completed_count INT DEFAULT 0 COMMENT '已完成次数',
    is_completed TINYINT DEFAULT 0 COMMENT '是否完成',
    stars_earned INT DEFAULT 0 COMMENT '获得的星星数',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (child_id) REFERENCES children(id) ON DELETE CASCADE,
    UNIQUE KEY uk_child_date (child_id, task_date),
    INDEX idx_task_date (task_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='每日任务表';

-- 10. 连胜记录表
CREATE TABLE streaks (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    child_id BIGINT NOT NULL COMMENT '孩子 ID',
    current_streak INT DEFAULT 0 COMMENT '当前连胜次数',
    best_streak INT DEFAULT 0 COMMENT '历史最高连胜',
    last_practice_at TIMESTAMP COMMENT '上次练习时间',
    shields INT DEFAULT 0 COMMENT '保护罩数量',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (child_id) REFERENCES children(id) ON DELETE CASCADE,
    UNIQUE KEY uk_child (child_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='连胜记录表';

-- 11. 成就表
CREATE TABLE achievements (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    achievement_key VARCHAR(50) UNIQUE NOT NULL COMMENT '成就键',
    name VARCHAR(100) NOT NULL COMMENT '成就名称',
    description VARCHAR(255) COMMENT '成就描述',
    category VARCHAR(20) COMMENT '分类：practice/streak/difficulty/speed',
    requirement INT COMMENT '达成条件数值',
    reward_stars INT DEFAULT 0 COMMENT '奖励星星数',
    badge_icon VARCHAR(255) COMMENT '徽章图标 URL',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='成就表';

-- 成就进度表
CREATE TABLE child_achievements (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    child_id BIGINT NOT NULL COMMENT '孩子 ID',
    achievement_id BIGINT NOT NULL COMMENT '成就 ID',
    progress INT DEFAULT 0 COMMENT '当前进度',
    is_completed TINYINT DEFAULT 0 COMMENT '是否已完成',
    completed_at TIMESTAMP COMMENT '完成时间',
    FOREIGN KEY (child_id) REFERENCES children(id) ON DELETE CASCADE,
    FOREIGN KEY (achievement_id) REFERENCES achievements(id),
    UNIQUE KEY uk_child_achievement (child_id, achievement_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='成就进度表';

-- 12. 排行榜表
CREATE TABLE leaderboards (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    season_week INT NOT NULL COMMENT '赛季周数',
    child_id BIGINT NOT NULL COMMENT '孩子 ID',
    group_level TINYINT DEFAULT 1 COMMENT '小组等级：1-青铜 2-白银...',
    weekly_stars INT DEFAULT 0 COMMENT '本周获得星星',
    rank INT COMMENT '当前排名',
    is_promoted TINYINT DEFAULT 0 COMMENT '是否晋级',
    is_demoted TINYINT DEFAULT 0 COMMENT '是否降级',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (child_id) REFERENCES children(id) ON DELETE CASCADE,
    UNIQUE KEY uk_child_week (child_id, season_week),
    INDEX idx_season_week (season_week)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='排行榜表';

-- 13. 星星流水表
CREATE TABLE star_transactions (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    child_id BIGINT NOT NULL COMMENT '孩子 ID',
    change_type VARCHAR(20) NOT NULL COMMENT '类型：earn/spend',
    source VARCHAR(50) NOT NULL COMMENT '来源：practice/task/achievement/ranking/shop',
    stars INT NOT NULL COMMENT '变动数量（正数增加，负数减少）',
    balance_after INT COMMENT '变动后余额',
    description VARCHAR(255) COMMENT '描述',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (child_id) REFERENCES children(id) ON DELETE CASCADE,
    INDEX idx_child_id (child_id),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='星星流水表';

-- 14. 操作日志表
CREATE TABLE operation_logs (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    admin_id BIGINT COMMENT '管理员 ID',
    operation VARCHAR(100) NOT NULL COMMENT '操作类型',
    module VARCHAR(50) COMMENT '模块',
    content TEXT COMMENT '操作内容',
    ip_address VARCHAR(50) COMMENT 'IP 地址',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (admin_id) REFERENCES admins(id),
    INDEX idx_admin_id (admin_id),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='操作日志表';

-- 插入默认管理员账号（密码：admin123，需要 bcrypt 加密）
-- 注意：实际密码需要使用 bcrypt 加密后插入
INSERT INTO admins (username, password_hash, real_name, role) VALUES
('admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzS3MebAJu', '系统管理员', 2);

-- 插入示例成就数据
INSERT INTO achievements (achievement_key, name, description, category, requirement, reward_stars) VALUES
('first_practice', '初次尝试', '完成第 1 次练习', 'practice', 1, 5),
('practice_10', '坚持不懈', '累计完成 10 次练习', 'practice', 10, 10),
('practice_50', '练习达人', '累计完成 50 次练习', 'practice', 50, 25),
('practice_100', '口算大师', '累计完成 100 次练习', 'practice', 100, 50),
('perfect_1', '完美表现', '单次练习 100% 正确', 'practice', 1, 10),
('perfect_10', '十全十美', '累计 10 次 100% 正确', 'practice', 10, 50),
('streak_3', '小火苗', '连胜 3 次', 'streak', 3, 10),
('streak_7', '热情似火', '连胜 7 次', 'streak', 7, 25),
('streak_15', '势不可挡', '连胜 15 次', 'streak', 15, 50),
('streak_30', '传奇之路', '连胜 30 次', 'streak', 30, 100);

-- 插入示例题目（10 以内加法）
INSERT INTO questions (level, type, question_text, answer, source) VALUES
(10, 1, '1 + 2 = ?', 3, 1),
(10, 1, '3 + 4 = ?', 7, 1),
(10, 1, '5 + 2 = ?', 7, 1),
(10, 1, '6 + 3 = ?', 9, 1),
(10, 1, '4 + 5 = ?', 9, 1),
(10, 2, '5 - 2 = ?', 3, 1),
(10, 2, '8 - 3 = ?', 5, 1),
(10, 2, '7 - 4 = ?', 3, 1),
(10, 2, '9 - 5 = ?', 4, 1),
(10, 2, '6 - 2 = ?', 4, 1);
