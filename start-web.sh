#!/bin/bash

# DataInsight Pro - Web UI 启动脚本

set -e

echo "========================================"
echo "  DataInsight Pro - Web UI 启动脚本"
echo "========================================"
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 未安装，请先安装 Python 3.10+"
    exit 1
fi

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js 未安装，请先安装 Node.js 18+"
    exit 1
fi

# 检查环境变量文件
if [ ! -f .env ]; then
    echo "⚠️  未找到 .env 文件，正在从 .env.example 复制..."
    cp .env.example .env
    echo "✅ 已创建 .env 文件，请编辑并填入你的 API Keys"
    echo "   PANDAAI_API_KEY=your_pandaai_api_key_here"
    echo "   OPENAI_API_KEY=your_openai_api_key_here"
    echo ""
    read -p "按 Enter 继续（确保已配置 .env 文件）..."
fi

# 创建必要的目录
mkdir -p web/backend/uploads
mkdir -p outputs

echo "📦 安装后端依赖..."
pip install -q fastapi uvicorn python-multipart pandas

echo ""
echo "📦 安装前端依赖..."
cd web/frontend
npm install --silent
cd ../..

echo ""
echo "🚀 启动后端服务..."
cd web/backend
python3 app.py &
BACKEND_PID=$!
cd ../..

echo "✅ 后端服务已启动 (PID: $BACKEND_PID) - http://localhost:8000"

# 等待后端启动
sleep 3

echo ""
echo "🚀 启动前端服务..."
cd web/frontend
npm run dev &
FRONTEND_PID=$!
cd ../..

echo "✅ 前端服务已启动 (PID: $FRONTEND_PID) - http://localhost:3000"
echo ""
echo "========================================"
echo "  🎉 DataInsight Pro Web UI 已启动！"
echo "========================================"
echo ""
echo "📊 后端 API: http://localhost:8000"
echo "📊 前端界面: http://localhost:3000"
echo "📊 API 文档: http://localhost:8000/docs"
echo ""
echo "按 Ctrl+C 停止所有服务"
echo ""

# 捕获退出信号，清理进程
trap 'echo ""; echo "🛑 停止服务..."; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit 0' INT TERM

# 等待进程
wait
