#!/usr/bin/env python3
"""
HTML转PNG导出器
使用html2image库将HTML页面渲染为高质量PNG图片
"""

import sys
from pathlib import Path
from html2image import Html2Image


def export_to_png(html_path, png_path, width=600):
    """
    将HTML文件导出为PNG图片

    Args:
        html_path: HTML文件路径
        png_path: 输出PNG文件路径
        width: 渲染宽度（默认600px，与HTML设计一致）
    """
    try:
        # 初始化html2image
        hti = Html2Image(
            size=(width, 800),  # 初始尺寸，会根据内容自动调整
            custom_flags=[
                '--disable-gpu',
                '--no-sandbox',
                '--disable-dev-shm-usage'
            ]
        )

        # 读取HTML文件
        html_file = Path(html_path)
        if not html_file.exists():
            raise FileNotFoundError(f"HTML文件不存在: {html_path}")

        # 渲染HTML为PNG
        output_dir = Path(png_path).parent
        output_file = Path(png_path).stem

        hti.screenshot(
            html_str=html_file.read_text(encoding='utf-8'),
            save_dir=str(output_dir),
            save_as=f"{output_file}.png",
            size=(width, 1500)  # 设置足够的高度以容纳所有内容
        )

        # 重命名为指定路径
        actual_png = output_dir / f"{output_file}.png"
        actual_png.rename(png_path)

        return str(png_path.absolute())

    except ImportError:
        print("错误: 缺少html2image库，请先安装:")
        print("pip install html2image")
        sys.exit(1)
    except Exception as e:
        print(f"导出PNG时出错: {e}")
        sys.exit(1)


def main():
    """命令行入口"""
    if len(sys.argv) < 3:
        print("Usage: python export_to_png.py <html_path> <png_path> [width]")
        print("Example: python export_to_png.py report.html report.png")
        print("Example: python export_to_png.py report.html report.png 600")
        sys.exit(1)

    html_path = sys.argv[1]
    png_path = sys.argv[2]
    width = int(sys.argv[3]) if len(sys.argv) > 3 else 600

    # 导出PNG
    output_file = export_to_png(html_path, png_path, width)
    print(f"[OK] PNG exported: {output_file}")


if __name__ == '__main__':
    main()
