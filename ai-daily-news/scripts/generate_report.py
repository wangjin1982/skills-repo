#!/usr/bin/env python3
"""
AI资讯日报HTML生成器
接收资讯数据，生成精美的卡片式HTML日报页面
"""

import json
import sys
import argparse
import base64
from datetime import datetime
from pathlib import Path


def image_to_base64(image_path):
    """
    将图片文件转换为base64编码

    Args:
        image_path: 图片文件路径

    Returns:
        base64编码的字符串，如果图片不存在则返回None
    """
    try:
        img_path = Path(image_path)
        if not img_path.exists():
            return None

        # 读取图片并转换为base64
        with open(img_path, 'rb') as f:
            img_data = f.read()
            base64_str = base64.b64encode(img_data).decode('utf-8')

        # 获取文件扩展名以确定MIME类型
        ext = img_path.suffix.lower()
        mime_type = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif'
        }.get(ext, 'image/png')

        return f"data:{mime_type};base64,{base64_str}"
    except Exception as e:
        print(f"[WARN] Failed to load image {image_path}: {e}")
        return None


def generate_html(news_items, date_str, output_path, qr_code_base64=None):
    """
    生成AI日报HTML页面 - 深色科技风格

    Args:
        news_items: 包含5条资讯的列表，每条包含 title, summary, source, url, tag
        date_str: 日期字符串
        output_path: 输出文件路径
    """

    html_template = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI资讯日报 - {date}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB',
                         'Microsoft YaHei', sans-serif;
            background-color: #121826;
            color: #FFFFFF;
            line-height: 1.6;
            min-height: 100vh;
            padding: 20px;
            font-size: 18px;
        }}

        .container {{
            max-width: 800px;
            margin: 0 auto;
        }}

        /* 头部区域 */
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 0;
            border-bottom: 1px solid #2A3142;
            margin-bottom: 20px;
        }}

        .header-left {{
            display: flex;
            flex-direction: column;
            gap: 4px;
        }}

        .date {{
            font-size: 18px;
            color: #8A8A8A;
            font-weight: 400;
        }}

        .subtitle {{
            font-size: 20px;
            font-weight: 500;
            color: #FFFFFF;
        }}

        .header-right {{
            width: 24px;
            height: 24px;
            border: 1px solid #FFFFFF;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 12px;
        }}

        .header-right:hover {{
            background-color: #FFFFFF;
            color: #121826;
        }}

        /* 内容区 */
        .content {{
            margin-top: 20px;
        }}

        .news-card {{
            background-color: #1E2532;
            border: 1px solid #2A3142;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            cursor: pointer;
            transition: background-color 0.3s ease, transform 0.2s ease;
            position: relative;
            text-decoration: none;
            display: block;
        }}

        .news-card:hover {{
            background-color: #232B3A;
            transform: translateY(-2px);
        }}

        .tag {{
            display: inline-block;
            background-color: #3B82F6;
            color: #FFFFFF;
            font-size: 14px;
            font-weight: 500;
            padding: 6px 12px;
            border-radius: 4px;
            margin-bottom: 12px;
        }}

        .card-title {{
            font-size: 22px;
            font-weight: 600;
            color: #FFFFFF;
            margin-bottom: 10px;
            line-height: 1.4;
        }}

        .card-summary {{
            font-size: 17px;
            color: #8A8A8A;
            margin-bottom: 14px;
            line-height: 1.6;
        }}

        .card-meta {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .source {{
            font-size: 15px;
            color: #8A8A8A;
        }}

        .arrow {{
            font-size: 18px;
            color: #8A8A8A;
            transition: transform 0.3s ease;
        }}

        .news-card:hover .arrow {{
            transform: translateX(4px);
        }}

        /* 底部区域 */
        .footer {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 0;
            border-top: 1px solid #2A3142;
            margin-top: 40px;
        }}

        .footer-left {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .qr-placeholder {{
            width: 80px;
            height: 80px;
            border: 1px solid #2A3142;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
        }}

        .qr-placeholder img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}

        .qr-placeholder .fallback {{
            font-size: 24px;
            color: #8A8A8A;
        }}

        .footer-guide {{
            font-size: 16px;
            color: #8A8A8A;
            line-height: 1.4;
        }}

        .copyright {{
            font-size: 13px;
            color: #8A8A8A;
            text-align: right;
        }}

        /* 响应式设计 */
        @media (max-width: 768px) {{
            .container {{
                padding: 0 10px;
            }}

            .header {{
                padding: 15px 0;
            }}

            .date {{
                font-size: 16px;
            }}

            .subtitle {{
                font-size: 18px;
            }}

            .news-card {{
                padding: 14px;
            }}

            .card-title {{
                font-size: 20px;
            }}

            .card-summary {{
                font-size: 16px;
            }}

            .source {{
                font-size: 14px;
            }}

            .footer-guide {{
                font-size: 14px;
            }}

            .footer {{
                flex-direction: column;
                gap: 20px;
                text-align: center;
            }}

            .footer-left {{
                flex-direction: column;
                gap: 8px;
            }}

            .copyright {{
                text-align: center;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- 头部区域 -->
        <div class="header">
            <div class="header-left">
                <div class="date">{date}</div>
                <div class="subtitle">精选全球AI领域前沿动态</div>
            </div>
            <div class="header-right">⚙</div>
        </div>

        <!-- 内容区 -->
        <div class="content">
            {news_cards}
        </div>

        <!-- 底部区域 -->
        <div class="footer">
            <div class="footer-left">
                <div class="qr-placeholder">
                    {qr_code_html}
                </div>
                <div class="footer-guide">
                    扫码关注公众号<br>
                    获取更多AI资讯
                </div>
            </div>
            <div class="copyright">
                AIDAILY<br>
                Designed by GenAI
            </div>
        </div>
    </div>
</body>
</html>
"""

    # 生成二维码HTML（如果有base64数据）
    if qr_code_base64:
        qr_html = f'<img src="{qr_code_base64}" alt="微信二维码">'
    else:
        qr_html = '<div class="fallback">📱</div>'

    # 生成新闻卡片HTML
    news_cards_html = ""
    for item in news_items:
        tag = item.get('tag', 'AI资讯')
        title = item.get('title', '未知标题')
        summary = item.get('summary', '暂无摘要')
        source = item.get('source', '互联网')
        url = item.get('url', '#')

        card_html = f"""
            <a href="{url}" class="news-card" target="_blank">
                <div class="tag">{tag}</div>
                <div class="card-title">{title}</div>
                <div class="card-summary">{summary}</div>
                <div class="card-meta">
                    <span class="source">From: {source}</span>
                    <span class="arrow">→</span>
                </div>
            </a>
        """
        news_cards_html += card_html

    # 填充模板
    final_html = html_template.format(
        date=date_str,
        news_cards=news_cards_html,
        qr_code_html=qr_html
    )

    # 写入文件
    output_file = Path(output_path)
    output_file.write_text(final_html, encoding='utf-8')

    return str(output_file.absolute())


def export_to_png(html_path, png_path=None, width=600):
    """
    将HTML导出为PNG图片

    Args:
        html_path: HTML文件路径
        png_path: 输出PNG路径（如为None则自动生成）
        width: 渲染宽度
    """
    try:
        from html2image import Html2Image
    except ImportError:
        print("[WARN] html2image not installed. PNG export skipped.")
        print("       Install with: pip install html2image")
        return None

    try:
        if png_path is None:
            png_path = Path(html_path).with_suffix('.png')
        else:
            png_path = Path(png_path)

        # 读取HTML内容
        html_content = Path(html_path).read_text(encoding='utf-8')

        # 设置输出目录和文件名
        output_dir = png_path.parent
        output_file = png_path.stem

        # 初始化html2image
        hti = Html2Image(
            output_path=str(output_dir),
            size=(width, 2000)
        )

        # 渲染为PNG
        hti.screenshot(
            html_str=html_content,
            save_as=f"{output_file}.png",
            size=(width, 2000)
        )

        # html2image会自动在output_path目录下生成文件
        actual_png = output_dir / f"{output_file}.png"

        # 检查是否成功生成
        if actual_png.exists():
            print(f"[OK] PNG exported: {actual_png.absolute()}")
            return str(actual_png.absolute())
        else:
            print(f"[ERROR] PNG file not generated at {actual_png}")
            return None

    except Exception as e:
        print(f"[ERROR] Failed to export PNG: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description='生成AI资讯日报HTML报告（可选导出PNG）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python generate_report.py news.json report.html
  python generate_report.py news.json report.html --export-png
  python generate_report.py news.json report.html --export-png --qr-code assets/weixin_qr.jpg
        """
    )

    parser.add_argument('news_json', help='新闻数据JSON文件路径')
    parser.add_argument('output_html', help='输出HTML文件路径')
    parser.add_argument('--export-png', action='store_true',
                        help='同时导出PNG图片')
    parser.add_argument('--output-png', help='指定PNG输出路径（默认与HTML同名）')
    parser.add_argument('--width', type=int, default=800,
                        help='PNG渲染宽度（默认800px）')
    parser.add_argument('--qr-code', help='微信二维码图片路径（支持jpg/png/gif）')

    args = parser.parse_args()

    # 读取新闻数据
    with open(args.news_json, 'r', encoding='utf-8') as f:
        data = json.load(f)

    news_items = data.get('news_items', [])
    date_str = data.get('date', datetime.now().strftime('%Y年%m月%d日'))

    # 处理二维码图片
    qr_code_base64 = None
    qr_code_path = args.qr_code

    # 如果未指定二维码路径，尝试使用默认路径
    if qr_code_path is None:
        # 尝试从当前目录、assets目录、脚本目录查找
        script_dir = Path(__file__).parent.parent
        possible_paths = [
            Path('assets/weixin_qr.png'),
            Path('assets/weixin_qr.jpg'),
            script_dir / 'assets' / 'weixin_qr.png',
            script_dir / 'assets' / 'weixin_qr.jpg',
        ]
        for path in possible_paths:
            if path.exists():
                qr_code_path = str(path)
                print(f"[INFO] Found QR code at: {qr_code_path}")
                break

    # 如果找到了二维码图片，转换为base64
    if qr_code_path:
        qr_code_base64 = image_to_base64(qr_code_path)
        if qr_code_base64:
            print(f"[INFO] QR code image loaded successfully")
        else:
            print(f"[WARN] Failed to load QR code, using fallback")

    # 生成HTML
    output_file = generate_html(news_items, date_str, args.output_html, qr_code_base64)
    print(f"[OK] HTML report generated: {output_file}")

    # 导出PNG（如果指定）
    if args.export_png:
        png_path = args.output_png or None
        export_to_png(output_file, png_path, args.width)


if __name__ == '__main__':
    main()
