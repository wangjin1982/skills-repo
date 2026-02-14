#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书文档API客户端 v2.0
支持富文本格式、代码块、正确的标题渲染
"""

import requests
import time
import json
import re
from typing import List, Dict, Optional, Tuple

CODE_LANGUAGE_MAP = {
    "text": 1,
    "plaintext": 1,
    "txt": 1,
    "bash": 7,
    "shell": 60,
    "sh": 60,
    "python": 49,
    "py": 49,
    "javascript": 30,
    "js": 30,
    "typescript": 63,
    "ts": 63,
    "java": 29,
    "go": 22,
    "golang": 22,
    "rust": 53,
    "ruby": 52,
    "php": 43,
    "c": 10,
    "cpp": 9,
    "c++": 9,
    "csharp": 8,
    "c#": 8,
    "swift": 61,
    "kotlin": 32,
    "dart": 15,
    "scala": 57,
    "sql": 56,
    "json": 28,
    "yaml": 67,
    "yml": 67,
    "html": 24,
    "css": 12,
    "markdown": 39
}


class FeishuDocClientV2:
    """飞书文档API客户端 v2.0 - 支持富文本格式"""

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
            domain: API域名
        """
        self.app_id = app_id
        self.app_secret = app_secret
        self.domain = domain
        self._token = None
        self._token_expire_time = 0

    def get_token(self) -> str:
        """获取访问令牌（自动缓存和刷新）"""
        if self._token and time.time() < self._token_expire_time - 300:
            return self._token

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
        self._token_expire_time = time.time() + 7200

        return self._token

    def create_document(self, title: str) -> str:
        """创建新的飞书文档"""
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

        return data["data"]["document"]["document_id"]

    def _default_text_style(self) -> Dict[str, bool]:
        return {
            "bold": False,
            "inline_code": False,
            "italic": False,
            "strikethrough": False,
            "underline": False
        }

    def _create_text_element(self, content: str, **styles) -> Dict:
        """
        创建文本元素（支持富文本样式）

        Args:
            content: 文本内容
            **styles: 样式属性（bold, inline_code, italic等）

        Returns:
            文本元素字典
        """
        style = self._default_text_style()
        for key in style.keys():
            if styles.get(key):
                style[key] = True

        text_run = {
            "content": content,
            "text_element_style": style
        }
        return {"text_run": text_run}

    def _parse_inline_styles(self, line: str) -> List[Dict]:
        """解析行内Markdown样式"""
        if not line:
            return [self._create_text_element("")]

        elements: List[Dict] = []
        buffer: List[str] = []
        i = 0
        length = len(line)

        while i < length:
            if line.startswith("**", i):
                end = line.find("**", i + 2)
                if end != -1:
                    if buffer:
                        elements.append(self._create_text_element("".join(buffer)))
                        buffer.clear()
                    elements.append(self._create_text_element(line[i + 2:end], bold=True))
                    i = end + 2
                    continue
            char = line[i]
            if char == "`":
                end = line.find("`", i + 1)
                if end != -1:
                    if buffer:
                        elements.append(self._create_text_element("".join(buffer)))
                        buffer.clear()
                    elements.append(self._create_text_element(line[i + 1:end], inline_code=True))
                    i = end + 1
                    continue
            if char == "*" and (i + 1 >= length or line[i + 1] != "*"):
                end = line.find("*", i + 1)
                if end != -1:
                    if buffer:
                        elements.append(self._create_text_element("".join(buffer)))
                        buffer.clear()
                    elements.append(self._create_text_element(line[i + 1:end], italic=True))
                    i = end + 1
                    continue

            buffer.append(char)
            i += 1

        if buffer:
            elements.append(self._create_text_element("".join(buffer)))

        if not elements:
            elements.append(self._create_text_element(line))

        return elements

    def _build_text_block(self, elements: List[Dict]) -> Dict:
        return {
            "block_type": 2,
            "text": {
                "elements": elements,
                "style": {
                    "align": 1,
                    "folded": False
                }
            }
        }

    def _build_heading_block(self, level: int, text: str) -> Dict:
        safe_level = max(1, min(9, level))
        block_type = 2 + safe_level
        key = f"heading{safe_level}"
        return {
            "block_type": block_type,
            key: {
                "elements": self._parse_inline_styles(text),
                "style": {
                    "align": 1,
                    "folded": False
                }
            }
        }

    def _build_list_block(self, text: str, is_ordered: bool = False) -> Dict:
        block_type = 13 if is_ordered else 12
        key = "ordered" if is_ordered else "bullet"
        return {
            "block_type": block_type,
            key: {
                "elements": self._parse_inline_styles(text),
                "style": {
                    "align": 1,
                    "folded": False
                }
            }
        }

    def _map_code_language(self, language: Optional[str]) -> int:
        if not language:
            return 1
        return CODE_LANGUAGE_MAP.get(language.lower(), 1)

    def _build_code_block(self, code_lines: List[str], language: Optional[str]) -> Dict:
        code_text = "\n".join(code_lines)
        return {
            "block_type": 14,
            "code": {
                "elements": [
                    {
                        "text_run": {
                            "content": code_text,
                            "text_element_style": self._default_text_style()
                        }
                    }
                ],
                "style": {
                    "language": self._map_code_language(language),
                    "wrap": True
                }
            }
        }

    def _parse_markdown_to_elements(self, line: str) -> List[Dict]:
        """
        解析Markdown行，提取文本元素（支持加粗、代码等）

        Args:
            line: Markdown文本行

        Returns:
            文本元素列表
        """
        return self._parse_inline_styles(line)

    def _parse_markdown_to_blocks(self, markdown_content: str) -> List[Dict]:
        """将Markdown文本解析为飞书文档块"""
        normalized = markdown_content.replace('\r\n', '\n')
        lines = normalized.split('\n')
        blocks: List[Dict] = []
        paragraph_buffer: List[str] = []
        code_block: Optional[Dict] = None

        def flush_paragraph(preserve_blank: bool = False):
            nonlocal paragraph_buffer
            if paragraph_buffer:
                text = "\n".join(paragraph_buffer).strip()
                paragraph_buffer = []
                if text:
                    blocks.append(self._build_text_block(self._parse_inline_styles(text)))
                    return
            paragraph_buffer = []
            if preserve_blank:
                blocks.append(self._build_text_block([self._create_text_element("")]))

        for raw_line in lines:
            stripped = raw_line.strip()

            if code_block is not None:
                if stripped.startswith('```'):
                    blocks.append(self._build_code_block(code_block["lines"], code_block["language"]))
                    code_block = None
                else:
                    code_block["lines"].append(raw_line)
                continue

            if stripped.startswith('```'):
                flush_paragraph()
                language = stripped[3:].strip()
                code_block = {"language": language, "lines": []}
                continue

            if not stripped:
                flush_paragraph(preserve_blank=True)
                continue

            heading_match = re.match(r'^(#{1,6})\s+(.*)$', stripped)
            if heading_match:
                flush_paragraph()
                level = len(heading_match.group(1))
                text = heading_match.group(2).strip()
                blocks.append(self._build_heading_block(level, text))
                continue

            ordered_match = re.match(r'^(\d+)\.\s+(.*)$', stripped)
            if ordered_match:
                flush_paragraph()
                blocks.append(self._build_list_block(ordered_match.group(2).strip(), is_ordered=True))
                continue

            bullet_match = re.match(r'^[-*+]\s+(.*)$', stripped)
            if bullet_match:
                flush_paragraph()
                blocks.append(self._build_list_block(bullet_match.group(1).strip(), is_ordered=False))
                continue

            quote_match = re.match(r'^>\s?(.*)$', stripped)
            if quote_match:
                flush_paragraph()
                quote_text = quote_match.group(1).strip()
                blocks.append(self._build_text_block(self._parse_inline_styles(f"> {quote_text}")))
                continue

            paragraph_buffer.append(raw_line)

        flush_paragraph()

        if code_block is not None:
            blocks.append(self._build_code_block(code_block["lines"], code_block["language"]))

        return blocks

    def add_content_from_markdown(
        self,
        doc_id: str,
        markdown_content: str,
        batch_size: int = 20,
        delay: float = 0.2
    ) -> Tuple[int, int]:
        """
        从Markdown内容添加到文档（支持富文本格式）

        Args:
            doc_id: 文档ID
            markdown_content: Markdown内容（字符串）
            batch_size: 每批添加的块数
            delay: 批次间延迟

        Returns:
            (成功数量, 失败数量)
        """
        blocks = self._parse_markdown_to_blocks(markdown_content)
        if not blocks:
            return 0, 0

        success_count = 0
        fail_count = 0

        for start in range(0, len(blocks), batch_size):
            batch = blocks[start:start + batch_size]
            try:
                self.add_blocks(doc_id, batch)
                success_count += len(batch)
            except Exception:
                fail_count += len(batch)

            if delay > 0 and start + batch_size < len(blocks):
                time.sleep(delay)

        return success_count, fail_count

    def add_blocks(self, doc_id: str, blocks: List[Dict], index: int = -1) -> bool:
        """批量添加块到文档"""
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
            raise Exception(f"HTTP错误: {response.status_code}")

        data = response.json()
        if data.get("code") != 0:
            raise Exception(f"添加块失败: {data.get('msg')}")

        return True

    def get_document_url(self, doc_id: str) -> str:
        """获取文档访问链接"""
        return f"https://feishu.cn/docx/{doc_id}"

    def create_document_from_markdown(
        self,
        title: str,
        markdown_content: str,
        show_progress: bool = True
    ) -> str:
        """
        从Markdown内容直接创建文档（一步到位）

        Args:
            title: 文档标题
            markdown_content: Markdown内容
            show_progress: 是否显示进度

        Returns:
            文档URL
        """
        if show_progress:
            print("=" * 60)
            print(f"创建飞书文档: {title}")
            print("=" * 60)
            print()

        # 创建文档
        doc_id = self.create_document(title)

        if show_progress:
            print(f"✅ 文档创建成功: {doc_id}")
            print()
            print("开始添加内容...")
            print("-" * 60)

        # 添加内容
        success, fail = self.add_content_from_markdown(
            doc_id,
            markdown_content,
            batch_size=20,
            delay=0.2
        )

        if show_progress:
            print("-" * 60)
            print()
            print(f"✅ 内容添加完成!")
            print(f"   成功: {success} 个块")
            print(f"   失败: {fail} 个块")
            print()

        # 获取URL
        doc_url = self.get_document_url(doc_id)

        if show_progress:
            print("=" * 60)
            print("🔗 文档链接")
            print("=" * 60)
            print()
            print(f"  {doc_url}")
            print()
            print("=" * 60)
            print()

        return doc_url
