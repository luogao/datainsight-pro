#!/usr/bin/env python3
"""
DataInsight Pro - AI 大数据自动化分析 Agent
主入口程序
"""
import os
import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv
import yaml

# 添加 src 到路径
sys.path.insert(0, str(Path(__file__).parent))

from src.crew import DataAnalysisCrew


def load_config():
    """加载配置文件"""
    config_path = Path(__file__).parent / "config" / "settings.yaml"
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as os.environ.get('LANG', 'en-US')) as f:
            return yaml.safe_load(f)
    return {}


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description="DataInsight Pro - AI 大数据自动化分析 Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 分析销售数据
  python main.py --goal "分析最近一个季度的销售数据，找出趋势和异常" --dataset data/sales_2024_Q1.csv

  # 交互式分析
  python main.py --interactive

  # 分析用户留存
  python main.py --goal "分析用户留存率，找出影响留存的关键因素" --dataset data/user_retention.csv --depth deep
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
        help='数据集路径（CSV、JSON 或 URL）'
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
        '--config',
        type=str,
        default='config/settings.yaml',
        help='配置文件路径'
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

    return parser.parse_args()


def interactive_input():
    """交互式输入分析目标"""
    print("\n" + "="*60)
    print("🚀 DataInsight Pro - AI 数据分析 Agent")
    print("="*60)
    print("\n请提供分析信息：\n")

    goal = input("📋 分析目标（用自然语言描述）：\n> ").strip()
    if not goal:
        print("❌ 分析目标不能为空！")
        return None, None, None

    dataset = input("📁 数据集路径（文件路径或 URL）：\n> ").strip()
    if not dataset:
        print("❌ 数据集路径不能为空！")
        return None, None, None

    depth = input("🎯 分析深度 [quick/standard/deep，默认：standard]：\n> ").strip()
    if depth not in ['quick', 'standard', 'deep']:
        depth = 'standard'

    output = input("📤 输出文件路径 [默认：report.md]：\n> ").strip()
    if not output:
        output = 'report.md'

    print(f"\n✅ 分析任务：{goal}")
    print(f"📊 数据集：{dataset}")
    print(f"🎯 深度：{depth}")
    print(f"📤 输出：{output}")
    print("\n开始分析...\n")

    return goal, dataset, {
        'depth': depth,
        'output': output,
        'format': 'markdown'
    }


def run_analysis(goal: str, dataset: str, options: dict, dry_run: bool = False):
    """执行数据分析"""
    print(f"\n🎬 开始分析任务...")
    print(f"📋 目标：{goal}")
    print(f"📊 数据：{dataset}")
    print(f"🎯 深度：{options['depth']}")
    print(f"📤 输出：{options['output']}")

    if dry_run:
        print("\n⚠️  空运行模式 - 不会真正执行分析")
        return

    try:
        # 初始化 Crew
        crew = DataAnalysisCrew()

        print("\n🤖 启动 Agent 团队...")
        print("   - DataExplorer: 数据探索")
        print("   - Analyst: 统计分析")
        print("   - PandaAI: AI 洞察")
        print("   - Reporter: 报告生成")

        # 执行分析
        result = crew.kickoff(
            inputs={
                'goal': goal,
                'dataset_path': dataset,
                'analysis_depth': options['depth'],
                'output_path': options['output'],
                'output_format': options['format']
            }
        )

        print(f"\n✅ 分析完成！")
        print(f"📄 报告已保存到：{result}")
        print(f"📊 输出格式：{options['format']}")

        return result

    except Exception as e:
        print(f"\n❌ 分析失败：{str(e)}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """主函数"""
    # 加载环境变量
    load_dotenv()

    # 解析参数
    args = parse_args()

    # 检查必需的 API Keys
    if not os.environ.get('PANDAAI_API_KEY'):
        print("\n⚠️  警告：未设置 PANDAAI_API_KEY 环境变量")
        print("   请设置：export PANDAAI_API_KEY='your-api-key'")
        print("   或创建 .env 文件并添加该变量")

    # 交互式模式
    if args.interactive:
        goal, dataset, options = interactive_input()
        if not goal:
            print("❌ 输入无效，退出")
            sys.exit(1)

        run_analysis(goal, dataset, options)
    else:
        # 命令行模式
        if not args.goal or not args.dataset:
            print("\n❌ 错误：--goal 和 --dataset 参数是必需的")
            print("   使用 --interactive 进入交互式模式")
            print("   或提供 --goal 和 --dataset 参数")
            sys.exit(1)

        options = {
            'depth': args.depth,
            'output': args.output,
            'format': args.format
        }

        run_analysis(args.goal, args.dataset, options, args.dry_run)


if __name__ == "__main__":
    main()
