from openai import OpenAI

client = OpenAI(
    api_key="sk-of-xbpMtWhFmirJfZCrehRXVRByJbPuuSVLJRwutlpZySqrYiUYlBiFUQiIgfLyfEVC",
    base_url="https://api.ofox.ai/v1",
)

try:
    response = client.chat.completions.create(
        model="google/gemini-3.1-flash-lite-preview",
        messages=[{"role": "user", "content": "生命的意义是什么？"}],
    )
    print("模型调用成功！")
    print("回复内容:", response.choices[0].message.content)
except Exception as e:
    print("模型调用失败，错误信息:", e)
