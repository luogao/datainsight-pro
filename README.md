# 🚀 DataInsight Pro - AI 大数据自动化分析 Agent

> **版本**: v2.0
> **状态**: 生产就绪 ✅
> **更新**: 2026-02-03

---

## 📌 项目简介

基于 **PandaAI** 和 **CrewAI** 构建的智能大数据分析自动化工具。用户只需提供**分析目标**和**数据集**，系统自动完成全流程分析并输出专业结论。

### 🎯 核心优势

- ✅ **100% AI 驱动** - 所有分析结论由 LLM 基于真实数据自主生成，无硬编码
- ✅ **零代码分析** - 用自然语言描述分析目标
- ✅ **多 Agent 协作** - 4 个专业 Agent 协同工作
- ✅ **真实数据分析** - 支持统计计算、相关性分析、趋势预测
- ✅ **可配置 LLM** - 支持任何 OpenAI 兼容 API（DeepSeek、智谱等）

---

## ✨ 核心特性

### 🤖 AI 驱动的分析

- **数据探索** - 自动读取数据、检查质量、生成概览
- **统计分析** - 计算统计量、相关性、趋势分析
- **AI 洞察** - PandaAI 深度分析、模式识别、异常检测
- **报告生成** - LLM 整合所有结果，生成可执行建议

### 🔧 灵活的配置

- **自定义 LLM** - 支持任何 OpenAI 兼容的 API
- **多种数据格式** - CSV、JSON、Excel
- **三种分析深度** - 快速、标准、深入
- **两种使用方式** - 命令行、交互式

---

## 🏗️ 技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| **Python** | 3.10+ | 主要开发语言 |
| **PandaAI** | Latest | AI 数据分析 |
| **CrewAI** | 1.9+ | Agent 编排框架 |
| **LangChain** | Latest | LLM 集成 |
| **Pandas** | 1.5+ | 数据处理 |
| **NumPy** | Latest | 数值计算 |

---

## 📁 项目结构

```
DataInsight-Pro/
├── main_v2.py                 # 主程序入口
├── start_v2.sh                # 快速启动脚本
├── install_deps.sh            # 依赖安装脚本
├── requirements.txt           # Python 依赖
│
├── src/
│   ├── crew_config.py         # LLM 配置
│   └── crew_v2.py             # CrewAI 配置
│
├── src/agents/
│   ├── data_explorer_v2.py    # 数据探索 Agent
│   ├── analyst_v2.py          # 统计分析 Agent
│   ├── pandaai_real.py        # PandaAI Agent
│   └── reporter_v2.py         # 报告生成 Agent
│
├── data/samples/
│   └── sales_2024_Q1.csv      # 示例数据集
│
└── 文档/
    ├── README.md                      # 本文件
    ├── FINAL_TEST_REPORT.md           # 测试报告
    ├── AI_DRIVEN_ANALYSIS_VERIFICATION.md  # AI 驱动验证
    └── NO_HARDCODING_GUARANTEE.md      # 无硬编码保证
```

---

## 🚀 快速开始

### 1. 安装依赖

```bash
bash install_deps.sh
```

或手动安装：

```bash
pip install -r requirements.txt
```

### 2. 配置环境

创建 `.env` 文件：

```bash
# OpenAI 兼容的 API 配置
OPENAI_API_KEY=your_api_key_here
OPENAI_BASE_URL=https://open.bigmodel.cn/api/paas/v4  # 智谱 AI
OPENAI_MODEL=glm-4.7
```

支持的 API：
- **智谱 AI** (GLM-4): `https://open.bigmodel.cn/api/paas/v4`
- **DeepSeek**: `https://api.deepseek.com/v1`
- **OpenAI**: `https://api.openai.com/v1`
- 其他兼容 OpenAI 的 API

### 3. 运行分析

#### 方式一：命令行模式

```bash
python main_v2.py \
  --dataset data/samples/sales_2024_Q1.csv \
  --goal "分析销售趋势，找出最佳销售策略"
```

#### 方式二：使用启动脚本

```bash
bash start_v2.sh
```

### 4. 查看报告

分析完成后，报告保存在 `report.md`。

---

## 🧪 测试

### 快速验证测试

```bash
python quick_test.py
```

验证：
- ✅ 每个 Agent 能独立读取数据
- ✅ 真实统计分析（非模拟）
- ✅ 无硬编码业务逻辑

### 无硬编码验证

```bash
python verify_no_hardcoding.py
```

创建不同数据集，验证分析结果是否完全不同。

---

## 📊 使用示例

### 示例 1：销售数据分析

```bash
python main_v2.py \
  --dataset data/samples/sales_2024_Q1.csv \
  --goal "分析销售趋势，找出最佳销售策略" \
  --depth standard
```

**生成的报告包含**：
- 📋 数据概览（规模、字段、质量）
- 📈 统计分析（均值、标准差、相关性）
- 🧠 AI 洞察（模式识别、趋势预测）
- 💡 可执行建议（短期、中期、长期）

### 示例 2：自定义分析

```bash
python main_v2.py \
  --dataset your_data.csv \
  --goal "你的分析目标" \
  --depth deep \
  --format json
```

---

## 🎯 Agent 工作流程

```
1️⃣ Data Explorer Agent
   ├─ 读取 CSV 数据
   ├─ 检查数据质量
   └─ 生成数据概览
        ↓
2️⃣ Analyst Agent
   ├─ 计算统计量
   ├─ 相关性分析
   └─ 趋势分析
        ↓
3️⃣ PandaAI Agent
   ├─ AI 智能问答
   ├─ 模式识别
   ├─ 异常检测
   └─ 趋势预测
        ↓
4️⃣ Reporter Agent
   ├─ 整合所有结果
   ├─ 生成执行摘要
   └─ 输出专业报告
```

---

## 🛡️ 架构保证

### ✅ 100% AI 驱动

- **工具负责计算** - 客观统计（均值、标准差等）
- **AI 负责判断** - 业务洞察、分析结论
- **无硬编码规则** - 无预设模板或固定逻辑

### ✅ 数据驱动

- 不同数据集 → 不同分析结论
- 不同分析目标 → 不同建议
- 无业务场景限制

详见：[NO_HARDCODING_GUARANTEE.md](NO_HARDCODING_GUARANTEE.md)

---

## 📝 配置选项

### 命令行参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--dataset` | 数据集路径 | - |
| `--goal` | 分析目标 | - |
| `--depth` | 分析深度 (quick/standard/deep) | standard |
| `--output` | 输出文件路径 | report.md |
| `--format` | 输出格式 (markdown/json/both) | markdown |
| `--interactive` | 交互式模式 | false |

### 环境变量

| 变量 | 说明 | 必填 |
|------|------|------|
| `OPENAI_API_KEY` | API 密钥 | ✅ |
| `OPENAI_BASE_URL` | API 端点 | ❌ |
| `OPENAI_MODEL` | 模型名称 | ❌ |

---

## 🔍 故障排查

### 问题 1：API 调用失败

**症状**：`Error: API connection failed`

**解决方案**：
1. 检查 `OPENAI_API_KEY` 是否正确
2. 检查 `OPENAI_BASE_URL` 是否可访问
3. 确认 API 配额是否充足

### 问题 2：pandasai 未安装

**症状**：`⚠️ pandasai 未安装`

**解决方案**：
```bash
pip install pandasai
```

### 问题 3：数据格式不支持

**症状**：`❌ 不支持的数据格式`

**解决方案**：
- 目前只支持 CSV 格式
- 确保文件编码为 UTF-8

---

## 📈 性能

| 指标 | 数值 |
|------|------|
| 支持数据规模 | 建议 < 1GB |
| 分析时间 | 5-15 分钟（取决于数据量和分析深度） |
| API 调用次数 | 10-20 次 |
| 成本 | 取决于 LLM 定价 |

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 许可证

MIT License

---

## 📞 联系方式

- 项目地址：[GitHub](https://github.com/your-username/datainsight-pro)
- 文档：[完整文档](./docs/)

---

**DataInsight Pro v2.0 - 让数据分析更智能！** 🚀
