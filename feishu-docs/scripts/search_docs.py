#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
搜索飞书文档的命令行工具
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from feishu_api import FeishuDocClient


def main():
    parser = argparse.ArgumentParser(description="搜索飞书文档")

    parser.add_argument("--app-id", required=True, help="飞书应用ID")
    parser.add_argument("--app-secret", required=True, help="飞书应用密钥")
    parser.add_argument("--config", help="配置文件路径")
    parser.add_argument("query", help="搜索关键词")
    parser.add_argument("--page-size", type=int, default=20, help="每页结果数")

    args = parser.parse_args()

    # 从配置文件读取
    app_id = args.app_id
    app_secret = args.app_secret

    if args.config:
        config = {}
        with open(args.config, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()

        app_id = app_id or config.get('FEISHU_APP_ID')
        app_secret = app_secret or config.get('FEISHU_APP_SECRET')

    # 初始化客户端
    client = FeishuDocClient(app_id=app_id, app_secret=app_secret)

    # 搜索文档
    print(f"搜索关键词: {args.query}")
    print("-" * 60)

    try:
        results = client.search_documents(args.query, args.page_size)

        if not results:
            print("未找到匹配的文档")
            return

        print(f"找到 {len(results)} 个文档:\n")

        for i, doc in enumerate(results, 1):
            title = doc.get('title', '无标题')
            doc_id = doc.get('document_id', '')
            url = client.get_document_url(doc_id)

            print(f"{i}. {title}")
            print(f"   ID: {doc_id}")
            print(f"   链接: {url}")
            print()

    except Exception as e:
        print(f"❌ 搜索失败: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
