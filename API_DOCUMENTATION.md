# ClimbTrack API 文档

## 概述

ClimbTrack 提供了完整的 RESTful API 接口，支持攀岩追踪应用的所有核心功能。API 采用分层架构设计：

- **数据访问层 (DAO)**: 提供基础的 CRUD 操作
- **业务逻辑层 (Services)**: 处理复杂的业务逻辑和数据联动
- **API 路由层**: 提供 HTTP 接口

## 认证

所有API接口都需要用户登录认证。使用session-based认证：

```bash
# 先登录获取session
POST /login
{
  "username": "alice",
  "password": "password123"
}
```

## API 接口

### 用户管理

#### 获取所有用户列表
```http
GET /api/users
```

**响应:**
```json
{
  "users": [
    {
      "id": 1,
      "username": "alice",
      "email": "alice@example.com",
      "created_at": "2024-01-15T10:00:00"
    }
  ]
}
```

#### 获取指定用户信息
```http
GET /api/users/{user_id}
```

**响应:**
```json
{
  "user": {...},
  "profile": {...},
  "statistics": {...},
  "personal_bests": [...]
}
```

#### 更新用户资料
```http
PUT /api/users/{user_id}/profile
Content-Type: application/json

{
  "display_name": "Alice Cooper",
  "shoe_size": "38",
  "preferred_wall_type": "Overhang",
  "bio": "Passionate climber"
}
```

### 攀登记录管理

#### 创建攀登记录
```http
POST /api/climb-logs
Content-Type: application/json

{
  "name": "Crimson Tide",
  "type": "bouldering",
  "grade": "V4",
  "session_date": "2024-01-15",
  "notes": "Great route!",
  "attempt_result": "completed",
  "attempts_count": 1
}
```

**响应:**
```json
{
  "climb_log_id": 123,
  "message": "Climb log created successfully"
}
```

#### 获取用户攀登记录
```http
GET /api/climb-logs/{user_id}
```

**响应:**
```json
{
  "grouped_logs": {
    "2024-01-15": [...]
  },
  "all_logs": [...]
}
```

### 统计数据

#### 更新用户统计数据
```http
POST /api/statistics/update/{user_id}
```

#### 更新所有用户统计数据
```http
POST /api/statistics/update-all
```

### 场馆管理

#### 获取所有场馆
```http
GET /api/gyms
```

#### 创建场馆
```http
POST /api/gyms
Content-Type: application/json

{
  "name": "Boulder Park",
  "address": "123 Climbing Street",
  "phone": "555-0123",
  "website": "http://boulderpark.com",
  "opening_hours": "Mon-Sun 10:00-22:00"
}
```

#### 更新场馆
```http
PUT /api/gyms/{gym_id}
Content-Type: application/json

{
  "name": "Updated Gym Name",
  ...
}
```

### 笔记管理

#### 创建动作笔记
```http
POST /api/movement-notes
Content-Type: application/json

{
  "climb_log_id": 123,
  "title": "Footwork Technique",
  "content": "Remember to keep center of gravity low",
  "movement_type": "technique",
  "tags": "footwork,technique"
}
```

#### 获取用户动作笔记
```http
GET /api/movement-notes/{user_id}
```

#### 更新动作笔记
```http
PUT /api/movement-notes/{note_id}
Content-Type: application/json

{
  "title": "Updated Title",
  "content": "Updated content"
}
```

#### 删除动作笔记
```http
DELETE /api/movement-notes/{note_id}
```

### 排名数据

#### 获取排名数据
```http
GET /api/rankings
```

**响应:**
```json
{
  "bouldering": [
    {
      "name": "Alice",
      "grade": "V5",
      "date": "2024-01-15"
    }
  ],
  "sport": [...]
}
```

## 数据库服务层

### AuthService (认证服务)

```python
from database.services import AuthService

# 创建用户
user_id = AuthService.create_user("username", "password", "email@example.com")

# 用户认证
user = AuthService.authenticate_user("username", "password")

# 更新密码
success = AuthService.update_password("username", "new_password")
```

### UserService (用户服务)

```python
from database.services import UserService

# 获取用户完整信息
user_info = UserService.get_user_info(user_id)

# 更新用户资料
profile_data = {"display_name": "New Name", "shoe_size": "39"}
success = UserService.update_user_profile(user_id, profile_data)
```

### ClimbingService (攀岩服务)

```python
from database.services import ClimbingService

# 创建攀登记录
climb_data = {
    "name": "Route Name",
    "type": "bouldering",
    "grade": "V4",
    "notes": "Great climb!"
}
climb_log_id = ClimbingService.create_climb_log(user_id, "2024-01-15", climb_data)

# 获取用户攀登记录
grouped_logs, all_logs = ClimbingService.get_user_climb_logs_grouped(user_id)

# 获取排名
rankings = ClimbingService.get_climbing_rankings()
```

### StatisticsService (统计服务)

```python
from database.services import StatisticsService

# 更新用户统计
StatisticsService.update_user_statistics(user_id)

# 更新所有用户统计
StatisticsService.update_all_user_statistics()

# 获取用户资料统计
stats = StatisticsService.get_user_profile_stats(user_id)
```

### GymService (场馆服务)

```python
from database.services import GymService

# 创建场馆
gym_data = {"name": "New Gym", "address": "123 Street"}
gym_id = GymService.create_gym(gym_data)

# 更新场馆
success = GymService.update_gym(gym_id, gym_data)

# 添加人流检测
detection_id = GymService.add_crowd_detection(gym_id, 25, "high", "Peak hours")
```

### NoteService (笔记服务)

```python
from database.services import NoteService

# 创建动作笔记
note_data = {
    "title": "Technique Note",
    "content": "Remember to...",
    "movement_type": "technique"
}
note_id = NoteService.create_movement_note(user_id, climb_log_id, note_data)

# 更新动作笔记
success = NoteService.update_movement_note(note_id, note_data)
```

## DAO 数据访问层

每个表都有对应的DAO类，提供基础的CRUD操作：

### 可用的DAO类

- `user_dao`: 用户数据访问
- `user_profile_dao`: 用户资料数据访问
- `user_statistics_dao`: 用户统计数据访问
- `climbing_session_dao`: 攀岩会话数据访问
- `climb_log_dao`: 攀登记录数据访问
- `personal_best_dao`: 个人最佳记录数据访问
- `climbing_gym_dao`: 攀岩场馆数据访问
- `movement_note_dao`: 动作笔记数据访问
- `crowd_detection_dao`: 人流检测数据访问

### 基础操作

```python
from database.dao import user_dao

# 创建
user_id = user_dao.create(user_model)

# 查询
user = user_dao.get_by_id(user_id)
all_users = user_dao.get_all()
user = user_dao.get_by_username("alice")

# 更新
rows_affected = user_dao.update(user_id, updated_user_model)

# 删除
rows_affected = user_dao.delete_by_id(user_id)
```

## 错误处理

所有API接口都会返回适当的HTTP状态码：

- `200`: 成功
- `400`: 请求错误（缺少必需字段等）
- `401`: 未认证
- `403`: 无权限
- `404`: 资源不存在
- `500`: 服务器错误

错误响应格式：
```json
{
  "error": "Error message description"
}
```

## 数据联动和业务逻辑

### 创建攀登记录时的自动操作：

1. 自动创建或关联攀岩会话
2. 更新个人最佳记录（如果新记录更好）
3. 自动更新用户统计数据

### 创建用户时的自动操作：

1. 创建用户记录
2. 创建用户资料记录
3. 初始化用户统计记录

### 数据完整性保障：

- 所有关联操作都在事务中执行
- 自动维护数据一致性
- 定期运行数据完整性检查

## 使用示例

### 完整的攀登记录流程

```python
# 1. 用户登录
user = AuthService.authenticate_user("alice", "password123")

# 2. 创建攀登记录
climb_data = {
    "name": "Blue Moon",
    "type": "bouldering", 
    "grade": "V5",
    "notes": "Finally completed this route!",
    "image_filename": "climb_photo.jpg"
}
climb_log_id = ClimbingService.create_climb_log(
    user['id'], 
    "2024-01-15", 
    climb_data
)

# 3. 自动更新统计（在create_climb_log中自动执行）
# 4. 获取更新后的用户数据
user_info = UserService.get_user_info(user['id'])
```

### 批量数据更新

```python
# 更新所有用户统计
StatisticsService.update_all_user_statistics()

# 检查数据完整性
from database.update_statistics import check_database_integrity
check_database_integrity()
``` 