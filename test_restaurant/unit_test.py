import sys
import os
import time
import json
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import adb_utils
import test_ocr_llm

# 配置
OUTPUT_DIR = "../crawler/test_test"
BACK_BUTTON_X = 50
BACK_BUTTON_Y = 150
VISITED_RESTAURANTS = {} # {name: bool}

def run_cycle():
    print("执行单次循环...")
    
    # 1. 调用 test_ocr_llm 获取清洗后的餐厅列表
    # 重新运行 OCR 和 LLM 清洗
    print("正在获取餐厅列表...")
    # 模拟调用 test_ocr_llm 的逻辑
    # 实际中可以直接调用 test_ocr_llm 中的函数
    # 这里为了保持逻辑，我们直接运行一次清洗流程
    
    # 截图
    screenshot_path = os.path.join(OUTPUT_DIR, "list.png")
    adb_utils.screenshot(screenshot_path)
    
    # OCR 识别
    import vision_utils
    restaurants = vision_utils.get_restaurant_list(screenshot_path)
    
    # LLM 清洗
    cleaned_restaurants = test_ocr_llm.clean_restaurant_names_with_llm(restaurants)
    
    # 2. 寻找第一个未访问的餐厅
    target_restaurant = None
    for r in cleaned_restaurants:
        name = r['name']
        y_min = r['y_min']
        # 假设 x 坐标为屏幕中心
        x = 540 
        if name not in VISITED_RESTAURANTS or not VISITED_RESTAURANTS[name]:
            target_restaurant = (name, x, y_min)
            break
            
    if not target_restaurant:
        print("未找到新餐厅")
        return

    # 3. 点击餐厅 (点击标题下方 50 处)
    print(f"点击餐厅: {target_restaurant[0]}, y_min: {target_restaurant[2]}")
    adb_utils.tap(target_restaurant[1], target_restaurant[2] + 50)
    VISITED_RESTAURANTS[target_restaurant[0]] = True
    time.sleep(2)
    
    # 4. 返回列表页
    print("返回列表页")
    adb_utils.tap(BACK_BUTTON_X, BACK_BUTTON_Y)
    time.sleep(1)

if __name__ == "__main__":
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    print("开始测试流程 (两次循环)...")
    run_cycle()
    run_cycle()
    print("测试流程结束。")
