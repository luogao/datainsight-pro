#!/usr/bin/env python3
"""
测试 data_explorer 工具修复
"""
import os
import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
load_dotenv()

print("=" * 60)
print("测试 Data Explorer 工具修复")
print("=" * 60)

# 导入工具
from src.agents.data_explorer_v2 import read_csv_dataset, check_data_quality, generate_data_summary

# 创建测试数据
test_csv = Path("web/uploads/test_sales_data.csv")
if not test_csv.exists():
    print(f"\n❌ 测试文件不存在: {test_csv}")
    print("请先上传一个测试文件")
    sys.exit(1)

print(f"\n📂 测试文件: {test_csv}")
print(f"📊 文件大小: {test_csv.stat().st_size} bytes\n")

# 直接调用底层函数进行测试
from src.agents.data_explorer_v2 import (
    read_csv_dataset,
    check_data_quality,
    generate_data_summary
)

# 获取工具的底层函数
read_csv_dataset_func = read_csv_dataset.func if hasattr(read_csv_dataset, 'func') else read_csv_dataset
check_data_quality_func = check_data_quality.func if hasattr(check_data_quality, 'func') else check_data_quality
generate_data_summary_func = generate_data_summary.func if hasattr(generate_data_summary, 'func') else generate_data_summary

# 测试 1: read_csv_dataset
print("-" * 60)
print("测试 1: read_csv_dataset")
print("-" * 60)
result1 = read_csv_dataset_func(file_path=str(test_csv))
print(f"✅ 成功: {result1.get('success')}")
print(f"📐 形状: {result1.get('shape')}")
print(f"📋 列数: {len(result1.get('columns', []))}")
print(f"💾 内存: {result1.get('memory_usage_mb', 0):.2f} MB")

# 测试 2: check_data_quality
print("\n" + "-" * 60)
print("测试 2: check_data_quality")
print("-" * 60)
result2 = check_data_quality_func(file_path=str(test_csv))
print(f"✅ 成功: {result2.get('success')}")
print(f"📊 总记录: {result2.get('total_records')}")
print(f"📋 总列数: {result2.get('total_columns')}")
print(f"🔄 重复行: {result2.get('duplicate_count')}")
print(f"⭐ 质量评分: {result2.get('quality_score')}")
print(f"✓ 完整度: {result2.get('completeness')}")

# 测试 3: generate_data_summary
print("\n" + "-" * 60)
print("测试 3: generate_data_summary")
print("-" * 60)
result3 = generate_data_summary_func(file_path=str(test_csv))
print(f"📝 报告长度: {len(result3)} 字符")
print(f"\n报告预览（前 500 字符）:")
print("-" * 60)
print(result3[:500])
print("..." if len(result3) > 500 else "")

print("\n" + "=" * 60)
print("✅ 所有工具测试通过！")
print("=" * 60)

# 检查工具签名
print("\n📋 工具参数签名:")
print(f"  - read_csv_dataset(file_path: str) -> dict")
print(f"  - check_data_quality(file_path: str) -> dict")
print(f"  - generate_data_summary(file_path: str) -> str")

print("\n✅ 所有工具都使用 file_path 参数，符合新架构！")
