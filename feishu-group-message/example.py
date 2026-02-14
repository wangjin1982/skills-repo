#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书群消息通知 Skill 使用示例
展示各种实际使用场景
"""

import os
import sys
import time
sys.path.insert(0, '/home/aiops/.claude/skills/feishu-group-message')

from feishu_group_messenger import create_messenger

def require_env(var_name: str, fallback: str | None = None) -> str:
    value = os.getenv(var_name)
    if not value and fallback:
        value = os.getenv(fallback)
    if not value:
        target = var_name if not fallback else f"{var_name}/{fallback}"
        raise EnvironmentError(f"缺少环境变量: {target}")
    return value

# 配置信息
APP_ID = require_env("FEISHU_APP_ID")
APP_SECRET = require_env("FEISHU_APP_SECRET")
CHAT_ID = require_env("FEISHU_CHAT_ID_DEMO", "FEISHU_CHAT_ID_MAIN")


def example_1_simple_notification():
    """示例1：简单的任务完成通知"""
    print("=" * 70)
    print("示例1：简单的任务完成通知")
    print("=" * 70)

    messenger = create_messenger(APP_ID, APP_SECRET)

    result = messenger.send_task_notification(
        chat_id=CHAT_ID,
        task_name="测试任务",
        status="success",
        details="这是一个测试通知"
    )

    print_result(result)
    print()


def example_2_data_import_notification():
    """示例2：数据导入完成通知"""
    print("=" * 70)
    print("示例2：数据导入完成通知")
    print("=" * 70)

    messenger = create_messenger(APP_ID, APP_SECRET)

    result = messenger.send_rich_task_notification(
        chat_id=CHAT_ID,
        task_name="飞书多维表格数据导入",
        status="success",
        details="成功导入生物医药数据到飞书多维表格",
        metrics={
            "表格数量": "5",
            "总记录数": "27",
            "处理时间": "15秒",
            "清理空记录": "50"
        },
        links={
            "全球生物医药动态": "https://feishu.cn/base/SRJFbpnpkaMVIcsfXrvcXTu3n70",
            "中国生物医药进展": "https://feishu.cn/base/AzeQbDbtQa05QYs5lPlcnJV3nKf",
            "mRNA疫苗技术进展": "https://feishu.cn/base/VhpPbz7x1aNKzVsEA40cF1mqntd"
        }
    )

    print_result(result)
    print()


def example_3_error_notification():
    """示例3：任务失败通知"""
    print("=" * 70)
    print("示例3：任务失败通知")
    print("=" * 70)

    messenger = create_messenger(APP_ID, APP_SECRET)

    result = messenger.send_task_notification(
        chat_id=CHAT_ID,
        task_name="API请求任务",
        status="failed",
        details="连接超时：无法连接到远程服务器\n\n可能原因：\n1. 网络不稳定\n2. 服务器宕机\n3. 防火墙阻止",
        links={
            "查看日志": "https://logs.example.com/task-123",
            "重试": "https://example.com/retry"
        }
    )

    print_result(result)
    print()


def example_4_warning_notification():
    """示例4：警告通知"""
    print("=" * 70)
    print("示例4：警告通知")
    print("=" * 70)

    messenger = create_messenger(APP_ID, APP_SECRET)

    result = messenger.send_task_notification(
        chat_id=CHAT_ID,
        task_name="数据质量检查",
        status="warning",
        details="发现3条记录缺少必填字段，已自动填充默认值",
        links={
            "查看详情": "https://example.com/data-quality"
        }
    )

    print_result(result)
    print()


def example_5_progress_updates():
    """示例5：进度更新"""
    print("=" * 70)
    print("示例5：进度更新（多个消息）")
    print("=" * 70)

    messenger = create_messenger(APP_ID, APP_SECRET)

    # 模拟任务进度
    steps = [
        ("初始化...", 0),
        ("加载数据...", 1),
        ("处理中...", 2),
        ("保存结果...", 3),
        ("完成！", 4)
    ]

    for step_name, step_num in steps:
        messenger.send_text(
            chat_id=CHAT_ID,
            message=f"📊 数据处理任务: [{step_num + 1}/5] {step_name}"
        )
        print(f"  发送: {step_name}")
        time.sleep(1)  # 实际使用时不需要sleep

    # 最终完成通知
    result = messenger.send_task_notification(
        chat_id=CHAT_ID,
        task_name="数据处理任务",
        status="success",
        details="所有步骤已完成",
        metrics={"总步骤": "5", "耗时": "5秒"}
    )

    print_result(result)
    print()


def example_6_batch_notification():
    """示例6：批量任务汇总通知"""
    print("=" * 70)
    print("示例6：批量任务汇总通知")
    print("=" * 70)

    messenger = create_messenger(APP_ID, APP_SECRET)

    # 模拟批量任务结果
    batch_results = [
        ("全球生物医药动态", True, "https://feishu.cn/base/xxx1"),
        ("中国生物医药进展", True, "https://feishu.cn/base/xxx2"),
        ("mRNA疫苗技术进展", False, None),
        ("关键数据统计", True, "https://feishu.cn/base/xxx3"),
        ("2026年行业展望", True, "https://feishu.cn/base/xxx4"),
    ]

    success_count = sum(1 for _, success, _ in batch_results if success)
    failed_tasks = [name for name, success, _ in batch_results if not success]

    # 构建链接字典
    links = {
        name: url
        for name, success, url in batch_results
        if success and url
    }

    result = messenger.send_rich_task_notification(
        chat_id=CHAT_ID,
        task_name="批量创建飞书多维表格",
        status="success" if not failed_tasks else "warning",
        details=f"失败任务: {', '.join(failed_tasks)}" if failed_tasks else "所有任务完成",
        metrics={
            "总任务数": str(len(batch_results)),
            "成功": str(success_count),
            "失败": str(len(failed_tasks))
        },
        links=links if links else None
    )

    print_result(result)
    print()


def example_7_custom_rich_text():
    """示例7：自定义富文本消息"""
    print("=" * 70)
    print("示例7：自定义富文本消息")
    print("=" * 70)

    messenger = create_messenger(APP_ID, APP_SECRET)

    # 构建富文本内容
    content = [
        {"tag": "text", "text": "📢 重要通知", "style": ["bold"]},
        {"tag": "text", "text": "\n\n"},
        {"tag": "text", "text": "系统将于今晚"},
        {"tag": "text", "text": "10:00 PM", "style": ["bold", "italic"]},
        {"tag": "text", "text": "进行维护升级\n\n"},
        {"tag": "text", "text": "预计耗时：", "style": ["bold"]},
        {"tag": "text", "text": "2小时\n\n"},
        {"tag": "text", "text": "影响范围：", "style": ["bold"]},
        {"tag": "text", "text": "所有在线服务\n\n"},
        {"tag": "text", "text": "请提前做好准备，如有问题请联系运维团队。", "style": ["italic"]},
        {"tag": "text", "text": "\n\n"},
        {"tag": "a", "text": "📋 查看维护计划", "href": "https://example.com/maintenance"},
        {"tag": "text", "text": "\n"},
        {"tag": "a", "text": "📞 联系运维", "href": "mailto:ops@example.com"}
    ]

    result = messenger.send_post(
        chat_id=CHAT_ID,
        title="系统维护通知",
        content=content
    )

    print_result(result)
    print()


def example_8_daily_report():
    """示例8：每日统计报告"""
    print("=" * 70)
    print("示例8：每日统计报告")
    print("=" * 70)

    messenger = create_messenger(APP_ID, APP_SECRET)

    # 模拟每日统计数据
    daily_stats = {
        "date": "2026-01-02",
        "new_users": "156",
        "active_users": "1,234",
        "data_processed": "45.6 GB",
        "api_calls": "12,345",
        "errors": "3"
    }

    result = messenger.send_rich_task_notification(
        chat_id=CHAT_ID,
        task_name=f"每日数据报告 - {daily_stats['date']}",
        status="warning" if int(daily_stats['errors']) > 0 else "success",
        details="今日系统运行平稳" if int(daily_stats['errors']) == 0 else f"发现 {daily_stats['errors']} 个错误",
        metrics={
            "新增用户": daily_stats['new_users'],
            "活跃用户": daily_stats['active_users'],
            "数据处理量": daily_stats['data_processed'],
            "API调用次数": daily_stats['api_calls'],
            "错误数": daily_stats['errors']
        },
        links={
            "📊 详细报告": "https://example.com/daily-report",
            "📈 数据看板": "https://example.com/dashboard"
        }
    )

    print_result(result)
    print()


def example_9_workflow_notification():
    """示例9：工作流程通知（完整示例）"""
    print("=" * 70)
    print("示例9：工作流程通知（完整示例）")
    print("=" * 70)

    messenger = create_messenger(APP_ID, APP_SECRET)

    # 阶段1：开始
    print("  [1/3] 开始处理...")
    messenger.send_text(CHAT_ID, "🔄 开始数据导入流程...")

    # 阶段2：处理中
    print("  [2/3] 处理中...")
    messenger.send_text(CHAT_ID, "📊 正在处理数据，请稍候...")

    # 模拟处理延迟
    time.sleep(1)

    # 阶段3：完成
    print("  [3/3] 完成")
    result = messenger.send_rich_task_notification(
        chat_id=CHAT_ID,
        task_name="数据导入流程",
        status="success",
        details="成功从CSV文件导入数据到飞书多维表格",
        metrics={
            "源文件": "biopharma_data.csv",
            "数据表": "5个",
            "总记录": "27条",
            "处理时间": "1.2秒"
        },
        links={
            "查看数据": "https://feishu.cn/base/SRJFbpnpkaMVIcsfXrvcXTu3n70",
            "查看日志": "https://logs.example.com/import-123"
        }
    )

    print_result(result)
    print()


def example_10_error_with_retry():
    """示例10：带重试的错误处理"""
    print("=" * 70)
    print("示例10：带重试的消息发送")
    print("=" * 70)

    messenger = create_messenger(APP_ID, APP_SECRET)

    def send_with_retry(messenger, method, max_retries=3, **kwargs):
        """带重试的消息发送"""
        for attempt in range(max_retries):
            result = method(**kwargs)

            if result['success']:
                print(f"  ✅ 第 {attempt + 1} 次尝试成功")
                return result

            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                print(f"  ⚠️  第 {attempt + 1} 次失败，{wait_time}秒后重试... (错误: {result['error']})")
                time.sleep(wait_time)

        print(f"  ❌ 所有重试均失败")
        return result

    # 正常情况会成功，这里只是演示重试机制
    result = send_with_retry(
        messenger,
        messenger.send_task_notification,
        max_retries=3,
        chat_id=CHAT_ID,
        task_name="测试重试机制",
        status="success",
        details="这是一个带重试机制的消息"
    )

    print_result(result)
    print()


def print_result(result):
    """打印结果"""
    if result['success']:
        print(f"  ✅ 消息发送成功！")
        print(f"  📨 消息ID: {result['message_id']}")
    else:
        print(f"  ❌ 消息发送失败！")
        print(f"  📝 错误信息: {result['error']}")


def main():
    """运行所有示例"""
    print()
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "飞书群消息通知 Skill - 使用示例" + " " * 18 + "║")
    print("╚" + "=" * 68 + "╝")
    print()

    examples = [
        ("简单任务通知", example_1_simple_notification),
        ("数据导入通知", example_2_data_import_notification),
        ("失败通知", example_3_error_notification),
        ("警告通知", example_4_warning_notification),
        ("进度更新", example_5_progress_updates),
        ("批量任务通知", example_6_batch_notification),
        ("自定义富文本", example_7_custom_rich_text),
        ("每日报告", example_8_daily_report),
        ("工作流程通知", example_9_workflow_notification),
        ("带重试的错误处理", example_10_error_with_retry),
    ]

    print("可用示例：")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")
    print()

    # 运行选中的示例
    selected = [1, 2, 6, 9]  # 选择要运行的示例

    for i in selected:
        if 1 <= i <= len(examples):
            name, func = examples[i - 1]
            try:
                func()
                time.sleep(0.5)  # 避免频率限制
            except Exception as e:
                print(f"  ❌ 示例执行失败: {e}")
                import traceback
                traceback.print_exc()

    print("=" * 70)
    print("✅ 所有示例执行完成！")
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()
