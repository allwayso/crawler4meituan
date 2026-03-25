import time
import os
import adb_utils
import vision_utils

# 配置
TEMPLATE_DIR = "../crawler/img/templates"
OUTPUT_DIR = "../crawler/img/captured_data"
MENU_TAB_TEMPLATE = os.path.join(TEMPLATE_DIR, "menu_tab.png")
VIEW_ALL_TEMPLATE = os.path.join(TEMPLATE_DIR, "view_all.png")

def capture_restaurant_menu(restaurant_name):
    """
    采集单个店家的菜单 (MVP版)
    """
    print(f"开始采集店家: {restaurant_name}")
    
    # 1. 截图并识别菜品栏
    screenshot_path = os.path.join(OUTPUT_DIR, f"{restaurant_name}_temp.png")
    adb_utils.screenshot(screenshot_path)
    
    menu_tab_pos = vision_utils.find_element(screenshot_path, MENU_TAB_TEMPLATE)
    if menu_tab_pos:
        adb_utils.tap(menu_tab_pos[0], menu_tab_pos[1])
        time.sleep(1)
        
        # 2. 识别并点击“查看全部”
        adb_utils.screenshot(screenshot_path)
        view_all_pos = vision_utils.find_element(screenshot_path, VIEW_ALL_TEMPLATE)
        if view_all_pos:
            adb_utils.tap(view_all_pos[0], view_all_pos[1])
            time.sleep(2)
            
            # 3. 循环截图
            for i in range(5):
                page_screenshot = os.path.join(OUTPUT_DIR, f"{restaurant_name}_menu_{i}.png")
                adb_utils.screenshot(page_screenshot)
                adb_utils.swipe(500, 1500, 500, 500, 500)
                time.sleep(1)
        
        # 4. 返回
        adb_utils.back()
        time.sleep(1)
        adb_utils.back()
        time.sleep(1)
    else:
        print("未找到菜品栏，跳过。")

if __name__ == "__main__":
    print("请确保手机已打开美团店家界面，并准备好模板图片。")
    capture_restaurant_menu("test_restaurant")
