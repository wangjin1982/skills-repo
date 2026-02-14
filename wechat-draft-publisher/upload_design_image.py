#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
上传设计图片到微信公众号素材库
"""

import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from publisher import WeChatPublisher

def main():
    # 图片路径
    image_path = "C:/Users/wangj/.claude/skills/canvas-design/goal_alignment.png"

    print("=" * 60)
    print("  上传设计图片到微信公众号素材库")
    print("=" * 60)
    print(f"\n图片: {os.path.basename(image_path)}")
    print("主题: 团队目标对齐概念图\n")

    try:
        # 创建发布器
        publisher = WeChatPublisher()

        # 上传图片
        result = publisher.upload_image(image_path, return_url=True)

        if isinstance(result, tuple):
            media_id, image_url = result
            print(f"\nMedia ID: {media_id}")
            print(f"图片URL: {image_url}")
        else:
            media_id = result
            print(f"\nMedia ID: {media_id}")

        print("\n" + "=" * 60)
        print("  上传成功！")
        print("=" * 60)
        print("\n使用方式：")
        print("1. 登录 https://mp.weixin.qq.com")
        print("2. 素材管理 → 图片")
        print("3. 找到刚上传的图片")
        print("4. 可以在编辑文章时插入使用\n")

    except Exception as e:
        print(f"\n错误: {e}")
        return 1

    return 0

if __name__ == '__main__':
    sys.exit(main())
