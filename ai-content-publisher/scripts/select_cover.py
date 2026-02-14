#!/usr/bin/env python3
"""
从封面图库中选择一张图片
按内容类型或随机选择

⚠️ 硬性要求：必须使用封面库的图片，不生成任何封面
"""

import os
import shutil
import random
import sys

def select_cover(content_type, output_dir):
    """
    从封面图库中选择图片（强制要求，失败则退出）

    Args:
        content_type: 内容类型 (new_tool/tutorial/industry_news)
        output_dir: 输出目录

    Returns:
        str: 选中的封面图路径

    Raises:
        SystemExit: 如果封面选择失败
    """
    cover_dir = "/c/Users/wangj/.claude/skills/ai-content-publisher/assets/covers"

    # 检查封面库是否存在
    if not os.path.exists(cover_dir):
        print(f"❌ 封面图库不存在: {cover_dir}")
        print("⚠️  硬性要求：必须使用封面库的图片")
        sys.exit(1)

    # 检查输出目录是否存在
    if not os.path.exists(output_dir):
        print(f"❌ 输出目录不存在: {output_dir}")
        sys.exit(1)

    # 获取所有图片文件
    image_extensions = ['.png', '.jpg', '.jpeg', '.webp']
    images = []
    for f in os.listdir(cover_dir):
        if any(f.lower().endswith(ext) for ext in image_extensions):
            images.append(f)

    if not images:
        print(f"❌ 封面图库中没有图片: {cover_dir}")
        print("⚠️  请确保封面库中有图片文件")
        sys.exit(1)

    # 按内容类型优先选择，或随机选择
    selected = None

    # 尝试匹配类型前缀
    type_prefix = {
        # AI工具实战类
        'tool_deep_dive': 'tool_',
        'tool_workflow': 'tool_',

        # 创业方法论类
        'startup_knowledge': 'startup_',
        'startup_pitfalls': 'startup_',

        # 效率提升类
        'workflow_optimization': 'efficiency_',
        'time_management': 'efficiency_',

        # 个人成长类
        'skill_development': 'growth_',
        'mindset_adjustment': 'growth_',

        # 案例分析类
        'success_case': 'case_',
        'failure_analysis': 'case_',

        # 资源整合类
        'tool_collection': 'collection_',
        'template_sharing': 'resource_',

        # 兼容旧类型
        'new_tool': 'tool_',
        'tutorial': 'tutorial_',
        'industry_news': 'news_'
    }

    prefix = type_prefix.get(content_type, '')
    if prefix:
        type_images = [img for img in images if img.startswith(prefix)]
        if type_images:
            selected = random.choice(type_images)
            print(f"📋 内容类型 '{content_type}' → 匹配前缀 '{prefix}'")
        else:
            print(f"⚠️  未找到匹配类型 '{content_type}' 的封面，使用随机封面")

    # 如果没有匹配的，随机选择
    if not selected:
        selected = random.choice(images)

    # 复制到输出目录
    src_path = os.path.join(cover_dir, selected)
    dst_path = os.path.join(output_dir, 'cover.png')

    try:
        shutil.copy2(src_path, dst_path)
        file_size = os.path.getsize(dst_path)
        print(f"✅ 选择封面图: {selected}")
        print(f"   来源: {cover_dir}")
        print(f"   目标: {dst_path}")
        print(f"   大小: {file_size:,} 字节 ({file_size // 1024 // 1024} MB)")
    except Exception as e:
        print(f"❌ 封面图复制失败: {e}")
        sys.exit(1)

    return dst_path


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("用法: select_cover.py <content_type> <output_dir>")
        print("\n内容类型: new_tool, tutorial, industry_news")
        sys.exit(1)

    content_type = sys.argv[1]
    output_dir = sys.argv[2]

    select_cover(content_type, output_dir)
