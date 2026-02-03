#!/usr/bin/env python3
"""
DataInsight Pro v2.0 - AI 大数据自动化分析 Agent
主入口程序（PandaAI 真实集成版）
"""
import os
import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv

# 添加 src 到路径
sys.path.insert(0, str(Path(__file__).parent))

from src.crew_v2 import run_analysis


def print_banner():
    """打印横幅"""
    print("""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   🚀 DataInsight Pro v2.0                                 ║
║   AI 大数据自动化分析 Agent (PandaAI 真实集成版)           ║
║                                                           ║
║   ✨ 特性:                                                ║
║   - 真正集成 PandaAI (pandasai 库)                       ║
║   - 支持自定义 LLM API (OpenAI/DeepSeek/其他)            ║
║   - CrewAI Agent 编排                                    ║
║   - 智能数据问答、清洗、分析和预测                        ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
    """)


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description="DataInsight Pro v2.0 - AI 大数据自动化分析 Agent (PandaAI 真实集成)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 分析销售数据（使用 PandaAI）
  python main_v2.py --goal "分析最近一个季度的销售数据，找出趋势和异常" \\
                    --dataset data/sales_2024_Q1.csv

  # 交互式分析
  python main_v2.py --interactive

  # 使用自定义 API（如 DeepSeek）
  export OPENAI_BASE_URL=https://api.deepseek.com/v1
  export OPENAI_MODEL=deepseek-chat
  python main_v2.py --goal "分析用户留存率" --dataset data/user_retention.csv

  # 深入分析
  python main_v2.py --goal "深入分析产品销量" \\
                    --dataset data/products.csv \\
                    --depth deep \\
                    --output products_report.md
        """
    )

    parser.add_argument(
        '--goal',
        type=str,
        help='分析目标（用自然语言描述）'
    )

    parser.add_argument(
        '--dataset',
        type=str,
        help='数据集路径（CSV、JSON 或 Excel 文件）'
    )

    parser.add_argument(
        '--output',
        type=str,
        default='report.md',
        help='输出报告路径（默认：report.md）'
    )

    parser.add_argument(
        '--depth',
        choices=['quick', 'standard', 'deep'],
        default='standard',
        help='分析深度：quick（快速）、standard（标准）、deep（深入）'
    )

    parser.add_argument(
        '--interactive',
        action='store_true',
        help='交互式模式'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='空运行（不真正执行分析）'
    )

    parser.add_argument(
        '--format',
        choices=['markdown', 'json', 'both'],
        default='markdown',
        help='输出格式'
    )

    parser.add_argument(
        '--check-env',
        action='store_true',
        help='检查环境配置'
    )

    return parser.parse_args()


def check_environment():
    """检查环境配置"""
    print("\n🔍 检查环境配置...\n")

    # 检查 .env 文件
    env_file = Path(__file__).parent / '.env'
    if env_file.exists():
        print(f"✅ .env 文件存在：{env_file}")
    else:
        print(f"⚠️  .env 文件不存在：{env_file}")
        print(f"   提示：复制 .env.example 并配置 API Keys")

    # 检查环境变量
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")
    model = os.getenv("OPENAI_MODEL")

    if api_key:
        print(f"✅ OPENAI_API_KEY: {'*' * 20}{api_key[-4:]}")
    else:
        print(f"❌ OPENAI_API_KEY: 未设置")

    if base_url:
        print(f"✅ OPENAI_BASE_URL: {base_url}")
    else:
        print(f"ℹ️  OPENAI_BASE_URL: 使用默认 (https://api.openai.com/v1)")

    if model:
        print(f"✅ OPENAI_MODEL: {model}")
    else:
        print(f"ℹ️  OPENAI_MODEL: 使用默认 (gpt-4)")

    # 检查依赖
    print("\n📦 检查依赖包...\n")

    dependencies = [
        ("pandas", "数据处理"),
        ("pandasai", "AI 数据分析"),
        ("crewai", "Agent 编排"),
        ("langchain_openai", "LLM 集成"),
    ]

    for package, description in dependencies:
        try:
            __import__(package)
            print(f"✅ {package:20s} - {description}")
        except ImportError:
            print(f"❌ {package:20s} - {description} (未安装)")

    print()


def interactive_mode():
    """交互式模式"""
    print("\n" + "="*60)
    print("🎯 交互式分析模式")
    print("="*60)

    # 分析目标
    print("\n📋 请输入分析目标（用自然语言描述）：")
    print("   示例：分析最近一个季度的销售数据，找出趋势和异常")
    goal = input("> ").strip()

    if not goal:
        print("❌ 分析目标不能为空")
        return 1

    # 数据集
    print("\n📁 请输入数据集路径（CSV、JSON 或 Excel 文件）：")
    print("   示例：data/sales_2024_Q1.csv")
    dataset = input("> ").strip()

    if not dataset:
        print("❌ 数据集路径不能为空")
        return 1

    # 检查文件是否存在
    if not Path(dataset).exists():
        print(f"❌ 文件不存在：{dataset}")
        return 1

    # 分析深度
    print("\n🎯 请选择分析深度 [quick/standard/deep，默认：standard]：")
    depth = input("> ").strip() or "standard"

    if depth not in ["quick", "standard", "deep"]:
        print("⚠️  无效的分析深度，使用默认值：standard")
        depth = "standard"

    # 输出文件
    print("\n📤 请输入输出文件路径 [默认：report.md]：")
    output = input("> ").strip() or "report.md"

    # 确认
    print("\n" + "="*60)
    print("✅ 分析任务确认")
    print("="*60)
    print(f"📋 分析目标：{goal}")
    print(f"📊 数据集：{dataset}")
    print(f"🎯 分析深度：{depth}")
    print(f"📤 输出文件：{output}")
    print("="*60)

    confirm = input("\n开始分析？[Y/n]: ").strip().lower()

    if confirm and confirm != 'y':
        print("❌ 已取消")
        return 1

    # 执行分析
    result = run_analysis(
        goal=goal,
        dataset_path=dataset,
        depth=depth,
        output_path=output
    )

    return 0 if result else 1


def main():
    """主函数"""
    print_banner()

    args = parse_args()

    # 检查环境
    if args.check_env:
        check_environment()
        return 0

    # 交互式模式
    if args.interactive:
        return interactive_mode()

    # 命令行模式
    if not args.goal or not args.dataset:
        print("\n❌ 错误：需要指定 --goal 和 --dataset 参数")
        print("\n使用 --interactive 进入交互式模式")
        print("使用 --help 查看帮助信息\n")
        return 1

    # 检查文件是否存在
    if not Path(args.dataset).exists():
        print(f"\n❌ 错误：文件不存在：{args.dataset}\n")
        return 1

    # 空运行
    if args.dry_run:
        print("\n🔍 空运行模式（不会真正执行分析）\n")
        print(f"📋 分析目标：{args.goal}")
        print(f"📊 数据集：{args.dataset}")
        print(f"🎯 分析深度：{args.depth}")
        print(f"📤 输出文件：{args.output}")
        print(f"📄 输出格式：{args.format}")
        print("\n✅ 配置检查完成，未发现错误\n")
        return 0

    # 执行分析
    result = run_analysis(
        goal=args.goal,
        dataset_path=args.dataset,
        depth=args.depth,
        output_path=args.output,
        output_format=args.format
    )

    return 0 if result else 1


if __name__ == "__main__":
    load_dotenv()
    sys.exit(main())
