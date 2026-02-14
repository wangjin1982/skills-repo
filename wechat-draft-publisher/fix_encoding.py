#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复publisher.py中的编码问题
替换所有可能导致GBK编码错误的特殊Unicode字符
"""

import re

file_path = "C:/Users/wangj/.claude/skills/wechat-draft-publisher/publisher.py"

# 读取文件
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 替换规则
replacements = [
    ('✓', '[OK]'),
    ('→', '->'),
    ('⚠', '[WARNING]'),
    ('⚠️', '[WARNING]'),
    ('❌', '[ERROR]'),
]

# 执行替换
for old, new in replacements:
    content = content.replace(old, new)

# 写回文件
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Encoding issues fixed in publisher.py")
