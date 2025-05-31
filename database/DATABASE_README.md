# ClimbTrack 数据库设计说明

## 概述
这是一个为攀岩跟踪应用 ClimbTrack 设计的完整数据库结构。数据库支持用户管理、攀岩会话记录、排名系统、媒体文件管理等功能。

## 数据库表结构

### 1. 用户相关表

#### users (用户表)
- **作用**: 存储用户的基本登录信息
- **主要字段**: 
  - `username`: 用户名（唯一）
  - `password_hash`: 加密后的密码
  - `email`: 邮箱（可选）
  - `is_active`: 账户状态

#### user_profiles (用户资料表)
- **作用**: 存储用户的详细个人信息和偏好
- **主要字段**:
  - `display_name`: 显示名称
  - `shoe_size`: 攀岩鞋尺码
  - `preferred_wall_type`: 偏好的岩壁类型
  - `bio`: 个人介绍

### 2. 攀岩记录相关表

#### climbing_sessions (攀岩会话表)
- **作用**: 记录每次去攀岩的会话信息
- **主要字段**:
  - `session_date`: 攀岩日期
  - `start_time/end_time`: 开始和结束时间
  - `location`: 攀岩地点

#### climb_logs (攀登记录表)
- **作用**: 记录每次具体的攀登尝试
- **主要字段**:
  - `climb_name`: 线路名称
  - `climb_type`: 攀岩类型（bouldering/sport）
  - `grade`: 难度等级
  - `attempt_result`: 完成情况
  - `image_filename`: 关联的图片文件

### 3. 媒体和统计表

#### media_files (媒体文件表)
- **作用**: 管理用户上传的图片和视频
- **主要字段**:
  - `filename`: 存储的文件名
  - `original_filename`: 原始文件名
  - `file_type`: 文件类型
  - `file_path`: 文件路径

#### personal_bests (个人最佳记录表)
- **作用**: 记录用户在不同类型攀岩中的最佳成绩
- **主要字段**:
  - `climb_type`: 攀岩类型
  - `best_grade`: 最佳难度等级
  - `achieved_date`: 达成日期

#### user_statistics (统计数据表)
- **作用**: 存储用户的各种统计数据
- **主要字段**:
  - `total_sessions`: 总会话数
  - `total_climbs`: 总攀登次数
  - `sessions_this_month`: 本月会话数

### 4. 场馆和功能表

#### climbing_gyms (场馆信息表)
- **作用**: 存储攀岩场馆的基本信息
- **主要字段**:
  - `name`: 场馆名称
  - `address`: 地址
  - `opening_hours`: 营业时间

#### crowd_detection (场馆拥挤度检测表)
- **作用**: 存储场馆人流量检测数据
- **主要字段**:
  - `people_count`: 人数统计
  - `activity_level`: 活动级别
  - `detection_time`: 检测时间

#### movement_notes (动作笔记表)
- **作用**: 存储攀登技巧和动作笔记
- **主要字段**:
  - `title`: 笔记标题
  - `content`: 笔记内容
  - `movement_type`: 动作类型
  - `tags`: 标签（JSON格式）

## 关键特性

### 1. 数据完整性
- 使用外键约束确保数据一致性
- 设置适当的级联删除策略
- 添加检查约束验证数据有效性

### 2. 性能优化
- 为常用查询字段创建索引
- 创建视图简化复杂查询
- 合理的表结构设计减少冗余

### 3. 扩展性
- 表结构设计考虑未来功能扩展
- 使用标准化设计避免数据冗余
- 支持多种攀岩类型和难度系统

## 数据视图

### user_climbing_summary
提供用户攀岩数据的综合摘要，包括：
- 总会话数和攀登次数
- 各类型攀岩的最佳成绩
- 用户基本信息

### climbing_rankings
提供排名功能，支持：
- 按攀岩类型分别排名
- 智能的难度等级排序
- 考虑达成日期的排名逻辑

## 使用建议

### 1. 数据迁移
当前应用使用内存存储，迁移到数据库时需要：
1. 将 `session_logs` 数据分别存储到 `climbing_sessions` 和 `climb_logs` 表
2. 将 `users` 字典数据迁移到 `users` 表，并加密密码
3. 更新个人最佳记录和统计数据

### 2. 查询优化
- 使用视图进行复杂查询
- 利用索引加速常用查询
- 考虑数据缓存策略

### 3. 数据安全
- 密码必须加密存储
- 实现用户权限控制
- 定期备份重要数据

## 与现有代码的对应关系

### app.py 中的数据结构对应：
```python
# 原始 session_logs 结构：
{
    'date': date,
    'image': filename,
    'grade': grade,
    'note': note,
    'name': name,
    'type': climb_type
}

# 对应新的表结构：
# climbing_sessions: date (会话日期)
# climb_logs: grade, note, name, type, image_filename
# media_files: filename 相关信息
```

这个数据库设计完全支持现有应用的所有功能，并为未来的功能扩展提供了良好的基础。 