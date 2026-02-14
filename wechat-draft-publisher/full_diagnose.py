#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整的IP白名单诊断工具
"""

import sys
import os
import requests
import socket

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def get_all_ips():
    """获取所有可能的IP地址"""
    ips = {}

    # 1. 获取本地IP
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        ips['Local IP'] = local_ip
    except:
        pass

    # 2. 获取公网IP
    public_ip_services = [
        'https://api.ipify.org?format=text',
        'https://ifconfig.me/ip',
        'http://icanhazip.com',
        'https://ipinfo.io/ip'
    ]

    for service in public_ip_services:
        try:
            response = requests.get(service, timeout=5)
            if response.status_code == 200:
                public_ip = response.text.strip()
                if public_ip and public_ip != local_ip:
                    ips['Public IP'] = public_ip
                    break
        except:
            continue

    # 3. 从错误信息中看到的IP
    ips['Error Message IP'] = '172.20.1.251'

    return ips

def test_direct_api():
    """直接测试微信API"""
    try:
        # 读取配置
        import json
        config_file = os.path.expanduser("~/.wechat-publisher/config.json")

        with open(config_file, 'r') as f:
            config = json.load(f)

        appid = config['appid']
        appsecret = config['appsecret']

        # 直接调用API
        url = "https://api.weixin.qq.com/cgi-bin/token"
        params = {
            'grant_type': 'client_credential',
            'appid': appid,
            'secret': appsecret
        }

        print("\n[Direct API Test]")
        print(f"  AppID: {appid[:6]}***")
        print(f"  Target: https://api.weixin.qq.com/cgi-bin/token")

        response = requests.get(url, params=params, timeout=10)

        result = response.json()

        if 'access_token' in result:
            print(f"  [SUCCESS] Got access_token!")
            print(f"  Token: {result['access_token'][:20]}...")
            print(f"  Expires in: {result.get('expires_in', 7200)} seconds")
            return True, result
        else:
            print(f"  [FAILED] API returned error")
            print(f"  Error Code: {result.get('errcode')}")
            print(f"  Error Message: {result.get('errmsg')}")

            errcode = result.get('errcode')

            if errcode == 40164:
                print("\n  [DIAGNOSIS]")
                print("  This is an IP Whitelist issue!")
                print("\n  [WHAT TO DO]")
                print("  1. Login: https://mp.weixin.qq.com")
                print("  2. Settings & Development -> Basic Configuration")
                print("  3. Find 'IP Whitelist' section")
                print("  4. Click 'Modify' or 'Configure'")
                print("  5. Add ALL the IPs listed below")
                print("  6. Click SAVE/CONFIRM")
                print("\n  [IMPORTANT]")
                print("  - Wait 1-5 minutes after saving")
                print("  - Make sure you clicked the SAVE button")
                print("  - Try adding ALL IPs from the list below")

            return False, result

    except Exception as e:
        print(f"  [ERROR] {str(e)}")
        return False, None

def main():
    print("=" * 70)
    print(" " * 15 + "WECHAT IP WHITELIST DIAGNOSTICS")
    print("=" * 70)

    # 获取所有IP
    print("\n[STEP 1] Detecting IP addresses...")
    ips = get_all_ips()

    print("\n  All detected IP addresses:")
    for name, ip in ips.items():
        print(f"    {name}: {ip}")

    # 测试API
    print("\n[STEP 2] Testing WeChat API connection...")
    success, result = test_direct_api()

    # 建议
    print("\n" + "=" * 70)
    if success:
        print("[RESULT] SUCCESS - IP whitelist is configured correctly!")
        print("\nYou can now run:")
        print("  python clear_and_upload.py")
    else:
        print("[RESULT] FAILED - IP whitelist needs configuration")
        print("\n[REQUIRED ACTION]")
        print("1. Go to WeChat MP backend")
        print("2. Add these IPs to whitelist (one per line or comma-separated):")
        for name, ip in ips.items():
            if 'Error Message' not in name:
                print(f"   - {ip}")
        print("\n3. SAVE the changes")
        print("4. Wait 1-5 minutes")
        print("5. Run this test again")
    print("=" * 70)

    return success

if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n[FATAL ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
