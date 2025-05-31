#!/usr/bin/env python3
"""
ClimbTrack 数据库初始化脚本
用于创建数据库表结构和插入示例数据
"""

import sqlite3
import hashlib
from datetime import datetime, date
import os

def hash_password(password):
    """加密密码"""
    return hashlib.sha256(password.encode()).hexdigest()

def init_database(db_path='climbtrack.db'):
    """初始化数据库"""
    print(f"正在初始化数据库: {db_path}")
    
    # 如果数据库文件已存在，询问是否覆盖
    if os.path.exists(db_path):
        response = input(f"数据库文件 {db_path} 已存在，是否覆盖？(y/N): ")
        if response.lower() != 'y':
            print("已取消初始化")
            return
        os.remove(db_path)
    
    # 连接数据库
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 读取并执行 SQL 文件
        sql_file_path = os.path.join(os.path.dirname(__file__), 'database_design.sql')
        with open(sql_file_path, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        # 执行 SQL 脚本
        cursor.executescript(sql_script)
        
        print("✅ 数据库表结构创建成功")
        
        # 插入示例数据
        insert_sample_data(cursor)
        
        # 提交事务
        conn.commit()
        print("✅ 数据库初始化完成")
        
    except FileNotFoundError:
        print("❌ 找不到 database_design.sql 文件")
    except Exception as e:
        print(f"❌ 数据库初始化失败: {e}")
        conn.rollback()
    finally:
        conn.close()

def insert_sample_data(cursor):
    """插入示例数据"""
    print("正在插入示例数据...")
    
    # 1. 插入示例用户
    users_data = [
        ('alice', hash_password('password123'), 'alice@example.com'),
        ('bob', hash_password('climbhard'), 'bob@example.com'),
        ('charlie', hash_password('bouldering'), 'charlie@example.com'),
    ]
    
    cursor.executemany('''
        INSERT INTO users (username, password_hash, email) 
        VALUES (?, ?, ?)
    ''', users_data)
    
    # 2. 插入用户资料
    profiles_data = [
        (1, 'Alice Cooper', '38', 'Overhang', 'Passionate bouldering beginner'),
        (2, 'Bob Smith', '42', 'Vertical', 'Experienced sport climbing enthusiast'),
        (3, 'Charlie Brown', '40', 'Slab', 'Technical climbing specialist'),
    ]
    
    cursor.executemany('''
        INSERT INTO user_profiles (user_id, display_name, shoe_size, preferred_wall_type, bio) 
        VALUES (?, ?, ?, ?, ?)
    ''', profiles_data)
    
    # 3. 插入攀岩场馆
    gyms_data = [
        ('Boulder Park', '123 Climbing Street, Downtown', '555-0123', 'http://boulderpark.com', 'Mon-Sun 10:00-22:00'),
        ('Vertical Limit', '456 Rock Avenue, Uptown', '555-0456', 'http://verticallimit.com', 'Mon-Sun 9:00-23:00'),
    ]
    
    cursor.executemany('''
        INSERT INTO climbing_gyms (name, address, phone, website, opening_hours) 
        VALUES (?, ?, ?, ?, ?)
    ''', gyms_data)
    
    # 4. 插入攀岩会话
    sessions_data = [
        (1, '2024-01-15', '19:00', '21:30', 'Boulder Park', 'Great session today, completed several new routes'),
        (1, '2024-01-18', '18:30', '20:00', 'Boulder Park', 'Practiced some technical moves'),
        (2, '2024-01-16', '14:00', '17:00', 'Vertical Limit', 'Attempted some challenging high-grade routes'),
        (3, '2024-01-17', '10:00', '12:00', 'Boulder Park', 'Weekend morning training session'),
    ]
    
    cursor.executemany('''
        INSERT INTO climbing_sessions (user_id, session_date, start_time, end_time, location, notes) 
        VALUES (?, ?, ?, ?, ?, ?)
    ''', sessions_data)
    
    # 5. 插入攀登记录
    climb_logs_data = [
        (1, 1, 'Crimson Tide', 'bouldering', 'V4', 'flash', 1, None, 'Smooth moves, completed on first try'),
        (1, 1, 'Blue Moon', 'bouldering', 'V5', 'redpoint', 3, None, 'Success on third attempt'),
        (2, 2, 'Green Monster', 'bouldering', 'V3', 'flash', 1, None, 'Good warm-up route'),
        (3, 3, 'Red Wall', 'sport', '6b+', 'onsight', 1, None, 'Technical route, very challenging'),
        (4, 3, 'Yellow Brick Road', 'bouldering', 'V6', 'failed', 5, None, 'Still need more practice'),
    ]
    
    cursor.executemany('''
        INSERT INTO climb_logs (session_id, user_id, climb_name, climb_type, grade, attempt_result, attempts_count, image_filename, notes) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', climb_logs_data)
    
    # 6. 插入个人最佳记录
    personal_bests_data = [
        (1, 'bouldering', 'V5', 1, '2024-01-15'),
        (2, 'bouldering', 'V3', 2, '2024-01-16'),
        (3, 'bouldering', 'V6', 4, '2024-01-17'),
        (3, 'sport', '6b+', 3, '2024-01-17'),
    ]
    
    cursor.executemany('''
        INSERT INTO personal_bests (user_id, climb_type, best_grade, climb_log_id, achieved_date) 
        VALUES (?, ?, ?, ?, ?)
    ''', personal_bests_data)
    
    # 7. 插入统计数据
    statistics_data = [
        (1, 2, 3, 2, 2),
        (2, 1, 1, 1, 1),
        (3, 1, 2, 1, 1),
    ]
    
    cursor.executemany('''
        INSERT INTO user_statistics (user_id, total_sessions, total_climbs, sessions_this_month, sessions_this_year) 
        VALUES (?, ?, ?, ?, ?)
    ''', statistics_data)
    
    # 8. 插入动作笔记
    notes_data = [
        (1, 1, 'Bouldering Technique: Footwork', 'Learned footwork technique on V4 route, keep center of gravity low and foot placement precise', 'technique', '["footwork", "technique", "bouldering"]'),
        (3, 3, 'Sport Climbing Insights', 'Insights from completing 6b+ route, need to stay calm and maintain rhythm', 'beta', '["sport", "technique", "mental"]'),
    ]
    
    cursor.executemany('''
        INSERT INTO movement_notes (user_id, climb_log_id, title, content, movement_type, tags) 
        VALUES (?, ?, ?, ?, ?, ?)
    ''', notes_data)
    
    # 9. 插入人流检测数据
    crowd_data = [
        (1, '2024-01-15 19:00:00', 25, 'high', None, 'Monday evening peak hours'),
        (1, '2024-01-16 14:00:00', 12, 'low', None, 'Tuesday afternoon quite empty'),
        (2, '2024-01-17 10:00:00', 8, 'low', None, 'Wednesday morning very quiet'),
    ]
    
    cursor.executemany('''
        INSERT INTO crowd_detection (gym_id, detection_time, people_count, activity_level, image_filename, notes) 
        VALUES (?, ?, ?, ?, ?, ?)
    ''', crowd_data)
    
    print("✅ 示例数据插入完成")

def verify_database(db_path='climbtrack.db'):
    """验证数据库数据"""
    print("\n正在验证数据库数据...")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 检查各表的记录数
        tables = [
            'users', 'user_profiles', 'climbing_sessions', 'climb_logs',
            'personal_bests', 'user_statistics', 'climbing_gyms', 
            'movement_notes', 'crowd_detection'
        ]
        
        for table in tables:
            cursor.execute(f'SELECT COUNT(*) FROM {table}')
            count = cursor.fetchone()[0]
            print(f"📊 {table}: {count} 条记录")
        
        # 测试视图
        print("\n测试数据视图...")
        cursor.execute('SELECT * FROM user_climbing_summary LIMIT 3')
        results = cursor.fetchall()
        print(f"✅ user_climbing_summary 视图: {len(results)} 条记录")
        
        cursor.execute('SELECT * FROM climbing_rankings LIMIT 5')
        results = cursor.fetchall()
        print(f"✅ climbing_rankings 视图: {len(results)} 条记录")
        
    except Exception as e:
        print(f"❌ 验证失败: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    # 初始化数据库
    init_database()
    
    # 验证数据库
    verify_database()
    
    print("\n🎉 数据库初始化完成！")
    print("💡 你现在可以使用以下测试账户登录：")
    print("   用户名: alice, 密码: password123")
    print("   用户名: bob, 密码: climbhard")
    print("   用户名: charlie, 密码: bouldering") 