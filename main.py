import json
from playwright.sync_api import sync_playwright
import time

def save_to_jsonl(data, filename):
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False) + '\n')

def run_crawler(url, output_file):
    with sync_playwright() as p:
        # 启动浏览器，设置 User-Agent 模拟真实浏览器
        browser = p.chromium.launch(headless=False) # 设置为 False 以便观察
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        print(f"正在访问: {url}")
        page.goto(url, wait_until="networkidle")
        
        # 模拟滚动以加载懒加载内容
        page.mouse.wheel(0, 1000)
        time.sleep(2)
        
        # 截图用于 OCR
        screenshot_path = 'crawler/data/menu_screenshot.png'
        page.screenshot(path=screenshot_path)
        print(f"页面截图已保存至: {screenshot_path}")
        
        # 此处可以添加解析页面 DOM 的逻辑 (如果页面结构允许)
        # ...
        
        browser.close()

if __name__ == "__main__":
    # 替换为实际的美团商家菜单 URL
    target_url = "https://www.meituan.com/" 
    run_crawler(target_url, 'crawler/data/dishes.jsonl')
