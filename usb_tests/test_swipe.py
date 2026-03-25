import adb_utils
import os
import time

# 配置
OUTPUT_DIR = "../crawler/img/captured_data"

def test_swipe():
    print("测试: 截图-滑动-截图...")
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    adb_utils.screenshot(os.path.join(OUTPUT_DIR, "test_before_swipe.png"))
    
    # 调整滑动长度：从屏幕底部(1500)到中部(400)，滑动距离为1100，约为屏幕的三分之二
    print("执行滑动操作...")
    adb_utils.swipe(500, 1500, 500, 400, 500)
    time.sleep(1)
    
    adb_utils.screenshot(os.path.join(OUTPUT_DIR, "test_after_swipe.png"))
    print("截图-滑动-截图测试完成，请检查 captured_data 目录下的两张图片。")

if __name__ == "__main__":
    test_swipe()
