#!/usr/bin/env python3
"""
简化的 V2 配置验证 - 只检查配置，不运行完整功能
"""
import os
from pathlib import Path

def main():
    print("""
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║   DataInsight Pro V2 - 配置验证（简化版）                       ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
    """)

    # 1. 检查 .env 文件
    env_path = Path(__file__).parent / '.env'

    print("📋 步骤 1: 检查 .env 文件")
    print("-" * 60)

    if not env_path.exists():
        print("❌ .env 文件不存在")
        print("   请复制 .env.example 并配置")
        return 1

    print(f"✅ .env 文件存在: {env_path}")

    # 2. 读取配置
    print("\n📋 步骤 2: 读取配置")
    print("-" * 60)

    config = {}
    with open(env_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                config[key.strip()] = value.strip()

    # 3. 验证关键配置
    print("\n📋 步骤 3: 验证配置")
    print("-" * 60)

    # API Key
    if 'OPENAI_API_KEY' in config:
        key = config['OPENAI_API_KEY']
        masked = '*' * 20 + key[-4:] if len(key) > 4 else '***'
        print(f"✅ OPENAI_API_KEY: {masked}")
    else:
        print("❌ OPENAI_API_KEY: 未设置")
        print("   错误：必须设置此环境变量")
        return 1

    # Base URL
    base_url = config.get('OPENAI_BASE_URL', 'https://api.openai.com/v1')
    print(f"✅ OPENAI_BASE_URL: {base_url}")

    # 检测服务类型
    if "bigmodel.cn" in base_url:
        print("   💡 服务提供商: 智谱 AI (GLM)")
    elif "deepseek.com" in base_url:
        print("   💡 服务提供商: DeepSeek")
    elif "openai.com" in base_url:
        print("   💡 服务提供商: OpenAI")
    else:
        print("   💡 服务提供商: 自定义/其他")

    # Model
    model = config.get('OPENAI_MODEL', 'gpt-4')
    print(f"✅ OPENAI_MODEL: {model}")

    # 4. 检查废弃配置
    print("\n📋 步骤 4: 检查废弃配置")
    print("-" * 60)

    if 'PANDAAI_API_KEY' in config:
        print("⚠️  警告: 检测到已废弃的 PANDAAI_API_KEY")
        print("   V2 版本不再需要此配置，建议删除")
    else:
        print("✅ 无废弃配置")

    # 5. 验证 V2 文件
    print("\n📋 步骤 5: 验证 V2 文件")
    print("-" * 60)

    v2_files = [
        "main_v2.py",
        "src/crew_config.py",
        "src/crew_v2.py",
        "src/agents/pandaai_real.py",
        "src/agents/data_explorer_v2.py",
        "src/agents/analyst_v2.py",
        "src/agents/reporter_v2.py",
    ]

    all_exist = True
    for file_path in v2_files:
        full_path = Path(__file__).parent / file_path
        if full_path.exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} (缺失)")
            all_exist = False

    if not all_exist:
        return 1

    # 6. 总结
    print("\n" + "=" * 60)
    print("✅ 配置验证通过！")
    print("=" * 60)

    print("\n📊 您的配置:")
    print(f"   服务端点: {base_url}")
    print(f"   使用模型: {model}")
    print(f"   API Key: {masked}")

    print("\n🎯 下一步操作:")
    print("   1. 安装依赖（如果还没安装）:")
    print("      pip install -r requirements.txt")
    print("      或运行: ./install_deps.sh")
    print()
    print("   2. 运行 V2 分析:")
    print("      python main_v2.py --check-env")
    print("      python main_v2.py --interactive")
    print()

    # 7. 测试 API 连接（可选）
    print("\n📋 步骤 6: 测试 API 连接（可选）")
    print("-" * 60)
    print("⚠️  注意：完整的 API 测试需要安装所有依赖")
    print("   安装后可运行: python main_v2.py --check-env")

    return 0


if __name__ == "__main__":
    import sys
    try:
        sys.exit(main())
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
