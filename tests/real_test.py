import sys
import os
# 添加项目根目录到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 在这里导入需要测试的组件
from components.restaurant_detector import restaurant_detector
from components.element_detector import element_detector, ElementNotFoundException

if __name__ == '__main__':
    print("正在执行手机真实操作测试...")
    
    # 1. 测试餐厅列表获取
    print("--- 测试餐厅列表获取 ---")
    restaurants = restaurant_detector.get_restaurants()
    print(f"获取到的餐厅列表: {restaurants}")
    
    # 2. 测试元素识别
    print("\n--- 测试元素识别 ---")
    target = "菜品"
    try:
        coord = element_detector.find_element(target)
        print(f"找到元素 '{target}'，坐标: {coord}")
    except ElementNotFoundException as e:
        print(e)
    
    print("\n测试完成。")
