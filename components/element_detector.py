"""
Spec:
3. 元素识别组件 (element_detector.py)
功能：在当前页面识别目标文字（如“菜品”、“查看全部”等）。
输入：目标文字字符串。
输出：返回目标元素的中心坐标。
异常：若未找到目标文字，抛出 ElementNotFoundException。
"""
import os
from typing import Tuple
from paddleocr import PaddleOCR
from test_restaurant import adb_utils

class ElementNotFoundException(Exception):
    """当未找到目标文字时抛出。"""
    def __init__(self, target_text: str):
        self.target_text = target_text
        super().__init__(f"未在当前页面找到目标元素: {target_text}")

class ElementDetector:
    def __init__(self, output_dir: str = "D:/crawler/data/temp/element_detection") -> None:
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        # 初始化 OCR
        self.ocr = PaddleOCR(use_angle_cls=True, lang='ch')

    def find_element(self, target_text: str) -> Tuple[int, int]:
        """
        在当前页面识别目标文字。
        
        Args:
            target_text (str): 目标文字字符串。
            
        Returns:
            Tuple[int, int]: 目标元素的中心坐标 (x, y)。
            
        Raises:
            ElementNotFoundException: 若未找到目标文字。
        """
        # 获取内存中的截图
        screenshot = adb_utils.screenshot()
        screenshot_path = os.path.join(self.output_dir, "current_screen.png")
        screenshot.save(screenshot_path)
        
        result = self.ocr.ocr(screenshot_path, cls=True)
        
        if result[0] is None:
            raise ElementNotFoundException(target_text)

        for line in result[0]:
            text = line[1][0]
            if target_text in text:
                # 计算中心坐标
                box = line[0]
                center_x = (box[0][0] + box[2][0]) / 2
                center_y = (box[0][1] + box[2][1]) / 2
                return (int(center_x), int(center_y))
        
        raise ElementNotFoundException(target_text)

# 创建全局元素检测器实例
element_detector = ElementDetector()
