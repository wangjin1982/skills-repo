#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号草稿发布工具（修复中文编码版本）
支持上传封面图片、创建草稿文章
"""

import os
import sys
import json
import time
import requests
import argparse
from pathlib import Path
from typing import Optional, Dict, Any


class WeChatPublisher:
    """微信公众号草稿发布器（UTF-8编码修复版）"""

    BASE_URL = "https://api.weixin.qq.com/cgi-bin"
    TOKEN_CACHE_FILE = os.path.expanduser("~/.wechat-publisher/token_cache.json")
    CONFIG_FILE = os.path.expanduser("~/.wechat-publisher/config.json")

    # 微信API错误码映射
    ERROR_CODES = {
        40001: "AppSecret错误或者AppSecret不属于这个AppID",
        40002: "请确保grant_type字段值为client_credential",
        40013: "不合法的AppID，请检查AppID是否正确",
        40125: "无效的appsecret，请检查AppSecret是否正确",
        40164: "调用接口的IP地址不在白名单中",
        41001: "缺少access_token参数",
        42001: "access_token超时，请检查缓存是否正常",
        45009: "接口调用超过限制（每日API调用量已用完）",
        47003: "参数错误，请检查必填字段是否完整",
        48001: "api功能未授权，请确认公众号类型",
        50005: "用户未关注公众号",
        -1: "系统繁忙，请稍后重试"
    }

    def __init__(self):
        """初始化发布器"""
        self.appid = None
        self.appsecret = None
        self.access_token = None
        self.load_config()

    def load_config(self):
        """加载配置文件"""
        if os.path.exists(self.CONFIG_FILE):
            with open(self.CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
                self.appid = config.get('appid')
                self.appsecret = config.get('appsecret')
        else:
            print("配置文件不存在，请先配置 AppID 和 AppSecret")
            print(f"配置文件位置: {self.CONFIG_FILE}")
            sys.exit(1)

    def get_access_token(self) -> str:
        """获取 access_token"""
        # 检查缓存
        if os.path.exists(self.TOKEN_CACHE_FILE):
            with open(self.TOKEN_CACHE_FILE, 'r', encoding='utf-8') as f:
                cache = json.load(f)
                # 检查是否过期（7200秒）
                if time.time() - cache.get('timestamp', 0) < 7000:
                    return cache.get('access_token')

        # 重新获取
        url = f"{self.BASE_URL}/token"
        params = {
            "grant_type": "client_credential",
            "appid": self.appid,
            "secret": self.appsecret
        }

        response = requests.get(url, params=params)
        result = response.json()

        if 'access_token' in result:
            self.access_token = result['access_token']
            # 缓存 token
            with open(self.TOKEN_CACHE_FILE, 'w', encoding='utf-8') as f:
                json.dump({
                    'access_token': self.access_token,
                    'timestamp': time.time()
                }, f, indent=2)
            return self.access_token
        else:
            error_msg = self.ERROR_CODES.get(result.get('errcode', -1), result.get('errmsg', '未知错误'))
            print(f"获取 access_token 失败: {error_msg}")
            sys.exit(1)

    def upload_cover(self, cover_path: str) -> str:
        """上传封面图"""
        token = self.get_access_token()
        url = f"{self.BASE_URL}/material/add_material"
        params = {
            "access_token": token,
            "type": "thumb"
        }

        if not os.path.exists(cover_path):
            print(f"警告: 封面图文件不存在: {cover_path}")
            return ""

        with open(cover_path, 'rb') as f:
            files = {"media": f}
            data = {"type": "thumb"}
            response = requests.post(url, params=params, files=files, data=data)
            result = response.json()

            if 'media_id' in result:
                print(f"✅ 封面图上传成功: {result['media_id']}")
                return result['media_id']
            else:
                print(f"✗ 封面图上传失败: {result.get('errmsg', '未知错误')}")
                return ""

    def publish_draft(self, title: str, content: str, author: str = "王金",
                       cover_media_id: Optional[str] = None, digest: str = "",
                       content_source_url: str = "", show_cover_pic: int = 1,
                       need_open_comment: int = 1, only_fans_can_comment: int = 0) -> Dict[str, Any]:
        """
        发布文章到草稿箱（UTF-8编码修复版）

        关键修复：使用 ensure_ascii=False 并手动编码为 UTF-8
        """
        token = self.get_access_token()
        url = f"{self.BASE_URL}/draft/add"
        params = {"access_token": token}

        # 关键：设置正确的 Content-Type
        headers = {'Content-Type': 'application/json; charset=utf-8'}

        # 构建文章数据
        article_data = {
            "articles": [
                {
                    "title": title[:64],  # 标题限制64字节
                    "author": author[:20],  # 作者限制20字节
                    "digest": digest[:120] if digest else "",  # 摘要限制120字节
                    "content": content,
                    "content_source_url": content_source_url,
                    "show_cover_pic": show_cover_pic,
                    "need_open_comment": need_open_comment,
                    "only_fans_can_comment": only_fans_can_comment
                }
            ]
        }

        # 只在 cover_media_id 非空时才添加它
        if cover_media_id:
            article_data["articles"][0]["thumb_media_id"] = cover_media_id

        # 关键修复：使用 ensure_ascii=False 并手动编码
        response = requests.post(
            url,
            params=params,
            data=json.dumps(article_data, ensure_ascii=False).encode('utf-8'),
            headers=headers
        )
        result = response.json()

        return result

    def format_result(self, result: Dict[str, Any]) -> bool:
        """格式化并输出结果"""
        if result.get('errcode') == 0:
            media_id = result.get('media_id', '')
            print("\n" + "=" * 50)
            print("✓ 文章成功发布到草稿箱!")
            print(f"  Media ID: {media_id}")
            print("=" * 50)
            print("\n请登录微信公众号后台查看草稿箱")
            print("https://mp.weixin.qq.com")
            return True
        elif result.get('media_id'):
            # 有时候 errcode 不为 0 但仍然成功
            media_id = result.get('media_id', '')
            print("\n" + "=" * 50)
            print("✓ 文章已创建（可能有警告）")
            print(f"  Media ID: {media_id}")
            print(f"  错误码: {result.get('errcode')}")
            print(f"  错误信息: {result.get('errmsg')}")
            print("=" * 50)
            print("\n请检查草稿箱确认文章是否正常")
            return True
        else:
            error_code = result.get('errcode', -1)
            error_msg = self.ERROR_CODES.get(error_code, result.get('errmsg', '未知错误'))
            print(f"\n✗ 发布失败: {error_msg}")
            print(f"  错误码: {error_code}")
            return False


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='微信公众号草稿发布工具')
    parser.add_argument('--title', required=True, help='文章标题')
    parser.add_argument('--content', required=True, help='HTML文件路径')
    parser.add_argument('--author', default='王金', help='作者名称')
    parser.add_argument('--cover', help='封面图路径')
    parser.add_argument('--digest', help='文章摘要')

    args = parser.parse_args()

    # 读取HTML内容
    try:
        with open(args.content, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except FileNotFoundError:
        print(f"错误: 找不到文件 {args.content}")
        sys.exit(1)

    # 上传封面图
    cover_media_id = None
    if args.cover and os.path.exists(args.cover):
        publisher = WeChatPublisher()
        cover_media_id = publisher.upload_cover(args.cover)

    # 发布草稿
    publisher = WeChatPublisher()
    result = publisher.publish_draft(
        title=args.title,
        content=html_content,
        author=args.author,
        cover_media_id=cover_media_id,
        digest=args.digest or ""
    )

    publisher.format_result(result)


if __name__ == '__main__':
    main()
