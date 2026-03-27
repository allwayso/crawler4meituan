"""
Spec:
1. 餐厅列表获取组件 (restaurant_detector.py)
功能：截图并识别当前屏幕上的餐厅列表，结合 OCR 与 LLM 进行清洗。
输入：无（内部调用截图与 OCR）。
输出：返回清洗后的餐厅列表（包含名称、坐标等信息）。
"""

import os
import json
from paddleocr import PaddleOCR
from components.config_manager import config_manager
from test_restaurant import adb_utils

class RestaurantDetector:
    def __init__(self, output_dir: str = "D:/crawler/data/temp/restaurant_list") -> None:
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        self.client = config_manager.get_client()
        # 初始化 OCR
        self.ocr = PaddleOCR(use_angle_cls=True, lang='ch')

    def ocr_detect(self, screenshot_path):
        """识别屏幕上的餐厅列表，返回 [(name, center_x, center_y, y_min), ...]"""
        result = self.ocr.ocr(screenshot_path, cls=True)
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

    def llm_clean(self, raw_data):
        """调用 LLM 从 OCR 原始数据中提取餐厅名称及其坐标。"""
        prompt = f"""
        你是一个餐厅数据采集专家。请从以下 OCR 识别出的原始数据（包含文本和坐标）中，提取出真正的餐厅名称及其对应的顶部 Y 坐标 (y_min)。
        忽略非餐厅名称的干扰项（如“评分”、“距离”、“优惠券”、“我的订单”、“快餐小吃”等）。
        
        OCR 原始数据：
        {json.dumps(raw_data, ensure_ascii=False)}
        
        请直接输出一个 JSON 格式的列表，每个元素包含餐厅名称和 y_min，例如：
        [ {{"name": "餐厅A", "y_min": 100}}, {{"name": "餐厅B", "y_min": 400}} ]
        """
        
        response = self.client.chat.completions.create(
            model="google/gemini-3.1-flash-lite-preview",
            messages=[{"role": "user", "content": prompt}]
        )
        
        content = response.choices[0].message.content
        content = content.replace("```json", "").replace("```", "").strip()
        cleaned_data = json.loads(content)
        
        # 过滤掉 y_min 小于 300 的项
        filtered_data = [item for item in cleaned_data if item.get('y_min', 0) >= 300]
        return filtered_data

    def get_restaurants(self):
        """获取并清洗餐厅列表。"""
        # 获取内存中的截图
        screenshot = adb_utils.screenshot()
        screenshot_path = os.path.join(self.output_dir, "list.png")
        screenshot.save(screenshot_path)
        
        # 1. OCR 识别
        restaurants = self.ocr_detect(screenshot_path)
        with open(os.path.join(self.output_dir, "ocr_raw.json"), "w", encoding="utf-8") as f:
            json.dump(restaurants, f, ensure_ascii=False, indent=4)
        
        # 2. LLM 清洗
        cleaned_data = self.llm_clean(restaurants)
        with open(os.path.join(self.output_dir, "cleaned_restaurants.json"), "w", encoding="utf-8") as f:
            json.dump(cleaned_data, f, ensure_ascii=False, indent=4)
        
        return cleaned_data

# 创建全局餐厅检测器实例
restaurant_detector = RestaurantDetector()
