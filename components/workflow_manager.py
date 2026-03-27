"""
Spec:
7. 工作流管理组件 (workflow_manager.py)
功能：协调各个组件，完成餐厅列表获取、菜单识别及数据整合。
"""

class WorkflowManager:
    def __init__(self) -> None:
        pass

    def run(self):
        """
        执行完整的工作流。
        
        TODO:
        1. 调用 restaurant_detector 获取餐厅列表信息。
        2. 遍历餐厅列表，对每个餐厅：
           a. 导航到餐厅详情页。
           b. 调用 menu_detector 获取菜单信息。
           c. 将菜单信息整合到餐厅信息中。
           d. 将整合后的完整餐厅信息（包含菜单）写入 JSONL 文件。
        """
        print("Workflow started...")
        pass

# 创建全局工作流管理器实例
workflow_manager = WorkflowManager()
