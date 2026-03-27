"""
Spec:
8. 餐厅信息识别组件 (restaurant_info_detector.py)
功能：接受一张截图，执行 OCR 识别和 LLM 清洗，返回 JSONL 格式的餐厅信息。
输入：一张截图路径。
输出：JSONL 格式的餐厅信息（包含餐厅名称和所在位置）。
"""

def detect_restaurant_info(restaurant_id: str, screenshot_path: str) -> str:
    """
    接受一张截图，执行 OCR 识别和 LLM 清洗。
    将截图、OCR 结果和 LLM 结果存入 data/temp/restaurants/{restaurant_id}/restaurant_info/。
    
    Args:
        restaurant_id (str): 餐厅 ID。
        screenshot_path (str): 截图路径。
        
    Returns:
        str: JSONL 格式的餐厅信息。
    """
    pass
