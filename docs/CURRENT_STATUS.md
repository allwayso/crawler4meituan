# 当前状态文档 (Current Status)

| 文件路径 | 作用描述 |
| :--- | :--- |
| `crawler/main.py` | 主入口文件（待重构）。 |
| `crawler/scripts/auto_capture.py` | 自动截图脚本。 |
| `crawler/scripts/clean_with_llm.py` | 使用 LLM 清洗餐厅名称。 |
| `crawler/scripts/main_capture.py` | 主采集逻辑。 |
| `crawler/scripts/vision_utils.py` | OCR 识别工具（餐厅列表识别）。 |
| `crawler/test_restaurant/adb_utils.py` | ADB 基础操作封装（点击、截图）。 |
| `crawler/test_restaurant/test_adb.py` | ADB 功能测试。 |
| `crawler/test_restaurant/test_ocr_llm.py` | OCR 与 LLM 集成测试。 |
| `crawler/test_restaurant/unit_test.py` | 现有流程测试（待拆解）。 |
