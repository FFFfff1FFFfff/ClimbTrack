#!/usr/bin/env python3
"""
添加路线字段迁移脚本
在climb_logs表中添加route_id和route_name字段
"""

import sqlite3
import os
from datetime import datetime

def migrate_add_route_fields():
    """添加路线相关字段到climb_logs表"""
    
    # 数据库文件路径
    db_path = 'database/climbtrack.db'
    
    # 检查数据库文件是否存在
    if not os.path.exists(db_path):
        print("❌ 数据库文件不存在！")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 检查climb_logs表是否存在
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='climb_logs'
        """)
        
        if not cursor.fetchone():
            print("❌ climb_logs表不存在！")
            return False
        
        print("🔄 开始添加路线字段...")
        
        # 检查字段是否已存在
        cursor.execute("PRAGMA table_info(climb_logs)")
        columns = [column[1] for column in cursor.fetchall()]
        
        fields_to_add = []
        if 'route_id' not in columns:
            fields_to_add.append(('route_id', 'INTEGER'))
        if 'route_name' not in columns:
            fields_to_add.append(('route_name', 'VARCHAR(200)'))
        
        if not fields_to_add:
            print("✅ 所有字段已存在，无需迁移")
            return True
        
        # 添加新字段
        for field_name, field_type in fields_to_add:
            print(f"🔧 添加字段: {field_name} ({field_type})")
            cursor.execute(f"ALTER TABLE climb_logs ADD COLUMN {field_name} {field_type}")
        
        # 添加外键约束（如果可能）
        if 'route_id' in [field[0] for field in fields_to_add]:
            print("📝 注意：route_id字段已添加，但外键约束需要在应用层维护")
        
        conn.commit()
        conn.close()
        
        print("🎉 路线字段添加完成！")
        print("✅ 新增字段:")
        for field_name, field_type in fields_to_add:
            print(f"   - {field_name}: {field_type}")
        
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
    print("🚀 开始添加路线字段迁移...")
    success = migrate_add_route_fields()
    if success:
        print("✅ 路线字段迁移成功！")
    else:
        print("❌ 路线字段迁移失败！") 