"""
Spec:
7. 工作流管理组件 (workflow_manager.py)
功能：协调各个组件，完成餐厅列表获取、菜单识别及数据整合。
"""

import json
import time
from components.restaurant_detector import restaurant_detector
from components.element_detector import element_detector
from components.menu_detector import menu_detector
from components.back_plugin import back_plugin
from test_restaurant import adb_utils

class WorkflowManager:
    def __init__(self, output_file: str = "D:/crawler/data/restaurants.json") -> None:
        self.output_file = output_file
        self.view_all_pos = (943, 476)
        self.recommend_pos = (677, 146)

    def run(self):
        """
        执行完整的工作流。
        """
        print("Workflow started...")
        
        # 1. 调用 restaurant_detector 获取餐厅列表信息。
        # 假设 restaurant_detector.get_restaurants() 返回列表，每个元素包含 is_visited 标记
        restaurants = restaurant_detector.get_restaurants()

        if not restaurants:
            print("Workflow finished early: no restaurants detected.")
            return

        print(f"Loaded {len(restaurants)} restaurants from detector.")

        # 2. 遍历列表（单次执行，不做无限循环）
        found_unvisited = False
        for index, restaurant in enumerate(restaurants, start=1):
            if restaurant.get('is_visited', False):
                print(f"[Skip] Restaurant #{index} already visited: {restaurant.get('name', '<unknown>')}")
                continue

            found_unvisited = True

            # 保存餐厅信息变量
            current_restaurant = restaurant
            restaurant_name = current_restaurant.get('name', '<unknown>')
            restaurant_id = current_restaurant.get('restaurant_id', '<unknown>')
            y_coord = current_restaurant.get('y_min', 0) + 50

            print(f"[Start] Restaurant #{index}: name={restaurant_name}, id={restaurant_id}, y={y_coord}")

            # 点击进入详情页
            print(f"[Action] Tap restaurant entry at (50, {y_coord})")
            adb_utils.tap(50, y_coord)
            time.sleep(2)

            # 3. 调用 element_detector 找“菜品”
            print("[Step] Searching for target element: 菜品")
            try:
                x, y = element_detector.find_element("菜品")
                print(f"[Found] 菜品 at ({x}, {y}), tapping...")
                adb_utils.tap(x, y)
                time.sleep(1)
            except Exception as exc:
                print(f"[Miss] 菜品 not found: {exc}. Backing out one level.")
                back_plugin.back()
                time.sleep(1)
                continue

            # 4. 点击固定位置的“查看全部”
            print(f"[Action] Tap fixed position 查看全部 at {self.view_all_pos}")
            adb_utils.tap(*self.view_all_pos)
            time.sleep(1)

            # 5. 点击固定位置的“网友推荐”
            print(f"[Action] Tap fixed position 网友推荐 at {self.recommend_pos}")
            adb_utils.tap(*self.recommend_pos)
            time.sleep(1)


            # 7. 调用 menu_detector 获取菜单
            print("[Step] Collecting menu data via menu_detector.detect_menu")
            menu_screenshot_1 = adb_utils.screenshot()

            print("[Action] Swipe for second menu screenshot")
            adb_utils.swipe(500, 1500, 500, 600, 900)
            time.sleep(1);
            menu_screenshot_2 = adb_utils.screenshot()

            menu_data = menu_detector.detect_menu(menu_screenshot_1, menu_screenshot_2)
            print(f"[Done] Menu items collected: {len(menu_data) if hasattr(menu_data, '__len__') else 'unknown'}")

            # 8. 整合信息并写入
            current_restaurant['menu'] = menu_data
            current_restaurant['is_visited'] = True

            print(f"[Write] Appending restaurant data to {self.output_file}")
            with open(self.output_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(current_restaurant, ensure_ascii=False) + "\n")

            # 9. 执行两次退出，返回步骤 2
            print("[Action] Backing out to restaurant list (2x)")
            back_plugin.back()
            time.sleep(1)
            back_plugin.back()
            time.sleep(1)

            # 更新列表状态
            restaurant['is_visited'] = True

        if not found_unvisited:
            print("Workflow finished early: no unvisited restaurants in current list.")

        print("Workflow finished.")

# 创建全局工作流管理器实例
workflow_manager = WorkflowManager()
