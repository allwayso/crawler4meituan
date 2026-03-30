"""location_navigator.py

用于在美团首页“顶部搜索栏”中输入（区/县 + 商圈名），从而跳转到对应的餐厅列表页。

注意：
- 当前实现使用“点击坐标 + ADB 注入文本”。坐标需要你在真机上通过探针方式确认后固化。
- 本组件目标是让 workflow_manager 能进入“餐厅列表页”，从而复用现有 restaurant_detector 流程。
"""

import time
from typing import Optional

from components.adb_utils import adb_utils


class LocationNavigator:
    # TODO: 这几个坐标需要你在真机上探针确认后改成正确值
    # 建议探针：在美团首页处于“美食”界面，先执行 adb tap 逐个调整直到输入框获得焦点。
    CITY_SEARCH_BAR_POS = (500, 150)  # 顶部输入框（按你经验值修正）

    # 若按回车后需要额外点“第一个候选项/结果”，这里预留坐标（可选）
    FIRST_SUGGESTION_POS = (250, 300)  # 占位值

    def _tap_search_bar(self):
        adb_utils.tap(*self.CITY_SEARCH_BAR_POS)
        time.sleep(0.8)

    def _input_and_submit(self, text: str, select_first: bool = False):
        # 清空输入（假设已有内容）
        # 如果你的页面不会自动保留上次输入，可把 press_delete 注释掉
        adb_utils.press_delete(times=30)

        adb_utils.input_text(text)
        time.sleep(0.5)
        adb_utils.press_enter()

        # 等待页面跳转/结果渲染
        time.sleep(2.0)

        if select_first:
            adb_utils.tap(*self.FIRST_SUGGESTION_POS)
            time.sleep(1.2)

    def search_by_district_and_area(
        self,
        district: str,
        area: str,
        select_first: bool = False,
    ):
        """在首页搜索栏输入："{district} {area}" 并提交。"""
        query = f"{district} {area}".strip()
        if not query:
            raise ValueError("district/area 不能为空")

        self._tap_search_bar()
        self._input_and_submit(query, select_first=select_first)


location_navigator = LocationNavigator()
