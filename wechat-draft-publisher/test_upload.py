#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 重定向输出到文件
log_file = "C:/Users/wangj/Documents/微信公众号/upload_log.txt"

try:
    from publisher import WeChatPublisher

    with open(log_file, 'w', encoding='utf-8') as f:
        f.write("Starting image upload...\n")

        publisher = WeChatPublisher()

        with open(log_file, 'a', encoding='utf-8') as f:
            f.write("Publisher initialized\n")
            f.write("Uploading image...\n")

        result = publisher.upload_image(
            "C:/Users/wangj/.claude/skills/canvas-design/goal_alignment.png",
            return_url=True
        )

        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"Upload result: {result}\n")
            if isinstance(result, tuple):
                f.write(f"Media ID: {result[0]}\n")
                f.write(f"Image URL: {result[1]}\n")

    # 输出简单的成功消息
    print("UPLOAD_COMPLETE")

except Exception as e:
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"Error: {str(e)}\n")
    print(f"ERROR: {str(e)}")
