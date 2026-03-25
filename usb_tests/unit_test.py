import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts')))
import adb_utils
import vision_utils
import time

# 配置
OUTPUT_DIR = "../crawler/img/captured_data"

def run_full_unit_test():
    print("开始完整单元测试流程...")
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    # 1. 识别并点击“菜品”
    screenshot_path = os.path.join(OUTPUT_DIR, "test_full_1.png")
    adb_utils.screenshot(screenshot_path)
    elements = vision_utils.find_text_elements(screenshot_path, "菜品")
    if elements:
        target = elements[0]
        print(f"点击“菜品”: {target[1]}")
        adb_utils.tap(target[1][0], target[1][1])
        time.sleep(1)
    
    # 2. 识别并点击“查看全部”
    screenshot_path = os.path.join(OUTPUT_DIR, "test_full_2.png")
    adb_utils.screenshot(screenshot_path)
    elements = vision_utils.find_text_elements(screenshot_path, "查看全部")
    if elements:
        target = elements[0]
        print(f"点击“查看全部”: {target[1]}")
        adb_utils.tap(target[1][0], target[1][1])
        time.sleep(1)
        
    # 3. 识别并点击“网友推荐”
    screenshot_path = os.path.join(OUTPUT_DIR, "test_full_3.png")
    adb_utils.screenshot(screenshot_path)
    elements = vision_utils.find_text_elements(screenshot_path, "网友推荐")
    if elements:
        target = elements[0]
        print(f"点击“网友推荐”: {target[1]}")
        adb_utils.tap(target[1][0], target[1][1])
        time.sleep(1)
        
    # 4. 截屏-滑动-截屏
    adb_utils.screenshot(os.path.join(OUTPUT_DIR, "test_full_before_swipe.png"))
    print("执行滑动...")
    adb_utils.swipe(500, 1500, 500, 400, 500)
    time.sleep(1)
    adb_utils.screenshot(os.path.join(OUTPUT_DIR, "test_full_after_swipe.png"))
    
    print("完整测试流程结束。")

if __name__ == "__main__":
    run_full_unit_test()
