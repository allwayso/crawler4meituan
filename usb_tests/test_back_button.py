import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts')))
import adb_utils
import time

# 配置
# 根据您的手机屏幕，左上角返回按钮通常在 (100, 100) 左右
# 请根据实际情况调整坐标
BACK_BUTTON_X = 50
BACK_BUTTON_Y =150

def test_back_button():
    print(f"测试: 点击左上角返回按钮 (坐标: {BACK_BUTTON_X}, {BACK_BUTTON_Y})...")
    
    print("执行点击...")
    adb_utils.tap(BACK_BUTTON_X, BACK_BUTTON_Y)
    time.sleep(1)
    print("点击完成。")

if __name__ == "__main__":
    test_back_button()
