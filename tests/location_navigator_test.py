"""location_navigator_test.py

目的：验证 LocationNavigator 的顶部输入框点击坐标、输入与回车是否能触发
对应餐厅列表页面（不做 OCR/菜单采集，只做导航）。

用法：
  python tests/location_navigator_test.py

在真机连接 ADB 且美团首页处于可输入状态时运行。
"""

import sys
import os
import time


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from components.location_navigator import location_navigator
from components.adb_utils import adb_utils


def main():
    # 先做一个很短的探针：确保能点击输入框
    # 你可以按实际页面调整 district/area。
    district = "浦东新区"
    area = "陆家嘴"

    print(f"[location_navigator_test] district={district}, area={area}")
    time.sleep(1)

    # 可选：先轻微返回/等待，避免焦点在别处（不保证）
    # adb_utils.back()
    # time.sleep(1)

    location_navigator.search_by_district_and_area(
        district=district,
        area=area,
        select_first=False,
    )

    print("[location_navigator_test] submit done, waiting for page to load...")
    time.sleep(3)

    # 最后截图，便于你观察是否进入了期望列表页
    adb_utils.screenshot(filename="D:/crawler/data/location_navigator_test.png")
    print("[location_navigator_test] screenshot saved.")


if __name__ == "__main__":
    main()
