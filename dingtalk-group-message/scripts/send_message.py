"""
钉钉群消息发送脚本
通过钉钉群机器人发送文本消息

使用方法：
    python send_message.py "消息内容"

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


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使用方法: python send_message.py \"消息内容\"")
        sys.exit(1)

    message = sys.argv[1]
    result = send_dingtalk_message(message)

    if result["success"]:
        print(f"✓ {result['message']}")
        sys.exit(0)
    else:
        print(f"✗ {result['message']}")
        sys.exit(1)
