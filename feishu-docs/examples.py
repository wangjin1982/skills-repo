#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书文档操作示例
展示如何使用 feishu-docs Skill 进行各种文档操作
"""

import sys
import os

# 添加scripts目录到路径
scripts_dir = os.path.join(os.path.dirname(__file__), 'scripts')
sys.path.insert(0, scripts_dir)

from feishu_api import FeishuDocClient


# 示例1: 创建一个简单的文档
def example1_create_simple_doc():
    """创建一个简单的文档并添加基本内容"""
    print("=" * 60)
    print("示例1: 创建简单文档")
    print("=" * 60)

    client = FeishuDocClient(
        app_id="your_app_id",
        app_secret="your_app_secret"
    )

    # 创建文档
    doc_id = client.create_document("测试文档")
    print(f"✅ 文档创建成功: {doc_id}")

    # 添加内容块
    blocks = [
        {"block_type": 1, "heading1": {"elements": [{"text_run": {"content": "一级标题"}}]}},
        {"block_type": 2, "text": {"elements": [{"text_run": {"content": "这是一段文本"}}]}},
        {"block_type": 2, "heading2": {"elements": [{"text_run": {"content": "二级标题"}}]}},
        {"block_type": 2, "text": {"elements": [{"text_run": {"content": "另一段文本"}}]}},
    ]

    client.add_blocks(doc_id, blocks)
    print("✅ 内容添加成功")

    print(f"🔗 文档链接: {client.get_document_url(doc_id)}")
    print()


# 示例2: 从Markdown文件创建文档
def example2_create_from_markdown():
    """从Markdown文件创建文档"""
    print("=" * 60)
    print("示例2: 从Markdown创建文档")
    print("=" * 60)

    client = FeishuDocClient(
        app_id="your_app_id",
        app_secret="your_app_secret"
    )

    # 创建文档
    doc_id = client.create_document("从Markdown创建的文档")
    print(f"✅ 文档创建成功: {doc_id}")

    # 从Markdown文件添加内容
    markdown_file = "/path/to/your/document.md"
    success, fail = client.add_content_from_markdown(
        doc_id,
        markdown_file,
        batch_size=20,
        delay=0.2
    )

    print(f"✅ 内容添加完成: 成功 {success}, 失败 {fail}")
    print(f"🔗 文档链接: {client.get_document_url(doc_id)}")
    print()


# 示例3: 批量创建文档
def example3_batch_create():
    """批量创建多个文档"""
    print("=" * 60)
    print("示例3: 批量创建文档")
    print("=" * 60)

    client = FeishuDocClient(
        app_id="your_app_id",
        app_secret="your_app_secret"
    )

    # 定义要创建的文档列表
    documents = [
        ("项目文档1", "/path/to/doc1.md"),
        ("项目文档2", "/path/to/doc2.md"),
        ("会议记录", "/path/to/meeting.md"),
    ]

    for title, md_file in documents:
        try:
            print(f"\n创建: {title}")
            doc_id = client.create_document(title)
            success, fail = client.add_content_from_markdown(doc_id, md_file)
            print(f"  ✅ 成功: {client.get_document_url(doc_id)}")
        except Exception as e:
            print(f"  ❌ 失败: {str(e)}")

    print()


# 示例4: 搜索文档
def example4_search_documents():
    """搜索文档"""
    print("=" * 60)
    print("示例4: 搜索文档")
    print("=" * 60)

    client = FeishuDocClient(
        app_id="your_app_id",
        app_secret="your_app_secret"
    )

    # 搜索文档
    query = "项目"
    results = client.search_documents(query)

    print(f"搜索 '{query}' 找到 {len(results)} 个结果:\n")

    for i, doc in enumerate(results, 1):
        title = doc.get('title', '无标题')
        doc_id = doc.get('document_id', '')
        url = client.get_document_url(doc_id)

        print(f"{i}. {title}")
        print(f"   {url}")
        print()


# 示例5: 获取文档信息和内容
def example5_get_document_info():
    """获取文档详细信息和内容块"""
    print("=" * 60)
    print("示例5: 获取文档信息")
    print("=" * 60)

    client = FeishuDocClient(
        app_id="your_app_id",
        app_secret="your_app_secret"
    )

    doc_id = "your_document_id"

    # 获取文档信息
    info = client.get_document_info(doc_id)
    print(f"文档标题: {info.get('title')}")
    print(f"文档ID: {info.get('document_id')}")

    # 获取文档块
    blocks = client.get_document_blocks(doc_id)
    print(f"\n文档包含 {len(blocks)} 个内容块\n")

    # 显示前几个块
    for i, block in enumerate(blocks[:5], 1):
        block_type = block.get('block_type')
        if block_type == 1:
            content = block.get('heading1', {}).get('elements', [{}])[0].get('text_run', {}).get('content', '')
            print(f"{i}. [标题1] {content}")
        elif block_type == 2:
            # 可能是heading2或text
            if 'heading2' in block:
                content = block['heading2'].get('elements', [{}])[0].get('text_run', {}).get('content', '')
                print(f"{i}. [标题2] {content}")
            elif 'text' in block:
                content = block['text'].get('elements', [{}])[0].get('text_run', {}).get('content', '')
                if content:
                    print(f"{i}. [文本] {content[:50]}...")

    print()


# 示例6: 使用配置文件
def example6_use_config():
    """使用配置文件初始化客户端"""
    print("=" * 60)
    print("示例6: 使用配置文件")
    print("=" * 60)

    # 读取配置文件
    config_file = "/path/to/config/feishu_config.txt"
    config = {}

    with open(config_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                config[key.strip()] = value.strip()

    client = FeishuDocClient(
        app_id=config['FEISHU_APP_ID'],
        app_secret=config['FEISHU_APP_SECRET'],
        domain=config.get('FEISHU_DOMAIN', 'https://open.feishu.cn')
    )

    # 使用客户端...
    print("✅ 客户端初始化成功（使用配置文件）")
    print()


# 示例7: 错误处理
def example7_error_handling():
    """展示如何处理常见的错误"""
    print("=" * 60)
    print("示例7: 错误处理")
    print("=" * 60)

    client = FeishuDocClient(
        app_id="your_app_id",
        app_secret="your_app_secret"
    )

    # 创建文档（带错误处理）
    try:
        doc_id = client.create_document("测试文档")
        print(f"✅ 文档创建成功: {doc_id}")
    except Exception as e:
        if "权限" in str(e):
            print("❌ 权限错误: 请检查飞书应用的权限配置")
        elif "凭证" in str(e):
            print("❌ 凭证错误: 请检查App ID和App Secret")
        else:
            print(f"❌ 错误: {str(e)}")
        return

    # 添加内容（带重试）
    max_retries = 3
    for attempt in range(max_retries):
        try:
            blocks = [
                {"block_type": 2, "text": {"elements": [{"text_run": {"content": "测试内容"}}]}}
            ]
            client.add_blocks(doc_id, blocks)
            print("✅ 内容添加成功")
            break
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"⚠️  添加失败，重试中... ({attempt + 1}/{max_retries})")
                import time
                time.sleep(1)
            else:
                print(f"❌ 添加失败: {str(e)}")

    print()


if __name__ == "__main__":
    # 运行示例（根据需要取消注释）

    # example1_create_simple_doc()
    # example2_create_from_markdown()
    # example3_batch_create()
    # example4_search_documents()
    # example5_get_document_info()
    # example6_use_config()
    # example7_error_handling()

    print("请编辑此文件，取消注释要运行的示例函数")
