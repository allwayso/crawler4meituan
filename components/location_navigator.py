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
    # 你已测试得到的关键坐标（美团首页“美食”顶部搜索栏）
    CITY_SEARCH_BAR_POS = (500, 150)  # 输入框
    SEARCH_BUTTON_POS = (960, 150)   # 搜索按钮
    CLEAR_BUTTON_POS = (840, 150)    # 输入框右侧“清除/叉号”按钮

    # 若按回车后需要额外点“第一个候选项/结果”，这里预留坐标（可选）
    FIRST_SUGGESTION_POS = (250, 300)  # 占位值

    def _tap_search_bar(self):
        adb_utils.tap(*self.CITY_SEARCH_BAR_POS)
        time.sleep(2)

    def _input_and_submit(self, text: str, select_first: bool = False):
        # 清空输入框：优先点击右侧叉按钮（比长按 Delete 更稳定）
        adb_utils.tap(*self.CLEAR_BUTTON_POS)
        time.sleep(2)

        # 点击叉号后有概率焦点丢失，需要再点一次输入框确保可输入
        adb_utils.tap(*self.CITY_SEARCH_BAR_POS)
        time.sleep(2)

        adb_utils.input_text(text)
        time.sleep(2)

        # 点击搜索按钮
        adb_utils.tap(*self.SEARCH_BUTTON_POS)

        # 等待页面跳转/结果渲染
        time.sleep(2.0)

        if select_first:
            adb_utils.tap(*self.FIRST_SUGGESTION_POS)
            time.sleep(1.2)

    def search(
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
