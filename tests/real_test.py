import sys
import os
# 添加项目根目录到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 在这里导入需要测试的组件
from components.restaurant_detector import restaurant_detector

if __name__ == '__main__':
    print("正在执行手机真实操作测试...")
    
    # 在这里编写具体的测试逻辑
    restaurants = restaurant_detector.get_restaurants()
    print(f"获取到的餐厅列表: {restaurants}")
    
    print("测试完成。")
