# 当前状态文档 (Current Status)

| 文件路径 | 作用描述 | 对系统的贡献 |
| :--- | :--- | :--- |
| `crawler/main.py` | 主入口文件 | 待重构，作为系统启动入口。 |
| `crawler/scripts/auto_capture.py` | 自动截图脚本 | 提供基础截图能力，可被 `interactor` 组件复用。 |
| `crawler/scripts/clean_with_llm.py` | LLM 清洗脚本 | 核心逻辑，将集成至 `restaurant_detector` 和 `menu_detector`。 |
| `crawler/scripts/main_capture.py` | 主采集逻辑 | 待拆解，逻辑将迁移至 `workflow_manager`。 |
| `crawler/scripts/vision_utils.py` | OCR 识别工具 | 核心 OCR 能力，将集成至 `restaurant_detector` 和 `menu_detector`。 |
| `crawler/test_restaurant/adb_utils.py` | ADB 基础操作封装 | 核心底层能力，将作为 `clicker`, `scroller`, `navigator` 的基础。 |
| `crawler/test_restaurant/test_adb.py` | ADB 功能测试 | 用于验证底层 ADB 操作的稳定性。 |
| `crawler/test_restaurant/test_ocr_llm.py` | OCR 与 LLM 集成测试 | 用于验证 OCR 和 LLM 的集成效果，指导组件开发。 |
| `crawler/test_restaurant/unit_test.py` | 现有流程测试 | 待拆解，作为重构的参考基准。 |
