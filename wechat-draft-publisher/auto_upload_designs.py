#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动上传设计图到微信公众号素材库
配置好IP白名单后直接运行此脚本
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    print("=" * 70)
    print(" " * 15 + "GOAL ALIGNMENT - DESIGN UPLOAD")
    print("=" * 70)
    print("\nPreparing to upload 2 design styles to WeChat Media Library...\n")

    # Import after print to avoid encoding issues in imports
    from publisher import WeChatPublisher

    images = [
        {
            'path': "C:/Users/wangj/.claude/skills/canvas-design/goal_alignment_style1.png",
            'name': "Style 1 - Radiant Convergence",
            'description': "Classic arrow convergence design, 16 arrows pointing to central goal"
        },
        {
            'path': "C:/Users/wangj/.claude/skills/canvas-design/goal_alignment_style2.png",
            'name': "Style 2 - Hierarchical Pyramid",
            'description': "Pyramid structure showing team-manager-leader-goal alignment"
        }
    ]

    results = []

    try:
        publisher = WeChatPublisher()

        for i, img in enumerate(images, 1):
            print(f"[{i}/2] {img['name']}")
            print(f"      {img['description']}")

            try:
                result = publisher.upload_image(img['path'], return_url=True)

                if isinstance(result, tuple):
                    media_id, url = result
                    print(f"      [OK] Media ID: {media_id}")
                    results.append({'name': img['name'], 'media_id': media_id, 'url': url, 'success': True})
                else:
                    print(f"      [OK] Media ID: {result}")
                    results.append({'name': img['name'], 'media_id': result, 'success': True})

            except Exception as e:
                print(f"      [ERROR] {str(e)}")
                results.append({'name': img['name'], 'error': str(e), 'success': False})

            print()

        # Summary
        print("=" * 70)
        print(" " * 25 + "UPLOAD SUMMARY")
        print("=" * 70)

        success = [r for r in results if r['success']]
        failed = [r for r in results if not r['success']]

        print(f"\nUploaded: {len(success)}/2")
        for r in success:
            print(f"  [OK] {r['name']}")
            print(f"       Media ID: {r['media_id']}")

        if failed:
            print(f"\nFailed: {len(failed)}/2")
            for r in failed:
                print(f"  [X] {r['name']}")

        print("\n" + "=" * 70)
        print("Access your images:")
        print("  https://mp.weixin.qq.com -> Materials -> Images")
        print("=" * 70)

        return len(success) == 2

    except Exception as e:
        print(f"\n[FATAL] {str(e)}")
        print("\nTroubleshooting:")
        print("  1. Check IP whitelist: https://mp.weixin.qq.com -> Basic Config")
        print("  2. Verify AppID/AppSecret in config file")
        print("  3. Check network connection")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
