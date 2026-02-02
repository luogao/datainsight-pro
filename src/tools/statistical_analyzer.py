"""
统计分析工具
"""
import numpy as np
import pandas as pd
from scipy import stats
from typing import Dict, List, Any
from datetime import datetime, timedelta


def calculate_basic_statistics(df: pd.DataFrame, column: str) -> Dict[str, float]:
    """
    计算基本统计量：均值、中位数、标准差、最小值、最大值、分位数

    Args:
        df: DataFrame
        column: 列名

    Returns:
        统计结果字典
    """
    try:
        series = df[column]

        if not pd.api.types.is_numeric_dtype(series):
            return {
                "column": column,
                "type": "categorical",
                "error": "该列不是数值类型"
            }

        stats = {
            "column": column,
            "type": "numeric",
            "count": len(series),
            "mean": float(series.mean()),
            "median": float(series.median()),
            "std": float(series.std()),
            "var": float(series.var()),
            "min": float(series.min()),
            "max": float(series.max()),
            "range": float(series.max() - series.min()),
            "q25": float(series.quantile(0.25)),
            "q50": float(series.quantile(0.50)),
            "q75": float(series.quantile(0.75)),
            "iqr": float(series.quantile(0.75) - series.quantile(0.25)),
            "skewness": float(series.skew()) if len(series) > 2 else 0.0,
            "kurtosis": float(series.kurtosis()) if len(series) > 3 else 0.0
        }

        return stats

    except Exception as e:
        return {
            "column": column,
            "error": str(e)
        }


def analyze_trend(df: pd.DataFrame, value_column: str, date_column: str, periods: int = 7) -> Dict[str, Any]:
    """
    分析时间序列趋势

    Args:
        df: DataFrame
        value_column: 数值列名
        date_column: 日期列名
        periods: 比较周期数（天）

    Returns:
        趋势分析结果
    """
    try:
        # 确保日期列是 datetime 类型
        df[date_column] = pd.to_datetime(df[date_column])

        # 按日期排序
        df_sorted = df.sort_values(date_column)

        # 计算同比/环比增长
        df_sorted['value_lag'] = df_sorted[value_column].shift(1)
        df_sorted['growth_rate'] = (
            (df_sorted[value_column] - df_sorted['value_lag']) /
            df_sorted['value_lag'] * 100
        ).round(2)

        # 计算移动平均
        df_sorted['ma'] = df_sorted[value_column].rolling(window=periods).mean()

        # 趋势判断
        avg_growth = df_sorted['growth_rate'].mean()
        if avg_growth > 5:
            trend = "上升"
        elif avg_growth < -5:
            trend = "下降"
        else:
            trend = "稳定"

        # 检测拐点
        df_sorted['growth_change'] = df_sorted['growth_rate'].diff()
        inflection_points = df_sorted[
            df_sorted['growth_change'].abs() > df_sorted['growth_change'].std()
        ][date_column].tolist()

        return {
            "value_column": value_column,
            "date_column": date_column,
            "analysis_period": {
                "start": df_sorted[date_column].min(),
                "end": df_sorted[date_column].max()
            },
            "trend": trend,
            "average_growth_rate": float(avg_growth),
            "total_growth": float(
                ((df_sorted[value_column].iloc[-1] - df_sorted[value_column].iloc[0]) /
                 df_sorted[value_column].iloc[0]) * 100).round(2)
            ),
            "moving_average": float(df_sorted['ma'].iloc[-1]),
            "inflection_points": inflection_points,
            "recent_performance": {
                "last_period_avg": float(df_sorted[value_column].tail(periods).mean()),
                "first_period_avg": float(df_sorted[value_column].head(periods).mean()),
                "performance_change": float(
                    ((df_sorted[value_column].tail(periods).mean() -
                      df_sorted[value_column].head(periods).mean()) /
                     df_sorted[value_column].head(periods).mean()) * 100
                ).round(2)
            }
        }

    except Exception as e:
        return {
            "error": str(e)
        }


def calculate_correlation_matrix(df: pd.DataFrame, columns: List[str], method: str = "pearson") -> Dict[str, Any]:
    """
    计算相关性矩阵

    Args:
        df: DataFrame
        columns: 要分析的列名列表
        method: 相关系数计算方法（pearson/spearman/kendall）

    Returns:
        相关性矩阵
    """
    try:
        # 确保只使用数值列
        numeric_cols = [col for col in columns if pd.api.types.is_numeric_dtype(df[col])]

        if len(numeric_cols) < 2:
            return {
                "error": "需要至少 2 个数值列",
                "numeric_columns": numeric_cols
            }

        # 计算相关系数
        corr_matrix = df[numeric_cols].corr(method=method)

        # 找出强相关关系
        strong_correlations = []
        for i, col1 in enumerate(numeric_cols):
            for j, col2 in enumerate(numeric_cols):
                if i < j:  # 避免重复和自相关
                    corr_value = corr_matrix.loc[col1, col2]
                    if abs(corr_value) >= 0.7:  # 强相关阈值
                        strong_correlations.append({
                            "var1": col1,
                            "var2": col2,
                            "correlation": round(corr_value, 3),
                            "strength": "strong" if abs(corr_value) >= 0.9 else "moderate"
                        })

        return {
            "method": method,
            "matrix": corr_matrix.to_dict(),
            "strong_correlations": sorted(strong_correlations, key=lambda x: abs(x['correlation']), reverse=True)
        }

    except Exception as e:
        return {
            "error": str(e)
        }


def detect_anomalies(df: pd.DataFrame, column: str, method: str = "zscore", threshold: float = 2.0) -> Dict[str, Any]:
    """
    检测异常值

    Args:
        df: DataFrame
        column: 列名
        method: 检测方法（zscore/iqr/isolation_forest）
        threshold: 异常阈值

    Returns:
        异常检测结果
    """
    try:
        series = df[column].dropna()

        anomalies = []

        if method == "zscore":
            # 使用标准差法
            z_scores = np.abs(stats.zscore(series))
            anomaly_indices = np.where(z_scores > threshold)[0]

            for idx in anomaly_indices:
                anomalies.append({
                    "index": int(df.index[idx]),
                    "value": float(series.iloc[idx]),
                    "z_score": float(z_scores[idx]),
                    "date": str(df.index[idx]) if hasattr(df.index[idx], 'strftime') else str(df.index[idx])
                })

        elif method == "iqr":
            # 使用四分位距法
            q1 = series.quantile(0.25)
            q3 = series.quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr

            anomaly_indices = series[(series < lower_bound) | (series > upper_bound)].index

            for idx in anomaly_indices:
                anomalies.append({
                    "index": int(idx),
                    "value": float(series.loc[idx]),
                    "lower_bound": float(lower_bound),
                    "upper_bound": float(upper_bound),
                    "method": "iqr"
                })

        else:
            return {
                "error": f"不支持的异常检测方法：{method}"
            }

        return {
            "column": column,
            "method": method,
            "threshold": threshold,
            "total_anomalies": len(anomalies),
            "anomaly_rate": round(len(anomalies) / len(series) * 100, 2),
            "anomalies": anomalies
        }

    except Exception as e:
        return {
            "error": str(e)
        }


def generate_chart_spec(chart_type: str, x_column: str, y_column: str, data: pd.DataFrame, title: str = "") -> Dict[str, Any]:
    """
    生成图表配置（用于 Matplotlib 或其他可视化库）

    Args:
        chart_type: 图表类型（line, bar, scatter, histogram, box）
        x_column: X 轴列名
        y_column: Y 轴列名
        data: 数据
        title: 图表标题

    Returns:
        图表配置字典
    """
    chart_config = {
        "type": chart_type,
        "title": title or f"{y_column} vs {x_column}",
        "x": {
            "column": x_column,
            "label": x_column
        },
        "y": {
            "column": y_column,
            "label": y_column
        },
        "data_sample": {
            "count": len(data),
            "x_sample": data[x_column].head(5).tolist(),
            "y_sample": data[y_column].head(5).tolist()
        },
        "config": {
            "theme": "seaborn",
            "figsize": [12, 6],
            "dpi": 100
        }
    }

    # 根据图表类型添加特定配置
    if chart_type == "line":
        chart_config["config"]["markersize"] = 5
        chart_config["config"]["linestyle"] = "-"
    elif chart_type == "bar":
        chart_config["config"]["edgecolor"] = "black"
    elif chart_type == "scatter":
        chart_config["config"]["alpha"] = 0.6
        chart_config["config"]["s"] = 100
    elif chart_type == "histogram":
        chart_config["config"]["bins"] = 30
        chart_config["config"]["edgecolor"] = "white"
    elif chart_type == "box":
        chart_config["config"]["patch_artist"] = True

    return chart_config


if __name__ == "__main__":
    # 快速测试
    print("=== 统计分析工具测试 ===\n")

    # 创建测试数据
    test_dates = pd.date_range('2024-01-01', periods=30)
    test_values = [100 + i * 5 + np.random.randint(-10, 10) for i in range(30)]

    test_data = {
        'date': test_dates,
        'sales': test_values,
        'quantity': [int(v/10) for v in test_values]
    }
    df = pd.DataFrame(test_data)
    df.set_index('date', inplace=True)

    # 测试基本统计
    print("1. 基本统计（sales 列）：")
    stats = calculate_basic_statistics(df, 'sales')
    print(f"   均值：{stats['mean']}")
    print(f"   中位数：{stats['median']}")
    print(f"   标准差：{stats['std']}")

    # 测试趋势分析
    print("\n2. 趋势分析：")
    trend = analyze_trend(df, 'sales', 'date')
    print(f"   趋势：{trend['trend']}")
    print(f"   平均增长率：{trend['average_growth_rate']}%")

    # 测试异常检测
    print("\n3. 异常检测：")
    anomalies = detect_anomalies(df, 'sales', threshold=2.5)
    print(f"   检测到异常：{anomalies['total_anomalies']} 个")
    for anomaly in anomalies['anomalies']:
        print(f"   - {anomaly['date']}: {anomaly['value']} (z-score: {anomaly['z_score']})")

    # 测试图表配置
    print("\n4. 图表配置：")
    chart = generate_chart_spec('line', 'date', 'sales', df, "销售额趋势")
    print(f"   图表类型：{chart['type']}")
    print(f"   标题：{chart['title']}")
