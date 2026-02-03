#!/usr/bin/env python3
"""
测试 Web UI 修复
验证 Task 导入和 Crew 创建是否正常
"""
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

print("=" * 60)
print("测试 1: 导入 CrewAI 核心组件")
print("=" * 60)

try:
    from crewai import Agent, Task, Crew, Process
    print("✅ from crewai import Agent, Task, Crew, Process - 成功")
except ImportError as e:
    print(f"❌ 导入失败: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("测试 2: 导入自定义 Agents")
print("=" * 60)

try:
    from src.agents.data_explorer_v2 import data_explorer
    print("✅ 导入 data_explorer - 成功")
    print(f"   - Role: {data_explorer.role}")
    print(f"   - Tools 数量: {len(data_explorer.tools)}")
except ImportError as e:
    print(f"❌ 导入 data_explorer 失败: {e}")
    sys.exit(1)

try:
    from src.agents.analyst_v2 import analyst
    print("✅ 导入 analyst - 成功")
    print(f"   - Role: {analyst.role}")
    print(f"   - Tools 数量: {len(analyst.tools)}")
except ImportError as e:
    print(f"❌ 导入 analyst 失败: {e}")
    sys.exit(1)

try:
    from src.agents.pandaai_real import pandaai_agent
    print("✅ 导入 pandaai_agent - 成功")
    print(f"   - Role: {pandaai_agent.role}")
    print(f"   - Tools 数量: {len(pandaai_agent.tools)}")
except ImportError as e:
    print(f"❌ 导入 pandaai_agent 失败: {e}")
    sys.exit(1)

try:
    from src.agents.reporter_v2 import reporter
    print("✅ 导入 reporter - 成功")
    print(f"   - Role: {reporter.role}")
    print(f"   - Tools 数量: {len(reporter.tools)}")
except ImportError as e:
    print(f"❌ 导入 reporter 失败: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("测试 3: 创建 Task")
print("=" * 60)

try:
    test_task = Task(
        description="测试任务：读取数据集 /tmp/test.csv",
        expected_output="测试输出",
        agent=data_explorer
    )
    print("✅ 创建 Task - 成功")
    print(f"   - Description: {test_task.description[:50]}...")
except Exception as e:
    print(f"❌ 创建 Task 失败: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("测试 4: 创建 Crew")
print("=" * 60)

try:
    test_crew = Crew(
        agents=[data_explorer, analyst],
        tasks=[test_task],
        process=Process.sequential,
        verbose=True
    )
    print("✅ 创建 Crew - 成功")
    print(f"   - Agents 数量: {len(test_crew.agents)}")
    print(f"   - Tasks 数量: {len(test_crew.tasks)}")
except Exception as e:
    print(f"❌ 创建 Crew 失败: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("✅ 所有测试通过！Web UI 修复成功")
print("=" * 60)
print("\n可以重启 Web UI 服务进行测试")
