#!/usr/bin/env python3
"""
V2 配置测试脚本 - 不需要安装所有依赖
"""
import os
from pathlib import Path

def test_env_file():
    """测试 .env 文件"""
    print("=" * 60)
    print("🔍 测试 1: .env 文件检查")
    print("=" * 60)

    env_path = Path(__file__).parent / '.env'

    if env_path.exists():
        print(f"✅ .env 文件存在：{env_path}")

        # 读取并解析 .env
        with open(env_path, 'r') as f:
            lines = f.readlines()

        config = {}
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                config[key.strip()] = value.strip()

        # 检查关键配置
        print("\n📋 配置内容：")

        if 'OPENAI_API_KEY' in config:
            key = config['OPENAI_API_KEY']
            masked = '*' * 20 + key[-4:] if len(key) > 4 else '***'
            print(f"✅ OPENAI_API_KEY: {masked}")
        else:
            print("❌ OPENAI_API_KEY: 未设置")

        if 'OPENAI_BASE_URL' in config:
            print(f"✅ OPENAI_BASE_URL: {config['OPENAI_BASE_URL']}")
        else:
            print("ℹ️  OPENAI_BASE_URL: 使用默认")

        if 'OPENAI_MODEL' in config:
            print(f"✅ OPENAI_MODEL: {config['OPENAI_MODEL']}")
        else:
            print("ℹ️  OPENAI_MODEL: 使用默认 (gpt-4)")

        # 检查废弃的配置
        if 'PANDAAI_API_KEY' in config:
            print("\n⚠️  警告：检测到已废弃的 PANDAAI_API_KEY")
            print("   提示：V2 版本不再需要此配置，可以删除")

        return config

    else:
        print(f"❌ .env 文件不存在：{env_path}")
        print("   请复制 .env.example 并配置")
        return None


def test_v2_files():
    """测试 V2 文件是否存在"""
    print("\n" + "=" * 60)
    print("🔍 测试 2: V2 文件检查")
    print("=" * 60)

    base_path = Path(__file__).parent

    v2_files = [
        ("main_v2.py", "V2 主入口"),
        ("src/crew_config.py", "LLM 配置工厂"),
        ("src/crew_v2.py", "V2 CrewAI 编排"),
        ("src/agents/pandaai_real.py", "真正的 PandaAI"),
        ("src/agents/data_explorer_v2.py", "V2 Data Explorer"),
        ("src/agents/analyst_v2.py", "V2 Analyst"),
        ("src/agents/reporter_v2.py", "V2 Reporter"),
        ("README_V2.md", "V2 文档"),
        ("MIGRATION_GUIDE.md", "迁移指南"),
        ("ENV_QUICK_REF.md", "环境变量参考"),
    ]

    all_exist = True
    for file_path, description in v2_files:
        full_path = base_path / file_path
        if full_path.exists():
            print(f"✅ {description}: {file_path}")
        else:
            print(f"❌ {description}: {file_path} (缺失)")
            all_exist = False

    return all_exist


def test_imports():
    """测试关键导入"""
    print("\n" + "=" * 60)
    print("🔍 测试 3: 导入检查")
    print("=" * 60)

    # 测试标准库
    try:
        import os
        import sys
        import json
        from pathlib import Path
        print("✅ 标准库导入成功")
    except ImportError as e:
        print(f"❌ 标准库导入失败: {e}")
        return False

    # 测试第三方库
    missing = []
    try:
        import pandas
        print("✅ pandas 已安装")
    except ImportError:
        print("❌ pandas 未安装")
        missing.append("pandas")

    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv 已安装")
    except ImportError:
        print("❌ python-dotenv 未安装")
        missing.append("python-dotenv")

    try:
        from langchain_openai import ChatOpenAI
        print("✅ langchain-openai 已安装")
    except ImportError:
        print("❌ langchain-openai 未安装")
        missing.append("langchain-openai")

    try:
        from pandasai import PandasAI
        print("✅ pandasai 已安装")
    except ImportError:
        print("⚠️  pandasai 未安装 (可选，其他功能仍可使用)")
        missing.append("pandasai (可选)")

    try:
        from crewai import Crew, Agent
        print("✅ crewai 已安装")
    except ImportError:
        print("❌ crewai 未安装")
        missing.append("crewai")

    if missing:
        print(f"\n💡 安装缺失的包:")
        print(f"   pip install {' '.join(missing)}")

    return len(missing) == 0


def test_llm_config():
    """测试 LLM 配置"""
    print("\n" + "=" * 60)
    print("🔍 测试 4: LLM 配置验证")
    print("=" * 60)

    # 加载环境变量
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        print("⚠️  无法加载 .env（python-dotenv 未安装）")
        return False

    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")
    model = os.getenv("OPENAI_MODEL", "gpt-4")

    print(f"\n📋 LLM 配置:")
    print(f"   API Key: {'✅ 已设置' if api_key else '❌ 未设置'}")
    print(f"   Base URL: {base_url or 'https://api.openai.com/v1 (默认)'}")
    print(f"   Model: {model}")

    if not api_key:
        print("\n❌ 错误：OPENAI_API_KEY 未设置")
        print("   请在 .env 文件中配置")
        return False

    # 检查您的配置（智谱 AI）
    if "bigmodel.cn" in (base_url or ""):
        print("\n✅ 检测到智谱 AI (GLM) 配置")
        print(f"   端点: {base_url}")
        print(f"   模型: {model}")

    return True


def main():
    """主测试函数"""
    print("""
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║   DataInsight Pro V2 - 配置测试工具                            ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
    """)

    results = []

    # 测试 1: .env 文件
    config = test_env_file()
    results.append(("环境配置", config is not None))

    # 测试 2: V2 文件
    files_ok = test_v2_files()
    results.append(("V2 文件", files_ok))

    # 测试 3: 导入
    imports_ok = test_imports()
    results.append(("依赖安装", imports_ok))

    # 测试 4: LLM 配置
    llm_ok = test_llm_config()
    results.append(("LLM 配置", llm_ok))

    # 总结
    print("\n" + "=" * 60)
    print("📊 测试总结")
    print("=" * 60)

    for name, ok in results:
        status = "✅ 通过" if ok else "❌ 失败"
        print(f"{name:20s} {status}")

    passed = sum(1 for _, ok in results if ok)
    total = len(results)

    print(f"\n总计: {passed}/{total} 项测试通过")

    if passed == total:
        print("\n🎉 所有测试通过！V2 配置正常")
        print("\n下一步: 运行 python main_v2.py --interactive")
        return 0
    else:
        print("\n⚠️  部分测试失败，请检查上述问题")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
