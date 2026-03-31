"""
Spec:
返回操作组件 (back_plugin.py)
功能：执行返回操作。
输入：无。
输出：无。
"""
from components.adb_utils import adb_utils

class BackPlugin:
    def back(self):
        """执行返回操作 (点击 70, 170)。"""
        adb_utils.tap(70, 170)

# 创建全局返回插件实例
back_plugin = BackPlugin()


# 兼容旧调用方式：某些测试/脚本可能期望 `components.back_plugin.back()` 可直接调用。
def back():
    back_plugin.back()
