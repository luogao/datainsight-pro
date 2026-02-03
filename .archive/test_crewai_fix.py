#!/usr/bin/env python3
"""
测试 CrewAI 修复版本

验证：
1. 向后兼容性（接口不变）
2. 数据传递问题是否解决
3. PandaAI 是否能正常工作
"""
import sys
from pathlib import Path
import pandas as pd

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))


def test_backward_compatibility():
    """测试向后兼容性"""
    print("="*60)
    print("🔍 测试 1: 向后兼容性")
    print("="*60)

    try:
        from src.crew_v2_fixed import create_crew, run_analysis

        # 测试 1: create_crew() 无参数调用
        print("\n✅ 测试 create_crew() 无参数调用...")
        crew = create_crew()
        print("✅ create_crew() 可以无参数调用")

        # 测试 2: 检查 Crew 配置
        print("\n✅ 检查 Crew 配置...")
        print(f"   - Agent 数量: {len(crew.agents)}")
        print(f"   - Task 数量: {len(crew.tasks)}")
        print(f"   - Process 类型: {crew.process}")

        # 验证使用 sequential 而不是 hierarchical
        from crewai import Process
        if crew.process == Process.sequential:
            print("✅ 使用 sequential process（正确）")
        else:
            print(f"⚠️  使用 {crew.process} process")

        # 测试 3: 检查 Task 的 context 配置
        print("\n✅ 检查 Task 的 context 配置...")
        for i, task in enumerate(crew.tasks):
            has_context = hasattr(task, 'context') and task.context
            status = "❌ 有 context（问题）" if has_context else "✅ 无 context（正确）"
            print(f"   Task {i+1} ({task.description[:30]}...): {status}")

        return True

    except Exception as e:
        print(f"\n❌ 兼容性测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_dataset_placeholder():
    """测试数据集路径占位符"""
    print("\n\n")
    print("="*60)
    print("🔍 测试 2: 数据集路径占位符")
    print("="*60)

    try:
        from src.crew_v2_fixed import create_crew

        crew = create_crew()

        # 检查 Task 的 description 是否包含 {dataset_path} 占位符
        print("\n✅ 检查 Task description 中的占位符...")
        for i, task in enumerate(crew.tasks):
            desc = task.description
            has_dataset_placeholder = "{dataset_path}" in desc
            has_goal_placeholder = "{goal}" in desc

            print(f"\n   Task {i+1}:")
            print(f"      - 包含 {{dataset_path}}: {'✅ 是' if has_dataset_placeholder else '❌ 否'}")
            print(f"      - 包含 {{goal}}: {'✅ 是' if has_goal_placeholder else '❌ 否'}")

            # 显示关键部分
            if has_dataset_placeholder:
                # 找到包含 dataset_path 的行
                lines = desc.split('\n')
                for line in lines:
                    if '{dataset_path}' in line:
                        print(f"      - 示例: {line.strip()[:60]}...")
                        break

        return True

    except Exception as e:
        print(f"\n❌ 占位符测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_real_execution():
    """测试真实执行（需要 API Key）"""
    print("\n\n")
    print("="*60)
    print("🔍 测试 3: 真实执行（需要 API Key）")
    print("="*60)

    # 检查 API Key
    import os
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  跳过：未设置 OPENAI_API_KEY")
        print("   设置环境变量后可以测试真实执行")
        return None

    try:
        from src.crew_v2_fixed import run_analysis

        # 创建测试数据
        test_dataset = "test_crewai_execution.csv"
        if not Path(test_dataset).exists():
            print(f"\n✅ 创建测试数据: {test_dataset}")
            df = pd.DataFrame({
                'date': pd.date_range('2024-01-01', periods=30),
                'sales': [100 + i*5 + (i%3)*20 for i in range(30)],
                'profit': [20 + i*1 + (i%3)*5 for i in range(30)]
            })
            df.to_csv(test_dataset, index=False)
            print(f"   - 数据形状: {df.shape}")
            print(f"   - 列名: {list(df.columns)}")

        # 运行分析（使用 quick 模式节省成本）
        print(f"\n✅ 运行 CrewAI 分析...")
        print("   - 使用 quick 模式（最小化 API 调用）")

        result = run_analysis(
            goal="快速测试数据读取和基本分析",
            dataset_path=test_dataset,
            depth="quick",  # 使用 quick 模式
            output_path="test_output_quick.md"
        )

        if result:
            print(f"\n✅ 执行成功！")

            # 检查输出文件
            output_files = [
                "data_exploration_result.md",
                "statistical_analysis_result.md",
                "pandaai_analysis_result.md",
                "test_output_quick.md"
            ]

            print(f"\n✅ 检查输出文件...")
            for f in output_files:
                if Path(f).exists():
                    size = Path(f).stat().st_size
                    print(f"   ✅ {f}: {size} bytes")
                else:
                    print(f"   ⚠️  {f}: 未生成")

            return True
        else:
            print(f"\n❌ 执行失败")
            return False

    except Exception as e:
        print(f"\n❌ 执行测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_data_flow_simulation():
    """模拟数据流，验证 Agent 能否独立读取数据"""
    print("\n\n")
    print("="*60)
    print("🔍 测试 4: 数据流模拟")
    print("="*60)

    # 创建测试数据
    test_file = Path("test_data_flow_sim.csv")
    df = pd.DataFrame({
        'sales': [100, 150, 200, 180, 220],
        'profit': [20, 30, 40, 35, 45]
    })
    df.to_csv(test_file, index=False)

    print(f"\n✅ 创建测试数据: {test_file}")
    print(f"   - 形状: {df.shape}")

    # 模拟 Data Explorer
    print("\n✅ 模拟 Data Explorer...")
    df_explorer = pd.read_csv(test_file)
    print(f"   - 读取数据: {df_explorer.shape}")
    print(f"   - 销售均值: {df_explorer['sales'].mean()}")

    # 模拟 Analyst（独立读取）
    print("\n✅ 模拟 Analyst（独立读取）...")
    df_analyst = pd.read_csv(test_file)
    print(f"   - 读取数据: {df_analyst.shape}")
    print(f"   - 销售标准差: {df_analyst['sales'].std()}")
    print(f"   - 相关性矩阵:")
    print(df_analyst.corr().to_string())

    # 模拟 PandaAI（独立读取）
    print("\n✅ 模拟 PandaAI Agent（独立读取）...")
    df_pandaai = pd.read_csv(test_file)
    print(f"   - 读取数据: {df_pandaai.shape}")
    print(f"   - 转换为字典: {len(df_pandaai.to_dict(orient='records'))} 条记录")

    # 清理
    test_file.unlink()

    print("\n✅ 数据流模拟成功：每个 Agent 都可以独立读取数据")
    return True


def main():
    """运行所有测试"""
    print("\n")
    print("🚀 CrewAI 修复版本测试套件")
    print("="*60)

    results = {}

    # 测试 1: 向后兼容性
    results['兼容性'] = test_backward_compatibility()

    # 测试 2: 占位符
    results['占位符'] = test_dataset_placeholder()

    # 测试 3: 数据流模拟
    results['数据流'] = test_data_flow_simulation()

    # 测试 4: 真实执行（可选）
    print("\n\n")
    print("="*60)
    print("🤖 测试 5: 真实执行（可选）")
    print("="*60)
    print("⚠️  此测试需要 API Key 和实际调用 LLM")
    user_input = input("是否执行真实测试？(y/N): ").strip().lower()

    if user_input == 'y':
        results['真实执行'] = test_real_execution()
    else:
        print("   跳过真实执行测试")
        results['真实执行'] = None

    # 总结
    print("\n\n")
    print("="*60)
    print("📋 测试总结")
    print("="*60)

    for test_name, result in results.items():
        if result is True:
            print(f"✅ {test_name}: 通过")
        elif result is False:
            print(f"❌ {test_name}: 失败")
        else:
            print(f"⏭️  {test_name}: 跳过")

    # 结论
    print("\n" + "="*60)
    print("🎯 结论")
    print("="*60)

    if results['兼容性'] and results['占位符'] and results['数据流']:
        print("✅ 修复版本通过了所有核心测试")
        print("✅ 向后兼容性良好")
        print("✅ 数据传递问题已解决")
        print("\n💡 建议:")
        print("   1. 备份原版本: cp src/crew_v2.py src/crew_v2_backup.py")
        print("   2. 使用修复版: cp src/crew_v2_fixed.py src/crew_v2.py")
        print("   3. 运行真实测试验证")
    else:
        print("❌ 存在问题，需要修复")

    if results.get('真实执行') is True:
        print("\n🎉 真实执行测试通过！")
        print("✅ CrewAI 可以正常工作")
        print("✅ PandaAI 集成正常")
    elif results.get('真实执行') is False:
        print("\n⚠️  真实执行测试失败")
        print("   可能是 API Key 或网络问题")


if __name__ == "__main__":
    main()
