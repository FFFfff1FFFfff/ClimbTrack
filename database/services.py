#!/usr/bin/env python3
"""
业务逻辑服务层
处理复杂的业务操作和数据联动
"""

import hashlib
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, date
from collections import defaultdict
import os

from .dao import *
from .models import *

class AuthService:
    """认证服务"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """加密密码"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def verify_password(stored_password: str, provided_password: str) -> bool:
        """验证密码"""
        return stored_password == AuthService.hash_password(provided_password)
    
    @staticmethod
    def create_user(username: str, password: str, email: str = "") -> Optional[int]:
        """创建新用户，包括相关资料和统计记录"""
        try:
            # 检查用户名是否已存在
            if user_dao.get_by_username(username):
                return None
            
            # 创建用户
            user = User(
                username=username,
                password_hash=AuthService.hash_password(password),
                email=email
            )
            user_id = user_dao.create(user)
            
            # 创建用户资料
            profile = UserProfile(
                user_id=user_id,
                display_name=username
            )
            user_profile_dao.create(profile)
            
            # 初始化统计数据
            stats = UserStatistics(user_id=user_id)
            user_statistics_dao.create(stats)
            
            return user_id
        except Exception as e:
            print(f"创建用户失败: {e}")
            return None
    
    @staticmethod
    def authenticate_user(username: str, password: str) -> Optional[Dict[str, Any]]:
        """用户认证"""
        user = user_dao.get_by_username(username)
        if user and AuthService.verify_password(user['password_hash'], password):
            return user
        return None
    
    @staticmethod
    def update_password(username: str, new_password: str) -> bool:
        """更新密码"""
        user = user_dao.get_by_username(username)
        if user:
            password_hash = AuthService.hash_password(new_password)
            return user_dao.update_password(user['id'], password_hash) > 0
        return False

class UserService:
    """用户服务"""
    
    @staticmethod
    def get_user_info(user_id: int) -> Optional[Dict[str, Any]]:
        """获取用户完整信息"""
        user = user_dao.get_by_id(user_id)
        if not user:
            return None
        
        profile = user_profile_dao.get_by_user_id(user_id)
        stats = user_statistics_dao.get_by_user_id(user_id)
        personal_bests = personal_best_dao.get_by_user_id(user_id)
        
        return {
            'user': user,
            'profile': profile,
            'statistics': stats,
            'personal_bests': personal_bests
        }
    
    @staticmethod
    def update_user_profile(user_id: int, profile_data: Dict[str, Any]) -> bool:
        """更新用户资料"""
        profile = user_profile_dao.get_by_user_id(user_id)
        if profile:
            updated_profile = UserProfile(
                user_id=user_id,
                display_name=profile_data.get('display_name', profile['display_name']),
                shoe_size=profile_data.get('shoe_size', profile['shoe_size']),
                preferred_wall_type=profile_data.get('preferred_wall_type', profile['preferred_wall_type']),
                bio=profile_data.get('bio', profile['bio'])
            )
            return user_profile_dao.update(profile['id'], updated_profile) > 0
        else:
            # 创建新的用户资料
            new_profile = UserProfile(
                user_id=user_id,
                display_name=profile_data.get('display_name', ''),
                shoe_size=profile_data.get('shoe_size', ''),
                preferred_wall_type=profile_data.get('preferred_wall_type', ''),
                bio=profile_data.get('bio', '')
            )
            return user_profile_dao.create(new_profile) > 0

class ClimbingService:
    """攀岩服务"""
    
    @staticmethod
    def v_grade_key(grade: str) -> int:
        """V等级转换为数值，用于比较"""
        if not grade or not grade.startswith('V'):
            return -1
        try:
            return int(grade[1:])
        except:
            return -1
    
    @staticmethod
    def french_grade_key(grade: str) -> int:
        """法式等级转换为数值，用于比较"""
        order = ['a', 'a+', 'b', 'b+', 'c', 'c+']
        if not grade:
            return -1
        try:
            num = int(grade[0])
            rest = grade[1:]
            idx = order.index(rest)
            return num * 10 + idx
        except:
            return -1
    
    @staticmethod
    def create_climb_log(user_id: int, session_date: str, climb_data: Dict[str, Any]) -> Optional[int]:
        """创建攀登记录，包括会话管理和个人最佳更新"""
        try:
            # 获取或创建当天的会话
            session = climbing_session_dao.get_by_user_and_date(user_id, session_date)
            if not session:
                new_session = ClimbingSession(
                    user_id=user_id,
                    session_date=session_date,
                    location=climb_data.get('location', 'Climbing Gym'),
                    notes=f'Session on {session_date}'
                )
                session_id = climbing_session_dao.create(new_session)
            else:
                session_id = session['id']
            
            # 创建攀登记录
            climb_log = ClimbLog(
                session_id=session_id,
                user_id=user_id,
                climb_name=climb_data['name'],
                climb_type=climb_data['type'],
                grade=climb_data['grade'],
                attempt_result=climb_data.get('attempt_result', 'completed'),
                attempts_count=climb_data.get('attempts_count', 1),
                image_filename=climb_data.get('image_filename', ''),
                notes=climb_data.get('notes', ''),
                timestamp=datetime.now()
            )
            climb_log_id = climb_log_dao.create(climb_log)
            
            # 更新个人最佳记录
            ClimbingService.update_personal_best(user_id, climb_data['type'], climb_data['grade'], climb_log_id)
            
            # 更新用户统计
            StatisticsService.update_user_statistics(user_id)
            
            return climb_log_id
        except Exception as e:
            print(f"创建攀登记录失败: {e}")
            return None
    
    @staticmethod
    def update_personal_best(user_id: int, climb_type: str, grade: str, climb_log_id: int):
        """更新个人最佳记录"""
        existing = personal_best_dao.get_by_user_and_type(user_id, climb_type)
        
        if existing:
            # 比较等级
            if climb_type == 'bouldering':
                current_grade_val = ClimbingService.v_grade_key(existing['best_grade'])
                new_grade_val = ClimbingService.v_grade_key(grade)
            else:
                current_grade_val = ClimbingService.french_grade_key(existing['best_grade'])
                new_grade_val = ClimbingService.french_grade_key(grade)
            
            if new_grade_val > current_grade_val:
                best = PersonalBest(
                    best_grade=grade,
                    climb_log_id=climb_log_id,
                    achieved_date=date.today().strftime('%Y-%m-%d')
                )
                personal_best_dao.update_by_user_and_type(user_id, climb_type, best)
        else:
            # 插入新记录
            best = PersonalBest(
                user_id=user_id,
                climb_type=climb_type,
                best_grade=grade,
                climb_log_id=climb_log_id,
                achieved_date=date.today().strftime('%Y-%m-%d')
            )
            personal_best_dao.create(best)
    
    @staticmethod
    def get_user_climb_logs_grouped(user_id: int) -> Tuple[Dict[str, List], List[Dict]]:
        """获取用户的攀登记录，按日期分组"""
        logs = climb_log_dao.get_by_user_id(user_id)
        
        # 按日期分组
        grouped_logs = defaultdict(list)
        formatted_logs = []
        
        for log in logs:
            # 转换为与模板兼容的格式
            log_dict = {
                'id': log['id'],  # Add ID for delete functionality
                'date': log['timestamp'],
                'session_date': log['session_date'],  # Add session_date for edit functionality
                'image': log['image_filename'],
                'grade': log['grade'],
                'note': log['notes'],
                'name': log['climb_name'],
                'type': log['climb_type']
            }
            log_day = log['session_date']
            grouped_logs[log_day].append(log_dict)
            formatted_logs.append(log_dict)
        
        return dict(grouped_logs), formatted_logs
    
    @staticmethod
    def delete_climb_log(log_id: int, user_id: int) -> bool:
        """删除攀登记录"""
        try:
            # First verify that this log belongs to the user
            log = climb_log_dao.get_by_id(log_id)
            if not log or log['user_id'] != user_id:
                return False
            
            # Delete the associated image file if it exists
            if log['image_filename']:
                image_path = os.path.join('static/uploads', log['image_filename'])
                if os.path.exists(image_path):
                    os.remove(image_path)
            
            # Delete the climb log
            result = climb_log_dao.delete_by_id(log_id)
            
            # Update user statistics
            if result > 0:
                StatisticsService.update_user_statistics(user_id)
                return True
            return False
        except Exception as e:
            print(f"删除攀登记录失败: {e}")
            return False
    
    @staticmethod
    def update_climb_log(log_id: int, user_id: int, climb_data: Dict[str, Any], new_image_filename: Optional[str] = None) -> bool:
        """更新攀登记录"""
        try:
            print(f"🔍 update_climb_log called: log_id={log_id}, user_id={user_id}")  # Debug
            
            # First verify that this log belongs to the user
            existing_log = climb_log_dao.get_by_id(log_id)
            if not existing_log:
                print(f"❌ Log {log_id} not found")  # Debug
                return False
            if existing_log['user_id'] != user_id:
                print(f"❌ Log {log_id} does not belong to user {user_id}, belongs to {existing_log['user_id']}")  # Debug
                return False
            
            print(f"✅ Found existing log: {existing_log}")  # Debug
            
            # Handle image file update
            image_filename = existing_log['image_filename']
            if new_image_filename:
                print(f"🖼️ Updating image from {image_filename} to {new_image_filename}")  # Debug
                # Delete old image if it exists
                if existing_log['image_filename']:
                    old_image_path = os.path.join('static/uploads', existing_log['image_filename'])
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)
                        print(f"🗑️ Deleted old image: {old_image_path}")  # Debug
                image_filename = new_image_filename
            
            # Update the climb log
            updated_log = ClimbLog(
                id=log_id,
                session_id=existing_log['session_id'],
                user_id=user_id,
                climb_name=climb_data['name'],
                climb_type=climb_data['type'],
                grade=climb_data['grade'],
                attempt_result=climb_data.get('attempt_result', existing_log['attempt_result']),
                attempts_count=climb_data.get('attempts_count', existing_log['attempts_count']),
                image_filename=image_filename,
                notes=climb_data.get('notes', ''),
                timestamp=existing_log['timestamp']  # Keep original timestamp
            )
            
            print(f"📝 Calling DAO update with: {updated_log.__dict__}")  # Debug
            
            result = climb_log_dao.update(log_id, updated_log)
            print(f"🔄 DAO update result: {result}")  # Debug
            
            # Update personal best if grade improved
            ClimbingService.update_personal_best(user_id, climb_data['type'], climb_data['grade'], log_id)
            
            # Update user statistics
            if result > 0:
                StatisticsService.update_user_statistics(user_id)
                print(f"✅ Successfully updated log {log_id}")  # Debug
                return True
            else:
                print(f"❌ DAO update returned {result} for log {log_id}")  # Debug
                return False
        except Exception as e:
            print(f"💥 Exception in update_climb_log: {e}")  # Debug
            return False
    
    @staticmethod
    def get_climbing_rankings() -> Dict[str, List[Dict]]:
        """获取攀岩排名"""
        query = '''
            SELECT user_id, username, best_grade, achieved_date, rank
            FROM climbing_rankings 
            WHERE climb_type = ?
            ORDER BY rank
        '''
        
        # 获取抱石排名
        bouldering_results = db_manager.execute_query(query, ('bouldering',))
        bouldering_ranks = [{'name': row['username'], 'grade': row['best_grade'], 'date': row['achieved_date']} 
                           for row in bouldering_results]
        
        # 获取线路攀登排名
        sport_results = db_manager.execute_query(query, ('sport',))
        sport_ranks = [{'name': row['username'], 'grade': row['best_grade'], 'date': row['achieved_date']} 
                      for row in sport_results]
        
        return {
            'bouldering': bouldering_ranks,
            'sport': sport_ranks
        }

class StatisticsService:
    """统计服务"""
    
    @staticmethod
    def update_user_statistics(user_id: int):
        """更新用户统计数据"""
        try:
            # 计算总会话数
            sessions = climbing_session_dao.get_by_user_id(user_id)
            total_sessions = len(sessions)
            
            # 计算总攀登次数
            logs = climb_log_dao.get_by_user_id(user_id)
            total_climbs = len(logs)
            
            # 计算本月会话数
            current_month = date.today().strftime('%Y-%m')
            sessions_this_month = len([s for s in sessions if s['session_date'].startswith(current_month)])
            
            # 计算今年会话数
            current_year = date.today().strftime('%Y')
            sessions_this_year = len([s for s in sessions if s['session_date'].startswith(current_year)])
            
            # 更新统计数据
            stats = UserStatistics(
                user_id=user_id,
                total_sessions=total_sessions,
                total_climbs=total_climbs,
                sessions_this_month=sessions_this_month,
                sessions_this_year=sessions_this_year
            )
            
            user_statistics_dao.update_by_user_id(user_id, stats)
        except Exception as e:
            print(f"更新用户统计失败: {e}")
    
    @staticmethod
    def update_all_user_statistics():
        """更新所有用户的统计数据"""
        users = user_dao.get_all()
        for user in users:
            StatisticsService.update_user_statistics(user['id'])
    
    @staticmethod
    def get_user_profile_stats(user_id: int) -> Dict[str, Any]:
        """获取用户资料页面的统计数据"""
        user_info = UserService.get_user_info(user_id)
        if not user_info:
            return {}
        
        profile = user_info['profile']
        statistics = user_info['statistics']
        personal_bests = user_info['personal_bests']
        
        # 整理数据
        stats = {
            'bouldering_max': 'N/A',
            'sport_max': 'N/A',
            'sessions_this_month': statistics['sessions_this_month'] if statistics else 0,
            'total_sessions': statistics['total_sessions'] if statistics else 0,
            'total_tops': statistics['total_climbs'] if statistics else 0,
            'shoe_size': profile['shoe_size'] if profile else 'N/A',
            'wall_pref': profile['preferred_wall_type'] if profile else 'N/A',
        }
        
        # 设置个人最佳记录
        for best in personal_bests:
            if best['climb_type'] == 'bouldering':
                stats['bouldering_max'] = best['best_grade']
            elif best['climb_type'] == 'sport':
                stats['sport_max'] = best['best_grade']
        
        # 计算排名（简化版）
        stats['bouldering_rank'] = StatisticsService.get_user_rank(user_id, 'bouldering')
        stats['sport_rank'] = StatisticsService.get_user_rank(user_id, 'sport')
        stats['attendance_rank'] = 'N/A'  # 可以后续实现
        
        return stats
    
    @staticmethod
    def get_user_rank(user_id: int, climb_type: str) -> str:
        """获取用户在指定类型中的排名"""
        try:
            query = '''
                SELECT COUNT(*) + 1 as rank FROM personal_bests pb1
                JOIN personal_bests pb2 ON pb1.user_id = ?
                WHERE pb1.climb_type = ? AND pb2.climb_type = ?
            '''
            
            if climb_type == 'bouldering':
                query += '''
                    AND (CASE WHEN pb2.best_grade LIKE 'V%' THEN CAST(SUBSTR(pb2.best_grade, 2) AS INTEGER) ELSE -1 END) > 
                        (CASE WHEN pb1.best_grade LIKE 'V%' THEN CAST(SUBSTR(pb1.best_grade, 2) AS INTEGER) ELSE -1 END)
                '''
            
            result = db_manager.execute_query(query, (user_id, climb_type, climb_type), fetch_one=True)
            return str(result['rank']) if result else 'N/A'
        except:
            return 'N/A'

class GymService:
    """场馆服务"""
    
    @staticmethod
    def create_gym(gym_data: Dict[str, Any]) -> Optional[int]:
        """创建攀岩场馆"""
        gym = ClimbingGym(
            name=gym_data['name'],
            address=gym_data.get('address', ''),
            phone=gym_data.get('phone', ''),
            website=gym_data.get('website', ''),
            opening_hours=gym_data.get('opening_hours', '')
        )
        return climbing_gym_dao.create(gym)
    
    @staticmethod
    def update_gym(gym_id: int, gym_data: Dict[str, Any]) -> bool:
        """更新攀岩场馆"""
        gym = ClimbingGym(
            name=gym_data['name'],
            address=gym_data.get('address', ''),
            phone=gym_data.get('phone', ''),
            website=gym_data.get('website', ''),
            opening_hours=gym_data.get('opening_hours', '')
        )
        return climbing_gym_dao.update(gym_id, gym) > 0
    
    @staticmethod
    def add_crowd_detection(gym_id: int, people_count: int, activity_level: str, notes: str = "") -> Optional[int]:
        """添加人流检测记录"""
        crowd = CrowdDetection(
            gym_id=gym_id,
            detection_time=datetime.now(),
            people_count=people_count,
            activity_level=activity_level,
            notes=notes
        )
        return crowd_detection_dao.create(crowd)

class NoteService:
    """笔记服务"""
    
    @staticmethod
    def create_movement_note(user_id: int, climb_log_id: int, note_data: Dict[str, Any]) -> Optional[int]:
        """创建动作笔记"""
        note = MovementNote(
            user_id=user_id,
            climb_log_id=climb_log_id,
            title=note_data['title'],
            content=note_data['content'],
            movement_type=note_data.get('movement_type', ''),
            tags=note_data.get('tags', '')
        )
        return movement_note_dao.create(note)
    
    @staticmethod
    def update_movement_note(note_id: int, note_data: Dict[str, Any]) -> bool:
        """更新动作笔记"""
        note = MovementNote(
            title=note_data['title'],
            content=note_data['content'],
            movement_type=note_data.get('movement_type', ''),
            tags=note_data.get('tags', '')
        )
        return movement_note_dao.update(note_id, note) > 0 