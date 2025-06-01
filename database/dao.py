#!/usr/bin/env python3
"""
数据访问对象 (DAO)
提供所有表的完整CRUD操作
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, date
from .db_manager import db_manager
from .models import *

class BaseDAO:
    """基础DAO类，提供通用的CRUD操作"""
    
    def __init__(self, table_name: str):
        self.table_name = table_name
        self.db = db_manager
    
    def get_by_id(self, id: int) -> Optional[Dict[str, Any]]:
        """根据ID获取单条记录"""
        query = f"SELECT * FROM {self.table_name} WHERE id = ?"
        result = self.db.execute_query(query, (id,), fetch_one=True)
        return dict(result) if result else None
    
    def get_all(self) -> List[Dict[str, Any]]:
        """获取所有记录"""
        query = f"SELECT * FROM {self.table_name}"
        results = self.db.execute_query(query)
        return [dict(row) for row in results]
    
    def delete_by_id(self, id: int) -> int:
        """根据ID删除记录"""
        query = f"DELETE FROM {self.table_name} WHERE id = ?"
        return self.db.execute_update(query, (id,))

class UserDAO(BaseDAO):
    """用户数据访问对象"""
    
    def __init__(self):
        super().__init__('users')
    
    def create(self, user: User) -> int:
        """创建用户"""
        query = '''
            INSERT INTO users (username, password_hash, email)
            VALUES (?, ?, ?)
        '''
        return self.db.execute_insert(query, (user.username, user.password_hash, user.email))
    
    def update(self, id: int, user: User) -> int:
        """更新用户"""
        query = '''
            UPDATE users 
            SET username = ?, password_hash = ?, email = ?, updated_at = ?
            WHERE id = ?
        '''
        return self.db.execute_update(query, (
            user.username, user.password_hash, user.email, datetime.now(), id
        ))
    
    def get_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """根据用户名获取用户"""
        query = "SELECT * FROM users WHERE username = ?"
        result = self.db.execute_query(query, (username,), fetch_one=True)
        return dict(result) if result else None
    
    def get_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """根据邮箱获取用户"""
        query = "SELECT * FROM users WHERE email = ?"
        result = self.db.execute_query(query, (email,), fetch_one=True)
        return dict(result) if result else None
    
    def update_password(self, id: int, password_hash: str) -> int:
        """更新密码"""
        query = "UPDATE users SET password_hash = ?, updated_at = ? WHERE id = ?"
        return self.db.execute_update(query, (password_hash, datetime.now(), id))

class UserProfileDAO(BaseDAO):
    """用户资料数据访问对象"""
    
    def __init__(self):
        super().__init__('user_profiles')
    
    def create(self, profile: UserProfile) -> int:
        """创建用户资料"""
        query = '''
            INSERT INTO user_profiles (user_id, display_name, shoe_size, preferred_wall_type, bio)
            VALUES (?, ?, ?, ?, ?)
        '''
        return self.db.execute_insert(query, (
            profile.user_id, profile.display_name, profile.shoe_size, 
            profile.preferred_wall_type, profile.bio
        ))
    
    def update(self, id: int, profile: UserProfile) -> int:
        """更新用户资料"""
        query = '''
            UPDATE user_profiles 
            SET display_name = ?, shoe_size = ?, preferred_wall_type = ?, bio = ?, updated_at = ?
            WHERE id = ?
        '''
        return self.db.execute_update(query, (
            profile.display_name, profile.shoe_size, profile.preferred_wall_type, 
            profile.bio, datetime.now(), id
        ))
    
    def get_by_user_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """根据用户ID获取资料"""
        query = "SELECT * FROM user_profiles WHERE user_id = ?"
        result = self.db.execute_query(query, (user_id,), fetch_one=True)
        return dict(result) if result else None

class UserStatisticsDAO(BaseDAO):
    """用户统计数据访问对象"""
    
    def __init__(self):
        super().__init__('user_statistics')
    
    def create(self, stats: UserStatistics) -> int:
        """创建用户统计"""
        query = '''
            INSERT INTO user_statistics (user_id, total_sessions, total_climbs, sessions_this_month, sessions_this_year)
            VALUES (?, ?, ?, ?, ?)
        '''
        return self.db.execute_insert(query, (
            stats.user_id, stats.total_sessions, stats.total_climbs, 
            stats.sessions_this_month, stats.sessions_this_year
        ))
    
    def update(self, id: int, stats: UserStatistics) -> int:
        """更新用户统计"""
        query = '''
            UPDATE user_statistics 
            SET total_sessions = ?, total_climbs = ?, sessions_this_month = ?, 
                sessions_this_year = ?, last_calculated = ?, updated_at = ?
            WHERE id = ?
        '''
        return self.db.execute_update(query, (
            stats.total_sessions, stats.total_climbs, stats.sessions_this_month,
            stats.sessions_this_year, datetime.now(), datetime.now(), id
        ))
    
    def get_by_user_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """根据用户ID获取统计"""
        query = "SELECT * FROM user_statistics WHERE user_id = ?"
        result = self.db.execute_query(query, (user_id,), fetch_one=True)
        return dict(result) if result else None
    
    def update_by_user_id(self, user_id: int, stats: UserStatistics) -> int:
        """根据用户ID更新统计"""
        query = '''
            INSERT OR REPLACE INTO user_statistics 
            (user_id, total_sessions, total_climbs, sessions_this_month, sessions_this_year, last_calculated)
            VALUES (?, ?, ?, ?, ?, ?)
        '''
        return self.db.execute_update(query, (
            user_id, stats.total_sessions, stats.total_climbs,
            stats.sessions_this_month, stats.sessions_this_year, datetime.now()
        ))

class ClimbingSessionDAO(BaseDAO):
    """攀岩会话数据访问对象"""
    
    def __init__(self):
        super().__init__('climbing_sessions')
    
    def create(self, session: ClimbingSession) -> int:
        """创建攀岩会话"""
        query = '''
            INSERT INTO climbing_sessions (user_id, session_date, start_time, end_time, location, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        '''
        return self.db.execute_insert(query, (
            session.user_id, session.session_date, session.start_time,
            session.end_time, session.location, session.notes
        ))
    
    def update(self, id: int, session: ClimbingSession) -> int:
        """更新攀岩会话"""
        query = '''
            UPDATE climbing_sessions 
            SET session_date = ?, start_time = ?, end_time = ?, location = ?, notes = ?, updated_at = ?
            WHERE id = ?
        '''
        return self.db.execute_update(query, (
            session.session_date, session.start_time, session.end_time,
            session.location, session.notes, datetime.now(), id
        ))
    
    def get_by_user_id(self, user_id: int) -> List[Dict[str, Any]]:
        """根据用户ID获取所有会话"""
        query = "SELECT * FROM climbing_sessions WHERE user_id = ? ORDER BY session_date DESC"
        results = self.db.execute_query(query, (user_id,))
        return [dict(row) for row in results]
    
    def get_by_user_and_date(self, user_id: int, session_date: str) -> Optional[Dict[str, Any]]:
        """根据用户ID和日期获取会话"""
        query = "SELECT * FROM climbing_sessions WHERE user_id = ? AND session_date = ?"
        result = self.db.execute_query(query, (user_id, session_date), fetch_one=True)
        return dict(result) if result else None

class ClimbLogDAO(BaseDAO):
    """攀登记录数据访问对象"""
    
    def __init__(self):
        super().__init__('climb_logs')
    
    def create(self, log: ClimbLog) -> int:
        """创建攀登记录"""
        query = '''
            INSERT INTO climb_logs (session_id, user_id, climb_name, climb_type, grade, 
                                  attempt_result, attempts_count, image_filename, notes, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        return self.db.execute_insert(query, (
            log.session_id, log.user_id, log.climb_name, log.climb_type, log.grade,
            log.attempt_result, log.attempts_count, log.image_filename, log.notes, 
            log.timestamp or datetime.now()
        ))
    
    def update(self, id: int, log: ClimbLog) -> int:
        """更新攀登记录"""
        query = '''
            UPDATE climb_logs 
            SET climb_name = ?, climb_type = ?, grade = ?, attempt_result = ?, 
                attempts_count = ?, image_filename = ?, notes = ?
            WHERE id = ?
        '''
        return self.db.execute_update(query, (
            log.climb_name, log.climb_type, log.grade, log.attempt_result,
            log.attempts_count, log.image_filename, log.notes, id
        ))
    
    def get_by_user_id(self, user_id: int) -> List[Dict[str, Any]]:
        """根据用户ID获取所有攀登记录"""
        query = '''
            SELECT cl.*, cs.session_date, cs.location
            FROM climb_logs cl
            JOIN climbing_sessions cs ON cl.session_id = cs.id
            WHERE cl.user_id = ?
            ORDER BY cl.timestamp DESC
        '''
        results = self.db.execute_query(query, (user_id,))
        return [dict(row) for row in results]
    
    def get_by_session_id(self, session_id: int) -> List[Dict[str, Any]]:
        """根据会话ID获取攀登记录"""
        query = "SELECT * FROM climb_logs WHERE session_id = ? ORDER BY timestamp DESC"
        results = self.db.execute_query(query, (session_id,))
        return [dict(row) for row in results]
    
    def get_by_user_and_type(self, user_id: int, climb_type: str) -> List[Dict[str, Any]]:
        """根据用户ID和攀岩类型获取记录"""
        query = "SELECT * FROM climb_logs WHERE user_id = ? AND climb_type = ? ORDER BY timestamp DESC"
        results = self.db.execute_query(query, (user_id, climb_type))
        return [dict(row) for row in results]

class PersonalBestDAO(BaseDAO):
    """个人最佳记录数据访问对象"""
    
    def __init__(self):
        super().__init__('personal_bests')
    
    def create(self, best: PersonalBest) -> int:
        """创建个人最佳记录"""
        query = '''
            INSERT INTO personal_bests (user_id, climb_type, best_grade, climb_log_id, achieved_date)
            VALUES (?, ?, ?, ?, ?)
        '''
        return self.db.execute_insert(query, (
            best.user_id, best.climb_type, best.best_grade, best.climb_log_id, best.achieved_date
        ))
    
    def update(self, id: int, best: PersonalBest) -> int:
        """更新个人最佳记录"""
        query = '''
            UPDATE personal_bests 
            SET best_grade = ?, climb_log_id = ?, achieved_date = ?, updated_at = ?
            WHERE id = ?
        '''
        return self.db.execute_update(query, (
            best.best_grade, best.climb_log_id, best.achieved_date, datetime.now(), id
        ))
    
    def get_by_user_id(self, user_id: int) -> List[Dict[str, Any]]:
        """根据用户ID获取所有个人最佳记录"""
        query = "SELECT * FROM personal_bests WHERE user_id = ?"
        results = self.db.execute_query(query, (user_id,))
        return [dict(row) for row in results]
    
    def get_by_user_and_type(self, user_id: int, climb_type: str) -> Optional[Dict[str, Any]]:
        """根据用户ID和攀岩类型获取个人最佳记录"""
        query = "SELECT * FROM personal_bests WHERE user_id = ? AND climb_type = ?"
        result = self.db.execute_query(query, (user_id, climb_type), fetch_one=True)
        return dict(result) if result else None
    
    def update_by_user_and_type(self, user_id: int, climb_type: str, best: PersonalBest) -> int:
        """根据用户ID和攀岩类型更新个人最佳记录"""
        query = '''
            UPDATE personal_bests 
            SET best_grade = ?, climb_log_id = ?, achieved_date = ?, updated_at = ?
            WHERE user_id = ? AND climb_type = ?
        '''
        return self.db.execute_update(query, (
            best.best_grade, best.climb_log_id, best.achieved_date, datetime.now(), user_id, climb_type
        ))

class ClimbingGymDAO(BaseDAO):
    """攀岩场馆数据访问对象"""
    
    def __init__(self):
        super().__init__('climbing_gyms')
    
    def create(self, gym: ClimbingGym) -> int:
        """创建攀岩场馆"""
        query = '''
            INSERT INTO climbing_gyms (name, address, phone, website, opening_hours)
            VALUES (?, ?, ?, ?, ?)
        '''
        return self.db.execute_insert(query, (
            gym.name, gym.address, gym.phone, gym.website, gym.opening_hours
        ))
    
    def update(self, id: int, gym: ClimbingGym) -> int:
        """更新攀岩场馆"""
        query = '''
            UPDATE climbing_gyms 
            SET name = ?, address = ?, phone = ?, website = ?, opening_hours = ?, updated_at = ?
            WHERE id = ?
        '''
        return self.db.execute_update(query, (
            gym.name, gym.address, gym.phone, gym.website, gym.opening_hours, datetime.now(), id
        ))
    
    def get_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """根据名称获取场馆"""
        query = "SELECT * FROM climbing_gyms WHERE name = ?"
        result = self.db.execute_query(query, (name,), fetch_one=True)
        return dict(result) if result else None

class MovementNoteDAO(BaseDAO):
    """动作笔记数据访问对象"""
    
    def __init__(self):
        super().__init__('movement_notes')
    
    def create(self, note: MovementNote) -> int:
        """创建动作笔记"""
        query = '''
            INSERT INTO movement_notes (user_id, climb_log_id, title, content, movement_type, tags)
            VALUES (?, ?, ?, ?, ?, ?)
        '''
        return self.db.execute_insert(query, (
            note.user_id, note.climb_log_id, note.title, note.content, note.movement_type, note.tags
        ))
    
    def update(self, id: int, note: MovementNote) -> int:
        """更新动作笔记"""
        query = '''
            UPDATE movement_notes 
            SET title = ?, content = ?, movement_type = ?, tags = ?, updated_at = ?
            WHERE id = ?
        '''
        return self.db.execute_update(query, (
            note.title, note.content, note.movement_type, note.tags, datetime.now(), id
        ))
    
    def get_by_user_id(self, user_id: int) -> List[Dict[str, Any]]:
        """根据用户ID获取所有动作笔记"""
        query = "SELECT * FROM movement_notes WHERE user_id = ? ORDER BY created_at DESC"
        results = self.db.execute_query(query, (user_id,))
        return [dict(row) for row in results]
    
    def get_by_climb_log_id(self, climb_log_id: int) -> List[Dict[str, Any]]:
        """根据攀登记录ID获取动作笔记"""
        query = "SELECT * FROM movement_notes WHERE climb_log_id = ?"
        results = self.db.execute_query(query, (climb_log_id,))
        return [dict(row) for row in results]

class CrowdDetectionDAO(BaseDAO):
    """人流检测数据访问对象"""
    
    def __init__(self):
        super().__init__('crowd_detection')
    
    def create(self, crowd: CrowdDetection) -> int:
        """创建人流检测记录"""
        query = '''
            INSERT INTO crowd_detection (gym_id, detection_time, people_count, activity_level, image_filename, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        '''
        return self.db.execute_insert(query, (
            crowd.gym_id, crowd.detection_time, crowd.people_count, 
            crowd.activity_level, crowd.image_filename, crowd.notes
        ))
    
    def update(self, id: int, crowd: CrowdDetection) -> int:
        """更新人流检测记录"""
        query = '''
            UPDATE crowd_detection 
            SET people_count = ?, activity_level = ?, image_filename = ?, notes = ?
            WHERE id = ?
        '''
        return self.db.execute_update(query, (
            crowd.people_count, crowd.activity_level, crowd.image_filename, crowd.notes, id
        ))
    
    def get_by_gym_id(self, gym_id: int) -> List[Dict[str, Any]]:
        """根据场馆ID获取人流检测记录"""
        query = "SELECT * FROM crowd_detection WHERE gym_id = ? ORDER BY detection_time DESC"
        results = self.db.execute_query(query, (gym_id,))
        return [dict(row) for row in results]
    
    def get_recent_by_gym(self, gym_id: int, hours: int = 24) -> List[Dict[str, Any]]:
        """获取场馆最近的人流检测记录"""
        query = '''
            SELECT * FROM crowd_detection 
            WHERE gym_id = ? AND detection_time >= datetime('now', '-{} hours')
            ORDER BY detection_time DESC
        '''.format(hours)
        results = self.db.execute_query(query, (gym_id,))
        return [dict(row) for row in results]

# DAO实例
user_dao = UserDAO()
user_profile_dao = UserProfileDAO()
user_statistics_dao = UserStatisticsDAO()
climbing_session_dao = ClimbingSessionDAO()
climb_log_dao = ClimbLogDAO()
personal_best_dao = PersonalBestDAO()
climbing_gym_dao = ClimbingGymDAO()
movement_note_dao = MovementNoteDAO()
crowd_detection_dao = CrowdDetectionDAO() 