"""workflow_manager.py

Spec:
7. 工作流管理组件 (workflow_manager.py)
功能：协调各个组件，完成餐厅列表获取、菜单识别及数据整合。

增强：支持按 city -> district(区/县) -> area(商圈) 参数化爬取，并把 city 写入 restaurants.json。
"""

import json
import time
from concurrent.futures import ThreadPoolExecutor, Future
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

        # 菜单识别耗时较长（OCR + LLM），可与 UI 操作并行。
        # 先用单线程执行 OCR/LLM，避免 PaddleOCR / LLM 客户端的潜在线程安全问题。
        self.menu_executor_workers = 1
        # 同时最多挂起多少个“等待 OCR+LLM 的菜单任务”（避免占用过多截图内存）
        self.menu_pending_limit = 2

    def _write_restaurant_with_menu(self, restaurant_snapshot: Dict, menu_data: List[Dict]) -> None:
        """只由主线程写文件，避免并发写导致数据竞争。"""
        restaurant_snapshot["menu"] = menu_data
        restaurant_snapshot["is_visited"] = True
        with open(self.output_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(restaurant_snapshot, ensure_ascii=False) + "\n")

    def _drain_completed_futures(
        self,
        pending: List[tuple[Future, Dict]],
        *,
        wait_for_one: bool = False,
    ) -> None:
        """收割已完成的菜单识别任务，把结果写入文件。

        pending: [(future, restaurant_snapshot), ...]
        """
        if not pending:
            return

        i = 0
        while i < len(pending):
            fut, snapshot = pending[i]
            if fut.done():
                try:
                    menu_data = fut.result()
                except Exception as e:
                    logger.warning(f"Menu detection failed, restaurant_id={snapshot.get('restaurant_id')}: {e}")
                    menu_data = []
                self._write_restaurant_with_menu(snapshot, menu_data)
                pending.pop(i)
            else:
                i += 1

        if wait_for_one and pending:
            # 等待至少一个完成
            for fut, _ in pending:
                if not fut.done():
                    fut.result()
                    break

            # 再清理一次
            i = 0
            while i < len(pending):
                fut, snapshot = pending[i]
                if fut.done():
                    try:
                        menu_data = fut.result()
                    except Exception as e:
                        logger.warning(f"Menu detection failed, restaurant_id={snapshot.get('restaurant_id')}: {e}")
                        menu_data = []
                    self._write_restaurant_with_menu(snapshot, menu_data)
                    pending.pop(i)
                else:
                    i += 1

    def _collect_for_current_restaurant_list(
        self,
        city: Optional[str] = None,
        *,
        menu_executor: ThreadPoolExecutor,
        pending: List[tuple[Future, Dict]],
    ):
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

            # 为异步 menu detection 做快照：主线程继续 UI 时，避免 snapshot 被后续覆盖。
            restaurant_snapshot = dict(current_restaurant)

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
                # 查看全部：直接点击固定点（避免 OCR 找不到导致流程抖动）
                adb_utils.tap(*self.view_all_pos)
                time.sleep(0.5)

                # 网友推荐：直接点击固定点（避免 OCR 找不到导致流程抖动）
                adb_utils.tap(*self.recommend_pos)
                time.sleep(0.5)

            # 菜单识别（正餐 & 非正餐：共同逻辑）
            logger.debug("[Step] Collecting menu data via menu_detector.detect_menu")
            menu_screenshot_1 = adb_utils.screenshot()
            logger.debug("[Action] Swipe for second menu screenshot")
            adb_utils.swipe(500, 1500, 500, 600, 900)
            time.sleep(1)
            menu_screenshot_2 = adb_utils.screenshot()

            # 写入
            # 改为异步：这里不等待 OCR/LLM 完成，直接把 future 丢进 pending。
            logger.debug(f"[Async] Submit menu detection for restaurant_id={restaurant_snapshot.get('restaurant_id')}")
            future = menu_executor.submit(menu_detector.detect_menu, menu_screenshot_1, menu_screenshot_2)
            pending.append((future, restaurant_snapshot))

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

            # 控制 pending 队列长度：达到阈值则先收割一个完成的
            if len(pending) >= self.menu_pending_limit:
                self._drain_completed_futures(pending, wait_for_one=True)

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

        pending: List[tuple[Future, Dict]] = []
        with ThreadPoolExecutor(max_workers=self.menu_executor_workers) as menu_executor:
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

                    # 在当前“区/商圈”列表页采集（菜单识别异步）
                    self._collect_for_current_restaurant_list(
                        city=city,
                        menu_executor=menu_executor,
                        pending=pending,
                    )

            # 收尾：确保所有 menu detection 都完成并写入
            self._drain_completed_futures(pending, wait_for_one=False)
            while pending:
                self._drain_completed_futures(pending, wait_for_one=True)

            logger.info("Workflow finished.")

# 创建全局工作流管理器实例
workflow_manager = WorkflowManager()
