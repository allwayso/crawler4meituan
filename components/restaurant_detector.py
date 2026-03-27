"""
Spec:
1. 餐厅列表获取组件 (restaurant_detector.py)
功能：截图并识别当前屏幕上的餐厅列表，结合 OCR 与 LLM 进行清洗。
输入：无（内部调用截图与 OCR）。
输出：返回清洗后的餐厅列表（包含名称、坐标等信息）。
"""
from typing import List, Dict, Any

def get_restaurant_list() -> List[Dict[str, Any]]:
    """
    获取并识别当前屏幕上的餐厅列表。
    清洗 Y 值小于 300 的识别结果。
    
    Returns:
        List[Dict[str, Any]]: 清洗后的餐厅列表，包含名称、坐标等信息。
    """
    pass
