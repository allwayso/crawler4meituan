import sys
import os
import time

# 添加项目根目录到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from components.element_detector import element_detector
from components.back_plugin import back_plugin
from components.workflow_manager import workflow_manager
from test_restaurant import adb_utils


def run_fixed_position_probe(rounds: int = 3):
    """在已进入餐厅详情页的前提下，重复执行固定操作序列。"""
    print("正在执行 fixed position probe...")

    for idx in range(1, rounds + 1):
        print(f"\n===== Round {idx}/{rounds} =====")

        print("[Step] 找 菜品")
        x, y = element_detector.find_element("菜品")
        print(f"[Found] 菜品 at ({x}, {y})")
        adb_utils.tap(x, y)
        time.sleep(1)

        print("[Step] 找 查看全部")
        x, y = element_detector.find_element("查看全部")
        print(f"[Found] 查看全部 at ({x}, {y})")
        adb_utils.tap(x, y)
        time.sleep(1)

        print("[Step] 找 网友推荐")
        x, y = element_detector.find_element("网友推荐")
        print(f"[Found] 网友推荐 at ({x}, {y})")
        adb_utils.tap(x, y)
        time.sleep(1)

        print("[Action] back 1 time")
        back_plugin.back()
        time.sleep(1)
        


if __name__ == '__main__':
    print("正在执行 workflow_manager 调试...")
    workflow_manager.run()
    print("\n测试完成。")
