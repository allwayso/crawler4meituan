import sys
import os
# 添加项目根目录到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 在这里导入需要测试的组件
from components.element_detector import element_detector, ElementNotFoundException
from test_restaurant.adb_utils import tap

if __name__ == '__main__':
    print("正在执行手机真实操作测试...")
    
    # 测试元素识别并点击
    print("\n--- 测试元素识别与点击 ---")
    target = "菜品"
    try:
        coord = element_detector.find_element(target)
        print(f"找到元素 '{target}'，坐标: {coord}")
        print(f"执行点击: {coord}")
        tap(coord[0], coord[1])
    except ElementNotFoundException as e:
        print(e)
    
    print("\n测试完成。")
