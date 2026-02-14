#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from publisher import WeChatPublisher
    import json

    publisher = WeChatPublisher()

    print("Testing WeChat API connection...")
    print(f"AppID: {publisher.appid[:6]}***")

    # Try to get access token
    try:
        token = publisher.get_access_token()
        print("SUCCESS! Access token obtained")
        print(f"Token: {token[:30]}...")

        # If successful, try to get material list
        print("\nTesting material list access...")
        images = publisher.get_material_list('image', 0, 5)
        print(f"Found {len(images)} images in library")

        for img in images[:5]:
            print(f"  - {img.get('name', 'unknown')}")

    except Exception as e:
        error_msg = str(e)
        print(f"ERROR: {error_msg}")

        if '40164' in error_msg:
            print("\n" + "="*60)
            print("IP WHITELIST ISSUE DETECTED")
            print("="*60)
            print("\nYou need to:")
            print("1. Go to https://mp.weixin.qq.com")
            print("2. Settings & Development -> Basic Configuration")
            print("3. Find IP Whitelist section")
            print("4. Add this IP: 172.20.1.251")
            print("\nAlso try adding your public IP if different")
            print("Save changes and wait 1-2 minutes")
            print("="*60)

except Exception as e:
    print(f"FATAL: {str(e)}")
    import traceback
    traceback.print_exc()
