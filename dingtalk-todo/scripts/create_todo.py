"""
钉钉待办任务创建工具
主入口脚本，支持多种认证方式
"""

import argparse
import sys
import os
import io

# 设置标准输出编码为 UTF-8，解决 Windows 下的 emoji 显示问题
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 添加脚本目录到路径
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from webhook_todo import send_webhook_todo
from enterprise_todo import create_enterprise_todo


def detect_auth_method():
    """
    检测可用的认证方式

    Returns:
        str: 'enterprise', 'webhook', 或 'none'
    """
    # 优先检测企业应用凭证
    if os.getenv('DINGTALK_APP_KEY') and os.getenv('DINGTALK_APP_SECRET') and os.getenv('DINGTALK_OPERATOR_ID'):
        return 'enterprise'

    # 检测 Webhook 凭证
    if os.getenv('DINGTALK_WEBHOOK_URL') and os.getenv('DINGTALK_SECRET'):
        return 'webhook'

    return 'none'


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description='钉钉待办任务创建工具 - 在钉钉中创建待办任务',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
使用示例：
  python create_todo.py --subject "完成项目报告"
  python create_todo.py --subject "代码审查" --description "审查PR #123"
  python create_todo.py -s "编写测试用例" -d "覆盖核心功能"
        '''
    )

    parser.add_argument(
        '--subject', '-s',
        required=True,
        help='任务标题（必需）'
    )

    parser.add_argument(
        '--description', '-d',
        default='',
        help='任务描述（可选）'
    )

    parser.add_argument(
        '--webhook-url',
        default=None,
        help='Webhook URL（可选，覆盖环境变量）'
    )

    parser.add_argument(
        '--secret',
        default=None,
        help='Webhook 密钥（可选，覆盖环境变量）'
    )

    args = parser.parse_args()

    # 如果提供了命令行参数，设置到环境变量
    if args.webhook_url:
        os.environ['DINGTALK_WEBHOOK_URL'] = args.webhook_url
    if args.secret:
        os.environ['DINGTALK_SECRET'] = args.secret

    # 显示任务信息
    print("=" * 50)
    print("📋 钉钉待办任务创建工具")
    print("=" * 50)
    print(f"任务标题：{args.subject}")
    if args.description:
        print(f"任务描述：{args.description}")
    print("-" * 50)

    # 检测认证方式
    auth_method = detect_auth_method()

    if auth_method == 'enterprise':
        print("📱 使用模式：企业应用 API")
        print("💡 创建真正的待办任务")
        print("-" * 50)
        success = create_enterprise_todo(args.subject, args.description)
    elif auth_method == 'webhook':
        print("💬 使用模式：Webhook 群消息")
        print("💡 发送结构化待办消息")
        print("-" * 50)
        success = send_webhook_todo(args.subject, args.description)
    else:
        print("❌ 错误：未找到有效的认证信息")
        print()
        print("请设置以下环境变量之一：")
        print()
        print("📱 方式一：企业应用模式（真正的待办任务）")
        print("   DINGTALK_APP_KEY=your_app_key")
        print("   DINGTALK_APP_SECRET=your_app_secret")
        print("   DINGTALK_OPERATOR_ID=your_union_id")
        print()
        print("💬 方式二：Webhook 模式（立即可用）")
        print("   DINGTALK_WEBHOOK_URL=https://oapi.dingtalk.com/robot/send?access_token=YOUR_TOKEN")
        print("   DINGTALK_SECRET=SECYOUR_SECRET_KEY")
        print()
        print("💡 提示：详见 .env.example 和 references/setup-guide.md")
        print("=" * 50)
        sys.exit(1)

    # 显示结果
    print("-" * 50)
    if success:
        print("✅ 任务创建成功！")
        print("=" * 50)
        sys.exit(0)
    else:
        print("❌ 任务创建失败！")
        print("=" * 50)
        sys.exit(1)


if __name__ == "__main__":
    main()
