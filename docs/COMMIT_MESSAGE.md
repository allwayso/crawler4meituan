feat: 完善组件设计与架构调整

本次提交主要完成了以下设计与架构调整：

1. 组件接口规范化：
   - 为所有核心组件（clicker, config_manager, restaurant_detector, navigator, element_detector, scroller, menu_detector, workflow_manager）完善了 Spec 文档，并定义了标准的函数/类声明与类型提示，为后续实现奠定基础。

2. 业务逻辑优化：
   - 餐厅列表获取组件 (`restaurant_detector`)：增加了对 Y 坐标小于 300 的识别结果的清洗逻辑。
   - 滑动组件 (`scroller`)：移除了方向参数，统一固定为向上滑动，简化接口。
   - 新增餐厅信息识别组件 (`restaurant_info_detector`)：专门用于识别餐厅名称与位置信息。

3. 数据存储架构调整：
   - 细化了中间数据（截图、OCR 结果、LLM 清洗结果）的存储目录结构，在 `data/temp/` 下按任务类型（餐厅列表、餐厅详情）进行组织，确保数据可追溯且结构清晰。
   - 调整了相关组件接口，使其支持按餐厅 ID 动态存储中间数据。
