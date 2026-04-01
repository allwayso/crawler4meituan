"""
Spec:
1. 餐厅列表获取组件 (restaurant_detector.py)
功能：截图并识别当前屏幕上的餐厅列表，结合 OCR 与 LLM 进行清洗，提取名称、地址、评分并生成唯一 ID。
输入：无（内部调用截图与 OCR）。
输出：返回清洗后的餐厅列表（包含名称、地址、评分、ID、坐标等信息）。
"""

import json
import hashlib
import numpy as np
from paddleocr import PaddleOCR
from components.config_manager import config_manager
from components.adb_utils import adb_utils
from components.logging_utils import get_logger


logger = get_logger(__name__)

class RestaurantDetector:
    def __init__(self) -> None:
        self.client = config_manager.get_client()
        # 初始化 OCR
        self.ocr = PaddleOCR(use_angle_cls=True, lang='ch', show_log=False)

    def _generate_id(self, name: str, address: str) -> str:
        """根据名称和地址生成唯一 ID。"""
        return hashlib.md5(f"{name}_{address}".encode('utf-8')).hexdigest()

    def ocr_detect(self, screenshot) -> list:
        """识别屏幕上的文字，直接返回 OCR 原始结构。"""
        if hasattr(screenshot, "convert"):
            screenshot = np.array(screenshot)
        result = self.ocr.ocr(screenshot, cls=True)
        texts = []
        if result[0] is not None:
            for line in result[0]:
                # 记录文字和对应的坐标 (取左上角 y 坐标)
                texts.append({"text": line[1][0], "y_min": line[0][0][1]})
        return texts

    def llm_clean(self, ocr_texts: list) -> list:
        """调用 LLM 从 OCR 原始数据中提取餐厅信息。"""
        prompt = f"""
        你是一个餐厅数据采集专家。请从以下 OCR 识别出的原始文本（包含文字和对应的 y 坐标）中，提取出餐厅列表。
        过滤规则：
        - 直接忽略连锁饮料/咖啡门店（例如：瑞幸、星巴克、喜茶、奈雪、CoCo、古茗、沪上阿姨、霸王茶姬、茶百道、一点点等），不要把它们输出为餐厅条目。
        - 同理忽略连锁快餐门店(例如：肯德基、麦当劳等等)
        每个餐厅需要包含：名称 (name)、地址 (address)、评分 (rating)、顶部 Y 坐标 (y_min)。
        另外需要判断餐厅是否为"正餐"：
        - 若为甜品/蛋糕/烘焙/西点/奶茶/饮品/咖啡/轻食等非正餐业态，则 is_main_dish=false
        - 若为正餐（中餐/西餐/快餐/火锅/烧烤等）则 is_main_dish=true
        
        注意：判定时优先使用 OCR 中餐厅名/地址附近出现的关键词。
        
        注意：
        1. y_min 必须是该餐厅标题文字在屏幕上的真实像素 Y 坐标，请从 OCR 数据中准确提取。
        2. 忽略非餐厅项的干扰项。
        3. 如果餐厅名后面有 "(xx" 且没有右括号包裹，请将这一部分清理掉。
        4. 忽略y值小于400的项
        
        OCR 原始数据：
        {json.dumps(ocr_texts, ensure_ascii=False)}
        
        请直接输出一个 JSON 格式的列表，例如：
        [
            {{"name": "餐厅A", "address": "地址A", "rating": 4.5, "y_min": 100, "is_main_dish": true}},
            {{"name": "餐厅B", "address": "地址B", "rating": 4.8, "y_min": 400, "is_main_dish": false}}
        ]
        """
        
        response = self.client.chat.completions.create(
            model="google/gemini-3.1-flash-lite-preview",
            messages=[{"role": "user", "content": prompt}]
        )
        
        content = response.choices[0].message.content
        content = content.replace("```json", "").replace("```", "").strip()
        try:
            cleaned_data = json.loads(content)
        except json.JSONDecodeError:
            logger.warning(f"LLM 返回内容无法解析为 JSON (restaurant_detector), content_prefix={content[:80]!r}")
            return []
        
        # 补充 ID
        normalized = []
        for item in cleaned_data:
            # 不兼容旧数据：必须有 is_main_dish
            if 'is_main_dish' not in item:
                logger.debug(f"skip item without is_main_dish: {item}")
                continue

            # 严格要求只接受 true/false（允许 JSON boolean 或字符串 'true'/'false'）
            is_main_dish = item.get('is_main_dish')
            if isinstance(is_main_dish, bool):
                pass
            elif isinstance(is_main_dish, str):
                lowered = is_main_dish.strip().lower()
                if lowered == 'true':
                    is_main_dish = True
                elif lowered == 'false':
                    is_main_dish = False
                else:
                    logger.debug(
                        f"invalid is_main_dish value: {is_main_dish!r}, item skipped"
                    )
                    continue
            else:
                logger.debug(
                    f"invalid is_main_dish type: {type(is_main_dish)}, item skipped"
                )
                continue

            item['restaurant_id'] = self._generate_id(item.get('name', ''), item.get('address', ''))
            item['is_main_dish'] = is_main_dish
            normalized.append(item)
            
        return normalized

    def get_restaurants(self) -> list:
        """获取并清洗餐厅列表。"""
        screenshot = adb_utils.screenshot()

        # 1. OCR 识别，直接保留在内存中
        ocr_texts = self.ocr_detect(screenshot)

        # 2. LLM 清洗，直接传入 OCR 结构
        cleaned_data = self.llm_clean(ocr_texts)
        
        return cleaned_data

# 创建全局餐厅检测器实例
restaurant_detector = RestaurantDetector()
