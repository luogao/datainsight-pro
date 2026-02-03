# 任务输出目录结构说明

## 概述

每次分析任务都会在 `web/outputs/` 目录下创建一个独立的文件夹，以任务 ID 命名，包含该任务所有中间和最终的分析结果。

## 目录结构

```
web/outputs/
├── {task_id}/                           # 任务专用文件夹
│   ├── data_exploration.md              # 数据探索 Agent 输出
│   ├── statistical_analysis.md          # 统计分析 Agent 输出
│   ├── pandaai_analysis.md              # PandaAI Agent 输出
│   ├── final_report.md                  # 最终整合报告
│   └── execution_log.txt                # CrewAI 执行日志
└── ...
```

## 文件说明

### 1. data_exploration.md
- **生成者**: Data Explorer Agent
- **内容**:
  - 数据集基本信息（行数、列数、字段名）
  - 数据类型分布
  - 缺失值统计
  - 数据质量评估
  - 前 10 行预览
  - 数值列基本统计

### 2. statistical_analysis.md
- **生成者**: Analyst Agent
- **内容**:
  - 基本统计量（均值、中位数、标准差等）
  - 时间序列趋势分析
  - 变量相关性分析
  - 异常值检测结果
  - 图表配置建议

### 3. pandaai_analysis.md
- **生成者**: PandaAI Agent
- **内容**:
  - AI 智能问答结果
  - 数据清洗报告
  - 模式识别洞察
  - 趋势预测
  - 可视化建议

### 4. final_report.md
- **生成者**: Reporter Agent
- **内容**:
  - 执行摘要
  - 数据概览
  - 统计发现
  - PandaAI 洞察
  - 综合建议
  - 附录（技术细节）

### 5. execution_log.txt
- **生成者**: 系统
- **内容**:
  - 任务 ID
  - 数据集路径
  - 分析目标
  - 分析深度
  - 输出格式
  - CrewAI 完整执行结果

## API 访问

### 1. 获取任务文件列表

```bash
GET /tasks/{task_id}/files
```

**响应示例**:
```json
{
  "task_id": "abc-123-def",
  "output_dir": "/path/to/outputs/abc-123-def",
  "files": [
    {
      "name": "data_exploration.md",
      "path": "/path/to/outputs/abc-123-def/data_exploration.md",
      "size": 2048,
      "url": "/tasks/abc-123-def/files/data_exploration.md"
    },
    {
      "name": "final_report.md",
      "path": "/path/to/outputs/abc-123-def/final_report.md",
      "size": 8192,
      "url": "/tasks/abc-123-def/files/final_report.md"
    }
  ]
}
```

### 2. 下载特定文件

```bash
GET /tasks/{task_id}/files/{filename}
```

**示例**:
```bash
# 下载最终报告
curl http://localhost:8000/tasks/abc-123-def/files/final_report.md

# 下载 PandaAI 分析
curl http://localhost:8000/tasks/abc-123-def/files/pandaai_analysis.md
```

### 3. 下载最终报告（兼容旧接口）

```bash
GET /reports/{task_id}/download
```

## 实现细节

### 自动创建目录

```python
# 为每个任务创建独立的输出目录
task_output_dir = OUTPUT_DIR / task_id
task_output_dir.mkdir(exist_ok=True)
```

### 提取任务输出

```python
# CrewAI 的 result 包含 tasks_output 属性
if hasattr(result, 'tasks_output'):
    task_outputs = result.tasks_output

    # 访问每个任务的输出
    for i, task_output in enumerate(task_outputs):
        output = str(task_output.raw if hasattr(task_output, 'raw') else task_output)
        # 保存到对应文件
```

### 进度更新

```python
update_task_status(task_id, "running", 70, "保存中间结果...")
# ... 保存各 Agent 输出 ...
update_task_status(task_id, "running", 90, "生成报告...")
```

## 测试

运行测试脚本验证输出结构:

```bash
python test_output_structure.py
```

## 前端集成建议

### 1. 显示任务文件列表

```typescript
const fetchTaskFiles = async (taskId: string) => {
  const response = await fetch(`/api/tasks/${taskId}/files`);
  const data = await response.json();
  return data.files;
};
```

### 2. 下载特定文件

```typescript
const downloadFile = async (taskId: string, filename: string) => {
  const url = `/api/tasks/${taskId}/files/${filename}`;
  window.open(url, '_blank');
};
```

### 3. 显示文件链接列表

```tsx
<div>
  <h3>分析结果文件</h3>
  <ul>
    {files.map(file => (
      <li key={file.name}>
        <a href={file.url} download={file.name}>
          {file.name} ({(file.size / 1024).toFixed(2)} KB)
        </a>
      </li>
    ))}
  </ul>
</div>
```

## 注意事项

1. **目录自动创建**: 系统会在任务开始时自动创建输出目录
2. **文件覆盖**: 如果任务 ID 重复，新结果会覆盖旧文件
3. **编码格式**: 所有文件使用 UTF-8 编码
4. **错误处理**: 如果某个 Agent 失败，对应的文件可能为空或不存在
5. **磁盘空间**: 长时间运行后，输出目录可能占用较多空间，建议定期清理

## 清理旧任务

```python
import shutil
from pathlib import Path

def clean_old_tasks(output_dir: Path, days: int = 7):
    """删除 N 天前的任务"""
    import time
    cutoff = time.time() - (days * 86400)

    for task_dir in output_dir.iterdir():
        if task_dir.is_dir() and task_dir.stat().st_mtime < cutoff:
            shutil.rmtree(task_dir)
            print(f"已删除: {task_dir.name}")
```

## 未来改进

1. **添加元数据**: 在每个任务文件夹中添加 `metadata.json`，记录任务配置
2. **压缩归档**: 提供将整个任务文件夹打包为 ZIP 的接口
3. **增量更新**: 支持追加到现有任务（而不是覆盖）
4. **搜索功能**: 跨所有任务文件进行全文搜索
