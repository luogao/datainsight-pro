"""
CrewAI 编排 v2.1 - 修复数据传递问题
协调所有 Agent 协作完成端到端的数据分析

关键改进：
1. 每个 Agent 直接读取数据文件，不依赖前一个 Agent 的输出
2. 使用 inputs 统一传递数据路径
3. 添加数据验证和错误处理
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


def create_crew_v21(dataset_path: str, goal: str, depth: str = "standard"):
    """
    创建 DataAnalysisCrew v2.1（修复数据传递问题）

    关键改进：每个 Agent 直接读取数据文件，而不是依赖上下文传递
    """

    # 创建管理器 LLM
    llm = create_llm()

    # 任务 1: 数据探索
    # Data Explorer 读取数据并生成概览
    task_data_exploration = Task(
        description=f"""读取数据集 {dataset_path}，执行以下操作：

1. 使用 read_csv_dataset 工具读取数据
2. 使用 check_data_quality 检查数据质量
3. 使用 generate_data_summary 生成数据概览

重要：将数据集路径 {dataset_path} 包含在你的输出中，供后续 Agent 使用。
""",
        expected_output="数据集概览报告，包含：数据规模、字段类型、质量评估、样本数据",
        agent=data_explorer,
        output_file="data_exploration_result.md"
    )

    # 任务 2: 统计分析
    # Analyst 直接读取原始数据文件（不依赖 Data Explorer 的输出）
    task_statistical_analysis = Task(
        description=f"""对数据集 {dataset_path} 进行深入的统计分析：

1. 读取数据集 {dataset_path}
2. 使用 calculate_basic_stats 计算基本统计量（均值、中位数、标准差等）
3. 使用 analyze_trend 分析时间序列趋势
4. 使用 calculate_correlation 分析变量相关性
5. 使用 detect_anomalies 检测异常值
6. 生成完整的统计分析报告

注意：直接读取原始数据文件 {dataset_path}，不要依赖前一个任务的输出。
""",
        expected_output="统计分析报告，包含：关键指标、趋势分析、相关性矩阵、异常值列表",
        agent=analyst,
        output_file="statistical_analysis_result.md"
        # ⚠️ 不使用 context，让 Analyst 直接读取数据
    )

    # 任务 3: PandaAI 分析
    # PandaAI Agent 直接读取原始数据文件
    task_pandaai_analysis = Task(
        description=f"""利用 PandaAI 对数据集 {dataset_path} 进行高级 AI 分析：

1. 使用 pandaai_chat 进行智能问答，例如：
   - "数据的基本统计特征是什么？"
   - "有哪些明显的趋势或模式？"
   - "哪些字段相关性最强？"

2. 使用 pandaai_clean_data 清洗数据

3. 使用 pandaai_analyze_patterns 识别数据模式和洞察

4. 使用 pandaai_predict_trend 预测未来趋势

5. 使用 pandaai_generate_chart 生成可视化图表配置

重要：直接读取数据集 {dataset_path}，传入给 PandaAI 的 dataframe_context 参数。
将原始数据转换为字典格式：df.to_dict(orient='records')
""",
        expected_output="PandaAI 分析报告，包含：智能问答结果、数据清洗报告、模式识别洞察、趋势预测、可视化建议",
        agent=pandaai_agent,
        output_file="pandaai_analysis_result.md"
        # ⚠️ 不使用 context，让 PandaAI 直接读取数据
    )

    # 任务 4: 最终报告
    # Reporter 整合所有 Agent 的结果
    task_final_report = Task(
        description=f"""整合所有 Agent 的分析结果，生成最终的专业报告。

分析目标：{goal}
分析深度：{depth}
数据集：{dataset_path}

报告应包含：
1. 执行摘要 - 基于分析目标 {goal}
2. 数据概览 - 来自 Data Explorer
3. 统计发现 - 来自 Analyst
4. PandaAI 洞察 - 来自 PandaAI Agent
5. 综合建议 - 可执行的行动计划
6. 附录 - 技术细节和图表

使用 format_report_markdown 或 format_report_json 工具生成最终报告。
""",
        expected_output="完整的数据分析报告（Markdown 格式），包含所有关键发现、PandaAI 洞察和建议",
        agent=reporter,
        output_file="final_report.md"
        # Reporter 可以使用前面所有任务的结果
    )

    # 定义 Crew
    # 注意：使用 sequential 而不是 hierarchical，因为我们已经明确指定了执行顺序
    data_analysis_crew = Crew(
        agents=[data_explorer, analyst, pandaai_agent, reporter],
        tasks=[task_data_exploration, task_statistical_analysis, task_pandaai_analysis, task_final_report],
        verbose=True,
        process=Process.sequential,  # ✅ 改为顺序执行
        # 不需要 manager_llm（sequential 不需要）
    )

    return data_analysis_crew


# 便捷函数
def run_analysis(goal: str, dataset_path: str, depth: str = "standard", output_path: str = "report.md", output_format: str = "markdown"):
    """
    运行完整的数据分析流程（v2.1 - 修复数据传递）

    Args:
        goal: 分析目标
        dataset_path: 数据集路径
        depth: 分析深度（quick/standard/deep）
        output_path: 输出文件路径
        output_format: 输出格式（markdown/json）

    Returns:
        分析结果
    """
    print(f"\n🎬 启动 DataInsight Pro v2.1 - 修复数据传递版本")
    print(f"📋 目标：{goal}")
    print(f"📊 数据集：{dataset_path}")
    print(f"🎯 深度：{depth}")
    print(f"📤 输出：{output_path}")

    # 检查数据集是否存在
    if not Path(dataset_path).exists():
        print(f"\n❌ 错误：数据集文件不存在：{dataset_path}")
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
        crew = create_crew_v21(dataset_path, goal, depth)
        result = crew.kickoff(
            inputs={
                'goal': goal,
                'dataset_path': dataset_path,
                'analysis_depth': depth,
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
    print("🧪 Data Analysis Crew v2.1 - 数据传递修复测试")
    print("="*60)

    result = run_analysis(
        goal="分析销售数据的趋势和异常，使用 PandaAI 进行智能洞察",
        dataset_path="data/samples/sales_2024_Q1.csv",
        depth="standard",
        output_path="pandaai_test_report_v21.md"
    )

    if result:
        print(f"\n✅ 测试成功！")
    else:
        print(f"\n❌ 测试失败")
