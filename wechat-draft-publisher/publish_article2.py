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
        content_file = r"C:\Users\wangj\Documents\微信公众号\output\20260119\article2\article_wechat.html"
        with open(content_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 上传封面图
        cover_file = r"C:\Users\wangj\Documents\微信公众号\output\20260119\article2\cover.png"
        print("\n正在上传封面图...")
        thumb_media_id = publisher.upload_image(cover_file, return_url=False)
        print(f"封面图上传成功 (Media ID: {thumb_media_id})")

        # 发布文章
        print("\n正在创建草稿...")
        result = publisher.create_draft(
            title="如何培养员工的主动性：从依赖到独立",
            content=content,
            author="阳桃AI干货",
            thumb_media_id=thumb_media_id
        )

        print(f"\n发布完成!")
        print(f"请前往微信公众号后台查看草稿箱：")
        print(f"https://mp.weixin.qq.com")

    except Exception as e:
        print(f"\n错误: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
