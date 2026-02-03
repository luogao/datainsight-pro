"""
LLM 配置工厂 - 支持自定义 base_url 和模型
"""
import os
from typing import Optional
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()


def create_llm(
    model: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 4096
) -> ChatOpenAI:
    """
    创建 LLM 实例（从环境变量读取配置）

    Args:
        model: 模型名称（默认从环境变量读取）
        temperature: 温度参数
        max_tokens: 最大 token 数

    Returns:
        ChatOpenAI 实例
    """
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")
    model = model or os.getenv("OPENAI_MODEL", "gpt-4")

    if not api_key:
        raise ValueError(
            "需要设置 OPENAI_API_KEY 环境变量\n"
            "请在 .env 文件中配置：\n"
            "  OPENAI_API_KEY=your_api_key_here\n"
            "  OPENAI_BASE_URL=https://api.openai.com/v1  # 可选\n"
            "  OPENAI_MODEL=gpt-4  # 可选"
        )

    # 构建 LLM 参数
    llm_kwargs = {
        "model": model,
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    # 如果设置了自定义 base_url，添加到参数中
    if base_url:
        llm_kwargs["base_url"] = base_url
        print(f"ℹ️  使用自定义 API 端点：{base_url}")
        print(f"ℹ️  使用模型：{model}")

    return ChatOpenAI(api_key=api_key, **llm_kwargs)


# 全局 LLM 实例（单例模式）
_global_llm: Optional[ChatOpenAI] = None


def get_global_llm() -> ChatOpenAI:
    """获取全局 LLM 实例"""
    global _global_llm
    if _global_llm is None:
        _global_llm = create_llm()
    return _global_llm
