import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts')))
import adb_utils
import vision_utils
import time

# 配置
OUTPUT_DIR = "../crawler/img/captured_data"

def test_view_all_click():
    print("测试: 识别并点击“查看全部”文字...")
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    screenshot_path = os.path.join(OUTPUT_DIR, "test_view_all_click.png")
    adb_utils.screenshot(screenshot_path)
    
    elements = vision_utils.find_text_elements(screenshot_path, "查看全部")
    if elements:
        # 选择最上方的一个
        target = elements[0]
        print(f"识别到“查看全部”文字: {target[0]}, 位置: {target[1]}")
        print("执行点击...")
        adb_utils.tap(target[1][0], target[1][1])
        time.sleep(1)
        print("点击完成。")
    else:
        print("未识别到“查看全部”文字。")

if __name__ == "__main__":
    test_view_all_click()
