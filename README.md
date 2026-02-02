# 🚀 DataInsight Pro - AI 大数据自动化分析 Agent

> **版本**: v1.0
> **状态**: 开发完成 🎉
> **日期**: 2026-02-01

---

## 📌 项目简介

基于 **PandaAI** 和 **CrewAI** 构建的智能大数据分析自动化工具。用户只需提供**分析目标**和**数据集**，系统自动完成全流程分析并输出专业结论。

---

## ✨ 核心特性

- ✅ **零代码分析** - 用自然语言描述分析目标
- ✅ **自动化流程** - 数据探索 → 统计分析 → AI 洞察 → 报告生成
- ✅ **多 Agent 协作** - DataExplorer、Analyst、PandaAI、Reporter 四个 Agent 协同工作
- ✅ **多种数据格式** - 支持 CSV、JSON、Excel
- ✅ **交互式/命令行** - 支持两种使用方式
- ✅ **多深度分析** - 快速、标准、深入三种分析模式

---

## 🏗️ 技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| **Python** | 3.10+ | 主要开发语言 |
| **PandaAI** | v2+ | 高级 AI 数据分析 |
| **CrewAI** | 0.1+ | Agent 编排框架 |
| **LangChain** | 0.1+ | LLM 集成框架 |
| **Pandas** | 2.0+ | 数据处理 |
| **NumPy** | 1.24+ | 数值计算 |
| **Matplotlib/Seaborn** | 3.7+/0.12+ | 数据可视化 |
| **OpenAI GPT-4** | v4+ | LLM 模型（可配置） |

---

## 🎨 Web UI 特性

✅ **现代化界面** - 深色主题 + 渐变设计
✅ **拖拽上传** - 支持 CSV、JSON、Excel
✅ **实时进度** - 可视化分析进度条
✅ **预览模式** - Markdown 渲染 + 源码查看
✅ **响应式设计** - 适配各种屏幕

访问 http://localhost:3000 体验 Web UI。

## 📦 项目结构

```
data-analysis-agent/
├── src/
│   ├── agents/          # CrewAI Agent 定义
│   │   ├── data_explorer.py   # 数据探索者
│   │   ├── analyst.py        # 数据分析师
│   │   ├── pandaai.py        # AI 洞察者
│   │   └── reporter.py       # 报告生成者
│   ├── tools/           # 工具函数
│   │   ├── data_loader.py    # 数据加载和清理
│   │   └── statistical_analyzer.py  # 统计分析
│   ├── crew.py          # CrewAI 编排
│   └── __init__.py
├── config/             # 配置文件
│   └── settings.yaml
├── data/               # 数据目录
│   └── samples/
│       └── sales_2024_Q1.csv  # 示例数据
├── docs/               # 文档
│   └── PRD.md           # 产品需求文档
├── tests/              # 测试
├── main.py             # 主入口程序
├── requirements.txt    # 依赖列表
└── README.md           # 本文件
```

---

## 🎯 快速开始

### Web UI（推荐）

最简单的使用方式是通过 Web 界面：

```bash
# 一键启动 Web UI（Linux/macOS）
./start-web.sh

# Windows
start-web.bat
```

然后访问 http://localhost:3000 使用可视化界面。

详细文档见：[web/QUICKSTART.md](web/QUICKSTART.md)

### 命令行模式

### 1. 环境配置

#### 安装依赖

```bash
cd data-analysis-agent
pip install -r requirements.txt
```

#### 配置 API Keys

创建 `.env` 文件：

```bash
# PandaAI API Key
PANDAAI_API_KEY=your_pandaai_api_key_here

# OpenAI API Key（CrewAI 需要）
OPENAI_API_KEY=your_openai_api_key_here
```

或者设置环境变量：

```bash
export PANDAAI_API_KEY="your_api_key"
export OPENAI_API_KEY="your_api_key"
```

### 2. 运行分析

#### 交互式模式（推荐）

```bash
python main.py --interactive
```

你会看到：
```
==============================================================
🚀 DataInsight Pro - AI 数据分析 Agent
==============================================================

请提供分析信息：

📋 分析目标（用自然语言描述）：
> 分析最近一个季度的销售数据，找出趋势和异常

📁 数据集路径（文件路径或 URL）：
> data/samples/sales_2024_Q1.csv

🎯 分析深度 [quick/standard/deep，默认：standard]：
> standard

📤 输出文件路径 [默认：report.md]：
> report.md

✅ 分析任务：分析最近一个季度的销售数据，找出趋势和异常
📊 数据集：data/samples/sales_2024_Q1.csv
🎯 深度：standard
📤 输出：report.md

开始分析...
```

#### 命令行模式

```bash
# 分析销售数据
python main.py \
  --goal "分析最近一个季度的销售数据，找出趋势和异常" \
  --dataset data/samples/sales_2024_Q1.csv

# 深入分析用户留存
python main.py \
  --goal "分析用户留存率，找出影响留存的关键因素" \
  --dataset data/user_retention.csv \
  --depth deep

# 分析并保存到指定文件
python main.py \
  --goal "分析产品销量和用户行为" \
  --dataset data/products.csv \
  --output products_report.md \
  --format json
```

### 3. 查看报告

分析完成后，报告会保存到指定位置（默认 `report.md`），包含：

- 📊 **数据概览** - 数据规模、字段类型、质量评估
- 📈 **统计发现** - 关键指标、趋势分析、相关性
- 🧠 **AI 洞察** - PandaAI 提供的智能分析和建议
- 💡 **业务建议** - 可执行的行动计划
- 📋 **行动计划** - 优先级排序的建议清单

---

## 🤖 Agent 协作流程

```
用户输入
    │
    ▼
Data Explorer (数据探索者)
    │  ├── 读取数据集
    │  ├── 检查数据质量
    │  └── 生成数据概览
    │
    ▼
Analyst (数据分析师)
    │  ├── 基本统计
    │  ├── 趋势分析
    │  ├── 相关性分析
    │  └── 异常检测
    │
    ▼
PandaAI (AI 洞察者)
    │  ├── 高级洞察
    │  ├── 趋势预测
    │  ├── 异常解释
    │  └── 业务建议
    │
    ▼
Reporter (报告生成者)
    │  ├── 整合结果
    │  ├── 生成报告
    │  └── 保存文件
    │
    ▼
最终报告 (Markdown/JSON)
```

---

## 📊 功能详解

### 1. 数据探索 (Data Explorer)

- 📁 读取多种数据格式（CSV、JSON、Excel）
- 🔍 分析数据结构和类型
- ✅ 检查数据质量（缺失值、重复值、异常值）
- 📋 生成数据概览报告

### 2. 统计分析 (Analyst)

- 📊 基本统计（均值、中位数、标准差等）
- 📈 趋势分析（时间序列、环比/同比增长）
- 🔗 相关性分析（Pearson 相关系数）
- 🔍 异常检测（标准差法、四分位距法）
- 📉 生成可视化图表配置

### 3. AI 洞察 (PandaAI)

- 🧠 高级数据洞察（模式识别）
- 🔮 趋势预测（未来值预测）
- 🚨 异常解释（为什么异常）
- 💡 业务建议（可执行的洞察）
- 📈 战略建议（长期发展规划）

### 4. 报告生成 (Reporter)

- 📝 整合所有 Agent 的结果
- 🎯 提取关键发现和建议
- 📋 生成可执行的行动计划
- 📤 支持多种输出格式（Markdown、JSON）
- 💾 自动保存到文件

---

## 📖 使用示例

### 示例 1: 销售数据分析

**输入**:
```
目标：分析最近一个季度的销售数据，找出趋势和异常
数据：data/samples/sales_2024_Q1.csv
```

**输出**:
- 📊 总销售额：¥1,234,567
- 📈 平均日销售额：¥13,717
- 📉 同比增长：+15.2%
- 🔍 发现 1 个异常点：3月 15 日销售额异常高
- 💡 建议：关注春节前后营销策略调整

### 示例 2: 用户留存分析

**输入**:
```
目标：分析用户留存率，找出影响留存的关键因素
数据：data/user_retention.csv
深度：深入
```

**输出**:
- 📊 总用户数：10,000
- 📈 7 日留存率：45.3%
- 🔍 关键影响因素：首次使用时长、活跃度、地区
- 💡 建议：加强用户引导，优化早期体验

---

## ⚙️ 配置说明

### 分析深度

- **quick** - 快速分析（基础统计 + 简单洞察）
- **standard** - 标准分析（完整统计 + AI 洞察）- **deep** - 深入分析（高级统计 + 预测 + 战略建议）

### 输出格式

- **markdown** - Markdown 格式报告（默认）
- **json** - JSON 格式结构化数据
- **both** - 同时生成 Markdown 和 JSON

### 高级配置

编辑 `config/settings.yaml`：

```yaml
data:
  max_rows: 100000      # 最大行数
  max_columns: 100       # 最大列数
  sample_size: 1000      # 采样大小

analysis:
  default_confidence: 0.8      # 置信度
  trend_window: 7              # 趋势窗口（天）
  anomaly_threshold: 2         # 异常阈值（标准差）

report:
  output_dir: "outputs"
  include_charts: true
  chart_format: "png"
```

---

## 🧪 测试

### 运行测试套件

```bash
# 单元测试
python -m pytest tests/

# 集成测试
python main.py --goal "测试分析" --dataset data/samples/sales_2024_Q1.csv --dry-run
```

### 快速测试

使用示例数据运行一次完整分析：

```bash
python main.py \
  --goal "分析示例销售数据的趋势和模式" \
  --dataset data/samples/sales_2024_Q1.csv \
  --output test_report.md
```

---

## 📝 API Keys 获取

### PandaAI

1. 访问 https://pandaai.com/
2. 注册账号并登录
3. 进入 API Keys 页面
4. 创建新的 API Key
5. 复制并保存到 `.env` 文件

### OpenAI (CrewAI 需要)

1. 访问 https://platform.openai.com/
2. 登录或注册账号
3. 进入 API Keys 页面
4. 创建新的 Secret Key
5. 复制并保存到 `.env` 文件

---

## 🚨 常见问题

### Q: PandaAI API 调用失败？

**A**: 检查：
- API Key 是否正确
- 网络连接是否正常
- API 额度是否超限

### Q: 数据加载失败？

**A**: 检查：
- 文件路径是否正确
- 文件格式是否支持（CSV、JSON、Excel）
- 文件是否损坏

### Q: 分析速度很慢？

**A**: 尝试：
- 减小数据集大小（采样）
- 使用 `quick` 分析深度
- 检查网络连接

### Q: 报告生成失败？

**A**: 检查：
- 输出目录是否有写入权限
- 磁盘空间是否充足
- 文件名是否包含非法字符

---

## 🔄 更新日志

### v1.0.0 (2026-02-01)

- ✅ 初始版本发布
- ✅ 4 个 Agent 协作框架
- ✅ 支持多种数据格式
- ✅ 交互式和命令行两种使用方式
- ✅ 完整的分析流程
- ✅ Markdown 和 JSON 报告输出

---

## 📄 许可证

MIT License

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📧 联系方式

- **项目主页**: https://github.com/your-org/data-insight-pro
- **文档**: https://docs.data-insight-pro.com
- **支持**: support@data-insight-pro.com

---

**🚀 现在开始你的数据探索之旅吧！**
