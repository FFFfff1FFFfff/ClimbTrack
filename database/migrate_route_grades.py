#!/usr/bin/env python3
"""
路线等级迁移脚本
将routes表的overall_difficulty从数字等级转换为标准攀岩等级
Bouldering: V0-V16
Sport Climbing: 5a-9b+
"""

import sqlite3
import os
from datetime import datetime

def migrate_route_grades():
    """迁移路线等级系统"""
    
    # 数据库文件路径
    db_path = 'database/climbtrack.db'
    
    # 检查数据库文件是否存在
    if not os.path.exists(db_path):
        print("❌ 数据库文件不存在！")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 检查routes表是否存在
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='routes'
        """)
        
        if not cursor.fetchone():
            print("❌ routes表不存在！")
            return False
        
        print("🔄 开始迁移路线等级...")
        
        # 1. 备份原始数据
        print("📋 备份原始数据...")
        cursor.execute("SELECT id, name, category, overall_difficulty FROM routes")
        original_data = cursor.fetchall()
        print(f"📊 找到 {len(original_data)} 条路线记录")
        
        # 2. 添加新的等级字段（临时）
        print("🔧 添加临时等级字段...")
        try:
            cursor.execute("ALTER TABLE routes ADD COLUMN new_overall_difficulty VARCHAR(10)")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("⚠️  临时字段已存在，跳过创建")
            else:
                raise e
        
        # 3. 定义等级映射
        def get_bouldering_grade(difficulty):
            """将数字难度转换为V等级"""
            mapping = {
                1: "V0", 2: "V1", 3: "V2", 4: "V3", 5: "V4",
                6: "V5", 7: "V6", 8: "V7", 9: "V8", 10: "V9"
            }
            return mapping.get(difficulty, "V0")
        
        def get_sport_grade(difficulty):
            """将数字难度转换为法式等级"""
            mapping = {
                1: "5a", 2: "5b", 3: "5c", 4: "6a", 5: "6b",
                6: "6c", 7: "7a", 8: "7b", 9: "7c", 10: "8a"
            }
            return mapping.get(difficulty, "5a")
        
        # 4. 更新数据
        print("🔄 转换等级数据...")
        updated_count = 0
        
        for route_id, name, category, old_difficulty in original_data:
            if category == "Bouldering":
                new_grade = get_bouldering_grade(old_difficulty)
            elif category == "Sport Climbing":
                new_grade = get_sport_grade(old_difficulty)
            else:
                new_grade = "V0"  # 默认值
            
            cursor.execute("""
                UPDATE routes 
                SET new_overall_difficulty = ?
                WHERE id = ?
            """, (new_grade, route_id))
            
            updated_count += 1
            if updated_count % 10 == 0:
                print(f"✅ 已更新 {updated_count}/{len(original_data)} 条记录")
        
        print(f"✅ 完成数据转换，共更新 {updated_count} 条记录")
        
        # 5. 删除旧字段，重命名新字段
        print("🔧 重构表结构...")
        
        # 创建新表结构
        cursor.execute("""
            CREATE TABLE routes_new (
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
                overall_difficulty VARCHAR(10) NOT NULL,
                description TEXT,
                image_filename VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 复制数据到新表
        cursor.execute("""
            INSERT INTO routes_new (
                id, name, category, balance, strength, technicality, 
                flexibility, strategy, endurance, mental_challenge, 
                overall_difficulty, description, image_filename, 
                created_at, updated_at
            )
            SELECT 
                id, name, category, balance, strength, technicality,
                flexibility, strategy, endurance, mental_challenge,
                new_overall_difficulty, description, image_filename,
                created_at, updated_at
            FROM routes
        """)
        
        # 删除旧表，重命名新表
        cursor.execute("DROP TABLE routes")
        cursor.execute("ALTER TABLE routes_new RENAME TO routes")
        
        # 重新创建索引
        cursor.execute("CREATE INDEX idx_routes_category ON routes(category)")
        cursor.execute("CREATE INDEX idx_routes_difficulty ON routes(overall_difficulty)")
        cursor.execute("CREATE INDEX idx_routes_name ON routes(name)")
        
        # 6. 验证迁移结果
        print("🔍 验证迁移结果...")
        cursor.execute("SELECT category, overall_difficulty, COUNT(*) FROM routes GROUP BY category, overall_difficulty ORDER BY category, overall_difficulty")
        results = cursor.fetchall()
        
        print("\n📊 迁移后的等级分布:")
        print("-" * 40)
        for category, grade, count in results:
            print(f"{category:15} {grade:6} : {count:2} 条路线")
        
        conn.commit()
        conn.close()
        
        print("\n🎉 路线等级迁移完成！")
        print("✅ Bouldering路线现在使用V等级 (V0-V9)")
        print("✅ Sport Climbing路线现在使用法式等级 (5a-8a)")
        return True
        
    except sqlite3.Error as e:
        print(f"❌ 数据库操作失败: {e}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        return False
    except Exception as e:
        print(f"❌ 迁移失败: {e}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        return False

if __name__ == "__main__":
    print("🚀 开始路线等级迁移...")
    success = migrate_route_grades()
    if success:
        print("✅ 路线等级迁移成功！")
    else:
        print("❌ 路线等级迁移失败！") 