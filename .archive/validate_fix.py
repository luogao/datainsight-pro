#!/usr/bin/env python3
"""
静态代码验证 - 不需要安装 CrewAI

验证修复版本的关键改进：
1. 向后兼容性
2. Task description 中的占位符
3. 移除不必要的 context
4. 使用 sequential process
"""
import re
from pathlib import Path


def validate_file(file_path):
    """验证单个文件"""
    print(f"\n{'='*60}")
    print(f"📄 验证文件: {file_path}")
    print(f"{'='*60}")

    content = Path(file_path).read_text()

    results = {}

    # 检查 1: create_crew 函数签名
    print("\n✅ 检查 1: create_crew 函数签名")
    if re.search(r'def create_crew\(\s*\):', content):
        print("   ✅ create_crew() 无参数（向后兼容）")
        results['signature'] = True
    else:
        print("   ❌ create_crew() 有参数（不兼容）")
        results['signature'] = False

    # 检查 2: 占位符使用
    print("\n✅ 检查 2: Task description 中的占位符")
    placeholder_count = content.count('{dataset_path}')
    goal_count = content.count('{goal}')
    depth_count = content.count('{depth}')

    print(f"   - {{dataset_path}} 出现次数: {placeholder_count}")
    print(f"   - {{goal}} 出现次数: {goal_count}")
    print(f"   - {{depth}} 出现次数: {depth_count}")

    if placeholder_count >= 3:
        print("   ✅ dataset_path 占位符使用正确")
        results['dataset_placeholder'] = True
    else:
        print("   ⚠️  dataset_path 占位符可能不足")
        results['dataset_placeholder'] = False

    # 检查 3: context 使用
    print("\n✅ 检查 3: Task 的 context 参数")
    context_matches = re.findall(r'context\s*=\s*\[([^\]]+)\]', content)

    if not context_matches:
        print("   ✅ 没有 context 参数（正确，避免数据传递问题）")
        results['no_context'] = True
    else:
        print(f"   ⚠️  发现 {len(context_matches)} 个 context 参数")
        for i, ctx in enumerate(context_matches, 1):
            print(f"      {i}. context=[{ctx[:50]}...]")
        results['no_context'] = False

    # 检查 4: Process 类型
    print("\n✅ 检查 4: Process 类型")
    if 'Process.sequential' in content:
        print("   ✅ 使用 sequential process")
        results['sequential'] = True
    elif 'Process.hierarchical' in content:
        print("   ⚠️  使用 hierarchical process（建议改用 sequential）")
        results['sequential'] = False
    else:
        print("   ❓ 未找到 Process 定义")
        results['sequential'] = None

    # 检查 5: manager_llm
    print("\n✅ 检查 5: manager_llm 参数")
    if 'manager_llm=' in content and 'Process.sequential' in content:
        print("   ⚠️  使用 sequential 不需要 manager_llm")
        results['no_manager'] = False
    elif 'manager_llm=' not in content:
        print("   ✅ 没有 manager_llm（sequential 不需要）")
        results['no_manager'] = True
    else:
        print("   ℹ️  使用 hierarchical + manager_llm")
        results['no_manager'] = False

    # 检查 6: 关键指令
    print("\n✅ 检查 6: Task description 中的关键指令")
    key_phrases = [
        ('直接读取', 'Direct read'),
        ('read_csv_dataset', 'Tool usage'),
        ('不要依赖', 'No dependency'),
        ('独立', 'Independent')
    ]

    for phrase, desc in key_phrases:
        count = content.count(phrase)
        if count > 0:
            print(f"   ✅ 包含 '{phrase}' ({count} 次) - {desc}")
        else:
            print(f"   ⚠️  未包含 '{phrase}' - {desc}")

    return results


def compare_versions(v2_path, fixed_path):
    """对比 V2 和修复版本"""
    print(f"\n{'='*60}")
    print("🔄 版本对比分析")
    print(f"{'='*60}")

    v2_content = Path(v2_path).read_text()
    fixed_content = Path(fixed_path).read_text()

    print("\n📊 关键差异:")
    print("-"*60)

    # 对比项 1: context 使用
    v2_contexts = len(re.findall(r'context\s*=', v2_content))
    fixed_contexts = len(re.findall(r'context\s*=', fixed_content))

    print(f"\n1. context 参数数量:")
    print(f"   V2: {v2_contexts} 个")
    print(f"   Fixed: {fixed_contexts} 个")
    if fixed_contexts < v2_contexts:
        print(f"   ✅ 改进: 减少了 {v2_contexts - fixed_contexts} 个 context 依赖")
    else:
        print(f"   ⚠️  未改进")

    # 对比项 2: Process 类型
    print(f"\n2. Process 类型:")
    v2_process = 'hierarchical' if 'Process.hierarchical' in v2_content else 'sequential'
    fixed_process = 'hierarchical' if 'Process.hierarchical' in fixed_content else 'sequential'
    print(f"   V2: {v2_process}")
    print(f"   Fixed: {fixed_process}")
    if v2_process != fixed_process:
        print(f"   ✅ 改进: 从 {v2_process} 改为 {fixed_process}")

    # 对比项 3: 占位符使用
    print(f"\n3. dataset_path 占位符:")
    v2_placeholder = v2_content.count('{dataset_path}')
    fixed_placeholder = fixed_content.count('{dataset_path}')
    print(f"   V2: {v2_placeholder} 次")
    print(f"   Fixed: {fixed_placeholder} 次")
    if fixed_placeholder > v2_placeholder:
        print(f"   ✅ 改进: 增加了 {fixed_placeholder - v2_placeholder} 个占位符")

    # 对比项 4: manager_llm
    print(f"\n4. manager_llm:")
    v2_manager = 'manager_llm=' in v2_content
    fixed_manager = 'manager_llm=' in fixed_content
    print(f"   V2: {'使用' if v2_manager else '不使用'}")
    print(f"   Fixed: {'使用' if fixed_manager else '不使用'}")
    if v2_manager and not fixed_manager:
        print(f"   ✅ 改进: 移除 manager_llm，节省成本")


def main():
    """主函数"""
    print("\n")
    print("🔍 CrewAI 修复版本 - 静态代码验证")
    print("="*60)

    # 验证修复版本
    fixed_path = "src/crew_v2_fixed.py"
    if Path(fixed_path).exists():
        results = validate_file(fixed_path)
    else:
        print(f"\n❌ 文件不存在: {fixed_path}")
        return

    # 对比 V2 和修复版本
    v2_path = "src/crew_v2.py"
    if Path(v2_path).exists():
        compare_versions(v2_path, fixed_path)
    else:
        print(f"\n⚠️  V2 版本不存在: {v2_path}")

    # 总结
    print("\n" + "="*60)
    print("📋 验证总结")
    print("="*60)

    if results.get('signature'):
        print("✅ 向后兼容性: 通过")
    else:
        print("❌ 向后兼容性: 失败")

    if results.get('dataset_placeholder'):
        print("✅ 占位符使用: 正确")
    else:
        print("⚠️  占位符使用: 需检查")

    if results.get('no_context'):
        print("✅ 移除 context: 通过（解决数据传递问题）")
    else:
        print("⚠️  仍然使用 context: 可能仍有数据传递问题")

    if results.get('sequential'):
        print("✅ Process 类型: sequential（推荐）")
    elif results.get('sequential') is False:
        print("⚠️  Process 类型: hierarchical（建议改用 sequential）")

    if results.get('no_manager'):
        print("✅ 无 manager_llm: 节省成本")
    else:
        print("ℹ️  使用 manager_llm: 适用于 hierarchical")

    # 最终建议
    print("\n" + "="*60)
    print("💡 建议")
    print("="*60)

    all_good = (
        results.get('signature') and
        results.get('dataset_placeholder') and
        results.get('no_context') and
        results.get('sequential') and
        results.get('no_manager')
    )

    if all_good:
        print("✅ 修复版本完全符合要求！")
        print("\n📝 应用修复:")
        print("   1. 备份原版本:")
        print("      cp src/crew_v2.py src/crew_v2_backup.py")
        print("\n   2. 应用修复:")
        print("      cp src/crew_v2_fixed.py src/crew_v2.py")
        print("\n   3. 验证功能:")
        print("      pip install -r requirements.txt")
        print("      python src/crew_v2.py")
    else:
        print("⚠️  修复版本需要进一步改进")

    print("\n" + "="*60)


if __name__ == "__main__":
    main()
