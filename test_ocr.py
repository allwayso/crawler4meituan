import os
import json
import sys
# 尝试禁用 oneDNN 以解决 NotImplementedError
os.environ['FLAGS_use_onednn'] = '0'

from paddleocr import PaddleOCR
import cv2
import numpy as np

# 初始化 OCR 引擎
ocr = PaddleOCR(use_textline_orientation=True, lang='ch')

def split_image(image_path, chunk_height=2000):
    """将长图切分成多个小块"""
    img = cv2.imread(image_path)
    if img is None:
        return []
    
    h, w, _ = img.shape
    chunks = []
    for i in range(0, h, chunk_height):
        chunk = img[i:i+chunk_height, :, :]
        chunks.append(chunk)
    return chunks

def test_ocr(image_path):
    print(f"正在尝试读取图片: {image_path}")
    
    # 检查图片尺寸，如果过长则切分
    img = cv2.imread(image_path)
    if img is None:
        print(f"无法读取图片: {image_path}")
        return
    
    h, w, _ = img.shape
    print(f"图片尺寸: {w}x{h}")
    
    results = []
    if h > 3000:
        print("图片过长，正在进行切分识别...")
        chunks = split_image(image_path)
        for i, chunk in enumerate(chunks):
            print(f"正在识别第 {i+1} 个切片...")
            # 将切片保存为临时文件进行识别
            temp_path = f"temp_chunk_{i}.png"
            cv2.imwrite(temp_path, chunk)
            chunk_result = ocr.ocr(temp_path, cls=True)
            results.append(chunk_result)
            os.remove(temp_path)
    else:
        print("正在进行 OCR 识别 (使用 ocr)...")
        results = ocr.ocr(image_path, cls=True)
    
    # 确保 raw_data 目录存在
    output_dir = 'd:\\crawler\\raw_data'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 将结果保存到 raw_data 目录
    image_name = os.path.basename(image_path)
    output_file = os.path.join(output_dir, f"{os.path.splitext(image_name)[0]}.json")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    
    print(f"识别结果已保存至: {output_file}")

if __name__ == "__main__":
    print("OCR 测试工具已启动。输入图片路径开始识别，输入 'exit' 退出。")
    while True:
        image_path = input("\n请输入图片路径: ").strip()
        if image_path.lower() == 'exit':
            print("正在退出...")
            break
        
        # 去除路径可能包含的引号
        image_path = image_path.replace('"', '').replace("'", "")
        
        if os.path.exists(image_path):
            test_ocr(image_path)
        else:
            print(f"错误: 文件不存在 - {image_path}")
