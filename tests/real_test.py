import sys
import os
import time

# 添加项目根目录到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from components.adb_utils import adb_utils
from components.location_navigator import LocationNavigator


if __name__ == '__main__':
    print("正在执行 location_navigator 调试...")

    nav = LocationNavigator()

    district = "浦东新区"
    area = "陆家嘴"

    # 直接走 location navigator：输入“district + area”并提交
    # select_first：如果候选列表需要二次点击“第一个候选项”，把它设为 True
    nav.search(
        district=district,
        area=area,
        select_first=False,
    )

    print("\n测试完成。")
