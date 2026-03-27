"""
Spec:
返回操作组件 (back_plugin.py)
功能：执行返回操作。
输入：无。
输出：无。
"""
from test_restaurant import adb_utils

class BackPlugin:
    def back(self):
        """执行返回操作 (点击 50, 150)。"""
        adb_utils.click(50, 150)

# 创建全局返回插件实例
back_plugin = BackPlugin()
