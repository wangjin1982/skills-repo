"""
钉钉群任务通知发送脚本
发送结构化的任务完成通知到钉钉群

使用方法：
    # 基本用法
    python send_task_notification.py --task "数据导出" --status "success" --message "已导出1000条记录"

    # 完整用法
    python send_task_notification.py --task "数据处理" --status "success" --message "处理完成" --duration "5分钟" --extra "文件: output.csv"

环境变量：
    DINGTALK_WEBHOOK_URL - 钉钉机器人 Webhook URL
    DINGTALK_SECRET - 钉钉机器人加签密钥
"""

import sys
import os
import time
import hmac
import hashlib
import base64
import urllib.parse
import requests
import argparse
from datetime import datetime

# 修复 Windows 终端编码问题
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def load_env_file():
    """自动加载 .env 文件中的环境变量"""
    # 获取脚本所在目录的父目录（skill 根目录）
    script_dir = os.path.dirname(os.path.abspath(__file__))
    env_file = os.path.join(script_dir, '..', '.env')

    if os.path.exists(env_file):
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # 跳过注释和空行
                if not line or line.startswith('#'):
                    continue
                # 解析 KEY=VALUE 格式
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    # 如果环境变量未设置，则从 .env 文件加载
                    if key not in os.environ:
                        os.environ[key] = value


# 自动加载 .env 文件
load_env_file()


def get_status_emoji(status):
    """根据状态返回对应的emoji"""
    status_map = {
        "success": "✅",
        "failure": "❌",
        "error": "⚠️",
        "warning": "⚡",
        "progress": "🔄",
        "pending": "⏳",
        "info": "ℹ️"
    }
    return status_map.get(status.lower(), "📋")


def get_status_text(status):
    """根据状态返回中文描述"""
    status_map = {
        "success": "成功",
        "failure": "失败",
        "error": "错误",
        "warning": "警告",
        "progress": "进行中",
        "pending": "等待中",
        "info": "信息"
    }
    return status_map.get(status.lower(), "未知")


def format_message(task_name, status, message, duration=None, extra=None, timestamp=None):
    """
    格式化任务通知消息

    Args:
        task_name (str): 任务名称
        status (str): 任务状态 (success/failure/error/warning/progress/pending/info)
        message (str): 详细消息
        duration (str): 任务耗时（可选）
        extra (str): 额外信息（可选）
        timestamp (str): 时间戳（可选，默认使用当前时间）

    Returns:
        str: 格式化后的消息
    """
    emoji = get_status_emoji(status)
    status_text = get_status_text(status)

    # 获取当前时间
    if timestamp is None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 构建消息
    lines = [
        f"{emoji} 任务通知",
        "",
        f"📌 任务名称：{task_name}",
        f"📊 状态：{status_text}",
        "",
        f"📝 详情：{message}"
    ]

    # 添加可选信息
    if duration:
        lines.append(f"⏱️ 耗时：{duration}")

    if extra:
        lines.append(f"📎 附加：{extra}")

    lines.append("")
    lines.append(f"🕒 时间：{timestamp}")

    return "\n".join(lines)


def send_dingtalk_message(content, webhook_url=None, secret=None):
    """
    发送消息到钉钉群

    Args:
        content (str): 消息内容
        webhook_url (str): Webhook URL（可选，默认从环境变量读取）
        secret (str): 加签密钥（可选，默认从环境变量读取）

    Returns:
        dict: 响应结果 {"success": bool, "message": str}
    """
    # 从环境变量获取配置
    webhook_url = webhook_url or os.environ.get("DINGTALK_WEBHOOK_URL")
    secret = secret or os.environ.get("DINGTALK_SECRET")

    if not webhook_url or not secret:
        return {
            "success": False,
            "message": "错误：未配置 Webhook URL 或 Secret。请设置环境变量 DINGTALK_WEBHOOK_URL 和 DINGTALK_SECRET"
        }

    try:
        # 生成签名
        timestamp = str(round(time.time() * 1000))
        secret_enc = secret.encode('utf-8')
        string_to_sign = f'{timestamp}\n{secret}'
        string_to_sign_enc = string_to_sign.encode('utf-8')

        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))

        # 构建完整 URL
        signed_url = f"{webhook_url}&timestamp={timestamp}&sign={sign}"

        # 发送消息
        data = {
            "msgtype": "text",
            "text": {
                "content": content
            }
        }

        response = requests.post(signed_url, json=data, timeout=10)
        result = response.json()

        if result.get('errcode') == 0:
            return {
                "success": True,
                "message": "消息发送成功"
            }
        else:
            return {
                "success": False,
                "message": f"发送失败：{result.get('errmsg', '未知错误')}"
            }

    except Exception as e:
        return {
            "success": False,
            "message": f"异常：{str(e)}"
        }


def main():
    parser = argparse.ArgumentParser(
        description="发送任务通知到钉钉群",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  python send_task_notification.py --task "数据导出" --status "success" --message "已导出1000条记录"
  python send_task_notification.py --task "数据处理" --status "failure" --message "连接超时" --duration "30秒"
  python send_task_notification.py --task "备份任务" --status "progress" --message "正在压缩文件" --extra "进度: 50%"
        """
    )

    parser.add_argument("--task", required=True, help="任务名称")
    parser.add_argument("--status", required=True,
                       choices=["success", "failure", "error", "warning", "progress", "pending", "info"],
                       help="任务状态")
    parser.add_argument("--message", required=True, help="详细消息")
    parser.add_argument("--duration", help="任务耗时（如：5分钟、30秒）")
    parser.add_argument("--extra", help="额外信息（如：文件路径、URL等）")
    parser.add_argument("--no-timestamp", action="store_true", help="不显示时间戳")

    args = parser.parse_args()

    # 格式化消息
    timestamp = None if args.no_timestamp else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = format_message(
        task_name=args.task,
        status=args.status,
        message=args.message,
        duration=args.duration,
        extra=args.extra,
        timestamp=timestamp
    )

    # 发送消息
    result = send_dingtalk_message(message)

    if result["success"]:
        print(f"✓ {result['message']}")
        print(f"\n发送内容预览：\n{message}")
        sys.exit(0)
    else:
        print(f"✗ {result['message']}")
        sys.exit(1)


if __name__ == "__main__":
    main()
