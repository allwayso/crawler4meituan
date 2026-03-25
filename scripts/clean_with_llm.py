import json
import openai

# 假设已经配置好 OpenAI API Key
# client = openai.OpenAI(api_key="YOUR_API_KEY")

def clean_with_llm(text_blocks):
    """
    调用 LLM 对合并后的文本块进行结构化清洗。
    """
    prompt = f"""
    你是一个菜品数据清洗专家。请将以下 OCR 识别出的文本块整理成结构化的 JSON 格式。
    每个菜品包含：name (菜名), description (描述), price (价格)。
    如果文本块中包含非菜品信息（如“温馨提示”），请忽略。
    
    文本块：
    {json.dumps(text_blocks, ensure_ascii=False)}
    
    请直接输出 JSON 列表。
    """
    
    # 这里模拟调用 LLM 的过程
    # response = client.chat.completions.create(
    #     model="gpt-4o",
    #     messages=[{"role": "user", "content": prompt}]
    # )
    # return json.loads(response.choices[0].message.content)
    
    # 暂时返回模拟数据
    return [{"name": "示例菜品", "description": "示例描述", "price": "￥10"}]

# 示例调用
text_blocks = ["珍珠香米饭", "灵魂蛋炒饭 ￥4.5"]
cleaned_data = clean_with_llm(text_blocks)
print(json.dumps(cleaned_data, ensure_ascii=False, indent=2))
