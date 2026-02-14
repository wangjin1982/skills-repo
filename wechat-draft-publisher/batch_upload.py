#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from publisher import WeChatPublisher

def upload_batch():
    """上传两张图片到微信素材库"""

    images = [
        ("C:/Users/wangj/.claude/skills/canvas-design/goal_alignment_style1.png", "Style 1 - Radiant Convergence"),
        ("C:/Users/wangj/.claude/skills/canvas-design/goal_alignment_style2.png", "Style 2 - Hierarchical Alignment")
    ]

    results = []

    try:
        publisher = WeChatPublisher()

        print("=" * 60)
        print("  Uploading Design Images to WeChat Media Library")
        print("=" * 60)

        for image_path, description in images:
            print(f"\n[{images.index((image_path, description)) + 1}/2] Uploading...")
            print(f"Style: {description}")
            print(f"File: {os.path.basename(image_path)}")

            try:
                result = publisher.upload_image(image_path, return_url=True)

                if isinstance(result, tuple):
                    media_id, image_url = result
                    print(f"[OK] Uploaded successfully")
                    print(f"    Media ID: {media_id}")
                    results.append({
                        'style': description,
                        'media_id': media_id,
                        'url': image_url,
                        'status': 'success'
                    })
                else:
                    media_id = result
                    print(f"[OK] Uploaded successfully")
                    print(f"    Media ID: {media_id}")
                    results.append({
                        'style': description,
                        'media_id': media_id,
                        'status': 'success'
                    })
            except Exception as e:
                print(f"[ERROR] Upload failed: {str(e)}")
                results.append({
                    'style': description,
                    'status': 'failed',
                    'error': str(e)
                })

        print("\n" + "=" * 60)
        print("  Upload Summary")
        print("=" * 60)

        success_count = sum(1 for r in results if r['status'] == 'success')
        print(f"\nSuccessfully uploaded: {success_count}/2")

        for r in results:
            status_symbol = "[OK]" if r['status'] == 'success' else "[FAIL]"
            print(f"{status_symbol} {r['style']}")
            if r['status'] == 'success':
                print(f"     Media ID: {r['media_id']}")

        print("\n" + "=" * 60)
        print("Next Steps:")
        print("=" * 60)
        print("1. Login to https://mp.weixin.qq.com")
        print("2. Go to: Materials Management -> Images")
        print("3. Select your preferred style for the article")
        print("=" * 60)

        return results

    except Exception as e:
        print(f"\n[FATAL ERROR] {str(e)}")
        print("\nTip: Make sure IP whitelist is configured in WeChat backend")
        return []

if __name__ == '__main__':
    upload_batch()
