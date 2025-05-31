# ClimbTrack 数据库关系图表

## 表关系图 (Entity Relationship Diagram)

```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│     users       │ 1───1 │ user_profiles   │       │ climbing_gyms   │
│                 │       │                 │       │                 │
│ • id (PK)       │       │ • id (PK)       │       │ • id (PK)       │
│ • username      │       │ • user_id (FK)  │       │ • name          │
│ • password_hash │       │ • display_name  │       │ • address       │
│ • email         │       │ • shoe_size     │       │ • phone         │
│ • created_at    │       │ • preferred_wall│       │ • website       │
│ • is_active     │       │ • bio           │       │ • opening_hours │
└─────────────────┘       └─────────────────┘       └─────────────────┘
         │                                                   │
         │ 1                                                 │
         │                                                   │ *
         │ *                                         ┌─────────────────┐
┌─────────────────┐                                  │ crowd_detection │
│climbing_sessions│                                  │                 │
│                 │                                  │ • id (PK)       │
│ • id (PK)       │                                  │ • gym_id (FK)   │
│ • user_id (FK)  │                                  │ • detection_time│
│ • session_date  │                                  │ • people_count  │
│ • start_time    │                                  │ • activity_level│
│ • end_time      │                                  │ • image_filename│
│ • location      │                                  │ • notes         │
│ • notes         │                                  └─────────────────┘
└─────────────────┘
         │ 1
         │
         │ *
┌─────────────────┐       ┌─────────────────┐
│   climb_logs    │ *───1 │   media_files   │
│                 │       │                 │
│ • id (PK)       │       │ • id (PK)       │
│ • session_id(FK)│       │ • climb_log_id  │
│ • user_id (FK)  │       │ • user_id (FK)  │
│ • climb_name    │       │ • filename      │
│ • climb_type    │       │ • original_name │
│ • grade         │       │ • file_type     │
│ • attempt_result│       │ • file_size     │
│ • attempts_count│       │ • file_path     │
│ • image_filename│       │ • upload_date   │
│ • notes         │       └─────────────────┘
│ • timestamp     │
└─────────────────┘
         │
         │ *
         │
         │ 1
┌─────────────────┐
│ personal_bests  │
│                 │
│ • id (PK)       │
│ • user_id (FK)  │
│ • climb_type    │
│ • best_grade    │
│ • climb_log_id  │
│ • achieved_date │
└─────────────────┘

┌─────────────────┐       ┌─────────────────┐
│ user_statistics │       │ movement_notes  │
│                 │       │                 │
│ • id (PK)       │       │ • id (PK)       │
│ • user_id (FK)  │       │ • user_id (FK)  │
│ • total_sessions│       │ • climb_log_id  │
│ • total_climbs  │       │ • title         │
│ • sessions_month│       │ • movement_type │
│ • sessions_year │       │ • tags          │
│ • last_calc     │       │ • created_at    │
└─────────────────┘       │ • updated_at    │
         │                │ • content       │
         │ 1              └─────────────────┘
         │                         │
         │                         │ *
         │                         │
users ───┘                         │ 1
 (FK relationships back to users)  │
                              climb_logs
                           (optional FK)
```

## 关系说明

### 一对一关系 (1:1)
- `users` ↔ `user_profiles`: 每个用户有一个资料档案
- `users` ↔ `user_statistics`: 每个用户有一套统计数据

### 一对多关系 (1:N)
- `users` → `climbing_sessions`: 一个用户可以有多个攀岩会话
- `climbing_sessions` → `climb_logs`: 一个会话可以包含多次攀登记录
- `users` → `climb_logs`: 一个用户可以有多个攀登记录
- `users` → `personal_bests`: 一个用户可以有多个最佳记录（不同类型）
- `users` → `media_files`: 一个用户可以上传多个文件
- `users` → `movement_notes`: 一个用户可以写多个笔记
- `climbing_gyms` → `crowd_detection`: 一个场馆可以有多个检测记录

### 多对一关系 (N:1)
- `climb_logs` → `media_files`: 一个攀登记录可以对应多个媒体文件
- `climb_logs` → `movement_notes`: 一个攀登记录可以有多个相关笔记

## 核心业务流程

### 1. 用户注册和登录流程
```
用户注册 → users 表
       ↓
创建资料 → user_profiles 表
       ↓
初始化统计 → user_statistics 表
```

### 2. 攀岩记录流程
```
创建会话 → climbing_sessions 表
       ↓
记录攀登 → climb_logs 表
       ↓
上传媒体 → media_files 表
       ↓
更新最佳 → personal_bests 表
       ↓
更新统计 → user_statistics 表
```

### 3. 排名计算流程
```
读取 personal_bests → 按类型分组 → 按难度排序 → climbing_rankings 视图
```

## 索引策略

### 主要查询场景和对应索引：
- 用户登录：`users.username`
- 会话查询：`climbing_sessions(user_id, session_date)`
- 攀登记录：`climb_logs(user_id, climb_type, grade)`
- 排名查询：`personal_bests(climb_type, user_id)`
- 媒体文件：`media_files(climb_log_id)`
- 人流检测：`crowd_detection(detection_time)`

## 数据完整性约束

### 外键约束：
- 所有 `user_id` 都引用 `users.id`
- `session_id` 引用 `climbing_sessions.id`
- `climb_log_id` 引用 `climb_logs.id`
- `gym_id` 引用 `climbing_gyms.id`

### 业务约束：
- `personal_bests` 每个用户每种类型只能有一条记录
- `user_statistics` 每个用户只能有一条记录
- 文件上传需要验证文件类型和大小
- 难度等级需要符合标准格式（V0-V16, 6a-9c+等） 