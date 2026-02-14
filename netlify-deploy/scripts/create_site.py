#!/usr/bin/env python3
"""
Netlify Site Creator
自动创建并链接 Netlify 站点
"""

import subprocess
import sys
import json
import os
import time


def create_site(site_name=None):
    """
    通过 Netlify API 创建新站点

    Args:
        site_name: 站点名称（可选，默认自动生成）

    Returns:
        dict: 站点信息或错误信息
    """
    try:
        # 如果没有提供站点名称，使用时间戳生成
        if not site_name:
            # 获取当前目录名称
            current_dir = os.path.basename(os.getcwd())
            timestamp = int(time.time())
            site_name = f"{current_dir}-{timestamp}"

        # 使用 Netlify API 创建站点
        cmd = [
            "netlify",
            "api",
            "createSite",
            "--data",
            json.dumps({"body": {"name": site_name}})
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            site_data = json.loads(result.stdout)
            return {
                "success": True,
                "site_id": site_data.get("id"),
                "site_name": site_data.get("name"),
                "url": site_data.get("ssl_url", site_data.get("url")),
                "admin_url": site_data.get("admin_url")
            }
        else:
            return {
                "success": False,
                "error": result.stderr or result.stdout
            }

    except json.JSONDecodeError as e:
        return {"success": False, "error": f"Failed to parse API response: {str(e)}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def link_site(site_id):
    """
    将当前目录链接到 Netlify 站点

    Args:
        site_id: Netlify 站点 ID

    Returns:
        dict: 成功或失败信息
    """
    try:
        # 创建 .netlify 目录
        netlify_dir = os.path.join(os.getcwd(), ".netlify")
        os.makedirs(netlify_dir, exist_ok=True)

        # 创建 state.json
        state_file = os.path.join(netlify_dir, "state.json")
        state_data = {"siteId": site_id}

        with open(state_file, 'w') as f:
            json.dump(state_data, f, indent=2)

        return {"success": True, "message": f"Site linked successfully: {site_id}"}

    except Exception as e:
        return {"success": False, "error": str(e)}


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="Create and link a Netlify site")
    parser.add_argument(
        "--name",
        help="Site name (optional, auto-generated if not provided)"
    )
    args = parser.parse_args()

    print("[*] Creating Netlify site...\n")

    # 创建站点
    result = create_site(args.name)

    if result["success"]:
        site_id = result["site_id"]
        site_name = result["site_name"]
        url = result["url"]
        admin_url = result["admin_url"]

        print(f"[OK] Site created successfully!")
        print(f"     Name: {site_name}")
        print(f"     URL: {url}")
        print(f"     Admin: {admin_url}")
        print(f"     Site ID: {site_id}\n")

        # 链接站点
        print("[*] Linking site to current directory...")
        link_result = link_site(site_id)

        if link_result["success"]:
            print(f"[OK] {link_result['message']}\n")
            print("[*] Ready to deploy! Run: netlify deploy --prod")
            return 0
        else:
            print(f"[ERROR] Failed to link site: {link_result['error']}")
            return 1
    else:
        print(f"[ERROR] Failed to create site: {result['error']}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
