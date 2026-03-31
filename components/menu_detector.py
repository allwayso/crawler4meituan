"""
Spec:
6. 菜单识别组件 (menu_detector.py)
功能：接受两张截图，执行 OCR 识别和 LLM 清洗，返回菜单数据列表。
输入：两张截图路径。
输出：菜单数据列表（包含菜名、价格、描述）。
"""
import json
from typing import List, Dict
import re
import numpy as np
from paddleocr import PaddleOCR
from components.config_manager import config_manager

class MenuDetector:
    def __init__(self) -> None:
        self.client = config_manager.get_client()
        # 初始化 OCR
        self.ocr = PaddleOCR(use_angle_cls=True, lang='ch')

    def ocr_detect(self, screenshot) -> List[str]:
        """识别截图中的文字。"""
        if hasattr(screenshot, "convert"):
            screenshot = np.array(screenshot)
        result = self.ocr.ocr(screenshot, cls=True)
        texts = []
        if result[0] is not None:
            for line in result[0]:
                texts.append(line[1][0])
        return texts

    def llm_clean(self, texts1: List[str], texts2: List[str]) -> List[Dict]:
        """调用 LLM 从 OCR 原始数据中提取菜单数据。"""
        prompt = f"""
        你是一个菜单数据采集专家。请从以下两张截图的 OCR 识别出的原始文本中，提取出菜单数据（菜名、价格、描述）。
        忽略非菜单项的干扰项。
        
        OCR 原始数据 1：
        {json.dumps(texts1, ensure_ascii=False)}
        
        OCR 原始数据 2：
        {json.dumps(texts2, ensure_ascii=False)}
        
        请直接输出一个 JSON 格式的菜单列表，每个元素包含 dish_name, price, description。
        如果没有从 OCR 中找到描述，则 description 留空字符串。
        注意：饮料/甜点等非正餐项也为合法菜品，但它们的 description 可能更简略。
        例如：
        [
            {{"dish_name": "红烧肉", "price": 38.0, "description": "精选五花肉，肥而不腻"}},
            {{"dish_name": "清蒸鱼", "price": 58.0, "description": ""}}
        ]
        """
        
        response = self.client.chat.completions.create(
            model="google/gemini-3.1-flash-lite-preview",
            messages=[{"role": "user", "content": prompt}]
        )
        
        content = response.choices[0].message.content
        content = content.replace("```json", "").replace("```", "").strip()

        # 兜底：LLM 有时会返回非严格 JSON（例如空字符串、前后夹杂说明文字）
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            pass

        # 尝试从文本中提取第一个 JSON 数组片段
        try:
            m = re.search(r"\[[\s\S]*\]", content)
            if m:
                return json.loads(m.group(0))
        except Exception:
            pass

        print(f"[MenuDetector] LLM返回内容无法解析为 JSON，返回空列表。content_prefix={content[:80]!r}")
        return []

    def detect_menu(self, screenshot1, screenshot2) -> List[Dict]:
        """
        接受两张截图对象，执行 OCR 识别和 LLM 清洗。
        
        Args:
            screenshot1: 第一张截图对象。
            screenshot2: 第二张截图对象。
            
        Returns:
            List[Dict]: 菜单数据列表。
        """
        texts1 = self.ocr_detect(screenshot1)
        texts2 = self.ocr_detect(screenshot2)
        
        return self.llm_clean(texts1, texts2)

# 创建全局菜单检测器实例
menu_detector = MenuDetector()
