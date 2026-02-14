#!/usr/bin/env python3
"""
Netlify Environment Checker
检查 Netlify CLI 安装和登录状态
"""

import subprocess
import sys
import json
import shutil


def resolve_netlify_command():
    """在 Windows 上优先使用 netlify.cmd，避免 CreateProcess 无法直接运行 .cmd"""
    if sys.platform.startswith("win"):
        if shutil.which("netlify.cmd"):
            return "netlify.cmd"
    return "netlify"


NETLIFY_COMMAND = resolve_netlify_command()


def check_netlify_cli():
    """检查 Netlify CLI 是否已安装"""
    try:
        result = subprocess.run(
            [NETLIFY_COMMAND, "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            version = result.stdout.strip()
            return {"installed": True, "version": version}
        else:
            return {"installed": False, "error": result.stderr}
    except FileNotFoundError:
        return {"installed": False, "error": "Netlify CLI not found"}
    except Exception as e:
        return {"installed": False, "error": str(e)}


def check_login_status():
    """检查 Netlify 登录状态"""
    try:
        result = subprocess.run(
            [NETLIFY_COMMAND, "status"],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            output = result.stdout
            # 提取用户信息
            user_info = {}
            for line in output.split('\n'):
                if 'Name:' in line:
                    user_info['name'] = line.split('Name:')[1].strip()
                elif 'Email:' in line:
                    user_info['email'] = line.split('Email:')[1].strip()

            return {
                "logged_in": True,
                "user": user_info
            }
        else:
            return {"logged_in": False, "error": result.stderr}
    except Exception as e:
        return {"logged_in": False, "error": str(e)}


def check_site_linked():
    """检查当前目录是否已链接到 Netlify 站点"""
    try:
        result = subprocess.run(
            [NETLIFY_COMMAND, "status"],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0 and "Current project:" in result.stdout:
            # 提取站点信息
            site_info = {}
            for line in result.stdout.split('\n'):
                if 'Current project:' in line:
                    site_info['name'] = line.split('Current project:')[1].strip()
                elif 'Project URL:' in line:
                    site_info['url'] = line.split('Project URL:')[1].strip()
                elif 'Project Id:' in line:
                    site_info['id'] = line.split('Project Id:')[1].strip()

            return {
                "linked": True,
                "site": site_info
            }
        else:
            return {"linked": False}
    except Exception as e:
        return {"linked": False, "error": str(e)}


def main():
    """主函数"""
    print("[*] Checking Netlify environment...\n")

    # 检查 CLI
    cli_status = check_netlify_cli()
    if cli_status["installed"]:
        print(f"[OK] Netlify CLI installed: {cli_status['version']}")
    else:
        print(f"[ERROR] Netlify CLI not installed: {cli_status.get('error', 'Unknown error')}")
        print("\n[TIP] Install with: npm install -g netlify-cli")
        return 1

    # 检查登录
    login_status = check_login_status()
    if login_status["logged_in"]:
        user = login_status.get("user", {})
        print(f"[OK] Logged in as: {user.get('name', 'Unknown')} ({user.get('email', 'Unknown')})")
    else:
        print(f"[ERROR] Not logged in: {login_status.get('error', 'Unknown error')}")
        print("\n[TIP] Login with: netlify login")
        return 1

    # 检查站点链接
    site_status = check_site_linked()
    if site_status["linked"]:
        site = site_status.get("site", {})
        print(f"[OK] Site linked: {site.get('name', 'Unknown')}")
        print(f"     URL: {site.get('url', 'Unknown')}")
    else:
        print("[INFO] No site linked (will create new site during deployment)")

    print("\n[OK] Environment check complete!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
