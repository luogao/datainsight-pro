@echo off
REM DataInsight Pro - Web UI 启动脚本 (Windows)

echo ========================================
echo   DataInsight Pro - Web UI 启动脚本
echo ========================================
echo.

REM 检查 Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python 未安装，请先安装 Python 3.10+
    pause
    exit /b 1
)

REM 检查 Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js 未安装，请先安装 Node.js 18+
    pause
    exit /b 1
)

REM 检查环境变量文件
if not exist .env (
    echo ⚠️  未找到 .env 文件，正在从 .env.example 复制...
    copy .env.example .env
    echo ✅ 已创建 .env 文件，请编辑并填入你的 API Keys
    echo.
    pause
)

REM 创建必要的目录
if not exist web\backend\uploads mkdir web\backend\uploads
if not exist outputs mkdir outputs

echo 📦 安装后端依赖...
pip install fastapi uvicorn[standard] python-multipart pandas

echo.
echo 📦 安装前端依赖...
cd web\frontend
call npm install
cd ..\..

echo.
echo 🚀 启动后端服务...
start "DataInsight Backend" cmd /k "cd web\backend && python app.py"

REM 等待后端启动
timeout /t 3 /nobreak >nul

echo.
echo 🚀 启动前端服务...
cd web\frontend
start "DataInsight Frontend" cmd /k "npm run dev"
cd ..\..

echo.
echo ========================================
echo   🎉 DataInsight Pro Web UI 已启动！
echo ========================================
echo.
echo 📊 后端 API: http://localhost:8000
echo 📊 前端界面: http://localhost:3000
echo 📊 API 文档: http://localhost:8000/docs
echo.
echo 关闭此窗口不会停止服务，请手动关闭弹出的两个命令行窗口
echo.
pause
