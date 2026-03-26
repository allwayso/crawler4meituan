from paddleocr import PaddleOCR

# 初始化 OCR
ocr = PaddleOCR(use_angle_cls=True, lang='ch')

def find_text_elements(screenshot_path, target_text):
    """
    识别图片中所有包含 target_text 的元素，并按 Y 坐标从小到大排序
    :return: 排序后的元素列表，每个元素包含 (text, box_center)
    """
    result = ocr.ocr(screenshot_path, cls=True)
    elements = []
    
    if result[0] is None:
        return []

    for line in result[0]:
        text = line[1][0]
        if target_text in text:
            # 计算中心坐标
            box = line[0]
            center_x = (box[0][0] + box[2][0]) / 2
            center_y = (box[0][1] + box[2][1]) / 2
            elements.append((text, (center_x, center_y)))
            
    # 按 Y 坐标排序 (从小到大，即从上到下)
    elements.sort(key=lambda x: x[1][1])
    return elements

def get_restaurant_list(screenshot_path):
    """
    识别屏幕上的餐厅列表，返回 [(name, center_x, center_y, y_min), ...]
    """
    result = ocr.ocr(screenshot_path, cls=True)
    restaurants = []
    
    if result[0] is None:
        return []

    # 假设餐厅名称通常在卡片上方，且字体较大
    # 这里需要根据实际 UI 调整过滤逻辑
    for line in result[0]:
        text = line[1][0]
        # 简单的过滤逻辑：排除非餐厅名称的干扰项
        if len(text) > 2 and "评分" not in text and "km" not in text:
            box = line[0]
            center_x = (box[0][0] + box[2][0]) / 2
            center_y = (box[0][1] + box[2][1]) / 2
            y_min = box[0][1] # 顶部 y 坐标
            restaurants.append((text, center_x, center_y, y_min))
            
    return restaurants
