-- ClimbTrack 数据库设计
-- 基于现有功能需求设计的完整数据库表结构

-- 1. 用户表 (Users)
-- 存储用户的基本信息和登录凭据
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,  -- 存储加密后的密码
    email VARCHAR(100) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    last_login TIMESTAMP
);

-- 2. 用户资料表 (User Profiles)
-- 存储用户的详细资料和偏好设置
CREATE TABLE user_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    display_name VARCHAR(100),
    shoe_size VARCHAR(10),
    preferred_wall_type VARCHAR(50),  -- 'Overhang', 'Slab', 'Vertical'等
    bio TEXT,
    profile_image VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 3. 攀岩会话表 (Climbing Sessions)
-- 存储每次攀岩会话的基本信息
CREATE TABLE climbing_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    session_date DATE NOT NULL,
    start_time TIME,
    end_time TIME,
    location VARCHAR(100),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 4. 攀登记录表 (Climb Logs)
-- 存储每个具体的攀登尝试记录
CREATE TABLE climb_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    climb_name VARCHAR(100),  -- 线路名称
    climb_type VARCHAR(20) NOT NULL,  -- 'bouldering' 或 'sport'
    grade VARCHAR(20) NOT NULL,  -- V4, 6b+, 5.11a等
    attempt_result VARCHAR(20),  -- 'flash', 'redpoint', 'onsight', 'failed'等
    attempts_count INTEGER DEFAULT 1,
    image_filename VARCHAR(255),
    notes TEXT,
    difficulty_rating INTEGER CHECK(difficulty_rating >= 1 AND difficulty_rating <= 10),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES climbing_sessions(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 5. 媒体文件表 (Media Files)
-- 存储上传的图片和视频文件信息
CREATE TABLE media_files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    climb_log_id INTEGER,
    user_id INTEGER NOT NULL,
    filename VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255),
    file_type VARCHAR(20) NOT NULL,  -- 'image', 'video'
    file_size INTEGER,
    file_path VARCHAR(500) NOT NULL,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (climb_log_id) REFERENCES climb_logs(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 6. 个人最佳记录表 (Personal Bests)
-- 存储用户各类型攀登的最佳成绩
CREATE TABLE personal_bests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    climb_type VARCHAR(20) NOT NULL,  -- 'bouldering', 'sport'
    best_grade VARCHAR(20) NOT NULL,
    climb_log_id INTEGER,  -- 关联到具体的攀登记录
    achieved_date DATE NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (climb_log_id) REFERENCES climb_logs(id) ON DELETE SET NULL,
    UNIQUE(user_id, climb_type)
);

-- 7. 统计数据表 (User Statistics)
-- 存储用户的各种统计数据
CREATE TABLE user_statistics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    total_sessions INTEGER DEFAULT 0,
    total_climbs INTEGER DEFAULT 0,
    sessions_this_month INTEGER DEFAULT 0,
    sessions_this_year INTEGER DEFAULT 0,
    last_calculated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE(user_id)
);

-- 8. 场馆信息表 (Gym/Location)
-- 存储攀岩场馆信息
CREATE TABLE climbing_gyms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    address TEXT,
    phone VARCHAR(20),
    website VARCHAR(255),
    opening_hours TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 9. 场馆拥挤度检测表 (Crowd Detection)
-- 存储场馆人流量检测数据
CREATE TABLE crowd_detection (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    gym_id INTEGER,
    detection_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    people_count INTEGER NOT NULL,
    activity_level VARCHAR(20),  -- 'low', 'medium', 'high'
    image_filename VARCHAR(255),
    notes TEXT,
    FOREIGN KEY (gym_id) REFERENCES climbing_gyms(id) ON DELETE SET NULL
);

-- 10. 动作笔记表 (Movement Notes)
-- 存储攀登技巧和动作笔记
CREATE TABLE movement_notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    climb_log_id INTEGER,
    title VARCHAR(200),
    content TEXT NOT NULL,
    movement_type VARCHAR(50),  -- 'technique', 'beta', 'training'等
    tags TEXT,  -- JSON格式存储标签
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (climb_log_id) REFERENCES climb_logs(id) ON DELETE SET NULL
);

-- 创建索引以提高查询性能
CREATE INDEX idx_climb_logs_user_id ON climb_logs(user_id);
CREATE INDEX idx_climb_logs_session_id ON climb_logs(session_id);
CREATE INDEX idx_climb_logs_type_grade ON climb_logs(climb_type, grade);
CREATE INDEX idx_climbing_sessions_user_date ON climbing_sessions(user_id, session_date);
CREATE INDEX idx_personal_bests_user_type ON personal_bests(user_id, climb_type);
CREATE INDEX idx_crowd_detection_time ON crowd_detection(detection_time);
CREATE INDEX idx_media_files_climb_log ON media_files(climb_log_id);

-- 创建视图以便于查询常用数据
CREATE VIEW user_climbing_summary AS
SELECT 
    u.id as user_id,
    u.username,
    up.display_name,
    COUNT(DISTINCT cs.id) as total_sessions,
    COUNT(cl.id) as total_climbs,
    pb_bouldering.best_grade as bouldering_max,
    pb_sport.best_grade as sport_max
FROM users u
LEFT JOIN user_profiles up ON u.id = up.user_id
LEFT JOIN climbing_sessions cs ON u.id = cs.user_id
LEFT JOIN climb_logs cl ON u.id = cl.user_id
LEFT JOIN personal_bests pb_bouldering ON u.id = pb_bouldering.user_id AND pb_bouldering.climb_type = 'bouldering'
LEFT JOIN personal_bests pb_sport ON u.id = pb_sport.user_id AND pb_sport.climb_type = 'sport'
GROUP BY u.id, u.username, up.display_name, pb_bouldering.best_grade, pb_sport.best_grade;

-- 创建排名视图
CREATE VIEW climbing_rankings AS
SELECT 
    u.id as user_id,
    u.username,
    pb.climb_type,
    pb.best_grade,
    pb.achieved_date,
    ROW_NUMBER() OVER (PARTITION BY pb.climb_type ORDER BY 
        CASE pb.climb_type 
            WHEN 'bouldering' THEN 
                CASE 
                    WHEN pb.best_grade LIKE 'V%' THEN CAST(SUBSTR(pb.best_grade, 2) AS INTEGER)
                    ELSE -1 
                END
            WHEN 'sport' THEN 
                -- 简化的法式难度等级排序
                CASE 
                    WHEN pb.best_grade LIKE '%a' THEN CAST(SUBSTR(pb.best_grade, 1, 1) AS INTEGER) * 10
                    WHEN pb.best_grade LIKE '%a+' THEN CAST(SUBSTR(pb.best_grade, 1, 1) AS INTEGER) * 10 + 1
                    WHEN pb.best_grade LIKE '%b' THEN CAST(SUBSTR(pb.best_grade, 1, 1) AS INTEGER) * 10 + 2
                    WHEN pb.best_grade LIKE '%b+' THEN CAST(SUBSTR(pb.best_grade, 1, 1) AS INTEGER) * 10 + 3
                    WHEN pb.best_grade LIKE '%c' THEN CAST(SUBSTR(pb.best_grade, 1, 1) AS INTEGER) * 10 + 4
                    WHEN pb.best_grade LIKE '%c+' THEN CAST(SUBSTR(pb.best_grade, 1, 1) AS INTEGER) * 10 + 5
                    ELSE -1
                END
        END DESC, 
        pb.achieved_date ASC
    ) as rank
FROM users u
JOIN personal_bests pb ON u.id = pb.user_id; 