#!/usr/bin/env python3
"""
直接测试 - 使用真实的 LLM API
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

print("="*70)
print("🚀 DataInsight Pro - 真实 LLM 测试")
print("="*70)

# 检查环境
print("\n📋 环境配置:")
print(f"   API Key: {'✅ 已设置' if os.getenv('OPENAI_API_KEY') else '❌ 未设置'}")
print(f"   Base URL: {os.getenv('OPENAI_BASE_URL', '默认')}")
print(f"   Model: {os.getenv('OPENAI_MODEL', 'gpt-4')}")

# 检查数据
dataset_path = "data/samples/sales_2024_Q1.csv"
if not Path(dataset_path).exists():
    print(f"\n❌ 数据不存在: {dataset_path}")
    sys.exit(1)

print(f"\n📊 数据集: {dataset_path}")
import pandas as pd
df = pd.read_csv(dataset_path)
print(f"   规模: {df.shape}")
print(f"   列: {list(df.columns)}")

# 测试导入
print("\n🔍 测试导入...")
try:
    from src.crew_v2 import create_crew
    print("   ✅ 导入成功")
except Exception as e:
    print(f"   ❌ 导入失败: {e}")
    sys.exit(1)

# 创建 Crew
print("\n🤖 创建 Crew...")
try:
    crew = create_crew()
    print(f"   ✅ Crew 创建成功")
    print(f"   - {len(crew.agents)} 个 Agents")
    for i, agent in enumerate(crew.agents, 1):
        print(f"     {i}. {agent.role}")
    print(f"   - {len(crew.tasks)} 个 Tasks")
except Exception as e:
    print(f"   ❌ Crew 创建失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 执行分析
print("\n⚙️  开始执行分析...")
print("   (这可能需要几分钟，请耐心等待)")
print("-"*70)

try:
    import time
    start_time = time.time()

    result = crew.kickoff(inputs={
        'goal': '分析2024年Q1销售数据，提供洞察和建议',
        'dataset_path': dataset_path,
        'analysis_depth': 'standard',
        'depth': 'standard',
        'output_path': 'llm_test_report.md',
        'output_format': 'markdown'
    })

    elapsed_time = time.time() - start_time

    print("-"*70)
    print(f"\n✅ 分析完成！")
    print(f"   执行时间: {elapsed_time:.1f} 秒")

    # 检查输出文件
    output_files = [
        "data_exploration_result.md",
        "statistical_analysis_result.md",
        "pandaai_analysis_result.md",
        "llm_test_report.md"
    ]

    print(f"\n📁 输出文件:")
    for filename in output_files:
        if Path(filename).exists():
            size = Path(filename).stat().st_size
            lines = len(Path(filename).read_text().split('\n'))
            print(f"   ✅ {filename}: {size} bytes, {lines} 行")
        else:
            print(f"   ❌ {filename}: 未生成")

    print("\n🎉 测试成功！")

except Exception as e:
    print(f"\n❌ 分析失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
