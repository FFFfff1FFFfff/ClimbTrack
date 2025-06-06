#!/usr/bin/env python3
"""
路线数据库初始化脚本
创建routes表并插入初始路线数据
"""

import sqlite3
import os
from datetime import datetime

def init_routes_table():
    """初始化路线表和数据"""
    
    # 数据库文件路径
    db_path = 'database/climbtrack.db'
    
    # 检查数据库文件是否存在
    if not os.path.exists(db_path):
        print("❌ 数据库文件不存在！请先运行 init_database.py")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 检查routes表是否已存在
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='routes'
        """)
        
        if cursor.fetchone():
            print("⚠️  routes表已存在，跳过创建")
        else:
            # 创建routes表
            print("🏗️  创建routes表...")
            cursor.execute("""
                CREATE TABLE routes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(200) NOT NULL,
                    category VARCHAR(20) NOT NULL CHECK(category IN ('Bouldering', 'Sport Climbing')),
                    balance INTEGER NOT NULL CHECK(balance >= 1 AND balance <= 10),
                    strength INTEGER NOT NULL CHECK(strength >= 1 AND strength <= 10),
                    technicality INTEGER NOT NULL CHECK(technicality >= 1 AND technicality <= 10),
                    flexibility INTEGER NOT NULL CHECK(flexibility >= 1 AND flexibility <= 10),
                    strategy INTEGER NOT NULL CHECK(strategy >= 1 AND strategy <= 10),
                    endurance INTEGER NOT NULL CHECK(endurance >= 1 AND endurance <= 10),
                    mental_challenge INTEGER NOT NULL CHECK(mental_challenge >= 1 AND mental_challenge <= 10),
                    overall_difficulty INTEGER NOT NULL CHECK(overall_difficulty >= 1 AND overall_difficulty <= 10),
                    description TEXT,
                    image_filename VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # 创建索引
            cursor.execute("CREATE INDEX idx_routes_category ON routes(category)")
            cursor.execute("CREATE INDEX idx_routes_difficulty ON routes(overall_difficulty)")
            cursor.execute("CREATE INDEX idx_routes_name ON routes(name)")
            
            print("✅ routes表创建成功")
        
        # 检查是否已有路线数据
        cursor.execute("SELECT COUNT(*) FROM routes")
        count = cursor.fetchone()[0]
        
        if count > 0:
            print(f"⚠️  routes表中已有 {count} 条数据，跳过插入")
        else:
            # 插入初始路线数据
            print("📝 插入初始路线数据...")
            
            routes_data = [
                (1, "Beginner Route", "Bouldering", 4, 3, 3, 2, 2, 2, 1, 3, "适合初学者的攀登路线，注重基础技巧练习"),
                (2, "Small Rock Path", "Sport Climbing", 5, 4, 4, 3, 4, 4, 1, 5, "小型岩石路径，考验基础体能和技巧"),
                (3, "Short Fast Route", "Bouldering", 6, 5, 4, 4, 5, 5, 2, 6, "短距离速度路线，需要爆发力"),
                (4, "Climbing Challenge", "Sport Climbing", 7, 6, 5, 5, 6, 6, 3, 7, "中级挑战路线，全面考验攀登技能"),
                (5, "Sliding Large Rocks", "Bouldering", 6, 6, 5, 5, 5, 6, 4, 7, "大型滑石路线，需要良好的平衡感"),
                (6, "Technical Challenge", "Sport Climbing", 4, 5, 6, 4, 6, 5, 2, 6, "技术性挑战路线，重点考验技巧"),
                (7, "Strength Training", "Bouldering", 8, 8, 6, 5, 4, 7, 2, 8, "力量训练路线，适合力量型选手"),
                (8, "Complex Technical Path", "Sport Climbing", 5, 4, 7, 6, 7, 6, 3, 7, "复杂技术路径，需要精确的动作"),
                (9, "Uphill Big Rocks", "Sport Climbing", 6, 7, 5, 4, 6, 8, 3, 8, "上坡大岩石路线，考验耐力"),
                (10, "Large Jump Path", "Bouldering", 7, 8, 6, 5, 7, 6, 4, 8, "大跳路线，需要强大的爆发力"),
                (11, "Extreme Technical Path", "Sport Climbing", 8, 7, 9, 6, 6, 6, 5, 9, "极限技术路径，高难度技巧挑战"),
                (12, "Long Endurance Path", "Bouldering", 4, 6, 4, 4, 5, 9, 3, 7, "长距离耐力路线，持久战"),
                (13, "Complex Rolling Path", "Sport Climbing", 7, 6, 6, 6, 6, 7, 2, 7, "复杂滚动路径，需要流畅动作"),
                (14, "Dual Hand Combat Path", "Bouldering", 5, 7, 6, 4, 5, 6, 3, 7, "双手格斗路线，协调性要求高"),
                (15, "High Difficulty Duel Path", "Sport Climbing", 8, 9, 7, 5, 6, 7, 6, 9, "高难度决斗路线，专家级挑战"),
                (16, "Explosive Power Training Path", "Bouldering", 7, 8, 6, 4, 5, 5, 2, 8, "爆发力训练路线，短时间高强度"),
                (17, "High Suspension Path", "Sport Climbing", 9, 8, 7, 6, 7, 7, 9, 9, "高悬挂路线，心理挑战巨大"),
                (18, "Directional Adjustment Path", "Bouldering", 5, 4, 5, 4, 7, 6, 3, 6, "方向调整路线，策略性强"),
                (19, "Advanced Technical Path", "Sport Climbing", 6, 5, 8, 5, 6, 6, 2, 7, "高级技术路径，精密技巧"),
                (20, "Small Steps Path", "Bouldering", 6, 4, 5, 6, 5, 4, 1, 6, "小步路线，需要精确脚法"),
                (21, "High Risk Jump Path", "Sport Climbing", 8, 8, 7, 5, 7, 5, 8, 9, "高风险跳跃路线，心理压力大"),
                (22, "Giant Rock Climbing Path", "Sport Climbing", 7, 8, 6, 5, 7, 6, 4, 8, "巨岩攀登路线，综合挑战"),
                (23, "Complex Turn Path", "Bouldering", 5, 6, 6, 5, 6, 7, 3, 7, "复杂转向路线，灵活性重要"),
                (24, "Precise Grip Path", "Sport Climbing", 6, 5, 7, 6, 5, 5, 2, 7, "精确抓握路线，手指力量关键"),
                (25, "Alternate Hand & Foot Path", "Bouldering", 7, 6, 6, 5, 6, 6, 3, 8, "交替手脚路线，协调性挑战"),
                (26, "High Sliding Path", "Sport Climbing", 8, 7, 7, 6, 6, 6, 4, 8, "高滑动路线，控制力要求高"),
                (27, "Jumping Challenge Path", "Bouldering", 8, 8, 7, 5, 8, 7, 5, 9, "跳跃挑战路线，动态动作"),
                (28, "Mental Challenge Path", "Sport Climbing", 5, 5, 5, 5, 4, 4, 8, 7, "心理挑战路线，重在克服恐惧"),
                (29, "High Speed Climbing Path", "Bouldering", 7, 8, 6, 4, 6, 5, 3, 8, "高速攀登路线，速度与力量"),
                (30, "Tense Atmosphere Path", "Sport Climbing", 9, 8, 7, 5, 7, 6, 8, 9, "紧张氛围路线，压力下的表现"),
                (31, "Short Speed Path", "Bouldering", 4, 5, 5, 3, 6, 6, 2, 6, "短距离速度路线，快速完成"),
                (32, "High Difficulty Duel Path", "Sport Climbing", 8, 9, 8, 6, 6, 6, 7, 9, "高难度决斗路线，顶级挑战"),
                (33, "Upper Body Strength Path", "Bouldering", 7, 9, 7, 4, 5, 6, 4, 9, "上身力量路线，核心力量训练"),
                (34, "Defensive Path", "Sport Climbing", 6, 6, 6, 5, 7, 6, 3, 7, "防守型路线，稳定性重要"),
                (35, "Thrilling High Jump Path", "Bouldering", 9, 8, 7, 6, 8, 5, 7, 9, "刺激高跳路线，勇气与技巧"),
                (36, "Passing Through Large Holes Path", "Sport Climbing", 6, 5, 6, 5, 6, 6, 2, 7, "穿越大洞路线，空间感知"),
                (37, "Underground Cave Path", "Bouldering", 7, 7, 6, 5, 5, 7, 4, 8, "地下洞穴路线，特殊环境挑战"),
                (38, "Narrow Gap Path", "Sport Climbing", 6, 6, 7, 5, 6, 7, 4, 8, "狭窄缝隙路线，身体灵活性"),
                (39, "Sliding Fast Path", "Bouldering", 4, 6, 5, 3, 6, 4, 1, 6, "滑动快速路线，动态平衡"),
                (40, "Competition Route", "Sport Climbing", 8, 8, 9, 6, 8, 8, 6, 10, "比赛路线，最高难度综合挑战"),
            ]
            
            cursor.executemany("""
                INSERT INTO routes (id, name, category, balance, strength, technicality, 
                                  flexibility, strategy, endurance, mental_challenge, 
                                  overall_difficulty, description)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, routes_data)
            
            print(f"✅ 成功插入 {len(routes_data)} 条路线数据")
        
        conn.commit()
        conn.close()
        
        print("🎉 路线数据库初始化完成！")
        return True
        
    except sqlite3.Error as e:
        print(f"❌ 数据库操作失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        return False

if __name__ == "__main__":
    print("🚀 开始初始化路线数据...")
    success = init_routes_table()
    if success:
        print("✅ 路线数据初始化成功！")
    else:
        print("❌ 路线数据初始化失败！") 