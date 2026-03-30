import subprocess
import io
import sys
from PIL import Image


def run_adb(command):
    """执行 ADB 命令并返回结果(stdout)。"""
    adb_path = r"D:\platform-tools\adb.exe"
    full_command = [adb_path] + command
    result = subprocess.run(full_command, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"ADB Error: {result.stderr}")
    return result.stdout


def tap(x, y):
    """点击指定坐标"""
    print(f"Executing tap at {x}, {y}")
    run_adb(["shell", "input", "tap", str(x), str(y)])


def swipe(x1, y1, x2, y2, duration=500):
    """滑动屏幕"""
    print(f"Executing swipe from ({x1}, {y1}) to ({x2}, {y2})")
    run_adb(["shell", "input", "swipe", str(x1), str(y1), str(x2), str(y2), str(duration)])


def input_text(text: str):
    """向当前获得焦点的输入框注入文本。

    说明：前提是光标已在输入框中（tap 到输入框）。
    """
    # ADB input text 使用空格需要转义为 %s（这里用最常见的处理：空格转为 %s）
    safe = text.replace(" ", "%s")
    print(f"Executing input_text: {text}")
    run_adb(["shell", "input", "text", safe])


def press_keyevent(keyevent: int):
    """执行 Android keyevent，例如 66(Enter)、67(Del) 等。"""
    print(f"Executing keyevent: {keyevent}")
    run_adb(["shell", "input", "keyevent", str(keyevent)])


def press_enter():
    """按 Enter."""
    press_keyevent(66)


def press_delete(times: int = 1):
    """按 Delete 指定次数（常用于清空输入框）。"""
    for _ in range(max(0, times)):
        press_keyevent(67)


def screenshot(filename=None):
    """截图并返回 PIL Image 对象。

    若提供 filename，则同时保存到本地。
    """
    adb_path = r"D:\platform-tools\adb.exe"
    # 使用 shell screencap -p 直接输出二进制数据
    result = subprocess.run([adb_path, "shell", "screencap", "-p"], capture_output=True)

    # 处理 screencap 的换行符问题 (Windows 下 \r\n)
    raw_data = result.stdout.replace(b'\r\n', b'\n')

    image = Image.open(io.BytesIO(raw_data))

    if filename:
        image.save(filename)
        print(f"Screenshot saved to {filename}")

    return image


def back():
    """模拟返回键"""
    run_adb(["shell", "input", "keyevent", "4"])


# 兼容旧写法：其它模块可能使用 `from components.adb_utils import adb_utils`
# 然后调用 `adb_utils.tap / adb_utils.screenshot / adb_utils.back`。
adb_utils = sys.modules[__name__]
