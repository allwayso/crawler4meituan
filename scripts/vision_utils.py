import cv2
import numpy as np

def find_element(screenshot_path, template_path, threshold=0.8):
    """
    在截图中查找模板图片的位置
    :param screenshot_path: 截图路径
    :param template_path: 模板图片路径
    :param threshold: 匹配阈值
    :return: 找到的中心坐标 (x, y) 或 None
    """
    img = cv2.imread(screenshot_path)
    template = cv2.imread(template_path)
    
    if img is None or template is None:
        print("Error: Image or template not found.")
        return None
        
    res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    
    if max_val >= threshold:
        h, w = template.shape[:2]
        center_x = max_loc[0] + w // 2
        center_y = max_loc[1] + h // 2
        return (center_x, center_y)
    
    return None
