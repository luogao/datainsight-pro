#!/usr/bin/env python3
"""
完整流程测试 - DataInsight Pro 分析能力测试

测试修复后的 CrewAI 系统是否能真正执行数据分析
"""
import os
import sys
from pathlib import Path
import time
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))


def check_environment():
    """检查环境配置"""
    print("\n" + "="*60)
    print("🔍 步骤 1: 环境检查")
    print("="*60)

    checks = []

    # 检查 API Key
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print(f"✅ OPENAI_API_KEY: 已设置 (长度: {len(api_key)})")
        checks.append(True)
    else:
        print("❌ OPENAI_API_KEY: 未设置")
        checks.append(False)

    # 检查 API Base URL
    base_url = os.getenv("OPENAI_BASE_URL")
    if base_url:
        print(f"✅ OPENAI_BASE_URL: {base_url}")
    else:
        print("ℹ️  OPENAI_BASE_URL: 使用默认")

    # 检查模型
    model = os.getenv("OPENAI_MODEL", "gpt-4")
    print(f"ℹ️  OPENAI_MODEL: {model}")

    # 检查依赖
    print("\n检查依赖包:")
    try:
        import crewai
        print(f"✅ crewai: {crewai.__version__}")
        checks.append(True)
    except ImportError as e:
        print(f"❌ crewai: {e}")
        checks.append(False)

    try:
        import pandasai
        print(f"✅ pandasai: {pandasai.__version__}")
        checks.append(True)
    except ImportError as e:
        print(f"⚠️  pandasai: {e}")
        checks.append(False)

    try:
        import pandas as pd
        print(f"✅ pandas: {pd.__version__}")
        checks.append(True)
    except ImportError as e:
        print(f"❌ pandas: {e}")
        checks.append(False)

    return all(checks)


def check_dataset():
    """检查测试数据"""
    print("\n" + "="*60)
    print("🔍 步骤 2: 数据检查")
    print("="*60)

    dataset_path = "data/samples/sales_2024_Q1.csv"

    if not Path(dataset_path).exists():
        print(f"❌ 数据集不存在: {dataset_path}")
        return False, None

    print(f"✅ 数据集存在: {dataset_path}")

    # 读取并显示数据信息
    import pandas as pd
    df = pd.read_csv(dataset_path)

    print(f"\n📊 数据集信息:")
    print(f"   - 形状: {df.shape}")
    print(f"   - 列名: {list(df.columns)}")
    print(f"   - 数据类型:\n{df.dtypes.to_string()}")

    print(f"\n📈 统计摘要:")
    print(df.describe().to_string())

    print(f"\n🔍 样本数据 (前 5 行):")
    print(df.head().to_string())

    return True, dataset_path


def run_crewai_test(dataset_path):
    """运行 CrewAI 分析测试"""
    print("\n" + "="*60)
    print("🚀 步骤 3: 运行 CrewAI 分析")
    print("="*60)

    from src.crew_v2 import create_crew

    print("\n创建 Crew...")
    crew = create_crew()

    print(f"✅ Crew 创建成功")
    print(f"   - Agent 数量: {len(crew.agents)}")
    print(f"   - Task 数量: {len(crew.tasks)}")

    # 显示 Agent 信息
    print(f"\n🤖 Agent 列表:")
    for i, agent in enumerate(crew.agents, 1):
        print(f"   {i}. {agent.role}")

    # 显示 Task 信息
    print(f"\n📋 Task 列表:")
    for i, task in enumerate(crew.tasks, 1):
        desc_preview = task.description.split('\n')[0][:50]
        print(f"   {i}. {desc_preview}...")

    return crew


def execute_analysis(crew, dataset_path):
    """执行分析"""
    print("\n" + "="*60)
    print("⚙️  步骤 4: 执行分析")
    print("="*60)

    print("\n开始分析...")
    print("这可能需要几分钟时间，请耐心等待...")
    print("每个 Agent 会依次执行:")
    print("  1️⃣  Data Explorer - 数据探索")
    print("  2️⃣  Analyst - 统计分析")
    print("  3️⃣  PandaAI - AI 洞察")
    print("  4️⃣  Reporter - 生成报告")

    start_time = time.time()

    try:
        result = crew.kickoff(inputs={
            'goal': '分析2024年Q1销售数据的趋势、模式和异常，提供可执行的商业洞察',
            'dataset_path': dataset_path,
            'analysis_depth': 'standard',
            'depth': 'standard',
            'output_path': 'final_analysis_report.md',
            'output_format': 'markdown'
        })

        elapsed_time = time.time() - start_time

        print(f"\n✅ 分析完成！")
        print(f"   - 执行时间: {elapsed_time:.1f} 秒")

        return result, elapsed_time

    except Exception as e:
        print(f"\n❌ 分析失败: {e}")
        import traceback
        traceback.print_exc()
        return None, None


def check_outputs():
    """检查输出文件"""
    print("\n" + "="*60)
    print("📁 步骤 5: 检查输出文件")
    print("="*60)

    output_files = [
        "data_exploration_result.md",
        "statistical_analysis_result.md",
        "pandaai_analysis_result.md",
        "final_analysis_report.md"
    ]

    results = {}

    for filename in output_files:
        if Path(filename).exists():
            size = Path(filename).stat().st_size
            lines = len(Path(filename).read_text().split('\n'))

            status = "✅" if size > 100 else "⚠️ "
            print(f"{status} {filename}: {size} bytes, {lines} 行")

            results[filename] = {
                'exists': True,
                'size': size,
                'lines': lines
            }

            # 显示预览
            if size > 0:
                content = Path(filename).read_text()
                preview = content[:300].replace('\n', ' ')
                print(f"      预览: {preview}...")

        else:
            print(f"❌ {filename}: 未生成")
            results[filename] = {'exists': False}

    return results


def display_report_summary():
    """显示报告摘要"""
    print("\n" + "="*60)
    print("📊 步骤 6: 报告摘要")
    print("="*60)

    report_file = "final_analysis_report.md"

    if not Path(report_file).exists():
        print(f"❌ 最终报告不存在: {report_file}")
        return

    content = Path(report_file).read_text()

    # 提取关键部分
    lines = content.split('\n')

    print("\n📄 报告结构:")

    sections = []
    for line in lines:
        if line.startswith('#'):
            level = len(line) - len(line.lstrip('#'))
            title = line.lstrip('#').strip()
            sections.append((level, title))

    for level, title in sections[:20]:  # 只显示前20个标题
        indent = "  " * (level - 1)
        print(f"{indent}{'#' * level} {title}")

    print(f"\n✅ 报告总行数: {len(lines)}")
    print(f"✅ 报告大小: {len(content)} 字符")


def evaluate_results():
    """评估结果"""
    print("\n" + "="*60)
    print("🎯 步骤 7: 结果评估")
    print("="*60)

    # 评估标准
    criteria = {
        "Data Explorer": "data_exploration_result.md",
        "Analyst": "statistical_analysis_result.md",
        "PandaAI": "pandaai_analysis_result.md",
        "Reporter": "final_analysis_report.md"
    }

    results = {}

    for agent, filename in criteria.items():
        if Path(filename).exists():
            content = Path(filename).read_text()
            size = len(content)

            # 检查内容质量
            has_data = "数据" in content or "data" in content.lower()
            has_insights = "分析" in content or "analysis" in content.lower()
            has_numbers = any(c.isdigit() for c in content)

            score = 0
            if size > 500: score += 25
            if has_data: score += 25
            if has_insights: score += 25
            if has_numbers: score += 25

            results[agent] = score

            status = "✅" if score >= 75 else "⚠️ " if score >= 50 else "❌"
            print(f"{status} {agent}: {score}/100")

        else:
            results[agent] = 0
            print(f"❌ {agent}: 0/100 (文件未生成)")

    # 计算总分
    total_score = sum(results.values()) / len(results)

    print(f"\n📊 总体评分: {total_score:.1f}/100")

    if total_score >= 75:
        print("✅ 优秀！系统分析能力表现良好")
    elif total_score >= 50:
        print("⚠️  良好，但仍有改进空间")
    else:
        print("❌ 需要改进")

    return total_score


def main():
    """主测试流程"""
    print("\n")
    print("🚀 DataInsight Pro - 完整分析能力测试")
    print("="*60)
    print("测试目标: 验证修复后的 CrewAI 能否真正执行数据分析")
    print("="*60)

    # 步骤 1: 环境检查
    env_ok = check_environment()
    if not env_ok:
        print("\n❌ 环境检查失败，请配置后重试")
        print("   1. 设置 OPENAI_API_KEY")
        print("   2. 安装依赖: pip install -r requirements.txt")
        return

    # 步骤 2: 数据检查
    data_ok, dataset_path = check_dataset()
    if not data_ok:
        print("\n❌ 数据检查失败")
        return

    # 询问是否继续
    print("\n" + "="*60)
    user_input = input("环境检查通过，是否开始分析？(Y/n): ").strip().lower()

    if user_input == 'n':
        print("测试已取消")
        return

    # 步骤 3: 创建 Crew
    try:
        crew = run_crewai_test(dataset_path)
    except Exception as e:
        print(f"\n❌ Crew 创建失败: {e}")
        import traceback
        traceback.print_exc()
        return

    # 步骤 4: 执行分析
    result, elapsed_time = execute_analysis(crew, dataset_path)

    if result is None:
        print("\n❌ 分析执行失败")
        return

    # 步骤 5: 检查输出
    outputs = check_outputs()

    # 步骤 6: 显示报告摘要
    display_report_summary()

    # 步骤 7: 评估结果
    score = evaluate_results()

    # 最终总结
    print("\n" + "="*60)
    print("🎉 测试完成")
    print("="*60)

    print(f"\n📊 测试结果:")
    print(f"   - 执行时间: {elapsed_time:.1f} 秒")
    print(f"   - 总体评分: {score:.1f}/100")

    print(f"\n📁 生成的文件:")
    for filename in ["data_exploration_result.md", "statistical_analysis_result.md",
                     "pandaai_analysis_result.md", "final_analysis_report.md"]:
        if Path(filename).exists():
            size = Path(filename).stat().st_size
            print(f"   ✅ {filename} ({size} bytes)")

    print(f"\n💡 查看完整报告:")
    print(f"   cat final_analysis_report.md")

    if score >= 75:
        print(f"\n🎊 恭喜！系统分析能力测试通过！")
        print(f"   修复后的 CrewAI 可以正常执行数据分析任务")
    elif score >= 50:
        print(f"\n⚠️  系统基本可用，但可能需要调优")
    else:
        print(f"\n❌ 系统存在问题，需要进一步调试")


if __name__ == "__main__":
    main()
