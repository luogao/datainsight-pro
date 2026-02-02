"""
CrewAI 编排 - Data Analysis Crew
协调所有 Agent 协作完成端到端的数据分析
"""
from crewai import Crew, Agent, Task, Process
from langchain_openai import ChatOpenAI

# 导入所有 Agent
from src.agents.data_explorer import data_explorer
from src.agents.analyst import analyst
from src.agents.pandaai import pandaai
from src.agents.reporter import reporter


# 定义 LLM
llm = ChatOpenAI(
    model="gpt-4",
    temperature=0.7,
    max_tokens=4096
)


# 定义任务
task_data_exploration = Task(
    description="读取数据集 {dataset_path}，探索数据结构，检查数据质量，生成数据概览报告",
    expected_output="包含数据规模、字段类型、数据质量评估和样本数据的 Markdown 报告",
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


task_ai_insights = Task(
    description="利用 PandaAI 进行高级数据分析，包括：趋势预测、模式识别、异常解释。基于统计分析结果提供智能洞察和业务建议。",
    expected_output="包含 AI 预测、高级洞察、业务建议和战略建议的 Markdown 报告",
    agent=pandaai,
    output_file="ai_insights_result.md",
    context=[task_data_exploration, task_statistical_analysis]
)


task_final_report = Task(
    description="整合所有 Agent 的分析结果，生成最终的专业报告。包括：摘要、数据概览、统计发现、AI 洞察、建议和行动计划。",
    expected_output="完整的数据分析报告（Markdown 格式），包含所有关键发现和建议",
    agent=reporter,
    output_file="final_report.md",
    context=[task_data_exploration, task_statistical_analysis, task_ai_insights]
)


# 定义流程
data_analysis_crew = Crew(
    agents=[data_explorer, analyst, pandaai, reporter],
    tasks=[task_data_exploration, task_statistical_analysis, task_ai_insights, task_final_report],
    verbose=True,
    process=Process.hierarchical,  # 层级流程：每个任务依赖前面的任务
    manager_llm=llm,
    share_crew=False
)


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
    print(f"\n🎬 启动数据分析...")
    print(f"📋 目标：{goal}")
    print(f"📊 数据集：{dataset_path}")
    print(f"🎯 深度：{depth}")
    print(f"📤 输出：{output_path}")

    # 执行 Crew
    result = data_analysis_crew.kickoff(
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


if __name__ == "__main__":
    # 快速测试
    print("="*60)
    print("🧪 Data Analysis Crew - 快速测试")
    print("="*60)

    result = run_analysis(
        goal="分析销售数据的趋势和异常",
        dataset_path="data/samples/sales_2024_Q1.csv",
        depth="standard",
        output_path="quick_test_report.md"
    )

    print(f"\n测试结果：{result}")
