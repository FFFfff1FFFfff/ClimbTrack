#!/usr/bin/env python3
"""
数据库连接管理器
提供统一的数据库连接和事务管理
"""

import sqlite3
import os
from contextlib import contextmanager
from typing import Optional, Any, Dict, List

class DatabaseManager:
    """数据库管理器"""
    
    def __init__(self, db_path: str = 'database/climbtrack.db'):
        self.db_path = db_path
        
    def get_connection(self) -> sqlite3.Connection:
        """获取数据库连接"""
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"数据库文件不存在: {self.db_path}")
        
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    @contextmanager
    def get_cursor(self, transaction: bool = False):
        """获取数据库游标的上下文管理器"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            yield cursor
            if transaction:
                conn.commit()
        except Exception as e:
            if transaction:
                conn.rollback()
            raise e
        finally:
            conn.close()
    
    def execute_query(self, query: str, params: tuple = (), fetch_one: bool = False, fetch_all: bool = True) -> Any:
        """执行查询语句"""
        with self.get_cursor() as cursor:
            cursor.execute(query, params)
            
            if fetch_one:
                return cursor.fetchone()
            elif fetch_all:
                return cursor.fetchall()
            else:
                return cursor.rowcount
    
    def execute_update(self, query: str, params: tuple = ()) -> int:
        """执行更新语句，返回受影响的行数"""
        with self.get_cursor(transaction=True) as cursor:
            cursor.execute(query, params)
            return cursor.rowcount
    
    def execute_insert(self, query: str, params: tuple = ()) -> int:
        """执行插入语句，返回新插入记录的ID"""
        with self.get_cursor(transaction=True) as cursor:
            cursor.execute(query, params)
            return cursor.lastrowid
    
    def execute_many(self, query: str, params_list: List[tuple]) -> int:
        """执行批量操作"""
        with self.get_cursor(transaction=True) as cursor:
            cursor.executemany(query, params_list)
            return cursor.rowcount

# 全局数据库管理器实例
db_manager = DatabaseManager() 