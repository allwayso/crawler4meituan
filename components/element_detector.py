"""
Spec:
3. 元素识别组件 (element_detector.py)
功能：在当前页面识别目标文字（如“菜品”、“查看全部”等）。
输入：目标文字字符串。
输出：返回目标元素的中心坐标。
异常：若未找到目标文字，抛出 ElementNotFoundException。
"""
from typing import Tuple

class ElementNotFoundException(Exception):
    """当未找到目标文字时抛出。"""
    pass

def find_element(text: str) -> Tuple[int, int]:
    """
    在当前页面识别目标文字。
    
    Args:
        text (str): 目标文字字符串。
        
    Returns:
        Tuple[int, int]: 目标元素的中心坐标 (x, y)。
        
    Raises:
        ElementNotFoundException: 若未找到目标文字。
    """
    pass
