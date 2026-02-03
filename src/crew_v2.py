"""
CrewAI 编排 v2.0_fixed - 修复数据传递问题（保持向后兼容）

关键修复：
1. 保持 create_crew() 无参数，与 V2 完全兼容
2. 在 Task description 中使用 {dataset_path} 占位符
3. CrewAI 会从 kickoff(inputs={}) 中自动替换这些占位符
4. 移除不必要的 context 依赖，让每个 Agent 直接读取数据
5. 改用 sequential process（更高效、更稳定）
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from crewai import Crew, Task, Process
from src.crew_config import create_llm
from src.agents.data_explorer_v2 import data_explorer
from src.agents.analyst_v2 import analyst
from src.agents.pandaai_real import pandaai_agent
from src.agents.reporter_v2 import reporter

load_dotenv()


def create_crew():
    """
    创建 DataAnalysisCrew（修复数据传递问题，保持完全向后兼容）

    关键改进：
    1. 使用 {dataset_path}、{goal}、{depth} 等占位符
    2. CrewAI 会从 kickoff(inputs={}) 中自动替换
    3. 每个 Agent 直接读取数据文件，不依赖 context 传递 DataFrame
    4. 使用 sequential process（不需要 manager LLM）
    """

    # ⚠️ 不再需要 manager LLM，改用 sequential
    # llm = create_llm()  # 保留但不再使用

    # 定义任务
    # ✅ 使用占位符 {dataset_path}，会从 inputs 中替换
    task_data_exploration = Task(
        description="""读取数据集 {dataset_path}，执行以下操作：

1. 使用 read_csv_dataset 工具读取数据
2. 使用 check_data_quality 检查数据质量
3. 使用 generate_data_summary 生成数据概览

重要：明确记录数据集路径 {dataset_path} 在输出中。
""",
        expected_output="数据集概览报告，包含：数据规模、字段类型、质量评估、样本数据",
        agent=data_explorer,
        output_file="data_exploration_result.md"
    )

    # ✅ Analyst 直接读取原始数据文件
    # 关键：不使用 context，让 Analyst 独立读取 {dataset_path}
    task_statistical_analysis = Task(
        description="""对数据集 {dataset_path} 进行深入的统计分析：

1. 使用 read_csv_dataset 读取数据集 {dataset_path}
2. 使用 calculate_basic_stats 计算基本统计量（均值、中位数、标准差等）
3. 使用 analyze_trend 分析时间序列趋势
4. 使用 calculate_correlation 分析变量相关性
5. 使用 detect_anomalies 检测异常值
6. 使用 generate_chart_config 生成图表配置
7. 生成完整的统计分析报告

重要：直接读取原始数据文件 {dataset_path}，执行真正的数值计算。
""",
        expected_output="统计分析报告，包含：关键指标、趋势分析、相关性矩阵、异常值列表、图表配置",
        agent=analyst,
        output_file="statistical_analysis_result.md"
        # ✅ 不使用 context，避免数据传递问题
    )

    # ✅ PandaAI Agent 直接读取原始数据文件
    # 关键：不使用 context，让 PandaAI 独立读取 {dataset_path}
    task_pandaai_analysis = Task(
        description="""利用 PandaAI 对数据集 {dataset_path} 进行高级 AI 分析：

1. 使用 pandaai_chat 进行智能问答，例如：
   - "数据的基本统计特征是什么？"
   - "有哪些明显的趋势或模式？"
   - "哪些字段相关性最强？"
   - "数据的分布情况如何？"

2. 使用 pandaai_clean_data 清洗数据

3. 使用 pandaai_analyze_patterns 识别数据模式和洞察

4. 使用 pandaai_predict_trend 预测未来趋势

5. 使用 pandaai_generate_chart 生成可视化图表配置

6. 使用 pandaai_data_summary 生成数据摘要

重要：
- 直接读取数据集 {dataset_path}
- 将 DataFrame 转换为字典格式传给 PandaAI
- 使用 pandasai 库的真实功能，不要使用模拟数据
- 生成可执行的数据洞察代码
""",
        expected_output="PandaAI 分析报告，包含：智能问答结果、数据清洗报告、模式识别洞察、趋势预测、可视化建议、可执行代码",
        agent=pandaai_agent,
        output_file="pandaai_analysis_result.md"
        # ✅ 不使用 context，避免数据传递问题
    )

    # ✅ Reporter 整合所有分析结果
    task_final_report = Task(
        description="""整合所有 Agent 的分析结果，生成最终的专业报告。

分析目标：{goal}
分析深度：{depth}
数据集：{dataset_path}
输出格式：{output_format}

报告应包含：
1. **执行摘要** - 基于分析目标 {goal} 的高层总结
2. **数据概览** - 来自 Data Explorer 的数据概况
3. **统计发现** - 来自 Analyst 的统计分析结果
4. **PandaAI 洞察** - 来自 PandaAI Agent 的 AI 分析
5. **综合建议** - 可执行的行动计划
6. **附录** - 技术细节、图表配置、代码示例

使用 format_report_markdown 或 format_report_json 工具生成最终报告。
保存到文件：{output_path}
""",
        expected_output="完整的数据分析报告（Markdown 格式），包含所有关键发现、PandaAI 洞察、可视化建议和行动计划",
        agent=reporter,
        output_file="{output_path}"
        # Reporter 可以访问前面所有任务的文本输出
    )

    # 定义 Crew
    # ✅ 使用 sequential 而不是 hierarchical
    # 优点：
    # 1. 不需要 manager_llm（节省成本）
    # 2. 每个 Agent 独立读取数据（真正执行分析）
    # 3. 流程清晰，易于调试
    data_analysis_crew = Crew(
        agents=[data_explorer, analyst, pandaai_agent, reporter],
        tasks=[
            task_data_exploration,
            task_statistical_analysis,
            task_pandaai_analysis,
            task_final_report
        ],
        verbose=True,
        process=Process.sequential,  # ✅ 顺序执行，不需要 manager
        # manager_llm 不需要（sequential 不使用）
        share_crew=False
    )

    return data_analysis_crew


# 便捷函数
def run_analysis(goal: str, dataset_path: str, depth: str = "standard", output_path: str = "report.md", output_format: str = "markdown"):
    """
    运行完整的数据分析流程（v2.0_fixed - 修复数据传递，保持兼容）

    Args:
        goal: 分析目标
        dataset_path: 数据集路径
        depth: 分析深度（quick/standard/deep）
        output_path: 输出文件路径
        output_format: 输出格式（markdown/json）

    Returns:
        分析结果
    """
    print(f"\n🎬 启动 DataInsight Pro v2.0_fixed - 数据传递修复版")
    print(f"📋 目标：{goal}")
    print(f"📊 数据集：{dataset_path}")
    print(f"🎯 深度：{depth}")
    print(f"📤 输出：{output_path}")

    # 检查数据集是否存在
    if not Path(dataset_path).exists():
        print(f"\n❌ 错误：数据集文件不存在：{dataset_path}")
        print(f"当前工作目录：{Path.cwd()}")
        return None

    # 检查 API Key
    if not os.getenv("OPENAI_API_KEY"):
        print("\n❌ 错误：未设置 OPENAI_API_KEY 环境变量")
        print("请在 .env 文件中配置：")
        print("  OPENAI_API_KEY=your_api_key_here")
        print("  OPENAI_BASE_URL=https://api.openai.com/v1  # 可选")
        print("  OPENAI_MODEL=gpt-4  # 可选")
        return None

    # 检查 PandaAI 是否安装
    try:
        import pandasai
        print(f"✅ PandaAI 已安装：{pandasai.__version__}")
    except ImportError:
        print("\n⚠️  警告：pandasai 未安装")
        print("请运行: pip install pandasai>=2.0.0")
        print("将无法使用 PandaAI 功能，但其他 Agent 可以正常工作")

    # 执行 Crew
    try:
        crew = create_crew()
        result = crew.kickoff(
            inputs={
                'goal': goal,
                'dataset_path': dataset_path,
                'analysis_depth': depth,
                'depth': depth,  # 添加 depth 占位符
                'output_path': output_path,
                'output_format': output_format
            }
        )

        print(f"\n✅ 分析完成！")
        print(f"📄 最终报告：{output_path}")

        return result

    except Exception as e:
        print(f"\n❌ 分析失败：{str(e)}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    # 快速测试
    print("="*60)
    print("🧪 Data Analysis Crew v2.0_fixed - 测试")
    print("="*60)

    # 先检查测试数据是否存在
    test_dataset = "data/samples/sales_2024_Q1.csv"
    if not Path(test_dataset).exists():
        print(f"\n⚠️  测试数据不存在：{test_dataset}")
        print("创建测试数据...")
        import pandas as pd
        Path("data/samples").mkdir(parents=True, exist_ok=True)
        df = pd.DataFrame({
            'date': pd.date_range('2024-01-01', periods=90),
            'sales': [100 + i*5 + (i%7)*10 for i in range(90)],
            'profit': [20 + i*1 + (i%7)*2 for i in range(90)],
            'customers': [10 + i%5 for i in range(90)]
        })
        df.to_csv(test_dataset, index=False)
        print(f"✅ 测试数据已创建：{test_dataset}")

    result = run_analysis(
        goal="分析销售数据的趋势和异常，使用 PandaAI 进行智能洞察",
        dataset_path=test_dataset,
        depth="standard",
        output_path="pandaai_test_report_fixed.md"
    )

    if result:
        print(f"\n✅ 测试成功！")
    else:
        print(f"\n❌ 测试失败")
