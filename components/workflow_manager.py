"""
Spec:
7. 工作流管理组件 (workflow_manager.py)
功能：协调各个组件，完成餐厅列表获取、菜单识别及数据整合。
"""

import json
import os
import time
from components.restaurant_detector import restaurant_detector
from components.element_detector import element_detector
from components.menu_detector import menu_detector
from components.back_plugin import back_plugin
from test_restaurant import adb_utils

class WorkflowManager:
    def __init__(self, output_file: str = "D:/crawler/data/restaurants.json") -> None:
        self.output_file = output_file

    def run(self):
        """
        执行完整的工作流。
        """
        print("Workflow started...")
        
        # 1. 调用 restaurant_detector 获取餐厅列表信息。
        # 假设 restaurant_detector.get_restaurants() 返回列表，每个元素包含 is_visited 标记
        restaurants = restaurant_detector.get_restaurants()
        
        while True:
            # 2. 遍历列表
            found_unvisited = False
            for restaurant in restaurants:
                if not restaurant.get('is_visited', False):
                    found_unvisited = True
                    
                    # 保存餐厅信息变量
                    current_restaurant = restaurant
                    
                    # 点击进入详情页
                    # 修正：直接点击 x=50, y=y_min+50
                    y_coord = restaurant.get('y_min', 0) + 50
                    adb_utils.tap(50, y_coord)
                    
                    # 3. 调用 element_detector 找“菜品”
                    try:
                        element_detector.find_element("菜品")
                        # 若找到，点击返回坐标 (这里假设返回坐标是固定的，或者需要动态获取)
                        # 根据需求，点击(50, 150)返回
                        back_plugin.back()
                    except Exception:
                        # 若抛出异常，break
                        break
                    
                    # 4. 调用 element_detector 找“查看更多”
                    try:
                        element_detector.find_element("查看更多")
                        back_plugin.back()
                    except Exception:
                        back_plugin.back()
                        
                    # 5. 调用 element_detector 找“网友推荐”
                    try:
                        element_detector.find_element("网友推荐")
                        back_plugin.back()
                    except Exception:
                        back_plugin.back()
                        back_plugin.back()
                        
                    # 6. 调用 menu_detector 获取菜单
                    menu_data = menu_detector.get_menu()
                    
                    # 7. 整合信息并写入
                    current_restaurant['menu'] = menu_data
                    current_restaurant['is_visited'] = True
                    
                    with open(self.output_file, "a", encoding="utf-8") as f:
                        f.write(json.dumps(current_restaurant, ensure_ascii=False) + "\n")
                    
                    # 8. 执行两次退出，返回步骤 2
                    back_plugin.back()
                    back_plugin.back()
                    
                    # 更新列表状态
                    restaurant['is_visited'] = True
            
            if not found_unvisited:
                # 若没有未访问的，滑动 900
                adb_utils.swipe(500, 1500, 500, 600, 900)
                # 重新获取列表
                restaurants = restaurant_detector.get_restaurants()
            
        print("Workflow finished.")

# 创建全局工作流管理器实例
workflow_manager = WorkflowManager()
