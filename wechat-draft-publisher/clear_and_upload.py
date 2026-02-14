#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整工作流：清空图片库 + 上传新图片
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    print("=" * 70)
    print(" " * 15 + "WECHAT IMAGE LIBRARY MANAGER")
    print("=" * 70)
    print("\nWorkflow: Clear All Images -> Upload 2 New Designs\n")

    from publisher import WeChatPublisher

    try:
        publisher = WeChatPublisher()

        # Step 1: Clear all images
        print("\n[STEP 1/2] Clearing existing images...")
        print("-" * 70)
        publisher.clear_all_images()
        print("\n[OK] Image library cleared successfully")

        # Step 2: Upload new images
        print("\n[STEP 2/2] Uploading new design images...")
        print("-" * 70)

        images = [
            {
                'path': "C:/Users/wangj/.claude/skills/canvas-design/goal_alignment_style1.png",
                'name': "Style 1 - Radiant Convergence"
            },
            {
                'path': "C:/Users/wangj/.claude/skills/canvas-design/goal_alignment_style2.png",
                'name': "Style 2 - Hierarchical Pyramid"
            }
        ]

        results = []
        for i, img in enumerate(images, 1):
            print(f"\n[{i}/2] Uploading: {img['name']}")

            try:
                result = publisher.upload_image(img['path'], return_url=True)

                if isinstance(result, tuple):
                    media_id, url = result
                    print(f"     [OK] Media ID: {media_id}")
                    results.append({'name': img['name'], 'media_id': media_id, 'success': True})
                else:
                    print(f"     [OK] Media ID: {result}")
                    results.append({'name': img['name'], 'media_id': result, 'success': True})

            except Exception as e:
                print(f"     [ERROR] {str(e)}")
                results.append({'name': img['name'], 'error': str(e), 'success': False})

        # Final summary
        print("\n" + "=" * 70)
        print(" " * 25 + "FINAL SUMMARY")
        print("=" * 70)

        success_count = sum(1 for r in results if r['success'])

        print(f"\n✓ Cleared all old images")
        print(f"✓ Uploaded {success_count}/2 new images")

        for r in results:
            if r['success']:
                print(f"\n  [OK] {r['name']}")
                print(f"       Media ID: {r['media_id']}")

        print("\n" + "=" * 70)
        print("Your image library now contains only these 2 designs!")
        print("Access: https://mp.weixin.qq.com -> Materials -> Images")
        print("=" * 70)

        return success_count == 2

    except Exception as e:
        print(f"\n[FATAL ERROR] {str(e)}")
        print("\nTroubleshooting:")
        print("  1. Check IP whitelist configuration")
        print("  2. Verify AppID/AppSecret")
        print("  3. Check network connection")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
