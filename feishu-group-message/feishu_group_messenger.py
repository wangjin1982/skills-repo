#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书群消息通知器
用于任务完成后向飞书群组发送通知消息
"""

import requests
import json
import os
from typing import Optional, Dict, List
from pathlib import Path


def _load_config():
    """从配置文件加载飞书凭证"""
    config_paths = [
        Path.home() / ".claude" / "feishu_config.json",
        Path("/home/aiops2/.claude/feishu_config.json"),
    ]
    for config_path in config_paths:
        if config_path.exists():
            with open(config_path, "r") as f:
                return json.load(f)
    return None


def _get_feishu_credentials():
    """获取飞书凭证，优先从配置文件读取，其次从环境变量读取"""
    config = _load_config()
    if config:
        return config.get("app_id"), config.get("app_secret"), config.get("domain", "https://open.feishu.cn")
    # 环境变量备选
    return (
        os.getenv("FEISHU_APP_ID"),
        os.getenv("FEISHU_APP_SECRET"),
        os.getenv("FEISHU_DOMAIN", "https://open.feishu.cn")
    )


class FeishuGroupMessenger:
    """飞书群消息通知器"""

    def __init__(self, app_id: str, app_secret: str, domain: str = "https://open.feishu.cn"):
        """
        初始化消息通知器

        Args:
            app_id: 飞书应用ID
            app_secret: 飞书应用密钥
            domain: API域名
        """
        self.app_id = app_id
        self.app_secret = app_secret
        self.domain = domain
        self._token = None

    def get_token(self) -> str:
        """获取访问令牌"""
        if self._token:
            return self._token

        url = f"{self.domain}/open-apis/auth/v3/tenant_access_token/internal"
        payload = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }

        response = requests.post(url, json=payload)
        data = response.json()

        if data.get("code") != 0:
            raise Exception(f"获取令牌失败: {data.get('msg')}")

        self._token = data.get("tenant_access_token")
        return self._token

    def send_text(self, chat_id: str, message: str) -> Dict:
        """
        发送文本消息到飞书群

        Args:
            chat_id: 群聊ID
            message: 消息内容

        Returns:
            发送结果 {"success": bool, "message_id": str, "error": str}
        """
        token = self.get_token()

        url = f"{self.domain}/open-apis/im/v1/messages?receive_id_type=chat_id"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        content = {"text": message}
        payload = {
            "receive_id": chat_id,
            "msg_type": "text",
            "content": json.dumps(content)
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            data = response.json()

            if data.get("code") == 0:
                return {
                    "success": True,
                    "message_id": data.get("data", {}).get("message_id"),
                    "error": None
                }
            else:
                return {
                    "success": False,
                    "message_id": None,
                    "error": f"Code {data.get('code')}: {data.get('msg')}"
                }

        except Exception as e:
            return {
                "success": False,
                "message_id": None,
                "error": str(e)
            }

    def send_post(self, chat_id: str, title: str, content: List[Dict]) -> Dict:
        """
        发送富文本消息到飞书群

        Args:
            chat_id: 群聊ID
            title: 消息标题
            content: 内容列表，格式为 [{"tag": "text", "text": "内容"}, ...]

        Returns:
            发送结果 {"success": bool, "message_id": str, "error": str}
        """
        token = self.get_token()

        url = f"{self.domain}/open-apis/im/v1/messages?receive_id_type=chat_id"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        post_content = {
            "post": {
                "zh_cn": {
                    "title": title,
                    "content": [content]
                }
            }
        }

        payload = {
            "receive_id": chat_id,
            "msg_type": "post",
            "content": json.dumps(post_content)
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            data = response.json()

            if data.get("code") == 0:
                return {
                    "success": True,
                    "message_id": data.get("data", {}).get("message_id"),
                    "error": None
                }
            else:
                return {
                    "success": False,
                    "message_id": None,
                    "error": f"Code {data.get('code')}: {data.get('msg')}"
                }

        except Exception as e:
            return {
                "success": False,
                "message_id": None,
                "error": str(e)
            }

    def _build_task_markdown(self, task_name: str, status_label: str,
                             details: Optional[str], links: Optional[Dict[str, str]]) -> str:
        """构建任务通知的Markdown正文"""
        lines: List[str] = [
            f"**{task_name}**",
            f"状态：{status_label}"
        ]

        if details:
            lines.append(details.strip())

        if links:
            link_lines = [f"- [{title}]({url})" for title, url in links.items()]
            if link_lines:
                lines.append("相关链接：\n" + "\n".join(link_lines))

        return "\n\n".join(line for line in lines if line).strip()

    def send_markdown_card(self, chat_id: str, title: str, markdown_content: str) -> Dict:
        """
        发送支持Markdown渲染的交互式卡片

        Args:
            chat_id: 群聊ID
            title: 卡片标题
            markdown_content: Markdown正文
        """
        token = self.get_token()

        url = f"{self.domain}/open-apis/im/v1/messages?receive_id_type=chat_id"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        card = {
            "config": {
                "wide_screen_mode": True,
                "enable_forward": True
            },
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": title[:80]
                }
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": markdown_content
                    }
                }
            ]
        }

        payload = {
            "receive_id": chat_id,
            "msg_type": "interactive",
            "content": json.dumps({"card": card})
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            data = response.json()

            if data.get("code") == 0:
                return {
                    "success": True,
                    "message_id": data.get("data", {}).get("message_id"),
                    "error": None
                }
            else:
                return {
                    "success": False,
                    "message_id": None,
                    "error": f"Code {data.get('code')}: {data.get('msg')}"
                }
        except Exception as e:
            return {
                "success": False,
                "message_id": None,
                "error": str(e)
            }

    def send_task_notification(self, chat_id: str, task_name: str,
                               status: str = "success",
                               details: Optional[str] = None,
                               links: Optional[Dict[str, str]] = None) -> Dict:
        """
        发送任务完成通知（推荐使用）

        Args:
            chat_id: 群聊ID
            task_name: 任务名称
            status: 任务状态 ("success", "failed", "warning")
            details: 详细信息
            links: 相关链接字典 {"标题": "URL"}

        Returns:
            发送结果
        """
        # 构建消息内容
        status_emoji = {
            "success": "✅",
            "failed": "❌",
            "warning": "⚠️"
        }

        emoji = status_emoji.get(status, "ℹ️")

        message_parts = [f"{emoji} {task_name}"]

        status_labels = {
            "success": "已完成",
            "failed": "失败",
            "warning": "完成（有警告）"
        }
        status_label = status_labels.get(status, "进行中")
        message_parts.append(status_label)

        if details:
            message_parts.append(f"\n\n📋 {details}")

        if links:
            message_parts.append("\n\n🔗 相关链接:")
            for title, url in links.items():
                message_parts.append(f"\n• {title}: {url}")

        message = "\n".join(message_parts)

        # 优先尝试发送Markdown交互卡片
        card_markdown = self._build_task_markdown(task_name, status_label, details, links)
        card_result = self.send_markdown_card(
            chat_id=chat_id,
            title=f"{emoji} 任务通知",
            markdown_content=card_markdown
        )

        if card_result.get("success"):
            return card_result

        # 兜底降级为纯文本
        return self.send_text(chat_id, message)

    def send_rich_task_notification(self, chat_id: str, task_name: str,
                                    status: str = "success",
                                    details: Optional[str] = None,
                                    links: Optional[Dict[str, str]] = None,
                                    metrics: Optional[Dict[str, str]] = None) -> Dict:
        """
        发送富文本任务完成通知（格式化更美观）

        Args:
            chat_id: 群聊ID
            task_name: 任务名称
            status: 任务状态 ("success", "failed", "warning")
            details: 详细信息
            links: 相关链接字典 {"标题": "URL"}
            metrics: 指标字典 {"指标名": "值"}

        Returns:
            发送结果
        """
        status_emoji = {
            "success": "✅",
            "failed": "❌",
            "warning": "⚠️"
        }

        emoji = status_emoji.get(status, "ℹ️")

        # 构建富文本内容
        content = [
            {"tag": "text", "text": f"{emoji} "},
            {"tag": "text", "text": task_name, "style": ["bold"]}
        ]

        if status == "success":
            content.append({"tag": "text", "text": " - 已完成\n\n"})
        elif status == "failed":
            content.append({"tag": "text", "text": " - 失败\n\n"})
        elif status == "warning":
            content.append({"tag": "text", "text": " - 完成（有警告）\n\n"})

        if details:
            content.extend([
                {"tag": "text", "text": "📋 详情:\n"},
                {"tag": "text", "text": details, "style": ["italic"]}
            ])

        if metrics:
            content.append({"tag": "text", "text": "\n\n📊 数据统计:\n"})
            for key, value in metrics.items():
                content.extend([
                    {"tag": "text", "text": f"• {key}: "},
                    {"tag": "text", "text": value, "style": ["bold"]},
                    {"tag": "text", "text": "\n"}
                ])

        if links:
            content.append({"tag": "text", "text": "\n🔗 相关链接:\n"})
            for title, url in links.items():
                content.append({
                    "tag": "a",
                    "text": f"• {title}",
                    "href": url
                })
                content.append({"tag": "text", "text": "\n"})

        # 构建标题
        title = f"{emoji} 任务通知"

        return self.send_post(chat_id, title, [content])


# 便捷函数
def create_messenger(app_id: str = None, app_secret: str = None) -> FeishuGroupMessenger:
    """
    创建消息通知器实例

    Args:
        app_id: 飞书应用ID（可选，不传则自动从配置文件读取）
        app_secret: 飞书应用密钥（可选，不传则自动从配置文件读取）

    Returns:
        FeishuGroupMessenger实例

    Raises:
        ValueError: 当无法获取凭证时抛出异常
    """
    if app_id is None or app_secret is None:
        cfg_app_id, cfg_app_secret, domain = _get_feishu_credentials()
        if app_id is None:
            app_id = cfg_app_id
        if app_secret is None:
            app_secret = cfg_app_secret

    if not app_id or not app_secret:
        raise ValueError(
            "无法获取飞书凭证。请:\n"
            "1. 在 ~/.claude/feishu_config.json 中配置凭证，或\n"
            "2. 设置环境变量 FEISHU_APP_ID 和 FEISHU_APP_SECRET，或\n"
            "3. 直接传入 app_id 和 app_secret 参数"
        )

    return FeishuGroupMessenger(app_id, app_secret)
