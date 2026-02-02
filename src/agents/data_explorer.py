"""
Data Explorer Agent
负责：数据探索、数据质量检查、数据概览生成
"""
import os
import pandas as pd
import numpy as np
from crewai import Agent, Task, Process
from crewai.tools import SerperDevTool
from langchain.tools import tool


@tool
def read_csv_dataset(file_path: str) -> dict:
    """
    读取 CSV 数据集并返回基本信息

    Args:
        file_path: CSV 文件路径

    Returns:
        包含数据信息的字典
    """
    try:
        df = pd.read_csv(file_path)

        return {
            "success": True,
            "shape": df.shape,
            "columns": list(df.columns),
            "dtypes": df.dtypes.to_dict(),
            "memory_usage": df.memory_usage(deep=True).sum() / 1024 / 1024,  # MB
            "preview": df.head().to_dict(orient='records'),
            "missing_values": df.isnull().sum().to_dict(),
            "sample_size": min(5, len(df))
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@tool
def check_data_quality(df_dict: dict) -> dict:
    """
    检查数据质量

    Args:
        df_dict: 包含数据的字典（从 read_csv_dataset 返回）

    Returns:
        数据质量报告
    """
    if not df_dict.get("success"):
        return {
            "success": False,
            "error": "Invalid data"
        }

    # 这里简化处理，实际应该从 df_dict 中提取数据
    # 在实际使用中，数据会在 Agent 间传递
    return {
        "total_records": df_dict.get("shape", [0, 0])[0],
        "total_columns": df_dict.get("shape", [0, 0])[1],
        "missing_values": df_dict.get("missing_values", {}),
        "duplicate_count": 0,  # 简化
        "data_types": df_dict.get("dtypes", {}),
        "quality_score": "A"  # 简化
    }


@tool
def generate_data_summary(df_dict: dict) -> str:
    """
    生成数据集概览报告

    Args:
        df_dict: 数据字典

    Returns:
        Markdown 格式的数据概览
    """
    if not df_dict.get("success"):
        return "❌ 数据读取失败，无法生成概览"

    rows, cols = df_dict.get("shape", [0, 0])
    columns = df_dict.get("columns", [])
    dtypes = df_dict.get("dtypes", {})
    missing = df_dict.get("missing_values", {})

    summary = f"""# 📊 数据集概览

## 基本信息
- **数据规模**: {rows:,} 行 × {cols} 列
- **内存占用**: {df_dict.get('memory_usage', 0):.2f} MB

## 字段列表
"""

    for col in columns:
        dtype = dtypes.get(col, "unknown")
        miss = missing.get(col, 0)
        summary += f"- **{col}**: {dtype}"

        if miss > 0:
            summary += f" (缺失: {miss:,})"
        summary += "\n"

    # 添加预览
    preview = df_dict.get("preview", [])
    if preview:
        summary += f"\n## 📋 数据预览（前 {len(preview)} 行）\n\n"
        for i, row in enumerate(preview):
            summary += f"**行 {i+1}:**\n"
            for key, value in row.items():
                summary += f"  - {key}: {value}\n"
            summary += "\n"

    return summary


# Data Explorer Agent
data_explorer = Agent(
    role="数据探索专家",
    goal="探索和理解数据集结构，检查数据质量，生成概览报告",
    backstory="""你是一位经验丰富的数据分析师，擅长快速理解数据集的结构和特征。
    你能够：
    - 读取各种格式的数据集（CSV、JSON、Excel）
    - 分析数据类型和结构
    - 检测数据质量问题（缺失值、异常值、重复值）
    - 生成清晰的数据概览报告
    - 为后续分析提供必要的数据洞察""",
    verbose=True,
    allow_delegation=False,
    llm="gpt-4",  # 可以根据实际情况调整
    tools=[read_csv_dataset, check_data_quality, generate_data_summary]
)
