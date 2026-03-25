import adb_utils
import vision_utils
import os
import time

# 配置
OUTPUT_DIR = "../crawler/img/captured_data"

def test_recommend_click():
    print("测试: 识别并点击“网友推荐”文字...")
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    screenshot_path = os.path.join(OUTPUT_DIR, "test_recommend_click.png")
    adb_utils.screenshot(screenshot_path)
    
    elements = vision_utils.find_text_elements(screenshot_path, "网友推荐")
    if elements:
        # 选择最上方的一个
        target = elements[0]
        print(f"识别到“网友推荐”文字: {target[0]}, 位置: {target[1]}")
        print("执行点击...")
        adb_utils.tap(target[1][0], target[1][1])
        time.sleep(1)
        print("点击完成。")
    else:
        print("未识别到“网友推荐”文字。")

if __name__ == "__main__":
    test_recommend_click()
