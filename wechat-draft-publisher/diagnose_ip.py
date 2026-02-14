#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IP白名单诊断工具
"""

import sys
import os
import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def get_public_ip():
    """获取当前公网IP"""
    try:
        # 尝试多个服务
        services = [
            'https://api.ipify.org',
            'https://ifconfig.me',
            'http://icanhazip.com'
        ]

        for service in services:
            try:
                response = requests.get(service, timeout=5)
                if response.status_code == 200:
                    return response.text.strip()
            except:
                continue

        return None
    except Exception as e:
        return None

def test_wechat_api():
    """测试微信API连接"""
    try:
        from publisher import WeChatPublisher

        publisher = WeChatPublisher()

        print("=" * 70)
        print(" " * 20 + "WECHAT API DIAGNOSTICS")
        print("=" * 70)

        # 显示配置信息
        print(f"\n[CONFIG]")
        print(f"  AppID: {publisher.appid[:6]}***")
        print(f"  Config File: {publisher.CONFIG_FILE}")

        # 尝试获取access_token
        print(f"\n[TEST] Testing access_token...")
        try:
            token = publisher.get_access_token()
            print(f"  [OK] Successfully obtained access_token")
            print(f"  Token (first 20 chars): {token[:20]}...")
            return True
        except Exception as e:
            error_str = str(e)
            print(f"  [FAIL] {error_str}")

            if '40164' in error_str:
                print(f"\n[DIAGNOSIS]")
                print(f"  Error Code: 40164")
                print(f"  Meaning: IP address not in whitelist")
                print(f"\n[ACTION REQUIRED]")
                print(f"  1. Login to https://mp.weixin.qq.com")
                print(f"  2. Go to: Settings & Development -> Basic Configuration")
                print(f"  3. Find 'IP Whitelist' section")
                print(f"  4. Add the IP address(es) shown below")

                # 获取当前IP
                print(f"\n[CURRENT IP ADDRESSES]")
                local_ip = '172.20.1.251'  # 从错误信息中看到
                print(f"  Local Network IP: {local_ip}")

                public_ip = get_public_ip()
                if public_ip:
                    print(f"  Public IP: {public_ip}")
                    print(f"\n  [TIP] Try adding BOTH IPs to the whitelist:")
                    print(f"    - {local_ip}")
                    print(f"    - {public_ip}")
                else:
                    print(f"  Public IP: Unable to detect")

                print(f"\n[NOTE]")
                print(f"  - IP whitelist changes may take a few minutes to take effect")
                print(f"  - Make sure to SAVE the changes after adding IPs")
                print(f"  - Some accounts require multiple IPs (proxy, NAT, etc.)")

            return False

    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        return False

if __name__ == '__main__':
    success = test_wechat_api()

    print("\n" + "=" * 70)
    if success:
        print("RESULT: API connection successful - IP whitelist is configured")
    else:
        print("RESULT: API connection failed - IP whitelist needs configuration")
    print("=" * 70)

    sys.exit(0 if success else 1)
