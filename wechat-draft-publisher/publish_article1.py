# -*- coding: utf-8 -*-
import sys
import os

# 设置标准输出编码为 UTF-8
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# 导入发布器
sys.path.insert(0, os.path.dirname(__file__))
from publisher import WeChatPublisher

def main():
    try:
        publisher = WeChatPublisher()

        # 读取文章内容
        content_file = r"C:\Users\wangj\Documents\微信公众号\output\20260119\article\article_wechat.html"
        with open(content_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 上传封面图
        cover_file = r"C:\Users\wangj\Documents\微信公众号\output\20260119\article\cover.png"
        print("\n正在上传封面图...")
        thumb_media_id = publisher.upload_image(cover_file, return_url=False)
        print(f"封面图上传成功 (Media ID: {thumb_media_id})")

        # 发布文章
        print("\n正在创建草稿...")
        result = publisher.create_draft(
            title="从控制者到教练：2025年忙碌管理者需要的一次思维升级",
            content=content,
            author="阳桃AI干货",
            thumb_media_id=thumb_media_id
        )

        if result['success']:
            print(f"\n发布成功!")
            print(f"Media ID: {result.get('media_id', 'N/A')}")
            print(f"\n请前往微信公众号后台查看草稿箱：")
            print(f"https://mp.weixin.qq.com")
        else:
            print(f"\n发布失败: {result.get('error', 'Unknown error')}")

    except Exception as e:
        print(f"\n错误: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
