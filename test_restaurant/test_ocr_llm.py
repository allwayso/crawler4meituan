import sys
import os
import json
from openai import OpenAI
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../crawler/scripts')))
import adb_utils
import vision_utils

# 配置 API
client = OpenAI(
    api_key="sk-of-xbpMtWhFmirJfZCrehRXVRByJbPuuSVLJRwutlpZySqrYiUYlBiFUQiIgfLyfEVC",
    base_url="https://api.ofox.ai/v1"
)

def clean_restaurant_names_with_llm(raw_data):
    """
    调用 LLM 从 OCR 原始数据中提取餐厅名称及其坐标。
    """
    prompt = f"""
    你是一个餐厅数据采集专家。请从以下 OCR 识别出的原始数据（包含文本和坐标）中，提取出真正的餐厅名称及其对应的顶部 Y 坐标 (y_min)。
    忽略非餐厅名称的干扰项（如“评分”、“距离”、“优惠券”、“我的订单”、“快餐小吃”等）。
    
    OCR 原始数据：
    {json.dumps(raw_data, ensure_ascii=False)}
    
    请直接输出一个 JSON 格式的列表，每个元素包含餐厅名称和 y_min，例如：
    [ {{"name": "餐厅A", "y_min": 100}}, {{"name": "餐厅B", "y_min": 400}} ]
    """
    
    # 调用 LLM
    response = client.chat.completions.create(
        model="google/gemini-3.1-flash-lite-preview",
        messages=[{"role": "user", "content": prompt}]
    )
    
    content = response.choices[0].message.content
    content = content.replace("```json", "").replace("```", "").strip()
    cleaned_data = json.loads(content)
    
    # 过滤掉 y_min 小于 300 的项
    filtered_data = [item for item in cleaned_data if item.get('y_min', 0) >= 300]
    return filtered_data

OUTPUT_DIR = "../crawler/img/test_test"

if __name__ == "__main__":
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    screenshot_path = os.path.join(OUTPUT_DIR, "list.png")
    adb_utils.screenshot(screenshot_path)
    
    # 1. OCR 识别
    restaurants = vision_utils.get_restaurant_list(screenshot_path)
    print(f"OCR 识别到的原始数据: {restaurants}")
    
    # 2. 保存原始数据
    with open(os.path.join(OUTPUT_DIR, "restaurants_with_coords.json"), "w", encoding="utf-8") as f:
        json.dump(restaurants, f, ensure_ascii=False, indent=4)
    
    # 3. LLM 清洗
    print("正在调用 LLM 清洗餐厅名称及坐标...")
    cleaned_data = clean_restaurant_names_with_llm(restaurants)
    print(f"清洗后的餐厅列表: {cleaned_data}")
    
    # 4. 保存结果
    output_path = os.path.join(OUTPUT_DIR, "cleaned_restaurants_with_coords.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, ensure_ascii=False, indent=4)
    
    print(f"测试结束，结果已保存至: {output_path}")
