#!/usr/bin/env python3
"""
DataInsight Pro - Web API Backend
FastAPI 后端服务
"""
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any
import os
import sys
import json
import uuid
from pathlib import Path
from datetime import datetime
import asyncio
import pandas as pd

# 添加项目根目录到路径（web/backend -> 项目根目录）
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.crew_v2 import create_crew
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

app = FastAPI(
    title="DataInsight Pro API",
    description="AI 大数据自动化分析 Agent API",
    version="1.0.0"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该限制具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 存储分析任务状态
tasks: Dict[str, Dict[str, Any]] = {}
UPLOAD_DIR = Path(__file__).parent.parent / "uploads"
OUTPUT_DIR = Path(__file__).parent.parent / "outputs"

# 确保目录存在
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)


# 数据模型
class AnalysisRequest(BaseModel):
    goal: str
    dataset_path: str
    depth: str = "standard"
    output_format: str = "markdown"


class TaskStatus(BaseModel):
    task_id: str
    status: str  # pending, running, completed, failed
    progress: int  # 0-100
    current_step: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    created_at: str
    updated_at: str


def update_task_status(task_id: str, status: str, progress: int, current_step: str, result: Optional[Dict] = None, error: Optional[str] = None):
    """更新任务状态"""
    if task_id in tasks:
        tasks[task_id]['status'] = status
        tasks[task_id]['progress'] = progress
        tasks[task_id]['current_step'] = current_step
        tasks[task_id]['updated_at'] = datetime.now().isoformat()
        if result:
            tasks[task_id]['result'] = result
        if error:
            tasks[task_id]['error'] = error


async def run_analysis_task(task_id: str, goal: str, dataset_path: str, depth: str, output_format: str):
    """后台运行分析任务"""
    try:
        update_task_status(task_id, "running", 10, "初始化分析...")

        # 导入已配置好的 Agents（它们已经有正确的 tools）
        from src.agents.data_explorer_v2 import data_explorer
        from src.agents.analyst_v2 import analyst
        from src.agents.pandaai_real import pandaai_agent
        from src.agents.reporter_v2 import reporter

        update_task_status(task_id, "running", 20, "加载数据探索 Agent...")

        # 创建 Crew
        from crewai import Crew, Process, Task

        # 定义任务（直接使用文件路径）
        task_data_exploration = Task(
            description=f"""读取数据集 {dataset_path}，执行以下操作：

1. 使用 read_csv_dataset 工具读取数据
2. 使用 check_data_quality 检查数据质量
3. 使用 generate_data_summary 生成数据概览

重要：明确记录数据集路径 {dataset_path} 在输出中。
""",
            expected_output="数据集概览报告，包含：数据规模、字段类型、质量评估、样本数据",
            agent=data_explorer
        )

        task_statistical_analysis = Task(
            description=f"""对数据集 {dataset_path} 进行深入的统计分析：

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
            agent=analyst
        )

        task_pandaai_analysis = Task(
            description=f"""利用 PandaAI 对数据集 {dataset_path} 进行高级 AI 分析：

分析目标：{goal}

请执行以下分析（重要：直接传递文件路径给工具）：
1. pandaai_chat(question="请帮我分析这个数据集的基本特征", file_path="{dataset_path}")
2. pandaai_clean_data(file_path="{dataset_path}")
3. pandaai_analyze_patterns(file_path="{dataset_path}")
4. pandaai_predict_trend(file_path="{dataset_path}")
5. pandaai_generate_chart(file_path="{dataset_path}", chart_type="line")
6. pandaai_data_summary(file_path="{dataset_path}")

重要说明：所有 PandaAI 工具都需要 file_path 参数，直接传递文件路径即可。
工具会自动读取数据并进行分析。
""",
            expected_output="PandaAI 分析报告，包含：智能问答结果、数据清洗报告、模式识别洞察、趋势预测、可视化建议",
            agent=pandaai_agent
        )

        # 定义输出路径（需要在创建任务前）
        output_path = OUTPUT_DIR / f"{task_id}_report.{output_format}" if output_format == 'json' else OUTPUT_DIR / f"{task_id}_report.md"

        task_report = Task(
            description=f"""整合所有 Agent 的分析结果，生成最终的专业报告。

分析目标：{goal}
数据集：{dataset_path}
分析深度：{depth}

报告应包含：
1. **执行摘要** - 基于分析目标 {goal} 的高层总结
2. **数据概览** - 来自前一个任务的数据概况
3. **统计发现** - 来自统计分析任务的结果
4. **PandaAI 洞察** - 来自 PandaAI 分析任务的结果
5. **综合建议** - 可执行的行动计划
6. **附录** - 技术细节、图表配置

使用 format_report_markdown 或 format_report_json 工具生成最终报告。
保存到文件：{output_path}
""",
            expected_output="完整的 Markdown 格式分析报告",
            agent=reporter
        )

        # 创建 Crew
        crew = Crew(
            agents=[data_explorer, analyst, pandaai_agent, reporter],
            tasks=[task_data_exploration, task_statistical_analysis, task_pandaai_analysis, task_report],
            process=Process.sequential,
            verbose=True
        )

        update_task_status(task_id, "running", 30, "开始分析...")

        # 执行分析（不依赖占位符替换）
        result = crew.kickoff()

        update_task_status(task_id, "running", 90, "生成报告...")

        # 读取报告内容
        if output_path.exists():
            if output_format == 'json':
                with open(output_path, 'r', encoding='utf-8') as f:
                    report_content = json.load(f)
            else:
                with open(output_path, 'r', encoding='utf-8') as f:
                    report_content = f.read()
        else:
            report_content = result

        update_task_status(task_id, "completed", 100, "分析完成！", {
            'report_path': str(output_path),
            'report_content': report_content,
            'output_format': output_format
        })

    except Exception as e:
        update_task_status(task_id, "failed", 0, "分析失败", error=str(e))
        import traceback
        print(f"任务 {task_id} 失败: {str(e)}")
        traceback.print_exc()


@app.get("/")
async def root():
    """根路径"""
    return {
        "name": "DataInsight Pro API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """上传数据文件"""
    try:
        # 生成唯一文件名
        file_ext = Path(file.filename).suffix
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        file_path = UPLOAD_DIR / unique_filename

        # 保存文件
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # 尝试读取文件以验证格式
        try:
            if file_ext == '.csv':
                df = pd.read_csv(file_path, nrows=100)
                preview = df.head(10).to_dict(orient='records')
            elif file_ext in ['.xlsx', '.xls']:
                df = pd.read_excel(file_path, nrows=100)
                preview = df.head(10).to_dict(orient='records')
            elif file_ext == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    df = pd.DataFrame(data[:10])
                    preview = df.head(10).to_dict(orient='records')
            else:
                preview = None

            file_info = {
                'rows': len(df) if 'df' in locals() else 0,
                'columns': len(df.columns) if 'df' in locals() else 0,
                'column_names': list(df.columns) if 'df' in locals() else [],
                'preview': preview
            }
        except Exception as e:
            file_info = {'error': f'无法预览文件: {str(e)}'}

        return {
            "filename": file.filename,
            "file_path": str(file_path),
            "size": len(content),
            "file_info": file_info
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件上传失败: {str(e)}")


@app.post("/analyze", response_model=TaskStatus)
async def analyze(
    background_tasks: BackgroundTasks,
    goal: str = Form(...),
    dataset_path: str = Form(...),
    depth: str = Form("standard"),
    output_format: str = Form("markdown")
):
    """启动分析任务"""
    try:
        # 生成任务 ID
        task_id = str(uuid.uuid4())

        # 创建任务
        tasks[task_id] = {
            'task_id': task_id,
            'status': 'pending',
            'progress': 0,
            'current_step': '等待开始...',
            'result': None,
            'error': None,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'goal': goal,
            'dataset_path': dataset_path,
            'depth': depth,
            'output_format': output_format
        }

        # 启动后台任务
        background_tasks.add_task(
            run_analysis_task,
            task_id=task_id,
            goal=goal,
            dataset_path=dataset_path,
            depth=depth,
            output_format=output_format
        )

        return TaskStatus(**tasks[task_id])

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"启动分析失败: {str(e)}")


@app.get("/tasks/{task_id}", response_model=TaskStatus)
async def get_task_status(task_id: str):
    """获取任务状态"""
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="任务不存在")
    return TaskStatus(**tasks[task_id])


@app.get("/tasks")
async def list_tasks():
    """列出所有任务"""
    return {
        "tasks": [
            {
                'task_id': task_id,
                'status': task['status'],
                'progress': task['progress'],
                'created_at': task['created_at']
            }
            for task_id, task in tasks.items()
        ]
    }


@app.get("/reports/{task_id}")
async def get_report(task_id: str):
    """获取分析报告"""
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="任务不存在")

    task = tasks[task_id]
    if task['status'] != 'completed':
        raise HTTPException(status_code=400, detail="任务尚未完成")

    if task['result'] and 'report_content' in task['result']:
        return JSONResponse(content={
            'task_id': task_id,
            'content': task['result']['report_content'],
            'format': task['result'].get('output_format', 'markdown')
        })

    raise HTTPException(status_code=404, detail="报告不存在")


@app.get("/reports/{task_id}/download")
async def download_report(task_id: str):
    """下载报告文件"""
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="任务不存在")

    task = tasks[task_id]
    if task['status'] != 'completed':
        raise HTTPException(status_code=400, detail="任务尚未完成")

    if task['result'] and 'report_path' in task['result']:
        report_path = Path(task['result']['report_path'])
        if report_path.exists():
            return FileResponse(
                path=str(report_path),
                filename=report_path.name,
                media_type='text/markdown'
            )

    raise HTTPException(status_code=404, detail="报告文件不存在")


@app.get("/sample-data")
async def get_sample_data():
    """获取示例数据列表"""
    sample_dir = Path(__file__).parent.parent / "data" / "samples"
    samples = []

    if sample_dir.exists():
        for file in sample_dir.glob("*"):
            if file.is_file():
                samples.append({
                    'name': file.name,
                    'path': str(file),
                    'size': file.stat().st_size
                })

    return {"samples": samples}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
