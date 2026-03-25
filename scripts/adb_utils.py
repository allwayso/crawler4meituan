import subprocess
import time
import os

def run_adb(command):
    """执行 ADB 命令并返回结果"""
    adb_path = r"D:\platform-tools\adb.exe"
    full_command = [adb_path] + command
    result = subprocess.run(full_command, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"ADB Error: {result.stderr}")
    return result.stdout

def tap(x, y):
    """点击指定坐标"""
    run_adb(["shell", "input", "tap", str(x), str(y)])

def swipe(x1, y1, x2, y2, duration=500):
    """滑动屏幕"""
    run_adb(["shell", "input", "swipe", str(x1), str(y1), str(x2), str(y2), str(duration)])

def screenshot(filename):
    """截图并保存到本地"""
    temp_path = "/sdcard/temp_screenshot.png"
    run_adb(["shell", "screencap", "-p", temp_path])
    run_adb(["pull", temp_path, filename])
    print(f"Screenshot saved to {filename}")

def back():
    """模拟返回键"""
    run_adb(["shell", "input", "keyevent", "4"])
