"""
Reporter Agent
负责：整合所有分析结果，生成最终报告
"""
import json
from datetime import datetime
from crewai import Agent, Task, Process
from crewai.tools import SerperDevTool
from langchain.tools import tool


@tool
def compile_summary(data_explorer_result: str, analyst_result: str, pandaai_result: str) -> str:
    """
    整合所有 Agent 的分析结果，生成统一摘要

    Args:
        data_explorer_result: Data Explorer 的结果
        analyst_result: Analyst 的结果
        pandaai_result: PandaAI 的结果

    Returns:
        Markdown 格式的摘要报告
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    summary = f"""# 📊 数据分析综合报告

> 生成时间：{timestamp}
> 分析系统：DataInsight Pro v1.0

---

## 📋 数据概览

{data_explorer_result}

---

## 📈 统计分析

{analyst_result}

---

## 🧠 AI 洞察

{pandaai_result}

---

## 💡 综合建议

基于以上分析，建议：

1. **短期行动**：关注数据中发现的主要异常点
2. **中期规划**：根据趋势预测调整策略
3. **长期战略**：利用 AI 洞察制定数据驱动的战略

---

## 📊 附录

- 数据规模：由 Data Explorer 提供
- 分析深度：标准分析
- AI 模型：PandaAI v2

*报告由 DataInsight Pro 自动生成*
"""

    return summary


@tool
def format_report_markdown(summary: str, charts: list) -> str:
    """
    格式化报告为 Markdown 格式

    Args:
        summary: 摘要内容
        charts: 图表配置列表

    Returns:
        完整的 Markdown 报告
    """
    report = summary

    if charts:
        report += "\n\n## 📊 可视化图表\n\n"
        for i, chart in enumerate(charts, 1):
            report += f"### 图表 {i}: {chart.get('title', 'Chart {i}')}\n"
            report += f"类型：{chart.get('type', 'unknown')}\n"
            report += f"说明：{chart.get('description', 'No description')}\n\n"

    return report


@tool
def format_report_json(summary: str, metrics: dict, findings: list, recommendations: list) -> str:
    """
    格式化报告为 JSON 格式

    Args:
        summary: 摘要
        metrics: 关键指标
        findings: 发现列表
        recommendations: 建议列表

    Returns:
        JSON 格式报告
    """
    report_json = {
        "generated_at": datetime.now().isoformat(),
        "version": "1.0.0",
        "system": "DataInsight Pro",
        "summary": summary,
        "metrics": metrics,
        "findings": findings,
        "recommendations": recommendations,
        "metadata": {
            "format": "json",
            "schema_version": "1.0"
        }
    }

    return json.dumps(report_json, indent=2, ensure_ascii=False)


@tool
def save_report(report_content: str, output_path: str, format: str = "markdown") -> str:
    """
    保存报告到文件

    Args:
        report_content: 报告内容
        output_path: 输出路径
        format: 文件格式（markdown/json）

    Returns:
        保存结果
    """
    try:
        # 确保输出目录存在
        from pathlib import Path
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # 写入文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report_content)

        return f"✅ 报告已保存到：{output_file.absolute()}"
    except Exception as e:
        return f"❌ 保存报告失败：{str(e)}"


@tool
def generate_executable_summary(analysis_goal: str, key_findings: list, priority_actions: list) -> str:
    """
    生成可执行的执行摘要（供决策者使用）

    Args:
        analysis_goal: 分析目标
        key_findings: 关键发现列表
        priority_actions: 优先级行动列表

    Returns:
        执行摘要
    """
    summary = f"""# 🎯 执行摘要

## 📋 分析目标

{analysis_goal}

## 🔑 关键发现

"""
    for i, finding in enumerate(key_findings, 1):
        summary += f"{i}. {finding}\n"

    summary += "\n## 🚀 优先级行动\n\n"
    for i, action in enumerate(priority_actions, 1):
        summary += f"### P{i}: {action.get('title', f'行动 {i}')}\n"
        summary += f"{action.get('description', '')}\n"
        summary += f"优先级：{action.get('priority', '中')}\n"
        summary += f"预期影响：{action.get('impact', '待评估')}\n"
        summary += f"负责人：{action.get('owner', '待分配')}\n\n"

    summary += "---\n"
    summary += f"*执行摘要由 DataInsight Pro 于 {datetime.now().strftime('%Y-%m-%d')} 生成*\n"

    return summary


# Reporter Agent
reporter = Agent(
    role="报告生成专家",
    goal="整合所有分析结果，生成清晰、结构化的专业报告",
    backstory="""你是一位专业的商业分析师和报告撰写专家。
    你能够：
    - 整合多个来源的分析结果
    - 提取关键信息和洞察
    - 生成结构化、易读的报告
    - 创建可执行的建议和行动计划
    - 适应不同受众的需求（执行层、管理层、战略层）

    你总是能够将复杂的数据分析转化为清晰的业务语言，
    并提供可行动的建议。你的报告既有数据支撑，又有战略眼光。""",
    verbose=True,
    allow_delegation=False,
    llm="gpt-4",  # 可以根据实际情况调整
    tools=[
        compile_summary,
        format_report_markdown,
        format_report_json,
        save_report,
        generate_executable_summary
    ]
)
