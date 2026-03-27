import sys
import os
import json
# 添加项目根目录到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 在这里导入需要测试的组件
from components.restaurant_detector import restaurant_detector

if __name__ == '__main__':
    print("正在执行餐厅列表识别测试...")
    
    # 测试餐厅列表识别
    print("\n--- 测试餐厅列表识别 ---")
    
    # 获取餐厅列表
    restaurants = restaurant_detector.get_restaurants()
    
    print(f"识别到的餐厅列表: {json.dumps(restaurants, ensure_ascii=False, indent=4)}")
    
    print("\n测试完成。")
