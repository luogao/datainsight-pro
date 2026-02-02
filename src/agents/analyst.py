"""
Analyst Agent
负责：统计分析、趋势分析、可视化生成
"""
import os
import pandas as pd
import numpy as np
from crewai import Agent, Task, Process
from crewai.tools import SerperDevTool
from langchain.tools import tool


@tool
def calculate_basic_stats(data_dict: dict, column: str) -> dict:
    """
    计算基本统计量：均值、中位数、标准差、最小值、最大值

    Args:
        data_dict: 包含数据的字典
        column: 要分析的列名

    Returns:
        统计结果字典
    """
    # 简化处理，实际应该从 DataFrame 计算统计量
    return {
        "column": column,
        "mean": 0,
        "median": 0,
        "std": 0,
        "min": 0,
        "max": 0,
        "note": "实际实现中应该从 DataFrame 计算这些统计量"
    }


@tool
def analyze_trend(data_dict: dict, column: str, date_column: str) -> dict:
    """
    分析时间序列趋势

    Args:
        data_dict: 数据字典
        column: 数值列名
        date_column: 日期列名

    Returns:
        趋势分析结果
    """
    return {
        "column": column,
        "date_column": date_column,
        "trend": "increasing",  # 简化
        "growth_rate": "10.5%",
        "note": "实际实现中应该计算环比/同比增长率"
    }


@tool
def calculate_correlation(data_dict: dict, columns: list) -> dict:
    """
    计算列之间的相关性

    Args:
        data_dict: 数据字典
        columns: 列名列表

    Returns:
        相关性矩阵
    """
    return {
        "columns": columns,
        "correlation": {},  # 简化
        "strong_correlations": [],
        "note": "实际实现中应该计算 Pearson 相关系数"
    }


@tool
def detect_anomalies(data_dict: dict, column: str, threshold: float = 2.0) -> list:
    """
    检测异常值（使用标准差法）

    Args:
        data_dict: 数据字典
        column: 列名
        threshold: 标准差倍数

    Returns:
        异常值列表
    """
    return [
        {
            "index": 10,
            "value": 999999,
            "date": "2024-01-15",
            "z_score": 3.5,
            "note": "实际实现中应该使用真实的统计方法检测异常"
        }
    ]


@tool
def generate_chart_config(chart_type: str, x_column: str, y_column: str) -> dict:
    """
    生成图表配置（用于 Matplotlib 或其他可视化库）

    Args:
        chart_type: 图表类型（line, bar, scatter 等）
        x_column: X 轴列名
        y_column: Y 轴列名

    Returns:
        图表配置字典
    """
    return {
        "type": chart_type,
        "data": {
            "x": x_column,
            "y": y_column,
        },
        "config": {
            "title": f"{chart_type.upper()} Chart: {y_column} vs {x_column}",
            "xlabel": x_column,
            "ylabel": y_column,
            "grid": True,
            "theme": "seaborn"
        }
    }


# Analyst Agent
analyst = Agent(
    role="数据分析专家",
    goal="对数据集进行深入的统计分析，计算关键指标，识别趋势和模式",
    backstory="""你是一位专业的数据科学家，擅长使用 Python 进行数据分析。
    你能够：
    - 计算各种统计量（均值、中位数、标准差、分位数等）
    - 分析时间序列数据的趋势和周期性
    - 检测异常值和离群点
    - 计算变量之间的相关性
    - 生成清晰的统计报告
    - 创建数据可视化图表

    你总是基于数据和统计事实得出结论，而不是凭空猜测。
    你能够清楚地解释分析结果的业务含义。""",
    verbose=True,
    allow_delegation=False,
    llm="gpt-4",  # 可以根据实际情况调整
    tools=[
        calculate_basic_stats,
        analyze_trend,
        calculate_correlation,
        detect_anomalies,
        generate_chart_config
    ]
)
