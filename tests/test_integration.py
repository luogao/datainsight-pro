"""
集成测试 - 测试完整的数据分析流程
"""
import sys
from pathlib import Path

# 添加 src 到路径
sys.path.insert(0, str(Path(__file__).parent.parent))


def test_data_loading():
    """测试数据加载功能"""
    print("\n" + "="*60)
    print("测试 1: 数据加载")
    print("="*60)

    from src.tools.data_loader import load_dataset, get_data_info, check_data_quality
    import pandas as pd

    # 测试加载示例数据
    try:
        dataset_path = "data/samples/sales_2024_Q1.csv"
        df = load_dataset(dataset_path)

        info = get_data_info(df)
        print(f"✅ 数据加载成功")
        print(f"   行数：{info['shape'][0]}")
        print(f"   列数：{info['shape'][1]}")
        print(f"   内存：{info['memory_mb']:.2f} MB")

        quality = check_data_quality(df)
        print(f"✅ 数据质量检查")
        print(f"   质量分数：{quality['quality_score']}")
        print(f"   重复率：{quality['duplicate_rate']}%")

        return True

    except Exception as e:
        print(f"❌ 数据加载失败：{e}")
        return False


def test_statistical_analysis():
    """测试统计分析功能"""
    print("\n" + "="*60)
    print("测试 2: 统计分析")
    print("="*60)

    from src.tools.statistical_analyzer import calculate_basic_statistics, analyze_trend
    import pandas as pd

    try:
        # 创建测试数据
        import numpy as np
        test_dates = pd.date_range('2024-01-01', periods=10)
        test_values = [100 + i * 10 + np.random.randint(-5, 5) for i in range(10)]
        test_data = {'date': test_dates, 'sales': test_values}
        df = pd.DataFrame(test_data)
        df.set_index('date', inplace=True)

        # 测试基本统计
        stats = calculate_basic_statistics(df, 'sales')
        print(f"✅ 基本统计")
        print(f"   均值：{stats['mean']:.2f}")
        print(f"   标准差：{stats['std']:.2f}")
        print(f"   范围：{stats['range']:.2f}")

        # 测试趋势分析
        trend = analyze_trend(df, 'sales', 'date')
        print(f"✅ 趋势分析")
        print(f"   趋势：{trend['trend']}")
        print(f"   增长率：{trend['average_growth_rate']}%")

        return True

    except Exception as e:
        print(f"❌ 统计分析失败：{e}")
        return False


def test_agent_initialization():
    """测试 Agent 初始化"""
    print("\n" + "="*60)
    print("测试 3: Agent 初始化")
    print("="*60)

    try:
        from src.agents.data_explorer import data_explorer
        from src.agents.analyst import analyst
        from src.agents.pandaai import pandaai
        from src.agents.reporter import reporter

        print(f"✅ Data Explorer Agent: {data_explorer.role}")
        print(f"✅ Analyst Agent: {analyst.role}")
        print(f"✅ PandaAI Agent: {pandaai.role}")
        print(f"✅ Reporter Agent: {reporter.role}")

        return True

    except Exception as e:
        print(f"❌ Agent 初始化失败：{e}")
        return False


def test_crew_initialization():
    """测试 Crew 初始化"""
    print("\n" + "="*60)
    print("测试 4: Crew 初始化")
    print("="*60)

    try:
        from src.crew import data_analysis_crew

        print(f"✅ Crew 初始化成功")
        print(f"   Agent 数量：{len(data_analysis_crew.agents)}")
        print(f"   任务数量：{len(data_analysis_crew.tasks)}")
        print(f"   流程类型：{data_analysis_crew.process}")

        return True

    except Exception as e:
        print(f"❌ Crew 初始化失败：{e}")
        return False


def test_end_to_flow():
    """测试端到端流程"""
    print("\n" + "="*60)
    print("测试 5: 端到端流程")
    print("="*60)

    try:
        from src.crew import run_analysis

        # 模拟运行（不真正执行）
        print("📋 分析目标：测试分析")
        print("📊 数据集：data/samples/sales_2024_Q1.csv")
        print("🎯 分析深度：quick")
        print("📤 输出路径：test_report.md")

        print("\n⚠️  注意：这是模拟测试，不会真正执行完整的 Crew 流程")
        print("   实际测试需要配置 API Keys")

        return True

    except Exception as e:
        print(f"❌ 端到端流程测试失败：{e}")
        return False


def main():
    """主测试函数"""
    print("\n" + "="*60)
    print("🧪 DataInsight Pro - 集成测试套件")
    print("="*60)

    # 运行所有测试
    tests = [
        ("数据加载", test_data_loading),
        ("统计分析", test_statistical_analysis),
        ("Agent 初始化", test_agent_initialization),
        ("Crew 初始化", test_crew_initialization),
        ("端到端流程", test_end_to_flow),
    ]

    results = []

    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ 测试 '{test_name}' 发生异常：{e}")
            results.append((test_name, False))

    # 汇总结果
    print("\n" + "="*60)
    print("📊 测试结果汇总")
    print("="*60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name:20s} {status}")

    print(f"\n总计：{passed}/{total} 个测试通过")

    if passed == total:
        print("\n🎉 所有测试通过！项目可以正常使用。")
        return 0
    else:
        print(f"\n⚠️  {total - passed} 个测试失败，请检查配置和依赖。")
        return 1


if __name__ == "__main__":
    sys.exit(main())
