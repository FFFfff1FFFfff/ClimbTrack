# ClimbTrack 应用设置指南

## 🚀 快速开始

### 1. 初始化数据库
首先运行数据库初始化脚本：
```bash
cd ClimbTrack
python database/init_database.py
```

这会创建：
- `database/climbtrack.db` 数据库文件
- 所有必要的表结构
- 示例数据（3个测试用户和相关记录）

### 2. 更新统计数据（可选）
运行统计数据更新脚本，确保数据完整性：
```bash
python database/update_statistics.py
```

### 3. 启动应用
```bash
python app.py
```

应用将运行在 `http://127.0.0.1:5000`

## 🔑 测试账户

初始化脚本会创建以下测试账户：

| 用户名 | 密码 | 描述 |
|--------|------|------|
| alice | password123 | 抱石初学者 |
| bob | climbhard | 线路攀登者 |
| charlie | bouldering | 技术型攀登者 |

## 📊 主要功能

### 1. 用户认证
- ✅ 登录/登出
- ✅ 用户注册
- ✅ 密码重置
- ✅ 密码加密存储

### 2. 攀岩记录
- ✅ 会话记录（Session Log）
- ✅ 图片上传
- ✅ 难度等级记录
- ✅ 攀岩类型分类（抱石/线路）
- ✅ 按日期分组显示

### 3. 个人资料
- ✅ 个人统计数据
- ✅ 最佳成绩显示
- ✅ 攀岩偏好设置
- ✅ 排名信息

### 4. 排名系统
- ✅ 抱石排名（按V等级）
- ✅ 线路攀登排名（按法式等级）
- ✅ 自动排名计算

## 🗂️ 数据库结构

应用使用 SQLite 数据库，包含以下主要表：

### 核心表
- `users` - 用户基本信息
- `user_profiles` - 用户详细资料
- `climbing_sessions` - 攀岩会话
- `climb_logs` - 具体攀登记录
- `personal_bests` - 个人最佳记录
- `user_statistics` - 用户统计数据

### 功能表
- `climbing_gyms` - 攀岩场馆信息
- `crowd_detection` - 人流检测数据
- `movement_notes` - 动作笔记
- `media_files` - 媒体文件管理

## 📝 使用流程

### 新用户注册
1. 访问 `/signup` 页面
2. 填写用户名、密码（和可选邮箱）
3. 系统自动创建用户资料和统计记录

### 记录攀岩会话
1. 登录后访问 `/session-log`
2. 点击 "+" 按钮上传新记录
3. 填写线路名称、类型、难度、笔记
4. 可选上传图片
5. 系统自动更新个人最佳记录

### 查看排名
1. 访问 `/rank` 页面
2. 查看抱石和线路攀登的排名
3. 排名基于个人最佳成绩自动计算

### 查看个人资料
1. 访问 `/profile` 页面
2. 查看个人统计数据
3. 查看当前排名位置

## 🔧 维护操作

### 定期更新统计数据
建议定期运行统计更新脚本：
```bash
python database/update_statistics.py
```

### 数据库备份
定期备份数据库文件：
```bash
cp database/climbtrack.db database/climbtrack_backup_$(date +%Y%m%d).db
```

### 查看数据库内容
使用 SQLite 客户端查看数据：
```bash
sqlite3 database/climbtrack.db
.tables
SELECT * FROM users;
```

## 🛠️ 开发说明

### 添加新功能
1. 修改 `database/database_design.sql` 添加新表
2. 更新 `database/init_database.py` 添加示例数据
3. 在 `app.py` 中添加新路由和功能
4. 运行 `python database/update_statistics.py` 更新数据

### 修改难度等级系统
- V等级处理：`v_grade_key()` 函数
- 法式等级处理：`french_grade_key()` 函数
- 排名计算：`climbing_rankings` 视图

### 自定义用户界面
- 模板文件位于 `templates/` 目录
- 静态文件位于 `static/` 目录
- 上传的图片存储在 `static/uploads/` 目录

## ⚠️ 注意事项

1. **首次使用必须运行数据库初始化**
2. **密码采用 SHA256 加密，安全性较基础**
3. **图片上传支持：PNG, JPG, JPEG, GIF**
4. **生产环境建议使用 PostgreSQL 或 MySQL**
5. **应用使用 Flask 开发模式，生产环境需要配置 WSGI**

## 🐛 常见问题

### Q: 数据库文件不存在
A: 运行 `python database/init_database.py` 初始化数据库

### Q: 登录失败
A: 使用提供的测试账户或注册新账户

### Q: 图片无法上传
A: 检查 `static/uploads/` 目录是否存在和可写

### Q: 排名不正确
A: 运行 `python database/update_statistics.py` 更新统计数据

### Q: 新注册用户无法查看资料
A: 运行 `python database/update_statistics.py` 检查数据完整性 

todo
1.session log要能删除 