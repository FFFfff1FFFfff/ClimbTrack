#!/usr/bin/env python3
"""
测试新的路线等级系统
验证数据库迁移和服务功能
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.services import RouteService
from database.dao import route_dao

def test_route_grades():
    """测试路线等级系统"""
    
    print("🧪 测试新的路线等级系统")
    print("=" * 50)
    
    # 1. 测试获取所有路线
    print("\n1️⃣ 获取所有路线...")
    all_routes = RouteService.get_all_routes()
    print(f"✅ 找到 {len(all_routes)} 条路线")
    
    # 2. 按类别分组显示
    bouldering_routes = [r for r in all_routes if r['category'] == 'Bouldering']
    sport_routes = [r for r in all_routes if r['category'] == 'Sport Climbing']
    
    print(f"\n📊 路线分布:")
    print(f"   🧗 Bouldering: {len(bouldering_routes)} 条")
    print(f"   🏔️  Sport Climbing: {len(sport_routes)} 条")
    
    # 3. 显示等级分布
    print(f"\n🎯 Bouldering等级分布:")
    v_grades = {}
    for route in bouldering_routes:
        grade = route['overall_difficulty']
        v_grades[grade] = v_grades.get(grade, 0) + 1
    
    for grade in sorted(v_grades.keys(), key=lambda x: int(x[1:]) if x.startswith('V') else 0):
        print(f"   {grade}: {v_grades[grade]} 条")
    
    print(f"\n🎯 Sport Climbing等级分布:")
    sport_grades = {}
    for route in sport_routes:
        grade = route['overall_difficulty']
        sport_grades[grade] = sport_grades.get(grade, 0) + 1
    
    for grade in sorted(sport_grades.keys()):
        print(f"   {grade}: {sport_grades[grade]} 条")
    
    # 4. 测试难度范围查询
    print(f"\n4️⃣ 测试难度范围查询...")
    
    # 测试V等级查询
    v5_to_v7 = RouteService.get_routes_by_difficulty("V5", "V7", "Bouldering")
    print(f"✅ V5-V7 Bouldering路线: {len(v5_to_v7)} 条")
    for route in v5_to_v7[:3]:  # 显示前3条
        print(f"   - {route['name']}: {route['overall_difficulty']}")
    
    # 测试法式等级查询
    sport_7a_7c = RouteService.get_routes_by_difficulty("7a", "7c", "Sport Climbing")
    print(f"✅ 7a-7c Sport Climbing路线: {len(sport_7a_7c)} 条")
    for route in sport_7a_7c[:3]:  # 显示前3条
        print(f"   - {route['name']}: {route['overall_difficulty']}")
    
    # 5. 测试搜索功能
    print(f"\n5️⃣ 测试搜索功能...")
    search_results = RouteService.search_routes_by_name("Challenge")
    print(f"✅ 包含'Challenge'的路线: {len(search_results)} 条")
    for route in search_results:
        print(f"   - {route['name']}: {route['category']} {route['overall_difficulty']}")
    
    # 6. 验证数据完整性
    print(f"\n6️⃣ 验证数据完整性...")
    invalid_grades = []
    for route in all_routes:
        grade = route['overall_difficulty']
        category = route['category']
        
        if category == 'Bouldering':
            if not (grade.startswith('V') and grade[1:].isdigit()):
                invalid_grades.append((route['name'], grade))
        elif category == 'Sport Climbing':
            if not (grade[0].isdigit() and len(grade) >= 2):
                invalid_grades.append((route['name'], grade))
    
    if invalid_grades:
        print(f"❌ 发现 {len(invalid_grades)} 个无效等级:")
        for name, grade in invalid_grades:
            print(f"   - {name}: {grade}")
    else:
        print("✅ 所有等级格式都正确")
    
    print(f"\n🎉 测试完成！")
    return len(invalid_grades) == 0

if __name__ == "__main__":
    success = test_route_grades()
    if success:
        print("✅ 所有测试通过！")
        sys.exit(0)
    else:
        print("❌ 测试失败！")
        sys.exit(1) 