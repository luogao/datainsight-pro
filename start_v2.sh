#!/bin/bash
# DataInsight Pro V2 - 快速启动脚本

echo """
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║   🚀 DataInsight Pro V2 - 快速启动                             ║
║                                                                ║
║   使用智谱 AI (GLM-4.7)                                         ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
"""

# 检查 .env
if [ ! -f .env ]; then
    echo "❌ .env 文件不存在"
    echo "   请复制 .env.example 并配置"
    exit 1
fi

echo "✅ .env 文件已找到"
echo ""

# 检查虚拟环境
if [ -d venv ]; then
    echo "✅ 检测到虚拟环境"
    echo "📦 激活虚拟环境..."
    source venv/bin/activate
else
    echo "⚠️  未检测到虚拟环境"
    echo ""
    echo "请选择安装方式："
    echo "  1. 创建虚拟环境（推荐）"
    echo "  2. 使用系统 Python"
    echo ""
    read -p "请选择 [1/2]: " choice

    if [ "$choice" = "1" ]; then
        echo "📦 创建虚拟环境..."
        python3 -m venv venv
        source venv/bin/activate

        echo "⬆️  升级 pip..."
        pip install --upgrade pip -q

        echo "📥 安装依赖..."
        pip install -r requirements.txt
    else
        echo "⚠️  使用系统 Python"
        echo "   如果遇到权限问题，请使用虚拟环境"
    fi
fi

echo ""
echo "============================================================"
echo "📋 配置信息"
echo "============================================================"

# 读取配置
source .env 2>/dev/null || true

if [ -n "$OPENAI_API_KEY" ]; then
    masked="********************${OPENAI_API_KEY: -4}"
    echo "✅ API Key: $masked"
else
    echo "❌ API Key: 未设置"
fi

if [ -n "$OPENAI_BASE_URL" ]; then
    echo "✅ Base URL: $OPENAI_BASE_URL"

    if [[ "$OPENAI_BASE_URL" == *"bigmodel.cn"* ]]; then
        echo "   💡 服务: 智谱 AI (GLM)"
    elif [[ "$OPENAI_BASE_URL" == *"deepseek.com"* ]]; then
        echo "   💡 服务: DeepSeek"
    elif [[ "$OPENAI_BASE_URL" == *"openai.com"* ]]; then
        echo "   💡 服务: OpenAI"
    fi
else
    echo "ℹ️  Base URL: 使用默认 (OpenAI)"
fi

if [ -n "$OPENAI_MODEL" ]; then
    echo "✅ Model: $OPENAI_MODEL"
else
    echo "ℹ️  Model: 使用默认 (gpt-4)"
fi

echo ""
echo "============================================================"
echo "🎯 选择运行模式"
echo "============================================================"
echo ""
echo "  1. 检查环境配置"
echo "  2. 交互式分析模式"
echo "  3. 命令行分析模式"
echo "  4. 查看测试报告"
echo "  5. 退出"
echo ""

read -p "请选择 [1-5]: " mode

case $mode in
    1)
        echo ""
        echo "🔍 检查环境配置..."
        python main_v2.py --check-env
        ;;
    2)
        echo ""
        echo "🎯 启动交互式分析模式..."
        python main_v2.py --interactive
        ;;
    3)
        echo ""
        echo "📝 命令行分析模式"
        echo ""
        read -p "请输入分析目标: " goal
        read -p "请输入数据集路径: " dataset
        read -p "分析深度 [quick/standard/deep，默认standard]: " depth
        depth=${depth:-standard}

        echo ""
        echo "🚀 开始分析..."
        python main_v2.py --goal "$goal" --dataset "$dataset" --depth "$depth"
        ;;
    4)
        echo ""
        echo "📊 打开测试报告..."
        if [ -f TEST_REPORT.md ]; then
            cat TEST_REPORT.md
        else
            echo "❌ 测试报告不存在"
        fi
        ;;
    5)
        echo "👋 再见！"
        exit 0
        ;;
    *)
        echo "❌ 无效选择"
        exit 1
        ;;
esac

echo ""
echo "✅ 完成！"
