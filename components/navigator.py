"""
Spec:
2. 餐厅导航组件 (navigator.py)
功能：遍历餐厅列表，选择第一个未访问的餐厅。
输入：餐厅列表。
输出：返回目标餐厅的 Y 坐标。
异常：若所有餐厅均已访问，抛出 AllRestaurantsVisitedException。
"""
from typing import List, Dict, Any

class AllRestaurantsVisitedException(Exception):
    """当所有餐厅均已访问时抛出。"""
    pass

def get_next_restaurant_y(restaurants: List[Dict[str, Any]]) -> int:
    """
    遍历餐厅列表，选择第一个未访问的餐厅。
    
    Args:
        restaurants (List[Dict[str, Any]]): 餐厅列表。
        
    Returns:
        int: 目标餐厅的 Y 坐标。
        
    Raises:
        AllRestaurantsVisitedException: 若所有餐厅均已访问。
    """
    pass
