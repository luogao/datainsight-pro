# PRD: AI 大数据自动化分析 Agent

> **项目代号**: DataInsight Pro
> **版本**: v1.0
> **日期**: 2026-02-01
> **状态**: 规划中

---

## 📌 产品定位

基于 **PandaAI** 和 **CrewAI** 构建的智能大数据分析自动化工具，用户只需提供**分析目标**和**数据集**，系统自动完成全流程分析并输出专业结论。

---

## 🎯 核心价值

- **零代码分析** - 用户无需编程，用自然语言描述分析目标
- **自动化流程** - 从数据探索到结论输出，全流程自动执行
- **智能决策** - 结合 AI 能力，提供数据驱动的洞察
- **多场景支持** - 支持销售、用户行为、运营、财务等多种分析场景

---

## 🏗️ 技术栈

| 技术 | 用途 | 说明 |
|------|------|------|
| **PandaAI** | 大数据分析核心 | 提供智能数据洞察、趋势预测、异常检测 |
| **CrewAI** | Agent 编排框架 | 管理多个 AI Agent 协作，处理复杂分析流程 |
| **Python** | 开发语言 | 主要开发语言 |
| **FastAPI** | Web API（可选） | 提供 HTTP 接口 |
| **Streamlit** | Web UI（可选） | 简单的交互界面 |

---

## 🎬 核心功能

### 1. 用户输入

```yaml
分析目标:
  - 描述: 用自然语言描述分析目标
  - 示例: "分析最近一个季度的销售数据，找出趋势和异常"
  - 示例: "分析用户留存率，找出影响留存的关键因素"

数据集:
  - 格式: CSV、JSON、Excel
  - 支持方式:
    - 本地文件上传
    - URL 指定
    - 数据库查询（后期）
  - 示例:
    - 文件: sales_2024_Q1.csv
    - URL: https://example.com/data.json

分析配置:
  - 时间范围: 可选
  - 维度选择: 可选（如地区、产品类别）
  - 分析深度: 快速/标准/深入
```

### 2. Agent 角色设计

CrewAI 将协调以下 Agent 协作：

| Agent | 角色 | 职责 |
|-------|------|------|
| **DataExplorer** | 数据探索者 | 理解数据结构、检查数据质量、生成数据概览 |
| **Analyst** | 数据分析师 | 执行统计分析、计算指标、生成图表 |
| **PandaAI** | 智能洞察者 | 提供高级 AI 洞察、趋势预测、异常检测 |
| **Reporter** | 报告生成者 | 整合所有结果，生成最终报告 |

### 3. 分析流程

```mermaid
graph LR
    A[用户输入] --> B[DataExplorer]
    B --> C[Analyst]
    C --> D[PandaAI]
    D --> E[Reporter]
    E --> F[输出报告]
```

**详细步骤**:

1. **数据探索** (DataExplorer)
   - 读取数据集
   - 分析数据结构（列名、类型）
   - 检查数据质量（缺失值、异常值）
   - 生成数据概览报告

2. **统计分析** (Analyst)
   - 基本统计：均值、中位数、标准差等
   - 趋势分析：时间序列趋势
   - 关联分析：相关性分析
   - 生成可视化图表

3. **AI 洞察** (PandaAI)
   - 使用 PandaAI API 进行高级分析
   - 趋势预测
   - 异常检测
   - 智能建议生成

4. **报告生成** (Reporter)
   - 整合所有分析结果
   - 生成结构化报告
   - 提供可执行的洞察和建议

### 4. 输出格式

**Markdown 报告**:
```markdown
# 数据分析报告

## 📊 数据概览
- 数据规模: 10,000 行
- 时间范围: 2024-01-01 至 2024-03-31
- 字段: 销售额、产品类别、地区、日期

## 📈 关键指标
- 总销售额: ¥1,234,567
- 平均日销售额: ¥13,717
- 同比增长: +15.2%

## 🔍 主要发现
1. **趋势**: 2月份销售额环比下降 10%，可能受春节影响
2. **异常**: 3月15日出现异常高峰，需核实
3. **洞察**: 华东地区贡献最大（45%），华北增长最快（+25%）

## 💡 建议
1. 关注春节前后的营销策略调整
2. 复盘 3 月 15 日的销售高峰
3. 加强华北地区的渠道建设
```

**JSON 结构化输出**:
```json
{
  "summary": "分析摘要",
  "metrics": {"total": 1234567, "growth": 15.2},
  "findings": [...],
  "recommendations": [...],
  "charts": [
    {
      "type": "line",
      "data": {...},
      "title": "销售额趋势"
    }
  ]
}
```

---

## 🚀 开发计划

### Phase 1: 基础框架 (Day 1-2)
- [ ] 项目初始化和环境配置
- [ ] CrewAI 基础框架搭建
- [ ] PandaAI API 集成
- [ ] 数据读取模块

### Phase 2: Agent 实现 (Day 3-4)
- [ ] DataExplorer Agent 实现
- [ ] Analyst Agent 实现
- [ ] PandaAI Agent 实现
- [ ] Reporter Agent 实现
- [ ] Agent 协作流程编排

### Phase 3: 功能完善 (Day 5-6)
- [ ] 多种数据格式支持
- [ ] 可视化图表生成
- [ ] 报告模板设计
- [ ] 错误处理和日志

### Phase 4: 测试和优化 (Day 7)
- [ ] 单元测试
- [ ] 集成测试
- [ ] 性能优化
- [ ] 文档完善

---

## 📦 交付物

### 代码
- 完整的 Python 项目代码
- CrewAI Agent 定义
- PandaAI 集成模块
- 配置文件和示例

### 文档
- 项目 README
- API 文档
- 使用指南
- 示例数据集

### 测试
- 功能测试用例
- 性能测试报告
- 示例运行演示

---

## 🔧 技术架构

### 目录结构
```
data-analysis-agent/
├── src/
│   ├── agents/          # CrewAI Agent 定义
│   │   ├── data_explorer.py
│   │   ├── analyst.py
│   │   ├── pandaai.py
│   │   └── reporter.py
│   ├── tools/           # 工具函数
│   │   ├── data_loader.py
│   │   ├── analyzer.py
│   │   └── visualizer.py
│   ├── crew.py          # CrewAI 编排
│   └── main.py         # 主入口
├── config/             # 配置文件
│   ├── pandaai.yaml
│   └── crewai.yaml
├── data/               # 示例数据
│   └── samples/
├── tests/              # 测试
├── docs/               # 文档
├── requirements.txt
└── README.md
```

### 配置文件

**pandaai.yaml**:
```yaml
pandaai:
  api_key: "YOUR_API_KEY"
  endpoint: "https://api.pandaai.com"
  timeout: 30
```

**crewai.yaml**:
```yaml
crewai:
  model: "gpt-4"
  verbose: true
  max_iter: 10
```

---

## 🎨 用户使用流程

### 方式 1: 命令行

```bash
python main.py \
  --goal "分析最近一个季度的销售数据，找出趋势和异常" \
  --dataset data/sales_2024_Q1.csv \
  --output report.md
```

### 方式 2: 交互式

```bash
python main.py --interactive

> 请输入分析目标:
分析用户留存率，找出影响留存的关键因素

> 请输入数据集路径:
data/user_retention.csv

> 分析深度:
深入

[分析进行中...]

> 分析完成！报告已保存到: report.md
```

---

## ⚠️ 风险和限制

### 技术风险
- PandaAI API 可用性和速率限制
- 大数据集的性能问题
- CrewAI Agent 协作的复杂度

### 数据限制
- 数据集大小建议 < 1GB
- 单次分析列数建议 < 50 列

---

## 📊 成功指标

- ✅ 能够处理 CSV/JSON/Excel 格式
- ✅ 完成一次端到端分析时间 < 5 分钟（小数据集）
- ✅ 报告准确率 > 80%（通过人工评估）
- ✅ 代码测试覆盖率 > 70%

---

## 🎯 Milestones

| 里程碑 | 目标 | 预计完成 |
|--------|------|----------|
| M1 | 项目框架搭建 | Day 2 |
| M2 | Agent 基础功能 | Day 4 |
| M3 | 完整分析流程 | Day 6 |
| M4 | 测试和优化 | Day 7 |

---

## 📝 备注

- 需要先申请 PandaAI API Key
- CrewAI 需要 OpenAI API Key（或兼容模型）
- 项目初期以 MVP 形式交付，后续迭代优化
