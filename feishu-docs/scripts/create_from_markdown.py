#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从Markdown文件创建飞书文档的命令行工具
"""

import argparse
import sys
import os

# 添加scripts目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from feishu_api import FeishuDocClient


def main():
    parser = argparse.ArgumentParser(
        description="从Markdown文件创建飞书文档",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基本使用
  python create_from_markdown.py --app-id xxx --app-secret yyy --title "我的文档" --markdown-file content.md

  # 使用配置文件
  python create_from_markdown.py --config ../config/feishu_config.txt --title "文档" --markdown-file content.md

  # 批量创建
  python create_from_markdown.py --app-id xxx --app-secret yyy --batch documents.txt
        """
    )

    parser.add_argument(
        "--app-id",
        help="飞书应用ID"
    )
    parser.add_argument(
        "--app-secret",
        help="飞书应用密钥"
    )
    parser.add_argument(
        "--domain",
        default="https://open.feishu.cn",
        help="API域名 (默认: https://open.feishu.cn)"
    )
    parser.add_argument(
        "--config",
        help="配置文件路径"
    )
    parser.add_argument(
        "--title",
        help="文档标题"
    )
    parser.add_argument(
        "--markdown-file",
        help="Markdown文件路径"
    )
    parser.add_argument(
        "--batch",
        help="批量创建模式，每行格式: 标题|markdown文件路径"
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=20,
        help="每批添加的块数 (默认: 20)"
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.2,
        help="批次间延迟秒数 (默认: 0.2)"
    )

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

    if not app_id or not app_secret:
        print("❌ 错误: 必须提供 app-id 和 app-secret，或使用配置文件")
        sys.exit(1)

    # 初始化客户端
    print("初始化飞书客户端...")
    client = FeishuDocClient(
        app_id=app_id,
        app_secret=app_secret,
        domain=args.domain
    )
    print("✅ 客户端初始化成功\n")

    # 批量创建模式
    if args.batch:
        print(f"批量创建模式: {args.batch}")
        print("=" * 60)

        with open(args.batch, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for i, line in enumerate(lines, 1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            parts = line.split('|')
            if len(parts) != 2:
                print(f"⚠️  跳过第 {i} 行: 格式错误")
                continue

            title, md_file = parts
            print(f"\n[{i}/{len(lines)}] 创建: {title}")

            try:
                # 创建文档
                doc_id = client.create_document(title)
                print(f"  ✅ 文档创建成功: {doc_id}")

                # 添加内容
                success, fail = client.add_content_from_markdown(
                    doc_id,
                    md_file,
                    batch_size=args.batch_size,
                    delay=args.delay
                )

                print(f"  ✅ 内容添加完成: 成功 {success}, 失败 {fail}")
                print(f"  🔗 链接: {client.get_document_url(doc_id)}")

            except Exception as e:
                print(f"  ❌ 失败: {str(e)}")

        print("\n" + "=" * 60)
        print("✅ 批量创建完成")
        return

    # 单个文档创建模式
    if not args.title or not args.markdown_file:
        print("❌ 错误: 必须提供 --title 和 --markdown-file")
        sys.exit(1)

    if not os.path.exists(args.markdown_file):
        print(f"❌ 错误: 文件不存在: {args.markdown_file}")
        sys.exit(1)

    # 创建文档
    print(f"创建文档: {args.title}")
    print(f"内容文件: {args.markdown_file}")
    print("-" * 60)

    try:
        # 创建文档
        doc_id = client.create_document(args.title)
        print(f"✅ 文档创建成功: {doc_id}\n")

        # 添加内容
        print("开始添加内容...")
        print("-" * 60)

        success, fail = client.add_content_from_markdown(
            doc_id,
            args.markdown_file,
            batch_size=args.batch_size,
            delay=args.delay
        )

        print("-" * 60)
        print(f"\n✅ 内容添加完成!")
        print(f"   成功: {success} 个块")
        print(f"   失败: {fail} 个块\n")

        # 显示链接
        doc_url = client.get_document_url(doc_id)
        print("=" * 60)
        print("🔗 文档链接")
        print("=" * 60)
        print(f"\n  {doc_url}\n")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ 错误: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
