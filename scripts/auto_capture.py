import subprocess
import time

def auto_scroll_and_capture(output_dir, scroll_count=10):
    """
    使用 ADB 实现自动滚动截图。
    """
    for i in range(scroll_count):
        # 截图
        filename = f"{output_dir}/screenshot_{i}.png"
        subprocess.run(["adb", "shell", "screencap", "-p", f"/sdcard/screenshot_{i}.png"])
        subprocess.run(["adb", "pull", f"/sdcard/screenshot_{i}.png", filename])
        
        # 滚动 (模拟从屏幕底部向上滑动)
        subprocess.run(["adb", "shell", "input", "swipe", "500", "1500", "500", "500", "500"])
        
        # 等待页面加载
        time.sleep(2)
        print(f"Captured {filename}")

# 示例调用
# auto_scroll_and_capture("../crawler/img/test_screenshots")
print("ADB 自动截图脚本已就绪。")
