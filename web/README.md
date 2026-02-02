# DataInsight Pro - Web UI

现代化的 AI 数据分析 Web 界面，基于 FastAPI + React + TypeScript 构建。

## 🎨 特性

- 📤 **拖拽式文件上传** - 支持 CSV、JSON、Excel 格式
- 🎯 **自然语言分析** - 用自然语言描述分析目标
- 📊 **实时进度显示** - 可视化分析进度
- 📈 **美观的报告展示** - Markdown 渲染 + 源码查看
- 🌙 **现代化 UI** - 深色主题 + 渐变效果
- 🚀 **响应式设计** - 适配各种屏幕尺寸

## 🏗️ 技术栈

### 后端
- **FastAPI** - 高性能 Python Web 框架
- **PandaAI** - AI 数据分析引擎
- **CrewAI** - Agent 编排框架
- **Pandas** - 数据处理

### 前端
- **React 18** - UI 框架
- **TypeScript** - 类型安全
- **Vite** - 构建工具
- **Tailwind CSS** - 样式框架
- **Lucide React** - 图标库
- **React Markdown** - Markdown 渲染

## 📦 安装与运行

### 前置要求

- Python 3.10+
- Node.js 18+
- npm 或 yarn

### 后端安装

```bash
# 1. 进入后端目录
cd web/backend

# 2. 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 安装依赖
pip install fastapi uvicorn python-multipart pandas

# 4. 安装项目依赖
cd ../..
pip install -r requirements.txt

# 5. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入你的 API Keys

# 6. 启动后端服务
cd web/backend
python app.py
# 或者使用 uvicorn
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

后端服务将在 `http://localhost:8000` 启动

API 文档：http://localhost:8000/docs

### 前端安装

```bash
# 1. 进入前端目录
cd web/frontend

# 2. 安装依赖
npm install

# 3. 启动开发服务器
npm run dev
```

前端服务将在 `http://localhost:3000` 启动

### 生产环境部署

#### 后端部署

```bash
cd web/backend

# 使用 gunicorn 部署
pip install gunicorn
gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000

# 或者使用 Docker (推荐)
docker build -t datainsight-backend .
docker run -p 8000:8000 --env-file .env datainsight-backend
```

#### 前端部署

```bash
cd web/frontend

# 构建生产版本
npm run build

# 使用 nginx 或其他静态文件服务器托管 dist 目录
# 或者使用 Docker
docker build -t datainsight-frontend .
docker run -p 80:80 datainsight-frontend
```

## 📁 项目结构

```
web/
├── backend/
│   ├── app.py              # FastAPI 主应用
│   └── uploads/            # 上传文件存储
├── frontend/
│   ├── src/
│   │   ├── components/     # React 组件
│   │   │   ├── FileUpload.tsx
│   │   │   ├── AnalysisForm.tsx
│   │   │   ├── ProgressDisplay.tsx
│   │   │   └── ReportViewer.tsx
│   │   ├── App.tsx         # 主应用
│   │   ├── main.tsx        # 入口
│   │   ├── types.ts        # 类型定义
│   │   └── api.ts          # API 服务
│   ├── public/             # 静态资源
│   ├── package.json
│   └── vite.config.ts
└── README.md
```

## 🔌 API 端点

### 上传文件
```
POST /upload
Content-Type: multipart/form-data

Response:
{
  "filename": "data.csv",
  "file_path": "/path/to/file",
  "size": 12345,
  "file_info": {
    "rows": 1000,
    "columns": 10,
    "column_names": [...],
    "preview": [...]
  }
}
```

### 启动分析
```
POST /analyze
Content-Type: multipart/form-data
Form Data: goal, dataset_path, depth, output_format

Response:
{
  "task_id": "uuid",
  "status": "pending",
  "progress": 0,
  "current_step": "等待开始...",
  ...
}
```

### 获取任务状态
```
GET /tasks/{task_id}

Response:
{
  "task_id": "uuid",
  "status": "running",
  "progress": 45,
  "current_step": "数据分析中...",
  ...
}
```

### 获取报告
```
GET /reports/{task_id}

Response:
{
  "task_id": "uuid",
  "content": "...",
  "format": "markdown"
}
```

## 🎨 界面预览

### 主界面
- 深色渐变背景
- 左侧：文件上传 + 分析配置 + 进度显示
- 右侧：报告展示区域

### 文件上传
- 拖拽上传区域
- 支持多格式
- 实时文件信息展示

### 分析配置
- 分析目标输入（文本框）
- 分析深度选择（快速/标准/深入）
- 输出格式选择（Markdown/JSON）

### 报告展示
- 渲染模式（Markdown 预览）
- 源码模式（原始内容）
- 下载功能

## 🔧 环境变量

在 `.env` 文件中配置：

```bash
# PandaAI API Key
PANDAAI_API_KEY=your_pandaai_api_key_here

# OpenAI API Key (CrewAI 需要)
OPENAI_API_KEY=your_openai_api_key_here

# 可选：后端服务端口
PORT=8000
```

## 🐳 Docker 部署

### 后端 Dockerfile
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "web.backend.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 前端 Dockerfile
```dockerfile
FROM node:18-alpine as builder

WORKDIR /app
COPY web/frontend/package*.json ./
RUN npm install

COPY web/frontend/ .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Docker Compose
```yaml
version: '3.8'

services:
  backend:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    volumes:
      - ./uploads:/app/web/backend/uploads
      - ./outputs:/app/outputs

  frontend:
    build: ./web/frontend
    ports:
      - "80:80"
    depends_on:
      - backend
```

## 📝 开发说明

### 添加新的 API 端点

在 `web/backend/app.py` 中添加：

```python
@app.get("/your-endpoint")
async def your_endpoint():
    return {"data": "your data"}
```

### 添加新的前端组件

在 `web/frontend/src/components/` 中创建新组件，然后在 `App.tsx` 中导入使用。

### 修改主题颜色

编辑 `web/frontend/tailwind.config.js`：

```javascript
theme: {
  extend: {
    colors: {
      primary: {
        // 你的颜色方案
      }
    }
  }
}
```

## 🚀 性能优化

- 后端：使用异步 I/O（async/await）
- 前端：使用 React.memo 和 useMemo 优化渲染
- 文件上传：使用分块上传（大文件）
- API 请求：使用防抖和节流

## 🐛 故障排除

### 后端启动失败
- 检查端口 8000 是否被占用
- 确认所有依赖已安装
- 查看 `.env` 文件配置是否正确

### 前端无法连接后端
- 确认后端服务已启动
- 检查 Vite 代理配置
- 查看 CORS 设置

### 分析任务失败
- 检查 API Keys 是否有效
- 确认文件格式正确
- 查看后端日志获取详细错误

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

**🚀 享受智能数据分析！**
