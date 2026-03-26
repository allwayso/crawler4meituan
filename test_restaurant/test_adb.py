import adb_utils
import time

def test_connection():
    print("正在测试 ADB 连接与控制...")
    
    # 1. 测试截图
    test_screenshot = "../crawler/img/test_connection.png"
    adb_utils.screenshot(test_screenshot)
    print(f"截图已保存至: {test_screenshot}，请检查是否为当前手机屏幕。")
    
    # 2. 测试滑动
    print("正在执行测试滑动...")
    adb_utils.swipe(500, 1500, 500, 500, 500)
    print("滑动测试完成。")
    
    # 3. 测试返回
    print("正在执行测试返回...")
    adb_utils.back()
    print("返回测试完成。")
    
    print("测试结束。如果以上操作均成功，说明 ADB 控制正常。")

if __name__ == "__main__":
    test_connection()
