#!/bin/bash
# DataInsight Pro V2 - 依赖安装脚本

echo "🚀 DataInsight Pro V2 - 依赖安装"
echo ""

# 创建虚拟环境
echo "📦 创建虚拟环境..."
python3 -m venv venv

# 激活虚拟环境
echo "✅ 激活虚拟环境..."
source venv/bin/activate

# 升级 pip
echo "⬆️  升级 pip..."
pip install --upgrade pip -q

# 安装依赖
echo "📥 安装依赖包..."
pip install -r requirements.txt

echo ""
echo "✅ 安装完成！"
echo ""
echo "使用方法："
echo "  1. 激活虚拟环境: source venv/bin/activate"
echo "  2. 运行测试: python test_v2_setup.py"
echo "  3. 运行 V2: python main_v2.py --interactive"
echo ""
