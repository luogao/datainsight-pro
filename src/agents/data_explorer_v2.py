"""
Data Explorer Agent - 支持自定义 LLM 配置
负责：数据探索、数据质量检查、数据概览生成
"""
import os
import pandas as pd
import numpy as np
from crewai import Agent
from crewai.tools import tool
from src.crew_config import create_llm


@tool
def read_csv_dataset(file_path: str) -> dict:
    """
    读取 CSV 数据集并返回基本信息

    Args:
        file_path: CSV 文件路径

    Returns:
        包含数据信息的字典（不包含全量数据，避免 Prompt 超长）
    """
    try:
        df = pd.read_csv(file_path)

        # 只返回统计信息和预览，不返回全量数据
        return {
            "success": True,
            "file_path": file_path,
            "shape": df.shape,
            "columns": list(df.columns),
            "dtypes": df.dtypes.to_dict(),
            "memory_usage_mb": df.memory_usage(deep=True).sum() / 1024 / 1024,
            "preview": df.head(10).to_dict(orient='records'),  # 只返回前 10 行
            "missing_values": df.isnull().sum().to_dict(),
            "missing_percentage": (df.isnull().sum() / len(df) * 100).to_dict(),
            "sample_size": min(10, len(df)),
            # 只返回数值列的统计信息，不返回原始数据
            "numeric_stats": df.describe().to_dict() if len(df.select_dtypes(include=[np.number]).columns) > 0 else {}
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@tool
def check_data_quality(file_path: str) -> dict:
    """
    检查数据质量

    Args:
        file_path: CSV 文件路径

    Returns:
        数据质量报告
    """
    try:
        df = pd.read_csv(file_path)

        # 计算重复行
        duplicate_count = df.duplicated().sum()

        # 计算缺失值
        missing_values = df.isnull().sum().to_dict()
        missing_percentage = (df.isnull().sum() / len(df) * 100).to_dict()

        # 计算质量评分
        total_cells = df.shape[0] * df.shape[1]
        missing_cells = df.isnull().sum().sum()
        quality_score = "A" if missing_cells / total_cells < 0.01 else "B" if missing_cells / total_cells < 0.05 else "C"

        return {
            "success": True,
            "file_path": file_path,
            "total_records": len(df),
            "total_columns": len(df.columns),
            "missing_values": missing_values,
            "missing_percentage": missing_percentage,
            "duplicate_count": int(duplicate_count),
            "data_types": df.dtypes.to_dict(),
            "quality_score": quality_score,
            "total_cells": total_cells,
            "missing_cells": int(missing_cells),
            "completeness": f"{(1 - missing_cells / total_cells) * 100:.2f}%"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@tool
def generate_data_summary(file_path: str) -> str:
    """
    生成数据集概览报告

    Args:
        file_path: CSV 文件路径

    Returns:
        Markdown 格式的数据概览
    """
    try:
        df = pd.read_csv(file_path)

        rows, cols = df.shape
        columns = list(df.columns)
        dtypes = df.dtypes.to_dict()
        missing = df.isnull().sum().to_dict()

        summary = f"""# 📊 数据集概览

## 基本信息
- **文件路径**: {file_path}
- **数据规模**: {rows:,} 行 × {cols} 列
- **内存占用**: {df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB

## 字段列表
"""

        for col in columns:
            dtype = str(dtypes.get(col, "unknown"))
            miss = missing.get(col, 0)
            summary += f"- **{col}**: {dtype}"

            if miss > 0:
                summary += f" (缺失: {miss:,} ({miss/rows*100:.1f}%))"
            summary += "\n"

        # 添加预览
        preview_rows = min(5, len(df))
        summary += f"\n## 📋 数据预览（前 {preview_rows} 行）\n\n"

        for i in range(preview_rows):
            row = df.iloc[i]
            summary += f"**行 {i+1}:**\n"
            for col in columns[:5]:  # 只显示前 5 列
                val = row[col]
                # 处理 NaN 和长字符串
                if pd.isna(val):
                    val = "NaN"
                elif isinstance(val, str) and len(val) > 50:
                    val = val[:47] + "..."
                summary += f"  - {col}: {val}\n"
            summary += "\n"

        return summary

    except Exception as e:
        return f"❌ 数据读取失败，无法生成概览: {str(e)}"


# Data Explorer Agent（支持自定义 LLM）
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
    llm=create_llm(),  # 使用可配置的 LLM
    tools=[read_csv_dataset, check_data_quality, generate_data_summary]
)
