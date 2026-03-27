import sys
import os
import json
# 添加项目根目录到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 在这里导入需要测试的组件
from components.workflow_manager import workflow_manager

if __name__ == '__main__':
    print("正在执行完整工作流测试...")
    
    # 执行工作流
    workflow_manager.run()
    
    print("\n测试完成。")
