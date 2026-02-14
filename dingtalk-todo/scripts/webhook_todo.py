"""
Webhook 模式待办消息发送
基于钉钉群机器人发送结构化待办消息
"""

import requests
import time
import hmac
import hashlib
import base64
import urllib.parse
import os


def send_webhook_todo(subject, description="", webhook_url=None, secret=None):
    """
    发送待办消息到钉钉群

    Args:
        subject (str): 任务标题
        description (str): 任务描述，可选
        webhook_url (str): Webhook URL，如果不提供则从环境变量读取
        secret (str): 签名密钥，如果不提供则从环境变量读取

    Returns:
        bool: 发送成功返回 True，失败返回 False
    """
    # 从环境变量获取配置
    webhook_url = webhook_url or os.getenv('DINGTALK_WEBHOOK_URL')
    secret = secret or os.getenv('DINGTALK_SECRET')

    if not webhook_url or not secret:
        print("[ERROR] 缺少 Webhook 配置")
        print("请设置环境变量：DINGTALK_WEBHOOK_URL 和 DINGTALK_SECRET")
        return False

    try:
        # 生成签名
        timestamp = str(round(time.time() * 1000))
        secret_enc = secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')

        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))

        # 构建完整 URL
        signed_url = f"{webhook_url}&timestamp={timestamp}&sign={sign}"

        # 构建待办消息内容
        message = "📋 新待办任务\n\n"
        message += f"📌 任务：{subject}"

        if description:
            message += f"\n\n📝 详情：{description}"

        message += "\n\n💡 提示：长按此消息可添加到待办"

        # 发送消息
        data = {
            "msgtype": "text",
            "text": {
                "content": message
            }
        }

        response = requests.post(signed_url, json=data, timeout=10)
        result = response.json()

        if result.get('errcode') == 0:
            print(f"[OK] 待办消息发送成功！")
            return True
        else:
            print(f"[ERROR] 待办消息发送失败: {result}")
            return False

    except Exception as e:
        print(f"[ERROR] 发送待办消息时出错: {str(e)}")
        return False
