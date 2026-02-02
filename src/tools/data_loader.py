"""
数据加载和处理工具
"""
import os
import pandas as pd
import json
from pathlib import Path
from typing import Union, Dict, Any


def load_dataset(file_path: str, format: str = "auto") -> pd.DataFrame:
    """
    加载数据集（支持多种格式）

    Args:
        file_path: 文件路径
        format: 文件格式（csv/json/xlsx/auto）

    Returns:
        pandas DataFrame
    """
    path = Path(file_path)

    if format == "auto":
        format = path.suffix.lower().lstrip('.')

    try:
        if format == "csv":
            df = pd.read_csv(file_path)
        elif format == "json":
            df = pd.read_json(file_path)
        elif format in ["xlsx", "xls"]:
            df = pd.read_excel(file_path)
        else:
            raise ValueError(f"不支持的文件格式：{format}")

        print(f"✅ 成功加载数据：{len(df)} 行 × {len(df.columns)} 列")
        return df

    except Exception as e:
        print(f"❌ 加载数据失败：{str(e)}")
        raise


def get_data_info(df: pd.DataFrame) -> Dict[str, Any]:
    """
    获取数据集基本信息

    Args:
        df: pandas DataFrame

    Returns:
        数据信息字典
    """
    return {
        "shape": df.shape,
        "columns": list(df.columns),
        "dtypes": df.dtypes.to_dict(),
        "memory_mb": df.memory_usage(deep=True).sum() / 1024 / 1024,
        "is_empty": df.empty,
        "sample": df.head().to_dict(orient='records')
    }


def check_data_quality(df: pd.DataFrame) -> Dict[str, Any]:
    """
    检查数据质量

    Args:
        df: pandas DataFrame

    Returns:
        数据质量报告
    """
    # 缺失值
    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100).round(2)

    # 重复值
    duplicates = df.duplicated().sum()

    # 数据类型检查
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    datetime_cols = df.select_dtypes(include=['datetime64']).columns.tolist()

    return {
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "missing_values": {
            "count": missing.to_dict(),
            "percentage": missing_pct.to_dict()
        },
        "duplicates": duplicates,
        "duplicate_rate": round(duplicates / len(df) * 100, 2) if len(df) > 0 else 0,
        "numeric_columns": numeric_cols,
        "categorical_columns": categorical_cols,
        "datetime_columns": datetime_cols,
        "quality_score": _calculate_quality_score(missing, duplicates, len(df))
    }


def _calculate_quality_score(missing: pd.Series, duplicates: int, total_rows: int) -> str:
    """
    计算数据质量分数（A/B/C/D/E）

    Args:
        missing: 缺失值统计
        duplicates: 重复值数量
        total_rows: 总行数

    Returns:
        质量等级
    """
    if total_rows == 0:
        return "E"

    missing_rate = missing.sum() / total_rows
    duplicate_rate = duplicates / total_rows

    score = 100 - (missing_rate * 50 + duplicate_rate * 30)

    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 60:
        return "C"
    elif score >= 40:
        return "D"
    else:
        return "E"


def clean_dataset(df: pd.DataFrame, strategy: str = "simple") -> pd.DataFrame:
    """
    清理数据集

    Args:
        df: 原始 DataFrame
        strategy: 清理策略（simple/medium/aggressive）

    Returns:
        清理后的 DataFrame
    """
    df_clean = df.copy()

    if strategy == "simple":
        # 删除完全为空的行
        df_clean = df_clean.dropna(how='all')
    elif strategy == "medium":
        # 删除完全为空的行和列
        df_clean = df_clean.dropna(how='all')
        df_clean = df_clean.dropna(axis=1, how='all')
    elif strategy == "aggressive":
        # 删除所有包含缺失值的行
        df_clean = df_clean.dropna()

    print(f"✅ 数据清理完成：{strategy} 策略")
    print(f"   原始：{df.shape}")
    print(f"   清理后：{df_clean.shape}")

    return df_clean


def sample_dataset(df: pd.DataFrame, size: int = 10, random_state: int = 42) -> pd.DataFrame:
    """
    采样数据集

    Args:
        df: 原始 DataFrame
        size: 采样大小
        random_state: 随机种子

    Returns:
        采样后的 DataFrame
    """
    if len(df) <= size:
        return df.copy()

    return df.sample(n=size, random_state=random_state)


if __name__ == "__main__":
    # 快速测试
    print("=== 数据工具测试 ===\n")

    # 创建测试数据
    test_data = {
        'date': pd.date_range('2024-01-01', periods=10),
        'sales': [100, 150, 200, 180, 220, 250, 300, 280, 320],
        'product': ['A', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A', 'C']
    }
    df = pd.DataFrame(test_data)

    # 测试
    print("1. 数据信息：")
    info = get_data_info(df)
    print(f"   行数：{info['shape'][0]}, 列数：{info['shape'][1]}")
    print(f"   列名：{info['columns']}")

    print("\n2. 数据质量：")
    quality = check_data_quality(df)
    print(f"   质量分数：{quality['quality_score']}")
    print(f"   重复值：{quality['duplicates']}")

    print("\n3. 数据采样：")
    sample = sample_dataset(df, size=5)
    print(sample)
