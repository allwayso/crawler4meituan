"""
Spec:
0. LLM 配置组件 (config_manager.py)
功能：统一管理 API 配置（如 API Key、Base URL）、模型参数以及所有组件共享的依赖库配置。
输入：无（从配置文件读取）。
输出：提供全局配置对象供其他组件调用。
"""

from openai import OpenAI

# 配置 API
client = OpenAI(
    api_key="sk-of-xbpMtWhFmirJfZCrehRXVRByJbPuuSVLJRwutlpZySqrYiUYlBiFUQiIgfLyfEVC",
    base_url="https://api.ofox.ai/v1"
)

class ConfigManager:
    def __init__(self) -> None:
        """初始化配置管理器。"""
        self.client = client

    def get_client(self):
        """获取 OpenAI 客户端实例。"""
        return self.client

# 创建全局配置管理器实例
config_manager = ConfigManager()
