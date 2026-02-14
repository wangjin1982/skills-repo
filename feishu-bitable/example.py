#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书多维表格 Skill - 示例和测试脚本
演示如何使用Skill将数据导入飞书多维表格
"""

import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from feishu_bitable_manager import create_manager

def require_env(var_name: str, fallback: str | None = None) -> str:
    value = os.getenv(var_name)
    if not value and fallback:
        value = os.getenv(fallback)
    if not value:
        target = var_name if not fallback else f"{var_name}/{fallback}"
        raise EnvironmentError(f"缺少环境变量: {target}")
    return value

# 配置
APP_ID = require_env("FEISHU_APP_ID")
APP_SECRET = require_env("FEISHU_APP_SECRET")

def example_1_simple_import():
    """示例1：简单的CSV导入"""
    print("=" * 70)
    print("示例1：简单的CSV导入")
    print("=" * 70)
    print()

    manager = create_manager(APP_ID, APP_SECRET)

    # 创建测试CSV文件
    test_csv = "/tmp/test_data.csv"
    with open(test_csv, 'w', encoding='utf-8-sig') as f:
        f.write("姓名,年龄,城市\n")
        f.write("张三,25,北京\n")
        f.write("李四,30,上海\n")
        f.write("王五,28,深圳\n")

    # 导入
    result = manager.import_csv_to_bitable(test_csv, "示例1-简单导入")

    print(f"✅ 导入成功！")
    print(f"📊 链接: {result['url']}")
    print(f"📈 写入: {result['written']} 条")
    print(f"✓ 验证: {result['verified']} 条")
    print()

def example_2_advanced_workflow():
    """示例2：高级工作流（分步操作）"""
    print("=" * 70)
    print("示例2：高级工作流")
    print("=" * 70)
    print()

    manager = create_manager(APP_ID, APP_SECRET)

    # 步骤1：创建应用
    print("步骤1：创建应用...")
    app_token = manager.create_app("示例2-高级工作流")
    print(f"✓ 应用Token: {app_token}")
    print()

    # 步骤2：获取默认数据表
    print("步骤2：获取默认数据表...")
    table_id, table_name = manager.get_default_table(app_token)
    print(f"✓ 数据表ID: {table_id}")
    print(f"✓ 数据表名: {table_name}")
    print()

    # 步骤3：清理现有数据
    print("步骤3：清理现有数据...")
    deleted = manager.delete_all_records(app_token, table_id)
    print(f"✓ 删除了 {deleted} 条旧记录")
    print()

    # 步骤4：删除模板字段
    print("步骤4：删除模板字段...")
    deleted_fields = manager.delete_template_fields(app_token, table_id)
    print(f"✓ 删除了 {deleted_fields} 个模板字段")
    print()

    # 步骤5：创建业务字段
    print("步骤5：创建业务字段...")
    field_names = ["产品", "数量", "价格"]
    created = manager.create_business_fields(app_token, table_id, field_names)
    print(f"✓ 创建了 {created} 个业务字段")
    print()

    # 步骤6：写入数据
    print("步骤6：写入数据...")
    records = [
        {"fields": {"产品": "苹果", "数量": "10", "价格": "5.5"}},
        {"fields": {"产品": "香蕉", "数量": "20", "价格": "3.2"}},
        {"fields": {"产品": "橙子", "数量": "15", "价格": "4.8"}}
    ]
    written = manager.write_records(app_token, table_id, records)
    print(f"✓ 写入了 {written} 条记录")
    print()

    # 步骤7：验证数据
    print("步骤7：验证数据...")
    verification = manager.verify_data(app_token, table_id)
    print(f"✓ 总记录数: {verification['total']}")
    print(f"✓ 业务记录: {verification['business']}")
    print(f"✓ 首条记录: {verification['first_record']}")
    print()

    print(f"📊 链接: https://feishu.cn/base/{app_token}")
    print()

def example_3_cleanup():
    """示例3：清理数据"""
    print("=" * 70)
    print("示例3：清理空记录和重复记录")
    print("=" * 70)
    print()

    manager = create_manager(APP_ID, APP_SECRET)

    # 先创建一个包含重复和空记录的表格
    app_token = manager.create_app("示例3-清理测试")
    table_id, _ = manager.get_default_table(app_token)

    # 写入一些数据（包括重复）
    records = [
        {"fields": {"名称": "A", "值": "1"}},
        {"fields": {"名称": "B", "值": "2"}},
        {"fields": {"名称": "A", "值": "1"}},  # 重复
        {"fields": {"名称": None, "值": None}},  # 空
        {"fields": {"名称": None, "值": None}},  # 空
    ]

    manager.write_records(app_token, table_id, records)
    print(f"写入了 {len(records)} 条记录（包括重复和空记录）")
    print()

    # 清理
    print("执行清理...")
    cleanup = manager.cleanup_data(app_token, table_id)
    print(f"✓ 删除空记录: {cleanup['empty']} 条")
    print(f"✓ 删除重复记录: {cleanup['duplicates']} 条")
    print()

    # 验证
    verification = manager.verify_data(app_token, table_id)
    print(f"✓ 清理后业务记录: {verification['business']} 条")
    print(f"📊 链接: https://feishu.cn/base/{app_token}")
    print()

def example_4_batch_import():
    """示例4：批量导入多个CSV"""
    print("=" * 70)
    print("示例4：批量导入多个CSV")
    print("=" * 70)
    print()

    manager = create_manager(APP_ID, APP_SECRET)

    # 创建测试CSV文件
    csv_files = []
    for i in range(1, 4):
        csv_file = f"/tmp/test_data_{i}.csv"
        with open(csv_file, 'w', encoding='utf-8-sig') as f:
            f.write(f"编号,名称,值\n")
            f.write(f"{i}001,项目{i}-1,100\n")
            f.write(f"{i}002,项目{i}-2,200\n")
        csv_files.append((csv_file, f"批量导入-{i}"))

    # 批量导入
    print(f"开始批量导入 {len(csv_files)} 个文件...")
    print()

    results = []
    for csv_file, table_name in csv_files:
        print(f"处理: {table_name}")
        result = manager.import_csv_to_bitable(csv_file, table_name)
        results.append((table_name, result))
        print(f"  ✓ {result['written']} 条记录")
        print()

    print("=" * 70)
    print("批量导入完成！")
    print()

    for table_name, result in results:
        print(f"✓ {table_name}: {result['url']}")
    print()

def run_all_examples():
    """运行所有示例"""
    print("\n")
    print("*" * 70)
    print("*" + " " * 68 + "*")
    print("*" + " " * 15 + "飞书多维表格 Skill - 示例演示" + " " * 23 + "*")
    print("*" + " " * 68 + "*")
    print("*" * 70)
    print("\n")

    examples = [
        ("示例1：简单的CSV导入", example_1_simple_import),
        ("示例2：高级工作流", example_2_advanced_workflow),
        ("示例3：清理数据", example_3_cleanup),
        ("示例4：批量导入", example_4_batch_import),
    ]

    for name, func in examples:
        try:
            func()
            input(f"按Enter继续下一个示例...")
            print("\n" * 2)
        except Exception as e:
            print(f"❌ 示例执行失败: {e}")
            import traceback
            traceback.print_exc()
            print()

    print("=" * 70)
    print("✅ 所有示例执行完成！")
    print("=" * 70)

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        example_num = sys.argv[1]
        examples = {
            "1": example_1_simple_import,
            "2": example_2_advanced_workflow,
            "3": example_3_cleanup,
            "4": example_4_batch_import,
        }

        if example_num in examples:
            examples[example_num]()
        else:
            print(f"未知示例: {example_num}")
            print("可用示例: 1, 2, 3, 4")
    else:
        run_all_examples()
