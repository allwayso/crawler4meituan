import sys
import os
# 添加项目根目录到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 在这里导入需要测试的组件
from components.menu_detector import menu_detector
from test_restaurant.adb_utils import screenshot, swipe

if __name__ == '__main__':
    print("正在执行手机真实操作测试...")
    
    # 测试菜单识别
    print("\n--- 测试菜单识别 ---")
    
    # 截图路径
    screenshot1 = "D:/crawler/data/temp/menu_detection/menu1.png"
    screenshot2 = "D:/crawler/data/temp/menu_detection/menu2.png"
    
    # 确保目录存在
    os.makedirs(os.path.dirname(screenshot1), exist_ok=True)
    
    # 1. 截图第一张
    print("截图第一张...")
    img1 = screenshot(screenshot1)
    
    # 2. 滑动屏幕
    print("滑动屏幕...")
    # 假设屏幕中心坐标，滑动距离 900
    swipe(500, 1500, 500, 600, 500)
    
    # 3. 截图第二张
    print("截图第二张...")
    img2 = screenshot(screenshot2)
    
    # 4. 识别菜单
    print("识别菜单...")
    menu_list = menu_detector.detect_menu(screenshot1, screenshot2)
    print(f"识别到的菜单: {menu_list}")
    
    print("\n测试完成。")
