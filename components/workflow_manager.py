"""
Spec:
7. 工作流管理组件 (workflow_manager.py)
功能：协调各个组件，完成餐厅列表获取、菜单识别及数据整合。
"""

import json
import os
from components.restaurant_detector import restaurant_detector
from components.element_detector import element_detector
from components.menu_detector import menu_detector
from test_restaurant import adb_utils

class WorkflowManager:
    def __init__(self, output_file: str = "D:/crawler/data/restaurants_data.jsonl") -> None:
        self.output_file = output_file
        self.visited_restaurants = set()

    def run(self):
        """
        执行完整的工作流。
        """
        print("Workflow started...")
        
        # 1. 调用 restaurant_detector 获取餐厅列表信息。
        restaurants = restaurant_detector.get_restaurants()
        
        # 2. 遍历餐厅列表，对每个餐厅：
        for restaurant in restaurants:
            restaurant_id = restaurant.get('restaurant_id')
            if restaurant_id in self.visited_restaurants:
                continue
            
            print(f"Processing restaurant: {restaurant.get('name')}")
            
            # a. 导航到餐厅详情页 (直接点击餐厅名称坐标)
            # 假设 restaurant 中包含 y_min，我们可以通过点击该坐标进入
            adb_utils.click(500, restaurant.get('y_min', 500))
            
            # b. 调用 menu_detector 获取菜单信息。
            # 假设 menu_detector 需要截图，这里需要根据实际情况调整
            # 暂时假设 menu_detector.get_menu() 会自动截图
            menu_data = menu_detector.get_menu()
            
            # c. 将菜单信息整合到餐厅信息中。
            restaurant['menu'] = menu_data
            
            # d. 将整合后的完整餐厅信息（包含菜单）写入 JSONL 文件。
            with open(self.output_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(restaurant, ensure_ascii=False) + "\n")
            
            self.visited_restaurants.add(restaurant_id)
            
            # 返回列表页
            adb_utils.back()
            
        print("Workflow finished.")

# 创建全局工作流管理器实例
workflow_manager = WorkflowManager()
