#!/usr/bin/env python3
"""
测试任务输出目录结构
验证每次分析任务都会创建独立的文件夹，包含所有中间结果
"""
import os
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
load_dotenv()


def test_output_directory_structure():
    """测试输出目录结构"""

    print("=" * 60)
    print("测试任务输出目录结构")
    print("=" * 60)

    # 检查输出目录
    output_dir = project_root / "web" / "outputs"
    print(f"\n📁 输出根目录: {output_dir}")
    print(f"   存在: {'✅' if output_dir.exists() else '❌'}")

    if output_dir.exists():
        # 列出所有任务文件夹
        task_dirs = [d for d in output_dir.iterdir() if d.is_dir()]

        print(f"\n📊 任务文件夹数量: {len(task_dirs)}")

        if task_dirs:
            print(f"\n最近的任务文件夹:")
            for task_dir in sorted(task_dirs, key=lambda x: x.stat().st_mtime, reverse=True)[:5]:
                print(f"\n  📂 {task_dir.name}/")

                # 检查期望的文件
                expected_files = [
                    "data_exploration.md",
                    "statistical_analysis.md",
                    "pandaai_analysis.md",
                    "final_report.md",
                    "execution_log.txt"
                ]

                for expected_file in expected_files:
                    file_path = task_dir / expected_file
                    exists = file_path.exists()
                    size = f"{file_path.stat().st_size} bytes" if exists else "N/A"
                    status = "✅" if exists else "❌"
                    print(f"     {status} {expected_file:30} ({size})")

    print("\n" + "=" * 60)
    print("✅ 输出目录结构检查完成")
    print("=" * 60)

    # 打印预期结构
    print("\n📋 预期的目录结构:")
    print("""
web/outputs/
├── {task_id}/
│   ├── data_exploration.md      # 数据探索 Agent 的输出
│   ├── statistical_analysis.md  # 统计分析 Agent 的输出
│   ├── pandaai_analysis.md      # PandaAI Agent 的输出
│   ├── final_report.md          # 最终报告
│   └── execution_log.txt        # 完整执行日志
    """)


def simulate_crewai_output():
    """模拟 CrewAI 输出对象，测试结果提取逻辑"""

    print("\n" + "=" * 60)
    print("测试 CrewAI 输出提取逻辑")
    print("=" * 60)

    # 创建模拟的 TaskOutput 类
    class MockTaskOutput:
        def __init__(self, raw_output):
            self.raw = raw_output

        def __str__(self):
            return self.raw

    # 创建模拟的 CrewOutput 类
    class MockCrewOutput:
        def __init__(self):
            self.tasks_output = [
                MockTaskOutput("# 数据探索\n\n这是数据探索的结果..."),
                MockTaskOutput("# 统计分析\n\n这是统计分析的结果..."),
                MockTaskOutput("# PandaAI 分析\n\n这是 PandaAI 分析的结果..."),
                MockTaskOutput("# 最终报告\n\n这是最终报告的内容...")
            ]

        def __str__(self):
            return "CrewAI 执行完成"

    # 测试提取逻辑
    mock_result = MockCrewOutput()

    print(f"\n📊 模拟结果对象类型: {type(mock_result)}")
    print(f"✅ 有 tasks_output 属性: {hasattr(mock_result, 'tasks_output')}")

    if hasattr(mock_result, 'tasks_output'):
        task_outputs = mock_result.tasks_output
        print(f"📝 任务输出数量: {len(task_outputs)}")

        for i, output in enumerate(task_outputs):
            raw_output = output.raw if hasattr(output, 'raw') else str(output)
            print(f"\n  任务 {i+1} 输出预览:")
            print(f"    {raw_output[:50]}...")

    print("\n✅ 提取逻辑测试完成")
    print("=" * 60)


if __name__ == "__main__":
    test_output_directory_structure()
    simulate_crewai_output()

    print("\n✅ 所有测试完成！")
    print("\n💡 提示：运行一次完整的 Web UI 分析任务后，")
    print("   再次运行此脚本以验证实际的输出文件结构。")
