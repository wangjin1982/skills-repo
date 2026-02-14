#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书文档API客户端
提供创建、编辑、搜索飞书文档的完整功能
"""

import requests
import time
import json
import os
from typing import List, Dict, Optional, Tuple
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


class FeishuDocClient:
    """飞书文档API客户端"""

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

    def create_document(self, title: str) -> str:
        """
        创建新的飞书文档

        Args:
            title: 文档标题

        Returns:
            文档ID

        Raises:
            Exception: 创建失败时抛出异常
        """
        token = self.get_token()
        url = f"{self.domain}/open-apis/docx/v1/documents"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        payload = {"title": title}

        response = requests.post(url, headers=headers, json=payload)
        data = response.json()

        if data.get("code") != 0:
            raise Exception(f"创建文档失败: {data.get('msg')}")

        doc_id = data["data"]["document"]["document_id"]
        return doc_id

    def add_text_block(
        self,
        doc_id: str,
        text: str,
        block_type: str = "text"
    ) -> bool:
        """
        添加单个文本块到文档

        Args:
            doc_id: 文档ID
            text: 文本内容
            block_type: 块类型 (text, heading1, heading2, heading3)

        Returns:
            是否添加成功
        """
        # 块类型映射
        block_type_map = {
            "heading1": 1,
            "heading2": 2,
            "heading3": 3,
            "text": 2  # 文本段落使用2
        }

        if block_type not in block_type_map:
            raise ValueError(f"不支持的块类型: {block_type}")

        block_type_code = block_type_map[block_type]

        # 构造块数据
        if block_type.startswith("heading"):
            # 标题块
            block = {
                "block_type": block_type_code,
                block_type: {
                    "elements": [
                        {"text_run": {"content": text}}
                    ]
                }
            }
        else:
            # 文本块
            block = {
                "block_type": block_type_code,
                "text": {
                    "elements": [
                        {"text_run": {"content": text}}
                    ]
                }
            }

        return self.add_blocks(doc_id, [block])

    def add_blocks(
        self,
        doc_id: str,
        blocks: List[Dict],
        index: int = -1
    ) -> bool:
        """
        批量添加块到文档

        Args:
            doc_id: 文档ID
            blocks: 块列表
            index: 插入位置，-1表示追加到末尾

        Returns:
            是否添加成功
        """
        token = self.get_token()
        url = f"{self.domain}/open-apis/docx/v1/documents/{doc_id}/blocks/{doc_id}/children"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        payload = {
            "children": blocks,
            "index": index
        }

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code != 200:
            error_detail = ""
            try:
                error_data = response.json()
                error_detail = f", 详情: {error_data}"
            except:
                error_detail = f", 响应: {response.text[:200]}"
            raise Exception(f"HTTP错误: {response.status_code}{error_detail}")

        data = response.json()
        if data.get("code") != 0:
            raise Exception(f"添加块失败: {data.get('msg')}, code: {data.get('code')}, 详情: {data}")

        return True

    def add_content_from_markdown(
        self,
        doc_id: str,
        markdown_file: str,
        batch_size: int = 20,
        delay: float = 0.2
    ) -> Tuple[int, int]:
        """
        从Markdown文件添加内容到文档

        Args:
            doc_id: 文档ID
            markdown_file: Markdown文件路径
            batch_size: 每批添加的块数
            delay: 批次之间的延迟（秒）

        Returns:
            (成功数量, 失败数量)
        """
        # 读取Markdown文件
        with open(markdown_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        success_count = 0
        fail_count = 0

        in_code_block = False
        code_block_content = []
        code_block_lang = ""

        all_blocks = []

        for line in lines:
            line_stripped = line.rstrip()

            # 检测代码块开始/结束
            if line_stripped.startswith("```"):
                if not in_code_block:
                    # 进入代码块
                    in_code_block = True
                    code_block_lang = line_stripped[3:].strip()
                    code_block_content = []
                else:
                    # 退出代码块 - 将整个代码块作为普通文本添加
                    # 先添加代码块标记
                    all_blocks.append({
                        "block_type": 2,
                        "text": {"elements": [{"text_run": {"content": f"代码示例 ({code_block_lang}):"}}]}
                    })
                    # 将每行代码作为独立文本块添加
                    for code_line in code_block_content:
                        if code_line.strip():  # 跳过空行
                            all_blocks.append({
                                "block_type": 2,
                                "text": {"elements": [{"text_run": {"content": "  " + code_line}}]}
                            })
                    in_code_block = False
                    code_block_content = []
                continue

            # 如果在代码块中,收集内容
            if in_code_block:
                code_block_content.append(line_stripped)
                continue

            # 处理普通Markdown内容
            if not line_stripped:
                # 空行 - 跳过空行以减少块数量
                continue

            # 根据Markdown语法转换
            # 注意:由于权限限制,所有标题都转换为普通文本块
            if line_stripped.startswith("# "):
                text = line_stripped[2:].strip()
                all_blocks.append({
                    "block_type": 2,
                    "text": {"elements": [{"text_run": {"content": "# " + text}}]}
                })
            elif line_stripped.startswith("## "):
                text = line_stripped[3:].strip()
                all_blocks.append({
                    "block_type": 2,
                    "text": {"elements": [{"text_run": {"content": "## " + text}}]}
                })
            elif line_stripped.startswith("### "):
                text = line_stripped[4:].strip()
                all_blocks.append({
                    "block_type": 2,
                    "text": {"elements": [{"text_run": {"content": "### " + text}}]}
                })
            elif line_stripped.startswith("- "):
                text = line_stripped[2:].strip()
                all_blocks.append({
                    "block_type": 2,
                    "text": {"elements": [{"text_run": {"content": "• " + text}}]}
                })
            else:
                # 普通文本，移除markdown格式
                text = line_stripped.replace("**", "").replace("*", "").strip()
                if text:  # 只添加非空文本
                    all_blocks.append({
                        "block_type": 2,
                        "text": {"elements": [{"text_run": {"content": text}}]}
                    })

        # 分批发送
        for i in range(0, len(all_blocks), batch_size):
            batch_blocks = all_blocks[i:i+batch_size]

            if batch_blocks:
                try:
                    self.add_blocks(doc_id, batch_blocks)
                    success_count += len(batch_blocks)
                    print(f"✅ 批次 {i//batch_size + 1}: 成功添加 {len(batch_blocks)} 个块")
                except Exception as e:
                    fail_count += len(batch_blocks)
                    print(f"❌ 批次 {i//batch_size + 1} 失败: {str(e)}")

            # 延迟避免触发频率限制
            if i + batch_size < len(all_blocks):
                time.sleep(delay)

        return success_count, fail_count

    def search_documents(
        self,
        query: str,
        page_size: int = 20
    ) -> List[Dict]:
        """
        搜索文档

        Args:
            query: 搜索关键词
            page_size: 每页结果数

        Returns:
            文档列表
        """
        token = self.get_token()
        url = f"{self.domain}/open-apis/docx/v1/documents/search"
        headers = {"Authorization": f"Bearer {token}"}
        params = {
            "query": query,
            "page_size": page_size
        }

        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        if data.get("code") != 0:
            raise Exception(f"搜索失败: {data.get('msg')}")

        items = data.get("data", {}).get("items", [])
        return items

    def get_document_blocks(
        self,
        doc_id: str,
        page_size: int = 50
    ) -> List[Dict]:
        """
        获取文档的块列表

        Args:
            doc_id: 文档ID
            page_size: 每页结果数

        Returns:
            块列表
        """
        token = self.get_token()
        url = f"{self.domain}/open-apis/docx/v1/documents/{doc_id}/blocks/{doc_id}/children"
        headers = {"Authorization": f"Bearer {token}"}
        params = {"page_size": page_size}

        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        if data.get("code") != 0:
            raise Exception(f"获取块失败: {data.get('msg')}")

        items = data.get("data", {}).get("items", [])
        return items

    def get_document_info(self, doc_id: str) -> Dict:
        """
        获取文档信息

        Args:
            doc_id: 文档ID

        Returns:
            文档信息字典
        """
        token = self.get_token()
        url = f"{self.domain}/open-apis/docx/v1/documents/{doc_id}"
        headers = {"Authorization": f"Bearer {token}"}

        response = requests.get(url, headers=headers)
        data = response.json()

        if data.get("code") != 0:
            raise Exception(f"获取文档信息失败: {data.get('msg')}")

        return data.get("data", {}).get("document", {})

    def get_document_url(self, doc_id: str) -> str:
        """
        获取文档访问链接

        Args:
            doc_id: 文档ID

        Returns:
            文档URL
        """
        return f"https://feishu.cn/docx/{doc_id}"

    def update_text_block(
        self,
        doc_id: str,
        block_id: str,
        new_text: str
    ) -> bool:
        """
        更新文本块的内容

        Args:
            doc_id: 文档ID
            block_id: 块ID
            new_text: 新的文本内容

        Returns:
            是否更新成功
        """
        # 注意：此功能需要额外的API端点
        # 实际实现取决于飞书API的具体版本
        raise NotImplementedError("此功能待实现")

    def delete_block(
        self,
        doc_id: str,
        block_id: str
    ) -> bool:
        """
        删除文档块

        Args:
            doc_id: 文档ID
            block_id: 块ID

        Returns:
            是否删除成功
        """
        token = self.get_token()
        url = f"{self.domain}/open-apis/docx/v1/documents/{doc_id}/blocks/{block_id}"
        headers = {"Authorization": f"Bearer {token}"}

        response = requests.delete(url, headers=headers)
        data = response.json()

        if data.get("code") != 0:
            raise Exception(f"删除块失败: {data.get('msg')}")

        return True


def create_manager(app_id: str = None, app_secret: str = None) -> FeishuDocClient:
    """
    创建飞书文档客户端实例（便捷函数）

    Args:
        app_id: 飞书应用ID（可选，不传则自动从配置文件读取）
        app_secret: 飞书应用密钥（可选，不传则自动从配置文件读取）

    Returns:
        FeishuDocClient实例

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

    return FeishuDocClient(app_id, app_secret)
