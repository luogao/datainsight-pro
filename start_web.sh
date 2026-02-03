#!/bin/bash
# DataInsight Pro - Web UI 启动脚本
# 启动后端和前端服务

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║${NC}                                                            ${BLUE}║${NC}"
echo -e "${BLUE}║${NC}   ${GREEN}DataInsight Pro - Web UI 启动脚本${NC}                    ${BLUE}║${NC}"
echo -e "${BLUE}║${NC}                                                            ${BLUE}║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# 检查环境
echo -e "${YELLOW}🔍 检查环境...${NC}"

# 检查 .env 文件
if [ ! -f .env ]; then
    echo -e "${RED}❌ 未找到 .env 文件${NC}"
    echo -e "${YELLOW}请先复制 .env.example 为 .env 并配置 API Keys${NC}"
    echo ""
    echo "运行以下命令："
    echo "  cp .env.example .env"
    echo "  然后编辑 .env 文件填入你的 API Keys"
    exit 1
fi

echo -e "${GREEN}✅ .env 文件已找到${NC}"

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ 未找到 Python 3${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo -e "${GREEN}✅ Python 版本: ${PYTHON_VERSION}${NC}"

# 检查依赖
echo ""
echo -e "${YELLOW}📦 检查依赖...${NC}"

# 检查后端依赖
BACKEND_DEPS=("fastapi" "uvicorn" "pandas" "crewai")
for dep in "${BACKEND_DEPS[@]}"; do
    if python3 -c "import $dep" 2>/dev/null; then
        echo -e "${GREEN}✅ $dep${NC}"
    else
        echo -e "${RED}❌ $dep 未安装${NC}"
        MISSING_DEPS=true
    fi
done

if [ "$MISSING_DEPS" = true ]; then
    echo ""
    echo -e "${YELLOW}正在安装缺失的依赖...${NC}"
    pip install -r requirements.txt
fi

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ 未找到 Node.js${NC}"
    echo -e "${YELLOW}请安装 Node.js: https://nodejs.org/${NC}"
    exit 1
fi

NODE_VERSION=$(node --version)
echo -e "${GREEN}✅ Node.js 版本: ${NODE_VERSION}${NC}"

# 检查前端依赖
if [ ! -d "web/frontend/node_modules" ]; then
    echo ""
    echo -e "${YELLOW}📦 安装前端依赖...${NC}"
    cd web/frontend
    npm install
    cd ../..
fi

# 创建必要的目录
mkdir -p web/backend/uploads
mkdir -p web/backend/outputs

echo ""
echo -e "${GREEN}✅ 环境检查完成！${NC}"
echo ""

# 启动服务
echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}🚀 启动服务...${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo ""

# 启动后端
echo -e "${YELLOW}启动后端服务...${NC}"
cd web/backend
python3 app.py &
BACKEND_PID=$!
cd ../..

echo -e "${GREEN}✅ 后端已启动 (PID: $BACKEND_PID)${NC}"
echo -e "${BLUE}   后端地址: http://localhost:8000${NC}"
echo -e "${BLUE}   API 文档: http://localhost:8000/docs${NC}"
echo ""

# 等待后端启动
sleep 3

# 启动前端
echo -e "${YELLOW}启动前端服务...${NC}"
cd web/frontend
npm run dev &
FRONTEND_PID=$!
cd ../..

echo -e "${GREEN}✅ 前端已启动 (PID: $FRONTEND_PID)${NC}"
echo -e "${BLUE}   前端地址: http://localhost:3000${NC}"
echo ""

echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}🎉 Web UI 已成功启动！${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "📱 访问地址: ${GREEN}http://localhost:3000${NC}"
echo -e "📖 API 文档: ${BLUE}http://localhost:8000/docs${NC}"
echo ""
echo -e "按 ${YELLOW}Ctrl+C${NC} 停止所有服务"
echo ""

# 保存 PID 以便清理
echo $BACKEND_PID > /tmp/datainsight_backend.pid
echo $FRONTEND_PID > /tmp/datainsight_frontend.pid

# 捕获退出信号
cleanup() {
    echo ""
    echo -e "${YELLOW}🛑 正在停止服务...${NC}"
    kill $BACKEND_PID 2>/dev/null || true
    kill $FRONTEND_PID 2>/dev/null || true
    rm -f /tmp/datainsight_backend.pid /tmp/datainsight_frontend.pid
    echo -e "${GREEN}✅ 所有服务已停止${NC}"
    exit 0
}

trap cleanup SIGINT SIGTERM

# 等待进程
wait
