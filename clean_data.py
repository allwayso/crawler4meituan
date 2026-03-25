import json
import os
from openai import OpenAI

# 配置 API
client = OpenAI(
    api_key="sk-of-xbpMtWhFmirJfZCrehRXVRByJbPuuSVLJRwutlpZySqrYiUYlBiFUQiIgfLyfEVC",
    base_url="https://api.ofox.ai/v1"
)

def clean_with_llm(raw_data):
    """
    直接调用 LLM 对 OCR 原始数据进行结构化清洗。
    """
    # 将原始数据转换为文本描述，供 LLM 理解
    text_content = json.dumps(raw_data, ensure_ascii=False)
    
    prompt = f"""
    你是一个菜品数据清洗专家。请将以下 OCR 识别出的原始数据整理成结构化的 JSON 格式。
    每个菜品包含：name (菜名), description (描述), price (价格)。
    如果文本块中包含非菜品信息（如“温馨提示”），请忽略。
    
    OCR 原始数据：
    {text_content}
    
    请直接输出 JSON 列表。
    """
    
    # 调用 LLM
    response = client.chat.completions.create(
        model="google/gemini-3.1-flash-lite-preview",
        messages=[{"role": "user", "content": prompt}]
    )
    # 提取 JSON 内容
    content = response.choices[0].message.content
    # 移除可能的 markdown 标记
    content = content.replace("```json", "").replace("```", "").strip()
    return json.loads(content)

def process_file():
    input_path = input("请输入待清洗的 OCR 原始 JSON 数据文件路径: ").strip()
    # 移除可能存在的引号和不可见字符
    input_path = input_path.replace('"', '').replace("'", "").replace('\ufeff', '')
    if not os.path.exists(input_path):
        print(f"文件不存在: {input_path}，请检查路径。")
        return

    with open(input_path, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)

    cleaned_data = clean_with_llm(raw_data)
    
    # 准备输出目录
    output_dir = "../crawler/cleaned_by_llm"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    file_name = os.path.basename(input_path)
    output_path = os.path.join(output_dir, f"llm_cleaned_{file_name}")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, ensure_ascii=False, indent=2)
        
    print(f"清洗完成，结果已保存至: {output_path}")

if __name__ == "__main__":
    process_file()
