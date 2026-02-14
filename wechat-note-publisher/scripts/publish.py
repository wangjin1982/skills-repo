#!/usr/bin/env python3
"""
微信笔记发布器 - 全局版本
支持配置文件，可在多个vault中使用

使用方法：
    python3 publish.py <笔记路径> [标题] [作者]

配置文件搜索顺序：
    1. ~/.wechat-publish-config.json      (用户配置，优先级最高)
    2. ~/.claude/skills/wechat-note-publisher/config.json
    3. 当前vault/.wechat-config.json
    4. 使用默认配置
"""

import os
import sys
import json
import re
import subprocess
import requests
from pathlib import Path
from datetime import datetime


# ==================== 配置管理 ====================

def find_config():
    """
    查找配置文件

    Returns:
        dict: 配置内容，如果没找到则返回默认配置
    """
    config_paths = [
        Path.home() / '.wechat-publish-config.json',           # 用户配置
        Path.home() / '.claude' / 'skills' / 'wechat-note-publisher' / 'config.json',  # 全局配置
        Path.cwd() / '.wechat-config.json',                    # 当前项目配置
    ]

    for config_path in config_paths:
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                print(f"✓ 使用配置文件: {config_path}")
                return config
            except Exception as e:
                print(f"警告: 读取配置文件失败 {config_path}: {e}")
                continue

    # 使用默认配置
    print("警告: 未找到配置文件，使用默认配置")
    return {
        "server": {"host": "localhost", "port": 5000, "timeout": 30},
        "wechat": {"app_id": "", "app_secret": "", "account_name": ""},
        "publish": {"default_author": "Administrator", "title_max_length": 10, "cover_required": True}
    }


# 加载配置
CONFIG = find_config()
SERVER_CONFIG = CONFIG.get('server', {})
WECHAT_CONFIG = CONFIG.get('wechat', {})
PUBLISH_CONFIG = CONFIG.get('publish', {})


# ==================== HTML转换模板 ====================

WECHAT_HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        /* 微信公众号适配样式 */
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.8;
            color: #333;
            max-width: 677px;
            margin: 0 auto;
            padding: 20px;
            font-size: 16px;
        }}

        h1, h2, h3, h4, h5, h6 {{
            margin-top: 1.5em;
            margin-bottom: 0.8em;
            font-weight: 600;
            line-height: 1.4;
        }}

        h1 {{ font-size: 1.8em; text-align: center; border-bottom: 2px solid #eee; padding-bottom: 15px; }}
        h2 {{ font-size: 1.5em; border-left: 4px solid #07c160; padding-left: 12px; margin-top: 2em; }}
        h3 {{ font-size: 1.3em; color: #555; }}
        h4 {{ font-size: 1.15em; }}

        p {{
            margin: 1em 0;
            text-align: justify;
        }}

        /* 代码块样式 */
        pre {{
            background: #f6f8fa;
            border-radius: 6px;
            padding: 16px;
            overflow-x: auto;
            margin: 1.5em 0;
            font-size: 14px;
            line-height: 1.5;
        }}

        code {{
            font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
            background: #f6f8fa;
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 0.9em;
        }}

        pre code {{
            background: transparent;
            padding: 0;
        }}

        /* 引用块 */
        blockquote {{
            border-left: 4px solid #dfe2e5;
            padding-left: 16px;
            color: #6a737d;
            margin: 1.5em 0;
        }}

        /* 列表 */
        ul, ol {{
            padding-left: 2em;
            margin: 1em 0;
        }}

        li {{
            margin: 0.5em 0;
        }}

        /* 表格 */
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 1.5em 0;
            font-size: 0.95em;
        }}

        th, td {{
            border: 1px solid #dfe2e5;
            padding: 8px 12px;
            text-align: left;
        }}

        th {{
            background: #f6f8fa;
            font-weight: 600;
        }}

        /* 图片 */
        img {{
            max-width: 100%;
            height: auto;
            border-radius: 4px;
            margin: 1.5em 0;
        }}

        /* 链接 */
        a {{
            color: #07c160;
            text-decoration: none;
        }}

        a:hover {{
            text-decoration: underline;
        }}

        /* 分隔线 */
        hr {{
            border: none;
            border-top: 1px solid #eee;
            margin: 2em 0;
        }}
    </style>
</head>
<body>
{content}
</body>
</html>
"""


# ==================== 核心功能 ====================

def read_markdown_file(file_path):
    """读取Markdown文件"""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 提取第一个一级标题作为标题
    title = path.stem
    for line in content.split('\n'):
        line = line.strip()
        if line.startswith('# '):
            extracted_title = line[2:].strip()
            if extracted_title:
                title = extracted_title
                break

    # 微信标题限制
    max_length = PUBLISH_CONFIG.get('title_max_length', 10)
    # 清理并截断标题
    title = re.sub(r'[^\w\s\u4e00-\u9fff\u3000-\u303f\uff00-\uffef.,!?;:()""''""—-]', '', title)
    if len(title) > max_length:
        title = title[:max_length]

    return content, title


def extract_first_image(markdown_content, base_path):
    """提取Markdown中的第一张本地图片"""
    lines = markdown_content.split('\n')
    for line in lines:
        if '![' in line and '](' in line and ')' in line:
            # 提取图片路径
            start = line.rfind('](') + 2
            end = line.rfind(')')
            if start > 0 and end > start:
                img_path = line[start:end]
                # 检查是否是本地图片
                if not img_path.startswith('http') and not img_path.startswith('www'):
                    # 尝试完整路径
                    full_path = os.path.join(base_path, img_path)
                    if os.path.exists(full_path):
                        return full_path
                    # 尝试当前目录
                    if os.path.exists(img_path):
                        return img_path

    return None


def markdown_to_html(markdown_content):
    """将Markdown转换为HTML"""
    try:
        # 使用pandoc转换
        process = subprocess.Popen(
            ['pandoc', '--from', 'markdown', '--to', 'html'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate(input=markdown_content)

        if process.returncode != 0:
            print(f"警告: pandoc转换出现问题: {stderr}")

        return stdout

    except FileNotFoundError:
        # 如果没有pandoc，使用简单的markdown转html
        print("警告: 未检测到pandoc，使用简单转换")
        return simple_markdown_to_html(markdown_content)


def simple_markdown_to_html(markdown_content):
    """简单的Markdown到HTML转换（备用方案）"""
    html = markdown_content

    # 标题
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)

    # 粗体和斜体
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)

    # 代码块
    html = re.sub(r'```(\w+)?\n(.+?)```', r'<pre><code>\2</code></pre>', html, flags=re.DOTALL)
    html = re.sub(r'`(.+?)`', r'<code>\1</code>', html)

    # 引用
    html = re.sub(r'^> (.+)$', r'<blockquote>\1</blockquote>', html, flags=re.MULTILINE)

    # 链接
    html = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', html)

    # 图片
    html = re.sub(r'!\[([^\]]*)\]\(([^\)]+)\)', r'<img src="\2" alt="\1">', html)

    # 段落
    paragraphs = html.split('\n\n')
    html = '\n'.join(f'<p>{p.strip()}</p>' if p.strip() and not p.strip().startswith('<') else p.strip()
                     for p in paragraphs if p.strip())

    return html


def create_wechat_html(markdown_content, base_path=None):
    """创建适配微信公众号的HTML"""
    # 转换为HTML
    html_content = markdown_to_html(markdown_content)

    # 包装在模板中
    return WECHAT_HTML_TEMPLATE.format(content=html_content)


def get_stable_access_token():
    """
    获取微信稳定版access_token

    Returns:
        str: access_token if successful, None otherwise
    """
    if not WECHAT_CONFIG.get('app_id') or not WECHAT_CONFIG.get('app_secret'):
        print("✗ 未配置微信AppID和AppSecret，请在配置文件中设置")
        return None

    # 使用新的稳定版 access_token API
    token_url = "https://api.weixin.qq.com/cgi-bin/stable_token"
    payload = {
        "grant_type": "client_credential",
        "appid": WECHAT_CONFIG['app_id'],
        "secret": WECHAT_CONFIG['app_secret']
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(token_url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        if 'access_token' not in data:
            print(f"✗ 获取stable access_token失败: {data.get('errmsg', '未知错误')}")
            return None

        access_token = data['access_token']
        print(f"✓ Stable Access Token 获取成功")
        return access_token

    except Exception as e:
        print(f"✗ 获取stable access_token异常: {e}")
        return None


def upload_image_to_wechat(image_path):
    """
    上传图片到微信公众号，获取 thumb_media_id

    Returns:
        str: thumb_media_id if successful, None otherwise
    """
    # 获取稳定版 access_token
    access_token = get_stable_access_token()
    if not access_token:
        return None

    try:
        # 上传图片
        upload_url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={access_token}&type=thumb"

        with open(image_path, 'rb') as f:
            files = {'media': f}
            upload_response = requests.post(upload_url, files=files, timeout=30)
            upload_response.raise_for_status()
            upload_data = upload_response.json()

        if 'media_id' in upload_data:
            media_id = upload_data['media_id']
            print(f"✓ 图片已上传到微信: {media_id}")
            return media_id
        else:
            error_msg = upload_data.get('errmsg', '未知错误')
            print(f"✗ 上传图片失败: {error_msg}")
            return None

    except Exception as e:
        print(f"✗ 上传图片异常: {e}")
        return None


def upload_to_server(html_content, filename, title=None, author=None):
    """
    上传HTML到云服务器

    Returns:
        dict: 上传结果
    """
    url = f"http://{SERVER_CONFIG['host']}:{SERVER_CONFIG['port']}/upload"

    # 准备文件 - 明确指定UTF-8编码
    files = {
        'file': (filename, html_content.encode('utf-8'), 'text/html; charset=utf-8')
    }

    # 准备表单数据 - 使用UTF-8编码
    data = {}
    if title:
        data['title'] = title
    if author:
        data['author'] = author

    try:
        response = requests.post(url, files=files, data=data, timeout=SERVER_CONFIG.get('timeout', 30))
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": f"上传失败: {str(e)}"
        }


def publish_to_server(filename, title, author=None, digest=None, thumb_media_id=None):
    """
    发布文章到微信公众号草稿箱

    Returns:
        dict: 发布结果
    """
    url = f"http://{SERVER_CONFIG['host']}:{SERVER_CONFIG['port']}/publish"

    payload = {
        "filename": filename,
        "title": title
    }

    if author:
        payload['author'] = author
    if digest:
        payload['digest'] = digest
    # 只有当 thumb_media_id 有值时才添加该字段
    if thumb_media_id:
        payload['thumb_media_id'] = thumb_media_id

    try:
        response = requests.post(url, json=payload, timeout=SERVER_CONFIG.get('timeout', 30))
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": f"发布失败: {str(e)}"
        }


# ==================== 主流程 ====================

def publish_note(note_path, title=None, author=None, auto_publish=True):
    """
    发布笔记到微信公众号

    Args:
        note_path: 笔记文件路径
        title: 文章标题（可选）
        author: 作者（可选）
        auto_publish: 是否自动发布到草稿箱（默认True）

    Returns:
        dict: 发布结果
    """
    print(f"\n{'='*50}")
    print(f"📝 开始处理笔记: {note_path}")
    print(f"{'='*50}\n")

    try:
        # 1. 读取Markdown
        print("[1/5] 读取笔记内容...")
        markdown_content, default_title = read_markdown_file(note_path)
        print(f"✓ 文件已读取 ({len(markdown_content)} 字符)")

        # 如果没有指定标题，使用文件名
        if not title:
            title = default_title

        # 2. 提取第一张图片（作为封面）
        print("[2/5] 检查封面图...")
        base_path = str(Path(note_path).parent)
        cover_image = extract_first_image(markdown_content, base_path)

        thumb_media_id = None
        if cover_image:
            print(f"找到封面图: {cover_image}")
            print("上传封面图到微信...")
            thumb_media_id = upload_image_to_wechat(cover_image)
            if not thumb_media_id:
                return {"success": False, "error": "封面图上传失败"}
        else:
            cover_required = PUBLISH_CONFIG.get('cover_required', True)
            if cover_required:
                print(f"✗ 未找到封面图")
                print(f"\n注意: 微信公众号文章必须有封面图")
                print(f"请在笔记中添加图片引用，例如: ![封面图](path/to/image.jpg)")
                print(f"或者使用 create_cover.py 生成封面图\n")
                return {"success": False, "error": "未找到封面图，微信公众号文章必须包含封面图"}
            else:
                print(f"未找到封面图（跳过，非必需）")

        # 3. 转换为HTML
        print("[3/5] 转换为HTML...")
        html_content = create_wechat_html(markdown_content, base_path)
        print(f"✓ HTML已生成 ({len(html_content)} 字符)")

        # 4. 上传到服务器
        print(f"[4/5] 上传到服务器 ({SERVER_CONFIG['host']})...")
        filename = f"{Path(note_path).stem}.html"
        upload_result = upload_to_server(html_content, filename, title, author)

        if not upload_result.get('success'):
            print(f"✗ 上传失败: {upload_result.get('error')}")
            return upload_result

        server_filename = upload_result.get('filename', filename)
        print(f"✓ 已上传: {server_filename}")

        # 5. 发布到草稿箱
        if auto_publish:
            print(f"[5/5] 发布到微信公众号草稿箱...")
            publish_result = publish_to_server(server_filename, title, author, thumb_media_id=thumb_media_id)

            if publish_result.get('success'):
                print(f"✓ 发布成功!")
                print(f"\n{'='*50}")
                print(f"✅ 文章已成功发布到草稿箱")
                print(f"   标题: {title}")
                if publish_result.get('media_id'):
                    print(f"   Media ID: {publish_result['media_id']}")
                print(f"{'='*50}\n")
            else:
                print(f"✗ 发布失败: {publish_result.get('error')}")
                return publish_result

        return {
            "success": True,
            "title": title,
            "filename": server_filename,
            "upload_result": upload_result,
            "publish_result": publish_result if auto_publish else None
        }

    except Exception as e:
        print(f"\n✗ 处理失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            "success": False,
            "error": str(e)
        }


# ==================== 命令行入口 ====================

def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法: python publish.py <笔记路径> [标题] [作者]")
        print("示例: python publish.py note.md \"我的文章\" \"作者名\"")
        print("\n配置文件搜索顺序:")
        print("  1. ~/.wechat-publish-config.json")
        print("  2. ~/.claude/skills/wechat-note-publisher/config.json")
        print("  3. 当前vault/.wechat-config.json")
        sys.exit(1)

    note_path = sys.argv[1]
    title = sys.argv[2] if len(sys.argv) > 2 else None
    author = sys.argv[3] if len(sys.argv) > 3 else None

    result = publish_note(note_path, title=title, author=author)

    if result.get('success'):
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
