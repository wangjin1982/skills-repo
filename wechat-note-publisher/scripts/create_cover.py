#!/usr/bin/env python3
"""
微信公众号封面图生成器 - 全局版本

使用方法：
    python3 create_cover.py <主标题> <副标题> <作者> <输出路径>

配置文件：使用与 publish.py 相同的配置
"""

import sys
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path


# 默认配置
DEFAULT_WIDTH = 900
DEFAULT_HEIGHT = 500
DEFAULT_BG_COLOR = '#1a365d'  # 深蓝色
DEFAULT_ACCENT_COLOR = '#d4af37'  # 金色
DEFAULT_TEXT_COLOR = '#ffffff'
DEFAULT_SUBTITLE_COLOR = '#d4af37'
DEFAULT_AUTHOR_COLOR = '#cccccc'


def get_font(size, font_name=None):
    """获取字体，支持跨平台"""
    font_paths = []

    # macOS
    font_paths.extend([
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/Library/Fonts/Arial Unicode.ttf"
    ])

    # Linux
    font_paths.extend([
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
    ])

    # Windows
    font_paths.extend([
        "C:\\Windows\\Fonts\\msyh.ttc",  # 微软雅黑
        "C:\\Windows\\Fonts\\simsun.ttc",  # 宋体
        "C:\\Windows\\Fonts\\simhei.ttf",  # 黑体
    ])

    # 尝试加载字体
    for font_path in font_paths:
        try:
            if Path(font_path).exists():
                return ImageFont.truetype(font_path, size)
        except:
            continue

    # 使用默认字体
    return ImageFont.load_default()


def create_cover_image(title, subtitle, author, output_path,
                        width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT,
                        bg_color=DEFAULT_BG_COLOR, accent_color=DEFAULT_ACCENT_COLOR):
    """
    创建封面图

    Args:
        title: 主标题
        subtitle: 副标题
        author: 作者
        output_path: 输出路径
        width: 图片宽度（默认900）
        height: 图片高度（默认500）
        bg_color: 背景颜色（默认深蓝）
        accent_color: 强调色（默认金色）

    Returns:
        str: 输出文件路径
    """

    # 创建图片
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)

    # 绘制装饰元素 - 顶部金色横条
    draw.rectangle([0, 0, width, 8], fill=accent_color)

    # 绘制装饰元素 - 底部金色横条
    draw.rectangle([0, height-8, width, height], fill=accent_color)

    # 绘制装饰元素 - 左侧金色竖条
    draw.rectangle([0, 0, 8, height], fill=accent_color)

    # 加载字体
    title_font = get_font(48)
    subtitle_font = get_font(28)
    author_font = get_font(20)

    # 计算文本位置
    # 标题居中
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (width - title_width) // 2
    title_y = 150

    # 副标题居中
    subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    subtitle_x = (width - subtitle_width) // 2
    subtitle_y = title_y + 80

    # 作者居中
    author_bbox = draw.textbbox((0, 0), author, font=author_font)
    author_width = author_bbox[2] - author_bbox[0]
    author_x = (width - author_width) // 2
    author_y = subtitle_y + 60

    # 绘制文本
    draw.text((title_x, title_y), title, fill=DEFAULT_TEXT_COLOR, font=title_font)
    draw.text((subtitle_x, subtitle_y), subtitle, fill=DEFAULT_SUBTITLE_COLOR, font=subtitle_font)
    draw.text((author_x, author_y), author, fill=DEFAULT_AUTHOR_COLOR, font=author_font)

    # 确保输出目录存在
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # 保存图片
    img.save(str(output_path), 'PNG', quality=95)
    print(f"✓ 封面图已保存: {output_path}")
    return str(output_path)


def main():
    """命令行入口"""
    if len(sys.argv) < 5:
        print("用法: python create_cover.py <主标题> <副标题> <作者> <输出路径>")
        print("\n示例:")
        print("  python create_cover.py \"思考的技术\" \"第一章：转换思路\" \"大前研一\" \"cover.png\"")
        print("  python create_cover.py \"管理美学\" \"团队建设\" \"王金\" \"images/cover_team.png\"")
        print("\n配置文件：与 publish.py 使用相同的配置文件")
        sys.exit(1)

    title = sys.argv[1]
    subtitle = sys.argv[2]
    author = sys.argv[3]
    output_path = sys.argv[4]

    # 可选：自定义尺寸
    width = int(sys.argv[5]) if len(sys.argv) > 5 else DEFAULT_WIDTH
    height = int(sys.argv[6]) if len(sys.argv) > 6 else DEFAULT_HEIGHT

    create_cover_image(title, subtitle, author, output_path, width, height)


if __name__ == '__main__':
    main()
