"""
CrewAI 编排 v2.0 - 真正集成 PandaAI
协调所有 Agent 协作完成端到端的数据分析
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
    """创建 DataAnalysisCrew（支持自定义 LLM 配置）"""

    # 创建管理器 LLM
    llm = create_llm()

    # 定义任务
    task_data_exploration = Task(
        description="读取数据集 {dataset_path}，探索数据结构，检查数据质量，生成数据概览报告。保留原始数据供后续 Agent 使用。",
        expected_output="包含数据规模、字段类型、数据质量评估、样本数据和原始数据字典的完整报告",
        agent=data_explorer,
        output_file="data_exploration_result.md"
    )

    task_statistical_analysis = Task(
        description="对数据进行深入的统计分析，包括：基本统计量计算、趋势分析、相关性分析、异常检测。生成统计报告和可视化图表配置。",
        expected_output="包含关键指标、趋势图、相关性矩阵、异常值列表的 Markdown 报告",
        agent=analyst,
        output_file="statistical_analysis_result.md",
        context=[task_data_exploration]
    )

    task_pandaai_analysis = Task(
        description="""利用 PandaAI 进行高级数据分析：

1. **智能数据问答**：使用 PandaAI 的自然语言查询能力，回答关于数据的关键问题
2. **数据清洗**：使用 PandaAI 智能清洗数据，处理缺失值和异常值
3. **模式识别**：使用 PandaAI 识别数据中的模式和洞察
4. **趋势预测**：使用 PandaAI 预测未来趋势
5. **可视化生成**：使用 PandaAI 生成数据可视化图表

注意：使用 PandaAI 的真实功能，不要使用模拟数据。传入 DataFrame 上下文。
""",
        expected_output="包含 PandaAI 智能问答结果、数据清洗报告、模式识别洞察、趋势预测和可视化建议的完整报告",
        agent=pandaai_agent,
        output_file="pandaai_analysis_result.md",
        context=[task_data_exploration, task_statistical_analysis]
    )

    task_final_report = Task(
        description="整合所有 Agent 的分析结果，生成最终的专业报告。包括：摘要、数据概览、统计发现、PandaAI 洞察、建议和行动计划。报告要突出 PandaAI 的 AI 分析价值。",
        expected_output="完整的数据分析报告（Markdown 格式），包含所有关键发现、PandaAI 洞察和建议",
        agent=reporter,
        output_file="final_report.md",
        context=[task_data_exploration, task_statistical_analysis, task_pandaai_analysis]
    )

    # 定义 Crew
    data_analysis_crew = Crew(
        agents=[data_explorer, analyst, pandaai_agent, reporter],
        tasks=[task_data_exploration, task_statistical_analysis, task_pandaai_analysis, task_final_report],
        verbose=True,
        process=Process.hierarchical,  # 层级流程：每个任务依赖前面的任务
        manager_llm=llm,
        share_crew=False
    )

    return data_analysis_crew


# 便捷函数
def run_analysis(goal: str, dataset_path: str, depth: str = "standard", output_path: str = "report.md", output_format: str = "markdown"):
    """
    运行完整的数据分析流程

    Args:
        goal: 分析目标
        dataset_path: 数据集路径
        depth: 分析深度（quick/standard/deep）
        output_path: 输出文件路径
        output_format: 输出格式（markdown/json）

    Returns:
        分析结果
    """
    print(f"\n🎬 启动 DataInsight Pro v2.0 - PandaAI 真实集成版")
    print(f"📋 目标：{goal}")
    print(f"📊 数据集：{dataset_path}")
    print(f"🎯 深度：{depth}")
    print(f"📤 输出：{output_path}")

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
    print("🧪 Data Analysis Crew v2.0 - PandaAI 真实集成测试")
    print("="*60)

    result = run_analysis(
        goal="分析销售数据的趋势和异常，使用 PandaAI 进行智能洞察",
        dataset_path="data/samples/sales_2024_Q1.csv",
        depth="standard",
        output_path="pandaai_test_report.md"
    )

    if result:
        print(f"\n✅ 测试成功！")
    else:
        print(f"\n❌ 测试失败")
