#!/usr/bin/env python3
"""
数据模型定义
定义所有数据库表对应的数据结构
"""

from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any
from datetime import datetime, date

@dataclass
class User:
    """用户模型"""
    id: Optional[int] = None
    username: str = ""
    password_hash: str = ""
    email: str = ""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class UserProfile:
    """用户资料模型"""
    id: Optional[int] = None
    user_id: int = 0
    display_name: str = ""
    shoe_size: str = ""
    preferred_wall_type: str = ""
    bio: str = ""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class UserStatistics:
    """用户统计模型"""
    id: Optional[int] = None
    user_id: int = 0
    total_sessions: int = 0
    total_climbs: int = 0
    sessions_this_month: int = 0
    sessions_this_year: int = 0
    last_calculated: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class ClimbingSession:
    """攀岩会话模型"""
    id: Optional[int] = None
    user_id: int = 0
    session_date: str = ""
    start_time: str = ""
    end_time: str = ""
    location: str = ""
    notes: str = ""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class ClimbLog:
    """攀登记录模型"""
    id: Optional[int] = None
    session_id: int = 0
    user_id: int = 0
    climb_name: str = ""
    climb_type: str = ""
    grade: str = ""
    attempt_result: str = ""
    attempts_count: int = 1
    image_filename: str = ""
    notes: str = ""
    timestamp: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class PersonalBest:
    """个人最佳记录模型"""
    id: Optional[int] = None
    user_id: int = 0
    climb_type: str = ""
    best_grade: str = ""
    climb_log_id: int = 0
    achieved_date: str = ""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class ClimbingGym:
    """攀岩场馆模型"""
    id: Optional[int] = None
    name: str = ""
    address: str = ""
    phone: str = ""
    website: str = ""
    opening_hours: str = ""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class MovementNote:
    """动作笔记模型"""
    id: Optional[int] = None
    user_id: int = 0
    climb_log_id: int = 0
    title: str = ""
    content: str = ""
    movement_type: str = ""
    tags: str = ""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class CrowdDetection:
    """人流检测模型"""
    id: Optional[int] = None
    gym_id: int = 0
    detection_time: Optional[datetime] = None
    people_count: int = 0
    activity_level: str = ""
    image_filename: str = ""
    notes: str = ""
    created_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class MediaFile:
    """媒体文件模型"""
    id: Optional[int] = None
    user_id: int = 0
    climb_log_id: int = 0
    filename: str = ""
    file_type: str = ""
    file_size: int = 0
    upload_date: Optional[datetime] = None
    description: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self) 