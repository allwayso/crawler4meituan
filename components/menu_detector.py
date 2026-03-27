"""
Spec:
6. 菜单识别组件 (menu_detector.py)
功能：接受两张截图，执行 OCR 识别和 LLM 清洗，返回 JSONL 格式的菜单数据。
输入：两张截图路径。
输出：JSONL 格式的菜单数据。
"""
from typing import List

def detect_menu(restaurant_id: str, screenshot_path1: str, screenshot_path2: str) -> str:
    """
    接受两张截图，执行 OCR 识别和 LLM 清洗。
    将截图、OCR 结果和 LLM 结果存入 data/temp/restaurants/{restaurant_id}/menu_info/。
    
    Args:
        restaurant_id (str): 餐厅 ID。
        screenshot_path1 (str): 第一张截图路径。
        screenshot_path2 (str): 第二张截图路径。
        
    Returns:
        str: JSONL 格式的菜单数据。
    """
    pass
