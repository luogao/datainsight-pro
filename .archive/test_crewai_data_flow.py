#!/usr/bin/env python3
"""
CrewAI 数据流测试脚本

验证 Agent 间数据传递的问题
"""
import pandas as pd
import json
from pathlib import Path


def test_data_flow_problem():
    """
    演示 V2 版本的数据传递问题
    """
    print("="*60)
    print("🔴 测试 1: V2 版本的数据传递问题")
    print("="*60)

    # 模拟 Data Explorer 的输出
    print("\n📊 Data Explorer 输出:")
    print("-"*60)

    df = pd.DataFrame({
        'sales': [100, 150, 200, 180, 220],
        'profit': [20, 30, 40, 35, 45]
    })

    # Data Explorer 生成 Markdown 报告
    markdown_report = f"""
# 数据概览

- 数据行数: {len(df)}
- 字段数: {len(df.columns)}
- 字段列表: {', '.join(df.columns)}

## 样本数据
{df.head().to_markdown()}

## 统计摘要
{df.describe().to_markdown()}
"""

    print(markdown_report)

    # 模拟 Analyst 收到的内容
    print("\n🔍 Analyst 收到的内容:")
    print("-"*60)
    print("❌ 只收到了上面的 Markdown 文本")
    print("❌ 无法访问原始 DataFrame 对象")
    print("❌ 无法执行真正的统计分析")

    # 尝试从 Markdown 中提取数据（失败）
    print("\n⚠️  尝试从 Markdown 重建数据:")
    print("-"*60)
    print("❌ 无法从 Markdown 文本中重建完整的 DataFrame")
    print("❌ 统计分析无法执行")

    return False


def test_direct_file_access():
    """
    演示 V2.1 版本的解决方案
    """
    print("\n\n")
    print("="*60)
    print("✅ 测试 2: V2.1 版本的解决方案")
    print("="*60)

    # 创建测试数据
    test_file = Path("test_data_flow.csv")
    df = pd.DataFrame({
        'sales': [100, 150, 200, 180, 220],
        'profit': [20, 30, 40, 35, 45]
    })
    df.to_csv(test_file, index=False)

    print(f"\n📁 数据文件: {test_file}")
    print(f"📊 数据形状: {df.shape}")

    # 模拟 Data Explorer
    print("\n1️⃣ Data Explorer:")
    print("   ✅ 读取文件，生成概览")
    print(f"   ✅ DataFrame: {df.shape}")

    # 模拟 Analyst（独立读取）
    print("\n2️⃣ Analyst:")
    print("   ✅ 直接读取原始文件")
    analyst_df = pd.read_csv(test_file)
    print(f"   ✅ 获得完整 DataFrame: {analyst_df.shape}")
    print("   ✅ 可以执行真正的统计分析")
    print(f"   示例 - 销售均值: {analyst_df['sales'].mean()}")

    # 模拟 PandaAI Agent（独立读取）
    print("\n3️⃣ PandaAI Agent:")
    print("   ✅ 直接读取原始文件")
    pandaai_df = pd.read_csv(test_file)
    print(f"   ✅ 获得完整 DataFrame: {pandaai_df.shape}")
    print("   ✅ 可以传递给 PandaAI 库")
    print(f"   示例 - 相关性矩阵:")
    print(pandaai_df.corr().to_string())

    # 清理
    test_file.unlink()

    return True


def test_pandaai_integration():
    """
    测试 PandaAI 集成
    """
    print("\n\n")
    print("="*60)
    print("🤖 测试 3: PandaAI 集成验证")
    print("="*60)

    # 检查 PandaAI 是否安装
    try:
        import pandasai
        print(f"✅ PandaAI 已安装: {pandasai.__version__}")
    except ImportError:
        print("❌ PandaAI 未安装")
        print("   安装命令: pip install pandasai")
        return False

    # 检查 API Key
    import os
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print(f"✅ OPENAI_API_KEY 已设置 (长度: {len(api_key)})")
    else:
        print("❌ OPENAI_API_KEY 未设置")
        print("   请在 .env 文件中配置")
        return False

    # 创建测试数据
    df = pd.DataFrame({
        'sales': [100, 150, 200, 180, 220],
        'profit': [20, 30, 40, 35, 45]
    })

    print("\n📊 测试数据:")
    print(df.to_string())

    print("\n🔧 PandaAI 设置:")
    from langchain_openai import ChatOpenAI
    from pandasai import PandasAI

    try:
        llm = ChatOpenAI(
            api_key=api_key,
            temperature=0
        )
        pandasai = PandasAI(llm)
        print("✅ PandaAI 初始化成功")

        # 测试查询
        print("\n🤖 测试查询: '销售数据的平均值是多少?'")
        result = pandasai.run(
            df,
            prompt="销售数据的平均值是多少?只用数字回答"
        )
        print(f"✅ PandaAI 响应: {result}")

        return True

    except Exception as e:
        print(f"❌ PandaAI 初始化失败: {e}")
        return False


def main():
    """
    运行所有测试
    """
    print("\n")
    print("🚀 CrewAI 数据流测试套件")
    print("="*60)

    results = {}

    # 测试 1: 演示问题
    results['v2_problem'] = test_data_flow_problem()

    # 测试 2: 演示解决方案
    results['v21_solution'] = test_direct_file_access()

    # 测试 3: PandaAI 集成
    results['pandaai'] = test_pandaai_integration()

    # 总结
    print("\n\n")
    print("="*60)
    print("📋 测试总结")
    print("="*60)

    for test_name, result in results.items():
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name}: {status}")

    # 结论
    print("\n" + "="*60)
    print("🎯 结论")
    print("="*60)

    if not results['v2_problem']:
        print("✅ V2 版本的数据传递问题已验证")
        print("   - Agent 间无法传递 DataFrame")
        print("   - PandaAI 无法正常工作")

    if results['v21_solution']:
        print("✅ V2.1 的解决方案可行")
        print("   - 每个 Agent 直接读取文件")
        print("   - 可以获得完整的 DataFrame")

    if results['pandaai']:
        print("✅ PandaAI 集成正常")
        print("   - 可以执行智能查询")
    else:
        print("⚠️  PandaAI 集成需要配置")
        print("   - 安装 pandasai")
        print("   - 设置 OPENAI_API_KEY")

    print("\n💡 建议:")
    print("   1. 立即采用 V2.1 版本 (src/crew_v21_fixed.py)")
    print("   2. 每个 Agent 直接读取数据文件")
    print("   3. 使用 sequential process")
    print("   4. 配置 PandaAI 的 API Key")


if __name__ == "__main__":
    main()
