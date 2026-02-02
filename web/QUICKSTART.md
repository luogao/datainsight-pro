# DataInsight Pro Web UI - 快速开始指南

## 🚀 一键启动（推荐）

### Linux / macOS

```bash
cd /home/node/.openclaw/workspace/data-analysis-agent
./start-web.sh
```

### Windows

双击运行 `start-web.bat`

或者命令行：

```cmd
cd C:\path\to\data-analysis-agent
start-web.bat
```

## 📋 手动启动

### 步骤 1: 配置环境变量

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的 API Keys：

```bash
PANDAAI_API_KEY=your_pandaai_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

### 步骤 2: 启动后端

```bash
# 安装依赖
pip install fastapi uvicorn[standard] python-multipart pandas

# 启动后端
cd web/backend
python app.py
```

后端将运行在：http://localhost:8000

### 步骤 3: 启动前端（新终端）

```bash
# 安装依赖
cd web/frontend
npm install

# 启动开发服务器
npm run dev
```

前端将运行在：http://localhost:3000

## 🎯 使用流程

1. **打开浏览器** 访问 http://localhost:3000

2. **上传数据**
   - 拖拽 CSV/JSON/Excel 文件到上传区域
   - 或点击选择文件

3. **配置分析**
   - 输入分析目标（例如："分析销售数据趋势"）
   - 选择分析深度（快速/标准/深入）
   - 选择输出格式（Markdown/JSON）

4. **查看报告**
   - 实时查看分析进度
   - 分析完成后自动显示报告
   - 可切换预览模式和源码模式
   - 点击"下载报告"保存到本地

## 📊 界面预览

```
┌─────────────────────────────────────────────────────────┐
│  DataInsight Pro                            Powered by AI │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────────┐  ┌─────────────────────────────┐ │
│  │ 第 1 步：上传   │  │      分析报告                │ │
│  │                 │  │                             │ │
│  │ [拖拽文件]      │  │  📊 数据概览                 │ │
│  │                 │  │                             │ │
│  └─────────────────┘  │  📈 关键指标                 │ │
│                       │                             │ │
│  ┌─────────────────┐  │  🔍 主要发现                 │ │
│  │ 第 2 步：配置   │  │                             │ │
│  │                 │  │  💡 业务建议                 │ │
│  │ 分析目标：      │  │                             │ │
│  │ [文本框]        │  │                             │ │
│  │                 │  │  [下载报告]                 │ │
│  │ 分析深度：      │  │                             │ │
│  │ ○ 快速 ● 标准  │  │                             │ │
│  │   ○ 深入       │  │                             │ │
│  │                 │  │                             │ │
│  │ [开始分析]      │  │                             │ │
│  └─────────────────┘  └─────────────────────────────┘ │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 🔧 常见问题

### Q: 后端启动失败？

A: 检查以下几点：
1. 确认 Python 版本 >= 3.10
2. 确认所有依赖已安装：`pip install -r requirements.txt`
3. 检查端口 8000 是否被占用
4. 确认 `.env` 文件中的 API Keys 是否正确

### Q: 前端无法连接后端？

A: 尝试以下解决方案：
1. 确认后端服务已启动（访问 http://localhost:8000/health）
2. 检查 Vite 代理配置（`vite.config.ts`）
3. 查看浏览器控制台的错误信息

### Q: 分析任务失败？

A: 常见原因：
1. API Keys 无效或额度不足
2. 文件格式不支持或损坏
3. 分析目标描述不清晰
4. 网络连接问题

查看后端日志获取详细错误信息。

### Q: 文件上传失败？

A: 检查：
1. 文件大小是否过大（建议 < 100MB）
2. 文件格式是否支持（CSV、JSON、Excel）
3. 磁盘空间是否充足

## 📝 示例数据

项目包含示例数据，你可以快速测试：

1. 上传示例文件：`data/samples/sales_2024_Q1.csv`
2. 分析目标示例：
   - "分析最近一个季度的销售数据，找出趋势和异常"
   - "按地区分析销售额分布"
   - "识别销售异常值并提供解释"

## 🐳 Docker 部署

### 一键部署

```bash
# 确保已配置 .env 文件
docker-compose up -d
```

访问 http://localhost 查看界面

### 停止服务

```bash
docker-compose down
```

## 📖 API 文档

访问 http://localhost:8000/docs 查看完整的 API 文档和交互式测试工具。

## 🎨 自定义主题

编辑 `web/frontend/tailwind.config.js` 修改颜色主题：

```javascript
theme: {
  extend: {
    colors: {
      primary: {
        50: '#your-color',
        // ...
      }
    }
  }
}
```

## 🚀 生产环境部署

### 使用 Nginx 反向代理

1. 构建前端：`cd web/frontend && npm run build`
2. 配置 Nginx 指向 `dist` 目录
3. 配置反向代理 `/api` 到后端服务

### 使用 systemd 管理（Linux）

创建 `/etc/systemd/system/datainsight.service`：

```ini
[Unit]
Description=DataInsight Pro
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/data-analysis-agent
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/uvicorn web.backend.app:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

启用服务：

```bash
sudo systemctl enable datainsight
sudo systemctl start datainsight
```

## 📞 获取帮助

- 查看完整文档：`web/README.md`
- 查看 API 文档：http://localhost:8000/docs
- 提交 Issue：https://github.com/your-repo/issues

---

**🎉 享受智能数据分析之旅！**
