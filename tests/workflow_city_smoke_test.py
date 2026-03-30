"""workflow_city_smoke_test.py

目标：仅做 smoke test（不执行ADB真实爬取逻辑）。

思路：
- mock location_navigator、restaurant_detector、menu_detector
- 验证 workflow_manager.run(city=...) 会把 city 写入每条 restaurant 记录
- 验证遍历 city->district->area->采集调用顺序（最基础层级）

说明：该文件用于“单元测试/联调”阶段，当前不自动运行。
"""

import sys
import os
import json
from typing import List, Dict

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from components.workflow_manager import WorkflowManager


class MockRestaurantDetector:
    def get_restaurants(self) -> List[Dict]:
        return [
            {"restaurant_id": "r1", "name": "餐厅1", "address": "A", "rating": 4.2, "y_min": 100, "is_visited": False},
            {"restaurant_id": "r2", "name": "餐厅2", "address": "B", "rating": 4.8, "y_min": 200, "is_visited": False},
        ]


class MockElementDetector:
    def find_element(self, target_text: str):
        # 返回任意坐标
        return (100, 200)


class MockMenuDetector:
    def detect_menu(self, s1, s2):
        return [
            {"dish_name": "菜1", "price": 10.0, "description": ""},
            {"dish_name": "菜2", "price": 20.0, "description": ""},
        ]


class MockLocationNavigator:
    def __init__(self):
        self.calls = []

    def search_by_district_and_area(self, district: str, area: str):
        self.calls.append({"district": district, "area": area})


def main():
    city = "武汉"
    districts = [
        {"district": "洪山区", "areas": ["街道口"]},
    ]

    wm = WorkflowManager(output_file="D:/crawler/data/restaurants_test.json")

    # monkey patch（最简方式：直接替换 workflow_manager.py 的模块级依赖）
    import components.workflow_manager as wm_module

    wm_module.restaurant_detector = MockRestaurantDetector()
    wm_module.element_detector = MockElementDetector()
    wm_module.menu_detector = MockMenuDetector()

    # 替换 location_navigator
    mock_nav = MockLocationNavigator()
    wm_module.location_navigator = mock_nav

    # 替换 adb + back_plugin 的调用为 no-op
    class NoopADB:
        def tap(self, *args, **kwargs):
            pass

        def screenshot(self, *args, **kwargs):
            return None

        def swipe(self, *args, **kwargs):
            pass

    wm_module.adb_utils = NoopADB()

    class NoopBack:
        def back(self):
            pass

    wm_module.back_plugin = NoopBack()

    # 把 districts 直接传入，跳过 LLM
    wm.run(city=city, districts=districts, dry_run=False)

    # 检查调用结果
    print("[workflow_city_smoke_test] nav calls:")
    print(json.dumps(mock_nav.calls, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
