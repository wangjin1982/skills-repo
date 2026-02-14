#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书多维表格管理器
经过验证的最佳实践实现
"""

import requests
import json
import csv
from typing import List, Dict, Optional

class FeishuBitableManager:
    """飞书多维表格管理器"""

    def __init__(self, app_id: str, app_secret: str, domain: str = "https://open.feishu.cn",
                 auto_share: bool = True, share_type: str = "anyone_with_link_can_edit"):
        """
        初始化管理器

        Args:
            app_id: 飞书应用ID
            app_secret: 飞书应用密钥
            domain: API域名
            auto_share: 是否自动设置分享权限（默认True）
            share_type: 分享类型（默认"anyone_with_link_can_edit"）
                - "anyone_with_link_can_view": 任何人获得链接可查看
                - "anyone_with_link_can_edit": 任何人获得链接可编辑
                - "anyone_with_link_can_comment": 任何人获得链接可评论
        """
        self.app_id = app_id
        self.app_secret = app_secret
        self.domain = domain
        self._token = None
        self.auto_share = auto_share
        self.share_type = share_type

    def set_public_share(self, app_token: str, share_type: str = "anyone_with_link_can_edit") -> bool:
        """
        设置多维表格为公开分享（任何人获得链接可编辑）

        Args:
            app_token: 应用令牌
            share_type: 分享类型
                - "anyone_with_link_can_view": 可查看
                - "anyone_with_link_can_edit": 可编辑
                - "anyone_with_link_can_comment": 可评论

        Returns:
            是否设置成功
        """
        token = self.get_token()

        # 方法1：使用drive API设置公开分享权限
        url = f"{self.domain}/open-apis/drive/v1/permissions/public/{app_token}"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        # 简化请求参数
        payload = {
            "type": share_type
        }

        try:
            response = requests.patch(url, headers=headers, json=payload)
            data = response.json()

            if data.get("code") == 0:
                return True

            # 如果方法1失败，返回False但不抛出异常
            return False

        except Exception as e:
            # 静默失败，不影响主流程
            return False

    def get_token(self) -> str:
        """获取访问令牌"""
        if self._token:
            return self._token

        url = f"{self.domain}/open-apis/auth/v3/tenant_access_token/internal"
        payload = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }

        response = requests.post(url, json=payload)
        data = response.json()

        if data.get("code") != 0:
            raise Exception(f"获取令牌失败: {data.get('msg')}")

        self._token = data.get("tenant_access_token")
        return self._token

    def create_app(self, name: str) -> str:
        """
        创建多维表格应用

        Args:
            name: 应用名称

        Returns:
            app_token: 应用令牌
        """
        token = self.get_token()
        url = f"{self.domain}/open-apis/bitable/v1/apps"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        payload = {"name": name, "folder": ""}
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()

        if data.get("code") != 0:
            raise Exception(f"创建应用失败: {data.get('msg')}")

        return data.get("data", {}).get("app", {}).get("app_token")

    def get_default_table(self, app_token: str) -> tuple:
        """
        获取默认数据表

        Args:
            app_token: 应用令牌

        Returns:
            (table_id, table_name): 数据表ID和名称
        """
        token = self.get_token()
        url = f"{self.domain}/open-apis/bitable/v1/apps/{app_token}/tables"
        headers = {"Authorization": f"Bearer {token}"}

        response = requests.get(url, headers=headers)
        data = response.json()

        if data.get("code") != 0:
            raise Exception(f"获取数据表失败: {data.get('msg')}")

        tables = data.get("data", {}).get("items", [])
        if not tables:
            raise Exception("没有找到默认数据表")

        table = tables[0]
        return table.get("table_id"), table.get("name")

    def delete_all_records(self, app_token: str, table_id: str) -> int:
        """
        删除所有记录

        Args:
            app_token: 应用令牌
            table_id: 数据表ID

        Returns:
            删除的记录数
        """
        token = self.get_token()
        url = f"{self.domain}/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records"
        headers = {"Authorization": f"Bearer {token}"}

        # 获取所有记录
        response = requests.get(url, headers=headers)
        data = response.json()

        if data.get("code") != 0:
            return 0

        items = data.get("data", {}).get("items", [])
        if not items:
            return 0

        # 批量删除
        record_ids = [item["record_id"] for item in items]
        batch_size = 500
        deleted = 0

        for i in range(0, len(record_ids), batch_size):
            batch = record_ids[i:i+batch_size]
            url_delete = f"{self.domain}/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_delete"
            headers_delete = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            payload = {"record_ids": batch}

            response = requests.delete(url_delete, headers=headers_delete, json=payload)
            if response.json().get("code") == 0:
                deleted += len(batch)

        return deleted

    def delete_template_fields(self, app_token: str, table_id: str) -> int:
        """
        删除模板字段（文本、单选、日期、附件）

        Args:
            app_token: 应用令牌
            table_id: 数据表ID

        Returns:
            删除的字段数
        """
        token = self.get_token()
        url = f"{self.domain}/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/fields"
        headers = {"Authorization": f"Bearer {token}"}

        response = requests.get(url, headers=headers)
        data = response.json()

        if data.get("code") != 0:
            return 0

        fields = data.get("data", {}).get("items", [])

        template_fields = ["文本", "单选", "日期", "附件"]
        deleted = 0

        for field in fields:
            field_name = field.get("field_name")
            if field_name in template_fields:
                field_id = field.get("field_id")
                url_delete = f"{self.domain}/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/fields/{field_id}"
                requests.delete(url_delete, headers={"Authorization": f"Bearer {token}"})
                deleted += 1

        return deleted

    def create_business_fields(self, app_token: str, table_id: str, field_names: List[str]) -> int:
        """
        创建业务字段

        Args:
            app_token: 应用令牌
            table_id: 数据表ID
            field_names: 字段名列表

        Returns:
            创建的字段数
        """
        token = self.get_token()
        url = f"{self.domain}/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/fields"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        created = 0
        for field_name in field_names:
            payload = {
                "field_name": field_name,
                "type": 1  # 文本类型
            }

            response = requests.post(url, headers=headers, json=payload)
            if response.json().get("code") == 0:
                created += 1

        return created

    def write_records(self, app_token: str, table_id: str, records: List[Dict]) -> int:
        """
        批量写入记录

        Args:
            app_token: 应用令牌
            table_id: 数据表ID
            records: 记录列表

        Returns:
            写入的记录数
        """
        token = self.get_token()
        url = f"{self.domain}/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_create"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        payload = {"records": records}
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()

        if data.get("code") != 0:
            raise Exception(f"写入记录失败: {data.get('msg')}")

        return len(records)

    def cleanup_data(self, app_token: str, table_id: str) -> Dict:
        """
        清理数据：删除空记录和重复记录

        Args:
            app_token: 应用令牌
            table_id: 数据表ID

        Returns:
            清理统计信息
        """
        token = self.get_token()
        url = f"{self.domain}/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records"
        headers = {"Authorization": f"Bearer {token}"}

        response = requests.get(url, headers=headers)
        data = response.json()

        if data.get("code") != 0:
            return {"empty": 0, "duplicates": 0}

        items = data.get("data", {}).get("items", [])

        # 找出空记录
        empty_ids = []
        business_records = []

        for item in items:
            fields = item.get("fields", {})
            if all(v is None or v == "" for v in fields.values()):
                empty_ids.append(item["record_id"])
            else:
                business_records.append(item)

        # 找出重复记录
        seen = {}
        duplicate_ids = []

        for record in business_records:
            fields = record.get("fields", {})
            key = tuple(sorted((k, v) for k, v in fields.items() if v is not None and v != ""))

            if key in seen:
                duplicate_ids.append(record["record_id"])
            else:
                seen[key] = record["record_id"]

        # 删除空记录
        if empty_ids:
            url_delete = f"{self.domain}/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_delete"
            headers_delete = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            payload = {"record_ids": empty_ids}
            requests.delete(url_delete, headers=headers_delete, json=payload)

        # 删除重复记录
        if duplicate_ids:
            url_delete = f"{self.domain}/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_delete"
            headers_delete = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            payload = {"record_ids": duplicate_ids}
            requests.delete(url_delete, headers=headers_delete, json=payload)

        return {
            "empty": len(empty_ids),
            "duplicates": len(duplicate_ids)
        }

    def verify_data(self, app_token: str, table_id: str) -> Dict:
        """
        验证数据

        Args:
            app_token: 应用令牌
            table_id: 数据表ID

        Returns:
            验证结果
        """
        token = self.get_token()
        url = f"{self.domain}/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records"
        headers = {"Authorization": f"Bearer {token}"}

        response = requests.get(url, headers=headers)
        data = response.json()

        if data.get("code") != 0:
            return {"success": False, "error": data.get("msg")}

        items = data.get("data", {}).get("items", [])

        # 统计业务记录数
        business_count = 0
        first_record = None

        for item in items:
            fields = item.get("fields", {})
            if any(v for v in fields.values() if v):
                business_count += 1
                if not first_record:
                    first_record = fields

        return {
            "success": True,
            "total": len(items),
            "business": business_count,
            "first_record": first_record
        }

    def import_csv_to_bitable(self, csv_file: str, table_name: str) -> Dict:
        """
        将CSV文件导入到飞书多维表格（完整流程）

        ⚠️ 已知问题：飞书系统会自动生成约10行空记录，这是飞书平台的行为，
        Skill会尝试清理但可能无法完全消除。不影响业务数据的完整性。

        Args:
            csv_file: CSV文件路径
            table_name: 表格名称

        Returns:
            导入结果，包含:
            - success: 是否成功
            - app_token: 应用令牌
            - table_id: 数据表ID
            - url: 多维表格链接
            - written: 写入的业务记录数
            - verified: 验证的业务记录数（排除空记录）
            - cleanup: 清理统计 {"empty": 空记录数, "duplicates": 重复记录数}
        """
        import time

        # 读取CSV
        with open(csv_file, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            data = list(reader)

        if not data:
            return {"success": False, "error": "CSV文件为空"}

        # 创建应用
        app_token = self.create_app(table_name)

        # 获取默认数据表
        table_id, _ = self.get_default_table(app_token)

        # 清理：删除所有记录
        self.delete_all_records(app_token, table_id)

        # 清理：删除模板字段
        self.delete_template_fields(app_token, table_id)

        # 等待系统处理
        time.sleep(0.5)

        # 创建业务字段
        field_names = list(data[0].keys())
        self.create_business_fields(app_token, table_id, field_names)

        # 写入数据
        records = [{"fields": row} for row in data]
        written = self.write_records(app_token, table_id, records)

        # 等待系统处理
        time.sleep(1)

        # 清理空记录和重复记录（注意：飞书系统可能仍会生成空记录）
        cleanup = self.cleanup_data(app_token, table_id)

        # 验证
        verification = self.verify_data(app_token, table_id)

        # 设置公开分享权限（如果启用）
        share_success = False
        if self.auto_share:
            try:
                share_success = self.set_public_share(app_token, self.share_type)
                if share_success:
                    print(f"     ✓ 已设置公开分享: {self.share_type}")
            except Exception as e:
                print(f"     ⚠️  设置分享权限失败: {e}")

        return {
            "success": True,
            "app_token": app_token,
            "table_id": table_id,
            "url": f"https://feishu.cn/base/{app_token}",
            "written": written,
            "verified": verification.get("business", 0),
            "cleanup": cleanup,
            "share_type": self.share_type if share_success else None
        }


# 便捷函数
def create_manager(app_id: str, app_secret: str,
                  auto_share: bool = True,
                  share_type: str = "anyone_with_link_can_edit") -> FeishuBitableManager:
    """
    创建管理器实例

    Args:
        app_id: 飞书应用ID
        app_secret: 飞书应用密钥
        auto_share: 是否自动设置分享权限（默认True）
        share_type: 分享类型（默认"anyone_with_link_can_edit"）

    Returns:
        FeishuBitableManager实例
    """
    return FeishuBitableManager(app_id, app_secret, auto_share=auto_share, share_type=share_type)
