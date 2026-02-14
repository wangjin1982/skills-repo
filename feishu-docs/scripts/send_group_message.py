#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书群消息发送客户端
提供发送文本消息到飞书群聊的功能
"""

import requests
import time
import json
from typing import Optional


class FeishuMessageClient:
    """飞书群消息API客户端"""

    def __init__(
        self,
        app_id: str,
        app_secret: str,
        domain: str = "https://open.feishu.cn"
    ):
        """
        初始化客户端

        Args:
            app_id: 飞书应用ID
            app_secret: 飞书应用密钥
            domain: API域名，默认为飞书国内版
        """
        self.app_id = app_id
        self.app_secret = app_secret
        self.domain = domain
        self._token = None
        self._token_expire_time = 0

    def get_token(self) -> str:
        """
        获取访问令牌（自动缓存和刷新）

        Returns:
            访问令牌字符串
        """
        # 检查token是否有效（提前5分钟刷新）
        if self._token and time.time() < self._token_expire_time - 300:
            return self._token

        # 获取新token
        url = f"{self.domain}/open-apis/auth/v3/tenant_access_token/internal"
        payload = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }

        response = requests.post(url, json=payload)
        data = response.json()

        if data.get("code") != 0:
            raise Exception(f"获取token失败: {data.get('msg')}")

        self._token = data.get("tenant_access_token")
        # token有效期2小时
        self._token_expire_time = time.time() + 7200

        return self._token

    def send_text_message(
        self,
        chat_id: str,
        text: str
    ) -> bool:
        """
        发送文本消息到群聊

        Args:
            chat_id: 群聊ID
            text: 消息文本内容

        Returns:
            是否发送成功
        """
        token = self.get_token()
        url = f"{self.domain}/open-apis/im/v1/messages"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        # 构造消息体
        payload = {
            "receive_id": chat_id,
            "msg_type": "text",
            "content": json.dumps({"text": text})
        }

        response = requests.post(url, headers=headers, json=payload)
        data = response.json()

        if data.get("code") != 0:
            raise Exception(f"发送消息失败: {data.get('msg')}")

        print(f"✅ 消息发送成功! Message ID: {data['data']['message_id']}")
        return True

    def send_post_message(
        self,
        chat_id: str,
        title: str,
        content: list
    ) -> bool:
        """
        发送富文本消息到群聊

        Args:
            chat_id: 群聊ID
            title: 消息标题
            content: 消息内容列表，每个元素是一个文本块

        Returns:
            是否发送成功
        """
        token = self.get_token()
        url = f"{self.domain}/open-apis/im/v1/messages"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        # 构造富文本消息体
        post_content = {
            "post": {
                "zh_cn": {
                    "title": title,
                    "content": content
                }
            }
        }

        payload = {
            "receive_id": chat_id,
            "msg_type": "post",
            "content": json.dumps(post_content)
        }

        response = requests.post(url, headers=headers, json=payload)
        data = response.json()

        if data.get("code") != 0:
            raise Exception(f"发送消息失败: {data.get('msg')}")

        print(f"✅ 富文本消息发送成功! Message ID: {data['data']['message_id']}")
        return True

    def send_interactive_message(
        self,
        chat_id: str,
        card: dict
    ) -> bool:
        """
        发送交互式卡片消息到群聊

        Args:
            chat_id: 群聊ID
            card: 卡片配置（JSON格式）

        Returns:
            是否发送成功
        """
        token = self.get_token()
        url = f"{self.domain}/open-apis/im/v1/messages"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        payload = {
            "receive_id": chat_id,
            "msg_type": "interactive",
            "content": json.dumps(card)
        }

        response = requests.post(url, headers=headers, json=payload)
        data = response.json()

        if data.get("code") != 0:
            raise Exception(f"发送消息失败: {data.get('msg')}")

        print(f"✅ 卡片消息发送成功! Message ID: {data['data']['message_id']}")
        return True


if __name__ == "__main__":
    # 示例用法
    import sys

    if len(sys.argv) < 4:
        print("用法: python send_group_message.py <app_id> <app_secret> <chat_id> <message_file>")
        sys.exit(1)

    app_id = sys.argv[1]
    app_secret = sys.argv[2]
    chat_id = sys.argv[3]
    message_file = sys.argv[4]

    # 读取消息内容
    with open(message_file, 'r', encoding='utf-8') as f:
        message_text = f.read()

    # 发送消息
    client = FeishuMessageClient(app_id, app_secret)
    client.send_text_message(chat_id, message_text)
