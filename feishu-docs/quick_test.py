#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速测试脚本
验证 feishu-docs Skill 是否正常工作
"""

import sys
import os

scripts_dir = os.path.join(os.path.dirname(__file__), 'scripts')
sys.path.insert(0, scripts_dir)

from feishu_api import FeishuDocClient


def test_feishu_docs():
    """测试飞书文档功能"""

    print("=" * 60)
    print("飞书文档Skill - 快速测试")
    print("=" * 60)
    print()

    def require_env(var_name: str, fallback: str | None = None) -> str:
        value = os.getenv(var_name)
        if not value and fallback:
            value = os.getenv(fallback)
        if not value:
            target = var_name if not fallback else f"{var_name}/{fallback}"
            raise EnvironmentError(f"缺少环境变量: {target}")
        return value

    # 配置信息（从环境变量读取）
    app_id = require_env("FEISHU_DOC_APP_ID", "FEISHU_APP_ID")
    app_secret = require_env("FEISHU_DOC_APP_SECRET", "FEISHU_APP_SECRET")

    print("1. 初始化客户端...")
    try:
        client = FeishuDocClient(
            app_id=app_id,
            app_secret=app_secret
        )
        print("   ✅ 客户端初始化成功\n")
    except Exception as e:
        print(f"   ❌ 初始化失败: {e}\n")
        return False

    print("2. 测试创建文档...")
    try:
        doc_id = client.create_document("测试文档 - Skill验证")
        print(f"   ✅ 文档创建成功")
        print(f"   文档ID: {doc_id}\n")
    except Exception as e:
        print(f"   ❌ 创建文档失败: {e}\n")
        return False

    print("3. 测试添加内容...")
    try:
        # 添加一些测试内容
        blocks = [
            {"block_type": 1, "heading1": {"elements": [{"text_run": {"content": "测试标题"}}]}},
            {"block_type": 2, "text": {"elements": [{"text_run": {"content": "这是一个测试文档，用于验证 feishu-docs Skill 的功能。"}}]}},
            {"block_type": 2, "heading2": {"elements": [{"text_run": {"content": "功能列表"}}]}},
            {"block_type": 2, "text": {"elements": [{"text_run": {"content": "✅ 创建文档"}}]}},
            {"block_type": 2, "text": {"elements": [{"text_run": {"content": "✅ 添加内容"}}]}},
            {"block_type": 2, "text": {"elements": [{"text_run": {"content": "✅ 获取链接"}}]}},
        ]

        client.add_blocks(doc_id, blocks)
        print("   ✅ 内容添加成功\n")
    except Exception as e:
        print(f"   ❌ 添加内容失败: {e}\n")
        return False

    print("4. 测试获取文档链接...")
    try:
        url = client.get_document_url(doc_id)
        print(f"   ✅ 文档链接获取成功")
        print(f"   {url}\n")
    except Exception as e:
        print(f"   ❌ 获取链接失败: {e}\n")
        return False

    print("=" * 60)
    print("✅✅✅ 所有测试通过！")
    print("=" * 60)
    print()
    print("飞书文档Skill已正确配置并可以使用！")
    print()
    print(f"测试文档链接: {url}")
    print()
    print("下一步:")
    print("1. 查看 README.md 了解更多功能")
    print("2. 查看 examples.py 学习使用方法")
    print("3. 使用 scripts/create_from_markdown.py 创建文档")
    print()

    return True


if __name__ == "__main__":
    success = test_feishu_docs()
    sys.exit(0 if success else 1)
