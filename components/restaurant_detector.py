"""
Spec:
1. 餐厅列表获取组件 (restaurant_detector.py)
功能：截图并识别当前屏幕上的餐厅列表，结合 OCR 与 LLM 进行清洗，提取名称、地址、评分并生成唯一 ID。
输入：无（内部调用截图与 OCR）。
输出：返回清洗后的餐厅列表（包含名称、地址、评分、ID、坐标等信息）。
"""

import os
import json
import hashlib
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

    def _generate_id(self, name: str, address: str) -> str:
        """根据名称和地址生成唯一 ID。"""
        return hashlib.md5(f"{name}_{address}".encode('utf-8')).hexdigest()

    def ocr_detect(self, screenshot_path: str) -> str:
        """识别屏幕上的文字。"""
        result = self.ocr.ocr(screenshot_path, cls=True)
        texts = []
        if result[0] is not None:
            for line in result[0]:
                texts.append(line[1][0])
        return json.dumps(texts, ensure_ascii=False)

    def llm_clean(self, ocr_text: str) -> list:
        """调用 LLM 从 OCR 原始数据中提取餐厅信息。"""
        prompt = f"""
        你是一个餐厅数据采集专家。请从以下 OCR 识别出的原始文本中，提取出餐厅列表。
        每个餐厅需要包含：名称 (name)、地址 (address)、评分 (rating)、顶部 Y 坐标 (y_min)。
        忽略非餐厅项的干扰项。
        
        OCR 原始数据：
        {ocr_text}
        
        请直接输出一个 JSON 格式的列表，例如：
        [
            {{"name": "餐厅A", "address": "地址A", "rating": 4.5, "y_min": 100}},
            {{"name": "餐厅B", "address": "地址B", "rating": 4.8, "y_min": 400}}
        ]
        """
        
        response = self.client.chat.completions.create(
            model="google/gemini-3.1-flash-lite-preview",
            messages=[{"role": "user", "content": prompt}]
        )
        
        content = response.choices[0].message.content
        content = content.replace("```json", "").replace("```", "").strip()
        cleaned_data = json.loads(content)
        
        # 补充 ID 并过滤
        for item in cleaned_data:
            item['restaurant_id'] = self._generate_id(item.get('name', ''), item.get('address', ''))
            
        return [item for item in cleaned_data if item.get('y_min', 0) >= 300]

    def get_restaurants(self) -> list:
        """获取并清洗餐厅列表。"""
        # 获取内存中的截图
        screenshot = adb_utils.screenshot()
        screenshot_path = os.path.join(self.output_dir, "list.png")
        screenshot.save(screenshot_path)
        
        # 1. OCR 识别
        ocr_text = self.ocr_detect(screenshot_path)
        
        # 2. LLM 清洗
        cleaned_data = self.llm_clean(ocr_text)
        with open(os.path.join(self.output_dir, "cleaned_restaurants.json"), "w", encoding="utf-8") as f:
            json.dump(cleaned_data, f, ensure_ascii=False, indent=4)
        
        return cleaned_data

# 创建全局餐厅检测器实例
restaurant_detector = RestaurantDetector()
