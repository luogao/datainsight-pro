"""
Analyst Agent - 支持自定义 LLM 配置
负责：统计分析、趋势分析、可视化生成
"""
import os
import pandas as pd
import numpy as np
from crewai import Agent
from crewai.tools import tool
from src.crew_config import create_llm


@tool
def calculate_basic_stats(file_path: str, column: str) -> dict:
    """
    计算基本统计量：均值、中位数、标准差、最小值、最大值

    Args:
        file_path: CSV 文件路径
        column: 要分析的列名

    Returns:
        统计结果字典
    """
    try:
        df = pd.read_csv(file_path)

        if column not in df.columns:
            return {"error": f"列 '{column}' 不存在"}

        series = df[column].dropna()

        return {
            "column": column,
            "count": len(series),
            "mean": float(series.mean()),
            "median": float(series.median()),
            "std": float(series.std()),
            "min": float(series.min()),
            "max": float(series.max()),
            "q25": float(series.quantile(0.25)),
            "q75": float(series.quantile(0.75))
        }
    except Exception as e:
        return {"error": str(e)}


@tool
def analyze_trend(file_path: str, column: str, date_column: str = None) -> dict:
    """
    分析时间序列趋势

    Args:
        file_path: CSV 文件路径
        column: 数值列名
        date_column: 日期列名（可选）

    Returns:
        趋势分析结果
    """
    try:
        df = pd.read_csv(file_path)

        if column not in df.columns:
            return {"error": f"列 '{column}' 不存在"}

        # 计算增长率
        values = df[column].values
        if len(values) < 2:
            return {"error": "数据不足，无法分析趋势"}

        growth_rates = []
        for i in range(1, len(values)):
            if values[i-1] != 0:
                rate = (values[i] - values[i-1]) / values[i-1] * 100
                growth_rates.append(rate)

        avg_growth = np.mean(growth_rates) if growth_rates else 0

        # 判断趋势
        if avg_growth > 1:
            trend = "increasing"
        elif avg_growth < -1:
            trend = "decreasing"
        else:
            trend = "stable"

        return {
            "column": column,
            "trend": trend,
            "average_growth_rate": round(avg_growth, 2),
            "min_growth": round(min(growth_rates), 2) if growth_rates else 0,
            "max_growth": round(max(growth_rates), 2) if growth_rates else 0
        }
    except Exception as e:
        return {"error": str(e)}


@tool
def calculate_correlation(file_path: str, columns: list) -> dict:
    """
    计算列之间的相关性

    Args:
        file_path: CSV 文件路径
        columns: 列名列表

    Returns:
        相关性矩阵
    """
    try:
        df = pd.read_csv(file_path)

        # 筛选数值列
        numeric_cols = df[columns].select_dtypes(include=[np.number]).columns.tolist()

        if len(numeric_cols) < 2:
            return {"error": "需要至少 2 个数值列"}

        corr_matrix = df[numeric_cols].corr()

        # 找出强相关关系
        strong_correlations = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                col1 = corr_matrix.columns[i]
                col2 = corr_matrix.columns[j]
                corr_val = corr_matrix.iloc[i, j]

                if abs(corr_val) > 0.7:  # 强相关阈值
                    strong_correlations.append({
                        "col1": col1,
                        "col2": col2,
                        "correlation": round(corr_val, 3)
                    })

        return {
            "columns": numeric_cols,
            "correlation_matrix": corr_matrix.to_dict(),
            "strong_correlations": strong_correlations
        }
    except Exception as e:
        return {"error": str(e)}


@tool
def detect_anomalies(file_path: str, column: str, threshold: float = 2.0) -> list:
    """
    检测异常值（使用标准差法）

    Args:
        file_path: CSV 文件路径
        column: 列名
        threshold: 标准差倍数

    Returns:
        异常值列表
    """
    try:
        df = pd.read_csv(file_path)

        if column not in df.columns:
            return [{"error": f"列 '{column}' 不存在"}]

        series = df[column].dropna()
        mean = series.mean()
        std = series.std()

        anomalies = []
        for idx, value in series.items():
            z_score = (value - mean) / std if std > 0 else 0
            if abs(z_score) > threshold:
                anomalies.append({
                    "index": int(idx),
                    "value": float(value),
                    "z_score": round(z_score, 2)
                })

        return anomalies
    except Exception as e:
        return [{"error": str(e)}]


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


# Analyst Agent（支持自定义 LLM）
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
    llm=create_llm(),  # 使用可配置的 LLM
    tools=[
        calculate_basic_stats,
        analyze_trend,
        calculate_correlation,
        detect_anomalies,
        generate_chart_config
    ]
)
