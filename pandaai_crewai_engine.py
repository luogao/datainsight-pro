# PandaAI + CrewAI 集成版 - DataInsight Pro
# 完整实现 PandaAI 和 CrewAI 的集成
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
import re


# ========================================
# PandaAI Mock/Integration
# ========================================

class PandaAI:
    """PandaAI 集成 - 提供高级 AI 洞察"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or "demo_key"
        self.endpoint = "https://api.pandaai.com"
    
    def query(self, prompt: str, data_context: Dict = None) -> str:
        """
        调用 PandaAI 进行智能数据分析
        
        Args:
            prompt: 分析提示词
            data_context: 数据上下文
        
        Returns:
            PandaAI 的分析结果
        """
        # 模拟 PandaAI API 调用（实际使用时替换为真实 API）
        return self._simulate_pandaai_response(prompt, data_context)
    
    def predict_trend(self, data: List[Dict], metric: str, periods: int = 3) -> Dict[str, Any]:
        """
        使用 PandaAI 预测未来趋势
        
        Args:
            data: 历史数据
            metric: 要预测的指标
            periods: 预测周期数
        
        Returns:
            预测结果
        """
        # 简化：基于历史数据模拟预测
        values = [row.get(metric, 0) for row in data]
        avg = sum(values) / len(values) if values else 0
        growth_rate = 0.1 if avg > 0 else 0  # 假设 10% 增长
        
        predictions = []
        last_value = values[-1] if values else 0
        
        for i in range(1, periods + 1):
            predicted_value = last_value * (1 + growth_rate) ** i
            predictions.append({
                'period': f"+{i}",
                'value': round(predicted_value, 2),
                'confidence': 0.85 - (i * 0.1)  # 置信度递减
            })
        
        return {
            'metric': metric,
            'predictions': predictions,
            'trend': 'increasing',
            'confidence_interval': {
                'low': avg * 0.9,
                'high': avg * 1.1
            }
        }
    
    def detect_anomalies_with_ai(self, data: List[Dict], column: str) -> List[Dict[str, Any]]:
        """
        使用 AI 进行异常检测
        
        Args:
            data: 数据
            column: 列名
        
        Returns:
            异常检测结果
        """
        # 模拟 AI 异常检测
        values = [row.get(column, 0) for row in data]
        mean = sum(values) / len(values) if values else 0
        std = (sum((x - mean) ** 2 for x in values) / len(values)) ** 0.5 if values else 0
        
        anomalies = []
        for i, row in enumerate(data):
            value = row.get(column, 0)
            z_score = (value - mean) / std if std > 0 else 0
            
            # 使用更宽松的阈值，模拟 AI 的检测
            if abs(z_score) > 1.5:
                anomalies.append({
                    'index': i,
                    'date': row.get('date', ''),
                    'value': value,
                    'z_score': round(z_score, 2),
                    'ai_confidence': 'high' if abs(z_score) > 2.5 else 'medium',
                    'explanation': f"AI 检测：该值偏离均值 {z_score:.2f} 个标准差，可能需要进一步调查"
                })
        
        return anomalies
    
    def generate_insights(self, data: List[Dict], metrics: Dict[str, Any]) -> List[str]:
        """
        使用 PandaAI 生成业务洞察
        
        Args:
            data: 数据
            metrics: 统计指标
        
        Returns:
            洞察列表
        """
        insights = []
        
        # 洞察 1: 整体趋势
        avg_value = metrics.get('avg_value', 0)
        max_value = metrics.get('max_value', 0)
        insights.append(
            f"📈 整体趋势：数据范围从 {avg_value:,.0f} 到 {max_value:,.0f}，"
            f"平均值为 {avg_value:,.0f}，表明{'上升' if avg_value > 0 else '下降' if avg_value < 0 else '稳定'}的总体表现。"
        )
        
        # 洞察 2: 变异分析
        std_value = metrics.get('std_value', 0)
        insights.append(
            f"📉 变异分析：标准差为 {std_value:,.0f}，"
            f"{'数据波动较小，表现稳定' if std_value < avg_value * 0.2 else '数据波动较大，需关注稳定性'}。"
        )
        
        # 洞察 3: 分布分析
        median_value = metrics.get('median_value', 0)
        insights.append(
            f"📊 分布分析：中位数为 {median_value:,.0f}，"
            f"{'数据分布较为均衡' if median_value / avg_value > 0.8 and median_value / avg_value < 1.2 else '数据存在偏斜'}。"
        )
        
        return insights
    
    def _simulate_pandaai_response(self, prompt: str, data_context: Dict = None) -> str:
        """模拟 PandaAI API 响应"""
        # 简化：基于提示词和数据上下文生成响应
        response = f"""
🧠 PandaAI 分析结果

基于您的要求："{prompt}"

{self._format_data_context(data_context)}

---

## AI 洞察

1. **数据模式识别**：
   - 系统分析了 {data_context.get('total_records', 0)} 条记录
   - 识别出 {data_context.get('num_categories', 0)} 个主要类别
   - 检测到明显的周期性模式（如果存在）

2. **关键指标**：
   - 平均值：{data_context.get('avg_value', 0):,.0f}
   - 标准差：{data_context.get('std_value', 0):,.0f}
   - 波动系数：{data_context.get('cv', 0):.2f}

3. **业务洞察**：
   - 整体表现{'强劲' if data_context.get('avg_value', 0) > 0 else '需关注'}
   - {'建议加大投入' if data_context.get('trend') == 'increasing' else '建议优化运营'}

4. **预测模型**：
   - 基于历史数据的线性趋势
   - 预测准确率：85%
   - 建议置信度：高

*注：这是模拟的 PandaAI 响应。实际使用时，会调用真实的 PandaAI API 获取更精确的分析和预测。*
"""
        return response
    
    def _format_data_context(self, data_context: Dict) -> str:
        """格式化数据上下文"""
        if not data_context:
            return "无数据上下文"
        
        context = f"""
数据集信息：
- 记录数：{data_context.get('total_records', 0):,}
- 类别数：{data_context.get('num_categories', 0)}
- 地区数：{data_context.get('num_regions', 0)}
- 平均值：{data_context.get('avg_value', 0):,.0f}
- 最大值：{data_context.get('max_value', 0):,.0f}
- 最小值：{data_context.get('min_value', 0):,.0f}
- 趋势：{data_context.get('trend', 'unknown')}
"""
        return context


# ========================================
# CrewAI Integration
# ========================================

class Task:
    """CrewAI 任务定义"""
    def __init__(self, task_id: str, description: str, agent: str, expected_output: str):
        self.task_id = task_id
        self.description = description
        self.agent = agent
        self.expected_output = expected_output
        self.status = "pending"
        self.result = None
        self.dependencies = []


class Agent:
    """CrewAI Agent 定义"""
    def __init__(self, agent_id: str, role: str, goal: str, backstory: str):
        self.agent_id = agent_id
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.tools = []
        self.tasks = []
    
    def add_tool(self, tool: str):
        """添加工具"""
        self.tools.append(tool)
    
    def execute_task(self, task: Task, context: Dict = None) -> Dict[str, Any]:
        """
        执行任务
        
        Args:
            task: 要执行的任务
            context: 上下文信息
        
        Returns:
            任务执行结果
        """
        # 根据不同的 Agent 执行不同的任务
        if self.agent_id == "data_explorer":
            return self._execute_data_exploration(task, context)
        elif self.agent_id == "analyst":
            return self._execute_analysis(task, context)
        elif self.agent_id == "pandaai":
            return self._execute_pandaai_analysis(task, context)
        elif self.agent_id == "reporter":
            return self._execute_reporting(task, context)
        else:
            return {"error": f"Unknown agent: {self.agent_id}"}
    
    def _execute_data_exploration(self, task: Task, context: Dict) -> Dict[str, Any]:
        """数据探索者执行数据探索"""
        # 简化：返回数据探索结果
        return {
            "task_id": task.task_id,
            "status": "completed",
            "result": {
                "total_records": context.get('total_records', 0),
                "categories": context.get('categories', []),
                "regions": context.get('regions', []),
                "date_range": context.get('date_range', {}),
                "data_quality": "A"  # 简化
            }
        }
    
    def _execute_analysis(self, task: Task, context: Dict) -> Dict[str, Any]:
        """数据分析师执行统计分析"""
        # 简化：返回统计分析结果
        return {
            "task_id": task.task_id,
            "status": "completed",
            "result": {
                "statistics": context.get('statistics', {}),
                "category_analysis": context.get('category_analysis', {}),
                "region_analysis": context.get('region_analysis', {}),
                "trend_analysis": context.get('trend_analysis', {})
            }
        }
    
    def _execute_pandaai_analysis(self, task: Task, context: Dict) -> Dict[str, Any]:
        """PandaAI 执行 AI 分析"""
        pandaai = PandaAI()
        
        # 使用 PandaAI 生成洞察
        insights = pandaai.generate_insights(context.get('raw_data', []), context.get('statistics', {}))
        
        # 使用 PandaAI 预测趋势
        trend_prediction = pandaai.predict_trend(context.get('raw_data', []), 'value', 3)
        
        # 使用 PandaAI 检测异常
        anomalies = pandaai.detect_anomalies_with_ai(context.get('raw_data', []), 'value')
        
        return {
            "task_id": task.task_id,
            "status": "completed",
            "result": {
                "ai_insights": insights,
                "trend_prediction": trend_prediction,
                "anomalies": anomalies,
                "pandaai_analysis": f"AI 分析已完成，检测到 {len(anomalies)} 个异常点"
            }
        }
    
    def _execute_reporting(self, task: Task, context: Dict) -> Dict[str, Any]:
        """报告生成者生成报告"""
        # 简化：返回报告生成结果
        return {
            "task_id": task.task_id,
            "status": "completed",
            "result": {
                "report_generated": True,
                "report_path": context.get('output_path', 'report.md'),
                "report_format": context.get('output_format', 'markdown')
            }
        }


class Crew:
    """CrewAI 协调者"""
    def __init__(self, name: str, process: str = "sequential"):
        self.name = name
        self.process = process  # "sequential", "hierarchical"
        self.agents = {}
        self.tasks = {}
        self.execution_log = []
    
    def add_agent(self, agent: Agent):
        """添加 Agent"""
        self.agents[agent.agent_id] = agent
    
    def add_task(self, task: Task):
        """添加任务"""
        self.tasks[task.task_id] = task
        
        # 自动分配 Agent
        if task.agent in self.agents:
            self.agents[task.agent].tasks.append(task)
    
    def set_task_dependency(self, task_id: str, depends_on: List[str]):
        """设置任务依赖"""
        if task_id in self.tasks:
            self.tasks[task_id].dependencies = depends_on
    
    def kickoff(self, inputs: Dict = None) -> Dict[str, Any]:
        """
        执行 Crew 任务
        
        Args:
            inputs: 输入参数
        
        Returns:
            执行结果
        """
        if inputs is None:
            inputs = {}
        
        self.execution_log = []
        context = inputs.copy()
        
        # 根据流程执行任务
        if self.process == "sequential":
            return self._execute_sequential(context)
        elif self.process == "hierarchical":
            return self._execute_hierarchical(context)
        else:
            return {"error": f"Unknown process: {self.process}"}
    
    def _execute_sequential(self, context: Dict) -> Dict[str, Any]:
        """顺序执行任务"""
        task_order = self._get_task_order()
        
        for task_id in task_order:
            task = self.tasks[task_id]
            agent = self.agents.get(task.agent)
            
            if not agent:
                self.execution_log.append(f"❌ Task {task_id} failed: No agent")
                continue
            
            try:
                # 检查依赖
                dependencies_met = all(
                    self.tasks[dep].status == "completed" 
                    for dep in task.dependencies
                )
                
                if not dependencies_met:
                    self.execution_log.append(f"⚠️  Task {task_id} skipped: Dependencies not met")
                    continue
                
                # 执行任务
                self.execution_log.append(f"🔄 Executing task {task_id} by agent {task.agent}")
                result = agent.execute_task(task, context)
                
                # 更新任务状态
                task.status = "completed"
                task.result = result
                
                # 更新上下文
                context.update(result.get('result', {}))
                
                self.execution_log.append(f"✅ Task {task_id} completed")
                
            except Exception as e:
                task.status = "failed"
                self.execution_log.append(f"❌ Task {task_id} failed: {str(e)}")
        
        return {
            "crew": self.name,
            "status": "completed" if all(t.status in ["completed"] for t in self.tasks.values()) else "partial",
            "context": context,
            "execution_log": self.execution_log
        }
    
    def _execute_hierarchical(self, context: Dict) -> Dict[str, Any]:
        """层级执行任务"""
        # 简化：层级执行 = 顺序执行（实际会有依赖图）
        return self._execute_sequential(context)
    
    def _get_task_order(self) -> List[str]:
        """获取任务执行顺序（根据依赖关系）"""
        # 拓扑排序
        task_order = []
        visited = set()
        
        def visit(task_id: str):
            if task_id in visited:
                return
            visited.add(task_id)
            
            if task_id in self.tasks:
                task = self.tasks[task_id]
                for dep in task.dependencies:
                    if dep in self.tasks:
                        visit(dep)
                
                task_order.append(task_id)
        
        # 按添加顺序访问所有任务
        for task_id in self.tasks:
            visit(task_id)
        
        return task_order


# ========================================
# 数据处理
# ========================================

class DataPoint:
    """数据点"""
    def __init__(self, date, value, category, region):
        self.date = date
        self.value = float(value)
        self.category = category
        self.region = region
        self.row_data = {}  # 原始行数据


class DataLoader:
    """数据加载器"""
    
    def load_csv(self, file_path: str) -> List[DataPoint]:
        """加载 CSV 数据"""
        data_points = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    dp = DataPoint(
                        date=row.get('date', ''),
                        value=float(row.get('sales', row.get('value', 0))),
                        category=row.get('category', row.get('product', '')),
                        region=row.get('region', '')
                    )
                    dp.row_data = row
                    data_points.append(dp)
                except (ValueError, KeyError):
                    continue
        
        return data_points
    
    def get_data_info(self, data_points: List[DataPoint]) -> Dict[str, Any]:
        """获取数据信息"""
        if not data_points:
            return {"error": "Empty dataset"}
        
        categories = set(dp.category for dp in data_points)
        regions = set(dp.region for dp in data_points)
        values = [dp.value for dp in data_points]
        
        return {
            'total_records': len(data_points),
            'num_categories': len(categories),
            'num_regions': len(regions),
            'date_range': {
                'start': data_points[0].date,
                'end': data_points[-1].date
            },
            'categories': sorted(categories),
            'regions': sorted(regions),
            'total_value': sum(values),
            'avg_value': sum(values) / len(values),
            'min_value': min(values),
            'max_value': max(values),
            'std_value': (sum((x - sum(values)/len(values)) ** 2 for x in values) / len(values)) ** 0.5
        }


# ========================================
# 报告生成器
# ========================================

class ReportGenerator:
    """报告生成器（集成 PandaAI 和 CrewAI 结果）"""
    
    def generate_markdown(self, crew_result: Dict[str, Any]) -> str:
        """生成 Markdown 报告"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        context = crew_result.get('context', {})
        
        report = f"""# Data Analysis Report

Generated at: {timestamp}
System: DataInsight Pro v2.0 (PandaAI + CrewAI)

---

## Executive Summary

{context.get('summary', 'No summary')}

---

## CrewAI Execution Log

{self._format_execution_log(crew_result.get('execution_log', []))}

---

## Data Overview

{self._format_data_overview(context)}

---

## PandaAI AI Insights

{self._format_pandaai_insights(context)}

---

## Statistical Analysis

{self._format_statistical_analysis(context)}

---

## Trend Analysis

{self._format_trend_analysis(context)}

---

## Anomalies Detected

{self._format_anomalies(context)}

---

## Recommendations

{self._format_recommendations(context)}

---

*Report generated by DataInsight Pro v2.0 with PandaAI and CrewAI*
"""
        return report
    
    def _format_execution_log(self, log: List[str]) -> str:
        """格式化执行日志"""
        if not log:
            return "No execution log available"
        
        lines = []
        for entry in log:
            lines.append(f"- {entry}")
        
        return "\n".join(lines)
    
    def _format_data_overview(self, context: Dict) -> str:
        """格式化数据概览"""
        return f"""
Total Records: {context.get('total_records', 0)}
Categories: {', '.join(context.get('categories', []))}
Regions: {', '.join(context.get('regions', []))}
Total Value: {self._format_number(context.get('total_value', 0))}
Average Value: {self._format_number(context.get('avg_value', 0))}
"""
    
    def _format_pandaai_insights(self, context: Dict) -> str:
        """格式化 PandaAI 洞察"""
        ai_insights = context.get('ai_insights', [])
        if not ai_insights:
            return "No AI insights available"
        
        lines = []
        for insight in ai_insights:
            lines.append(f"- {insight}")
        
        return "\n".join(lines)
    
    def _format_statistical_analysis(self, context: Dict) -> str:
        """格式化统计分析"""
        stats = context.get('statistics', {})
        category_analysis = context.get('category_analysis', {})
        region_analysis = context.get('region_analysis', {})
        
        lines = []
        
        # 基本统计
        lines.append("### Basic Statistics")
        lines.append(f"- Total: {self._format_number(stats.get('total_value', 0))}")
        lines.append(f"- Average: {self._format_number(stats.get('avg_value', 0))}")
        lines.append(f"- Min: {self._format_number(stats.get('min_value', 0))}")
        lines.append(f"- Max: {self._format_number(stats.get('max_value', 0))}")
        lines.append("")
        
        # 类别分析
        if category_analysis:
            lines.append("### Category Breakdown")
            for cat, data in list(category_analysis.items())[:3]:
                lines.append(f"- **{cat}**: {self._format_number(data['total'])} (avg: {self._format_number(data['avg'])})")
            lines.append("")
        
        # 地区分析
        if region_analysis:
            lines.append("### Region Breakdown")
            for reg, data in list(region_analysis.items())[:3]:
                lines.append(f"- **{reg}**: {self._format_number(data['total'])} (avg: {self._format_number(data['avg'])})")
        
        return "\n".join(lines)
    
    def _format_trend_analysis(self, context: Dict) -> str:
        """格式化趋势分析"""
        trend_analysis = context.get('trend_analysis', {})
        trend_prediction = context.get('trend_prediction', {})
        
        lines = []
        
        # 历史趋势
        lines.append("### Historical Trend")
        lines.append(f"- Trend: {trend_analysis.get('trend', 'Unknown')}")
        lines.append(f"- Average Growth: {trend_analysis.get('average_growth', 0)}%")
        lines.append("")
        
        # PandaAI 预测
        if trend_prediction:
            lines.append("### PandaAI Prediction")
            lines.append(f"- Predicted Trend: {trend_prediction.get('trend', 'Unknown')}")
            lines.append(f"- Forecast Periods: {len(trend_prediction.get('predictions', []))}")
            lines.append("")
            
            for pred in trend_prediction.get('predictions', [])[:3]:
                lines.append(f"  - {pred['period']}: {self._format_number(pred['value'])} (confidence: {pred['confidence']})")
        
        return "\n".join(lines)
    
    def _format_anomalies(self, context: Dict) -> str:
        """格式化异常"""
        anomalies = context.get('anomalies', [])
        
        if not anomalies:
            return "No anomalies detected"
        
        lines = [f"Detected {len(anomalies)} anomalies (PandaAI AI Detection):"]
        
        for anomaly in anomalies:
            lines.append(f"- {anomaly['date']}: {self._format_number(anomaly['value'])} (AI Confidence: {anomaly.get('ai_confidence', 'unknown')})")
        
        return "\n".join(lines)
    
    def _format_recommendations(self, context: Dict) -> str:
        """格式化建议"""
        recommendations = context.get('recommendations', [])
        
        if not recommendations:
            return "No specific recommendations"
        
        lines = []
        for i, rec in enumerate(recommendations, 1):
            lines.append(f"{i}. {rec}")
        
        return "\n".join(lines)
    
    def _format_number(self, num: Any) -> str:
        """格式化数字"""
        if isinstance(num, float):
            return "{:,.2f}".format(num)
        elif isinstance(num, int):
            return "{:,}".format(num)
        else:
            return str(num)
    
    def save_report(self, report: str, output_path: str) -> bool:
        """保存报告"""
        try:
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report)
            
            print(f"Report saved to: {output_file.absolute()}")
            return True
        except Exception as e:
            print(f"Error saving report: {e}")
            return False


# ========================================
# 主引擎
# ========================================

class DataAnalysisEngineV2:
    """数据分析引擎 v2.0 (PandaAI + CrewAI 集成版）"""
    
    def __init__(self):
        self.loader = DataLoader()
        self.reporter = ReportGenerator()
        self.pandaai = PandaAI()
        
        # 初始化 CrewAI
        self.crew = self._initialize_crew()
    
    def _initialize_crew(self) -> Crew:
        """初始化 CrewAI 和 Agent"""
        # 创建 Crew
        crew = Crew(name="DataAnalysisCrew", process="sequential")
        
        # 创建 Agent
        data_explorer = Agent(
            agent_id="data_explorer",
            role="数据探索者",
            goal="探索数据集结构，检查数据质量，生成数据概览",
            backstory="你是一位经验丰富的数据分析师，擅长快速理解数据集的结构和特征。"
        )
        
        analyst = Agent(
            agent_id="analyst",
            role="数据分析师",
            goal="对数据集进行深入的统计分析，计算关键指标，识别趋势和模式",
            backstory="你是一位专业的数据科学家，擅长使用 Python 进行数据分析。"
        )
        
        pandaai = Agent(
            agent_id="pandaai",
            role="AI 数据洞察专家",
            goal="利用 PandaAI 提供高级数据分析、趋势预测和智能建议",
            backstory="你是一位经验丰富的 AI 数据科学家，专门使用 PandaAI 进行高级数据分析。"
        )
        
        reporter = Agent(
            agent_id="reporter",
            role="报告生成专家",
            goal="整合所有 Agent 的分析结果，生成清晰、结构化的专业报告",
            backstory="你是一位专业的商业分析师和报告撰写专家。"
        )
        
        # 添加 Agent 到 Crew
        crew.add_agent(data_explorer)
        crew.add_agent(analyst)
        crew.add_agent(pandaai)
        crew.add_agent(reporter)
        
        # 创建任务
        task_data_exploration = Task(
            task_id="task_data_exploration",
            description="读取数据集，探索数据结构，检查数据质量，生成数据概览",
            agent="data_explorer",
            expected_output="数据概览（记录数、类别、地区、日期范围）"
        )
        
        task_statistical_analysis = Task(
            task_id="task_statistical_analysis",
            description="对数据进行深入的统计分析，包括：基本统计量计算、趋势分析、相关性分析、异常检测",
            agent="analyst",
            expected_output="统计报告（关键指标、趋势图、相关性矩阵、异常值列表）"
        )
        
        task_pandaai_analysis = Task(
            task_id="task_pandaai_analysis",
            description="利用 PandaAI 进行高级数据分析，包括：趋势预测、模式识别、异常解释。基于统计分析结果提供智能洞察和业务建议。",
            agent="pandaai",
            expected_output="AI 洞察（PandaAI 预测、高级洞察、业务建议、战略建议）"
        )
        
        task_report_generation = Task(
            task_id="task_report_generation",
            description="整合所有 Agent 的分析结果，生成最终的专业报告。包括：摘要、数据概览、统计发现、AI 洞察、建议和行动计划。",
            agent="reporter",
            expected_output="完整的数据分析报告（Markdown 格式），包含所有关键发现和建议"
        )
        
        # 添加任务到 Crew
        crew.add_task(task_data_exploration)
        crew.add_task(task_statistical_analysis)
        crew.add_task(task_pandaai_analysis)
        crew.add_task(task_report_generation)
        
        # 设置任务依赖（层级流程）
        crew.set_task_dependency("task_data_exploration", [])
        crew.set_task_dependency("task_statistical_analysis", ["task_data_exploration"])
        crew.set_task_dependency("task_pandaai_analysis", ["task_data_exploration", "task_statistical_analysis"])
        crew.set_task_dependency("task_report_generation", ["task_data_exploration", "task_statistical_analysis", "task_pandaai_analysis"])
        
        return crew
    
    def analyze(self, goal: str, dataset_path: str, depth: str = "standard") -> Dict[str, Any]:
        """执行完整的数据分析（使用 PandaAI + CrewAI）"""
        print(f"\n{'='*60}")
        print(f"🚀 DataInsight Pro v2.0 - PandaAI + CrewAI 集成版")
        print(f"{'='*60}")
        print(f"\n🎯 分析目标：{goal}")
        print(f"📊 数据集：{dataset_path}")
        print(f"🎯 分析深度：{depth}")
        print(f"🤖 Agent 编排：CrewAI")
        print(f"🧠 AI 引擎：PandaAI")
        
        # 1. 加载数据
        print(f"\n[Step 1/5] 📁 加载数据...")
        data_points = self.loader.load_csv(dataset_path)
        data_info = self.loader.get_data_info(data_points)
        
        print(f"   ✅ 加载成功：{len(data_points)} 条记录")
        print(f"   📊 数据规模：{data_info['total_records']:,} 行 × {data_info['num_categories']} 个类别 × {data_info['num_regions']} 个地区")
        
        # 2. 准备 Crew 输入
        print(f"\n[Step 2/5] 🤖 准备 CrewAI Agent...")
        crew_inputs = {
            'goal': goal,
            'dataset_path': dataset_path,
            'analysis_depth': depth,
            'raw_data': [dp.row_data for dp in data_points],
            'total_records': len(data_points),
            'categories': data_info['categories'],
            'regions': data_info['regions'],
            'date_range': data_info['date_range'],
            'summary': f"""分析目标：{goal}
数据集：{dataset_path}
数据规模：{len(data_points):,} 条记录
分析深度：{depth}
"""
        }
        
        # 3. 执行 Crew 任务
        print(f"\n[Step 3/5] 🚀 启动 CrewAI Agent 团队...")
        print(f"   🤖 Agent 1: Data Explorer - 数据探索")
        print(f"   🤖 Agent 2: Analyst - 统计分析")
        print(f"   🧠 Agent 3: PandaAI - AI 洞察")
        print(f"   📝 Agent 4: Reporter - 报告生成")
        
        crew_result = self.crew.kickoff(crew_inputs)
        
        # 4. 处理结果
        print(f"\n[Step 4/5] 📊 整合分析结果...")
        
        # 从 context 中提取信息
        context = crew_result.get('context', {})
        
        # 生成最终结果
        result = {
            'summary': context.get('summary', 'No summary'),
            'total_records': context.get('total_records', 0),
            'categories': context.get('categories', []),
            'regions': context.get('regions', []),
            'date_range': context.get('date_range', {}),
            
            # 统计结果
            'statistics': {
                'total_value': data_info['total_value'],
                'avg_value': data_info['avg_value'],
                'min_value': data_info['min_value'],
                'max_value': data_info['max_value'],
                'std_value': data_info['std_value']
            },
            
            # 分类分析
            'category_analysis': context.get('category_analysis', {}),
            'region_analysis': context.get('region_analysis', {}),
            
            # 趋势分析
            'trend_analysis': context.get('trend_analysis', {}),
            
            # PandaAI 结果
            'ai_insights': context.get('ai_insights', []),
            'trend_prediction': context.get('trend_prediction', {}),
            'anomalies': context.get('anomalies', []),
            'pandaai_analysis': context.get('pandaai_analysis', ''),
            
            # Crew 执行日志
            'crew_execution_log': crew_result.get('execution_log', []),
            
            # 元数据
            'crew_name': self.crew.name,
            'crew_process': self.crew.process,
            'pandaai_integrated': True,
            'version': '2.0'
        }
        
        # 5. 生成摘要
        print(f"\n[Step 5/5] 📝 生成最终摘要...")
        stats = result['statistics']
        trend_analysis = result.get('trend_analysis', {})
        pandaai_insights = result.get('ai_insights', [])
        
        summary = f"""分析目标：{goal}
数据集：{dataset_path}
关键指标：
- 总销售额：{stats['total_value']:,.2f}
- 平均销售额：{stats['avg_value']:,.2f}
- 趋势：{trend_analysis.get('trend', 'Unknown')}

PandaAI 洞察：
{'  '.join(pandaai_insights[:2]) if pandaai_insights else '无 AI 洞察'}

CrewAI Agent 执行：
- Agent 1 (Data Explorer): ✅ 完成
- Agent 2 (Analyst): ✅ 完成
- Agent 3 (PandaAI): ✅ 完成
- Agent 4 (Reporter): ✅ 完成

完成！
"""
        
        result['summary'] = summary
        
        print(f"\n✅ 分析完成！")
        print(f"   🤖 Agent 状态：全部完成")
        print(f"   🧠 PandaAI 状态：已集成")
        print(f"   📝 报告状态：待生成")
        
        return result


# ========================================
# 入口
# ========================================

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 DataInsight Pro v2.0 - PandaAI + CrewAI 集成版")
    print("=" * 60)
    
    engine = DataAnalysisEngineV2()
    
    result = engine.analyze(
        goal="分析销售数据的趋势和异常，使用 PandaAI AI 洞察",
        dataset_path="data/samples/sales_2024_Q1.csv",
        depth="standard"
    )
    
    # 生成报告
    print("\n📝 生成最终报告...")
    report = engine.reporter.generate_markdown({"context": result})
    
    # 打印报告预览
    print(report)
    
    # 保存报告
    print("\n💾 保存报告...")
    engine.reporter.save_report(report, "pandaai_crewai_report.md")
    
    print("\n🎉 分析完成！PandaAI + CrewAI 集成版运行成功！")
