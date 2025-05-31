#!/usr/bin/env python3
"""
更新用户统计数据脚本
定期运行此脚本以确保用户统计数据的准确性
"""

import os
import sys

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.services import StatisticsService
from database.dao import user_dao, user_profile_dao, user_statistics_dao

def check_database_integrity():
    """检查数据库完整性"""
    print("🔍 检查数据库完整性...")
    
    # 检查用户是否都有对应的profile和statistics
    users = user_dao.get_all()
    
    users_without_profile = []
    users_without_stats = []
    
    for user in users:
        profile = user_profile_dao.get_by_user_id(user['id'])
        stats = user_statistics_dao.get_by_user_id(user['id'])
        
        if not profile:
            users_without_profile.append(user)
        
        if not stats:
            users_without_stats.append(user)
    
    if users_without_profile:
        print(f"⚠️  发现 {len(users_without_profile)} 个用户缺少资料记录")
        from database.models import UserProfile
        for user in users_without_profile:
            profile = UserProfile(
                user_id=user['id'],
                display_name=user['username']
            )
            user_profile_dao.create(profile)
        print("✅ 已补充缺少的用户资料")
    
    if users_without_stats:
        print(f"⚠️  发现 {len(users_without_stats)} 个用户缺少统计记录")
        from database.models import UserStatistics
        for user in users_without_stats:
            stats = UserStatistics(user_id=user['id'])
            user_statistics_dao.create(stats)
        print("✅ 已补充缺少的统计记录")
    
    print("✅ 数据库完整性检查完成")

if __name__ == '__main__':
    print("🚀 开始更新数据库统计信息...")
    
    try:
        # 检查数据库完整性
        check_database_integrity()
        
        # 更新所有用户统计数据
        print("\n📊 更新用户统计数据...")
        StatisticsService.update_all_user_statistics()
        
        print("\n🎉 数据库统计信息更新完成！")
        
    except Exception as e:
        print(f"❌ 更新过程中出现错误: {e}")
        print("�� 请确保数据库文件存在且可访问") 