"""workflow_manager.py

Spec:
7. 工作流管理组件 (workflow_manager.py)
功能：协调各个组件，完成餐厅列表获取、菜单识别及数据整合。

增强：支持按 city -> district(区/县) -> area(商圈) 参数化爬取，并把 city 写入 restaurants.json。
"""

import json
import time
from components.restaurant_detector import restaurant_detector
from components.element_detector import element_detector
from components.menu_detector import menu_detector
from components.back_plugin import back_plugin
from components.adb_utils import adb_utils
from components.city_searcher import city_district_area_searcher

from typing import List, Dict, Optional
from components.location_navigator import location_navigator
from components.logging_utils import get_logger


logger = get_logger(__name__)

class WorkflowManager:
    def __init__(self, output_file: str = "D:/crawler/data/restaurants.json") -> None:
        self.output_file = output_file
        self.view_all_pos = (943, 476)
        self.recommend_pos = (677, 146)
        self.top_district = 5
        self.top_area_per_district = 5

    def _collect_for_current_restaurant_list(self, city: Optional[str] = None):
        """从当前餐厅列表页开始，采集每家餐厅菜单并追加写入 restaurants.json。"""
        restaurants = restaurant_detector.get_restaurants()

        if not restaurants:
            logger.warning("No restaurants detected on current page.")
            return

        logger.debug(f"Loaded {len(restaurants)} restaurants from detector.")

        found_unvisited = False
        for index, restaurant in enumerate(restaurants, start=1):
            if restaurant.get('is_visited', False):
                logger.debug(
                    f"[Skip] Restaurant #{index} already visited: {restaurant.get('name', '<unknown>')}"
                )
                continue

            found_unvisited = True

            current_restaurant = restaurant
            # 与 DATA_FORMAT.md 对齐：restaurants.json 中增加 city 字段
            current_restaurant['city'] = city or ''

            restaurant_name = current_restaurant.get('name', '<unknown>')
            restaurant_id = current_restaurant.get('restaurant_id', '<unknown>')
            y_coord = current_restaurant.get('y_min', 0) + 50

            # is_main_dish 由 restaurant_detector.llm_clean 严格保证为 true/false
            is_main_dish = current_restaurant.get('is_main_dish')
            if not isinstance(is_main_dish, bool):
                logger.warning(
                    f"[RestaurantType] invalid is_main_dish={is_main_dish!r}, skipping restaurant: {restaurant_name}"
                )
                continue

            logger.debug(
                f"[Start] Restaurant #{index}: name={restaurant_name}, id={restaurant_id}, y={y_coord}"
            )

            # 点击进入详情页
            logger.debug(f"[Action] Tap restaurant entry at (50, {y_coord})")
            adb_utils.tap(50, y_coord)
            time.sleep(2.5)

            # 找“菜品”
            logger.debug("[Step] Searching for target element: 菜品")
            try:
                x, y = element_detector.find_element("菜品")
                logger.debug(f"[Found] 菜品 at ({x}, {y}), tapping...")
                adb_utils.tap(x, y)
                time.sleep(1)
            except Exception as exc:
                logger.warning(f"[Miss] 菜品 not found: {exc}. Backing out one level.")
                back_plugin.back()
                time.sleep(1)
                continue

            logger.debug(f"[RestaurantType] is_main_dish={is_main_dish}")

            if is_main_dish:
                # 查看全部（优先 OCR 定位，找不到则 fallback 固定坐标）
                try:
                    x, y = element_detector.find_element("查看全部")
                    logger.debug(f"[Found] 查看全部 at ({x}, {y}), tapping...")
                    adb_utils.tap(x, y)
                    time.sleep(1)
                except Exception:
                    logger.debug(
                        f"[Fallback] Tap fixed position 查看全部 at {self.view_all_pos}"
                    )
                    adb_utils.tap(*self.view_all_pos)
                    time.sleep(1)

                # 网友推荐（优先 OCR 定位，找不到则 fallback 固定坐标）
                try:
                    x, y = element_detector.find_element("网友推荐")
                    logger.debug(f"[Found] 网友推荐 at ({x}, {y}), tapping...")
                    adb_utils.tap(x, y)
                    time.sleep(1)
                except Exception:
                    logger.debug(
                        f"[Fallback] Tap fixed position 网友推荐 at {self.recommend_pos}"
                    )
                    adb_utils.tap(*self.recommend_pos)
                    time.sleep(1)

            # 菜单识别（正餐 & 非正餐：共同逻辑）
            logger.debug("[Step] Collecting menu data via menu_detector.detect_menu")
            menu_screenshot_1 = adb_utils.screenshot()
            logger.debug("[Action] Swipe for second menu screenshot")
            adb_utils.swipe(500, 1500, 500, 600, 900)
            time.sleep(1)
            menu_screenshot_2 = adb_utils.screenshot()

            menu_data = menu_detector.detect_menu(menu_screenshot_1, menu_screenshot_2)
            logger.debug(
                f"[Done] Menu items collected: {len(menu_data) if hasattr(menu_data, '__len__') else 'unknown'}"
            )

            # 写入
            current_restaurant['menu'] = menu_data
            current_restaurant['is_visited'] = True

            logger.debug(f"[Write] Appending restaurant data to {self.output_file}")
            with open(self.output_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(current_restaurant, ensure_ascii=False) + "\n")

            # 返回逻辑：
            # - 正餐：原逻辑两次返回
            # - 非正餐：只需要返回一次（回到餐厅列表页）
            if is_main_dish:
                logger.debug("[Action] Backing out to restaurant list (2x)")
                back_plugin.back()
                time.sleep(1)
                back_plugin.back()
                time.sleep(1)
            else:
                logger.debug("[Action] Backing out to restaurant list (1x for non-main-dish)")
                back_plugin.back()
                time.sleep(1)

            restaurant['is_visited'] = True

        if not found_unvisited:
            logger.info("No unvisited restaurants in current list.")

    def run(
        self,
        city: str,
        districts: Optional[List[Dict]] = None,
        top_district: Optional[int] = None,
        top_area_per_district: Optional[int] = None,
        dry_run: bool = False,
    ):
        """执行工作流。

        参数 city 为必填：会先生成/读取 districts(district->areas)，然后逐个区县/商圈切换到餐厅列表页采集。
        """

        logger.info("Workflow started...")

        if top_district is None:
            top_district = self.top_district
        if top_area_per_district is None:
            top_area_per_district = self.top_area_per_district

        if districts is None:
            districts = city_district_area_searcher.search(
                city=city,
                top_district=top_district,
                top_area_per_district=top_area_per_district,
            )

        logger.info(f"Plan: city={city}, districts={len(districts)}")
        if dry_run:
            logger.info("Dry run enabled, skip adb operations.")
            return districts

        # 逐个 district -> area 切换
        for d in districts:
            district = d.get('district')
            areas = d.get('areas', []) or []
            if not district:
                continue

            for area in areas:
                if not area:
                    continue

                # 导航日志默认不刷屏
                logger.info(f"[Navigate] city={city}, district={district}, area={area}")
                # LocationNavigator 当前对外接口为 search(district, area)
                location_navigator.search(
                    district=str(district),
                    area=str(area),
                )
                time.sleep(2)

                # 在当前“区/商圈”列表页采集
                self._collect_for_current_restaurant_list(city=city)

        logger.info("Workflow finished.")

# 创建全局工作流管理器实例
workflow_manager = WorkflowManager()
