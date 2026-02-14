#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书智能日历管理器
自动读取现有日程，智能插入新日程
"""

import requests
import json
import time
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple


class FeishuSmartCalendar:
    """飞书智能日历管理器"""

    def __init__(self, app_id: str, app_secret: str, domain: str = "https://open.feishu.cn"):
        self.app_id = app_id
        self.app_secret = app_secret
        self.domain = domain
        self._token = None
        self._token_expire_time = 0

        # 工作时间配置
        self.work_start_hour = 9  # 早上9点
        self.work_end_hour = 18  # 晚上6点
        self.min_gap_minutes = 15  # 两个日程之间最小间隔（分钟）

    def get_token(self) -> str:
        """获取访问令牌"""
        if self._token and time.time() < self._token_expire_time - 300:
            return self._token

        url = f"{self.domain}/open-apis/auth/v3/tenant_access_token/internal"
        payload = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }

        response = requests.post(url, json=payload)
        data = response.json()

        if data.get("code") != 0:
            raise Exception(f"获取token失败: {data.get('msg')}")

        self._token = data.get("tenant_access_token")
        self._token_expire_time = time.time() + 7200

        return self._token

    def get_calendar_list(self) -> List[Dict]:
        """获取日历列表"""
        token = self.get_token()
        url = f"{self.domain}/open-apis/calendar/v4/calendars"
        headers = {"Authorization": f"Bearer {token}"}

        response = requests.get(url, headers=headers)
        data = response.json()

        if data.get("code") == 0:
            return data.get("data", {}).get("calendar_list", [])
        else:
            raise Exception(f"获取日历列表失败: {data.get('msg')}")

    def get_primary_calendar_id(self) -> str:
        """获取主日历ID"""
        calendars = self.get_calendar_list()
        if not calendars:
            raise Exception("没有找到日历")
        return calendars[0].get('calendar_id')

    def get_events(self, calendar_id: str, start_time: int = None, end_time: int = None) -> List[Dict]:
        """获取日程列表"""
        token = self.get_token()

        if not start_time:
            now = datetime.now()
            start_time = int(now.timestamp())
        if not end_time:
            future = datetime.now() + timedelta(days=7)
            end_time = int(future.timestamp())

        url = f"{self.domain}/open-apis/calendar/v4/calendars/{calendar_id}/events"
        headers = {"Authorization": f"Bearer {token}"}
        params = {
            "start_time": str(start_time),
            "end_time": str(end_time),
            "page_size": 50
        }

        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        if data.get("code") == 0:
            return data.get("data", {}).get("items", [])
        else:
            raise Exception(f"获取日程列表失败: {data.get('msg')}")

    def create_event(self, calendar_id: str, summary: str, start_time: int, end_time: int,
                     description: str = "", location: str = "") -> Dict:
        """创建日程"""
        token = self.get_token()
        url = f"{self.domain}/open-apis/calendar/v4/calendars/{calendar_id}/events"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        payload = {
            "summary": summary,
            "start_time": {"timestamp": str(start_time)},
            "end_time": {"timestamp": str(end_time)}
        }

        if description:
            payload["description"] = description
        if location:
            payload["location"] = {"name": location}

        response = requests.post(url, headers=headers, json=payload)
        data = response.json()

        if data.get("code") == 0:
            return data.get("data", {}).get("event", {})
        else:
            raise Exception(f"创建日程失败: {data.get('msg')}")

    def find_free_slots(self, events: List[Dict], start_date: datetime, end_date: datetime,
                       duration_minutes: int) -> List[Tuple[datetime, datetime]]:
        """
        找到空闲时间段

        Args:
            events: 现有日程列表
            start_date: 搜索开始日期
            end_date: 搜索结束日期
            duration_minutes: 需要的时长（分钟）

        Returns:
            可用时间段列表 [(开始时间, 结束时间), ...]
        """
        # 将events转换为时间段列表
        busy_slots = []
        for event in events:
            start_ts = int(event.get('start_time', {}).get('timestamp', 0))
            end_ts = int(event.get('end_time', {}).get('timestamp', 0))
            if start_ts and end_ts:
                busy_slots.append((
                    datetime.fromtimestamp(start_ts),
                    datetime.fromtimestamp(end_ts)
                ))

        # 按开始时间排序
        busy_slots.sort(key=lambda x: x[0])

        # 查找空闲时间段
        free_slots = []
        current_date = start_date.replace(hour=self.work_start_hour, minute=0, second=0, microsecond=0)

        while current_date.date() <= end_date.date():
            # 当天工作时间的开始和结束
            day_start = current_date.replace(hour=self.work_start_hour, minute=0, second=0)
            day_end = current_date.replace(hour=self.work_end_hour, minute=0, second=0)

            # 找出当天的忙碌时段
            day_busy = [slot for slot in busy_slots if slot[0].date() == current_date.date()]

            # 如果当天没有任何日程
            if not day_busy:
                if day_end > datetime.now():
                    # 检查是否有足够的时间
                    potential_start = max(day_start, datetime.now() + timedelta(minutes=self.min_gap_minutes))
                    if potential_start < day_end:
                        available_minutes = (day_end - potential_start).total_seconds() / 60
                        if available_minutes >= duration_minutes:
                            free_slots.append((potential_start, potential_start + timedelta(minutes=duration_minutes)))
            else:
                # 检查第一个日程之前的时间
                first_busy_start = day_busy[0][0]
                potential_start = max(day_start, datetime.now() + timedelta(minutes=self.min_gap_minutes))
                if potential_start < first_busy_start:
                    available_minutes = (first_busy_start - potential_start).total_seconds() / 60
                    if available_minutes >= duration_minutes + self.min_gap_minutes:
                        free_slots.append((potential_start, potential_start + timedelta(minutes=duration_minutes)))

                # 检查日程之间的间隙
                for i in range(len(day_busy) - 1):
                    gap_start = day_busy[i][1] + timedelta(minutes=self.min_gap_minutes)
                    gap_end = day_busy[i + 1][0]
                    available_minutes = (gap_end - gap_start).total_seconds() / 60
                    if available_minutes >= duration_minutes + self.min_gap_minutes:
                        free_slots.append((gap_start, gap_start + timedelta(minutes=duration_minutes)))

                # 检查最后一个日程之后的时间
                last_busy_end = day_busy[-1][1]
                gap_start = last_busy_end + timedelta(minutes=self.min_gap_minutes)
                if gap_start < day_end:
                    available_minutes = (day_end - gap_start).total_seconds() / 60
                    if available_minutes >= duration_minutes + self.min_gap_minutes:
                        free_slots.append((gap_start, gap_start + timedelta(minutes=duration_minutes)))

            # 移动到下一天
            current_date += timedelta(days=1)

        return free_slots

    def smart_add_event(self, summary: str, duration_minutes: int,
                       description: str = "", location: str = "",
                       preferred_time: Optional[datetime] = None,
                       days_to_search: int = 7) -> Dict:
        """
        智能添加日程

        Args:
            summary: 日程标题
            duration_minutes: 持续时间（分钟）
            description: 描述
            location: 地点
            preferred_time: 首选时间（可选）
            days_to_search: 搜索未来几天

        Returns:
            创建的日程信息，包含建议的时间
        """
        # 获取主日历
        calendar_id = self.get_primary_calendar_id()

        # 获取现有日程
        now = datetime.now()
        search_end = now + timedelta(days=days_to_search)
        start_time = int(now.timestamp())
        end_time = int(search_end.timestamp())
        events = self.get_events(calendar_id, start_time, end_time)

        # 查找空闲时间段
        free_slots = self.find_free_slots(events, now, search_end, duration_minutes)

        if not free_slots:
            raise Exception(f"未来{days_to_search}天内没有找到{duration_minutes}分钟的空闲时间")

        # 选择最佳时间段
        if preferred_time:
            # 找到最接近首选时间的空闲段
            best_slot = min(free_slots, key=lambda slot: abs((slot[0] - preferred_time).total_seconds()))
        else:
            # 使用第一个可用时间段
            best_slot = free_slots[0]

        chosen_start, chosen_end = best_slot

        # 创建日程
        event = self.create_event(
            calendar_id=calendar_id,
            summary=summary,
            start_time=int(chosen_start.timestamp()),
            end_time=int(chosen_end.timestamp()),
            description=description,
            location=location
        )

        return {
            "event": event,
            "chosen_time": {
                "start": chosen_start.strftime("%Y-%m-%d %H:%M:%S"),
                "end": chosen_end.strftime("%Y-%m-%d %H:%M:%S")
            },
            "alternative_slots": [
                {
                    "start": slot[0].strftime("%Y-%m-%d %H:%M:%S"),
                    "end": slot[1].strftime("%Y-%m-%d %H:%M:%S")
                }
                for slot in free_slots[:5]  # 返回前5个备选时间段
            ]
        }

    def batch_add_events(self, events_to_add: List[Dict]) -> List[Dict]:
        """
        批量智能添加多个日程

        Args:
            events_to_add: 待添加的日程列表，每个元素包含 {summary, duration_minutes, description, location}

        Returns:
            创建结果列表
        """
        results = []
        for event_info in events_to_add:
            try:
                result = self.smart_add_event(
                    summary=event_info.get("summary", ""),
                    duration_minutes=event_info.get("duration_minutes", 60),
                    description=event_info.get("description", ""),
                    location=event_info.get("location", "")
                )
                results.append({
                    "success": True,
                    "summary": event_info.get("summary"),
                    "result": result
                })
            except Exception as e:
                results.append({
                    "success": False,
                    "summary": event_info.get("summary"),
                    "error": str(e)
                })

        return results


def main():
    """示例：智能添加日程"""
    # 加载配置
    with open("/home/aiops3/.claude/feishu_config.json", "r") as f:
        config = json.load(f)

    manager = FeishuSmartCalendar(
        app_id=config["app_id"],
        app_secret=config["app_secret"],
        domain=config["domain"]
    )

    print("=" * 60)
    print("飞书智能日历管理器 - 示例")
    print("=" * 60)

    try:
        # 示例1：添加单个日程
        print("\n[示例1] 智能添加单个日程...")
        result = manager.smart_add_event(
            summary="团队周会",
            duration_minutes=60,
            description="讨论本周工作进展和下周计划",
            location="会议室A"
        )

        print(f"\n✅ 日程已创建!")
        print(f"   标题: {result['event']['summary']}")
        print(f"   时间: {result['chosen_time']['start']} - {result['chosen_time']['end']}")
        print(f"\n   其他可选时间段:")
        for i, slot in enumerate(result['alternative_slots'][:3], 1):
            print(f"   {i}. {slot['start']} - {slot['end']}")

        # 示例2：批量添加多个日程
        print("\n" + "=" * 60)
        print("[示例2] 批量添加多个日程...")
        events_to_add = [
            {
                "summary": "代码评审",
                "duration_minutes": 30,
                "description": "评审新功能代码",
                "location": "线上"
            },
            {
                "summary": "客户沟通",
                "duration_minutes": 45,
                "description": "讨论项目需求",
                "location": "电话会议"
            }
        ]

        results = manager.batch_add_events(events_to_add)

        print(f"\n✅ 批量添加完成!")
        for result in results:
            if result["success"]:
                print(f"   ✓ {result['summary']}: {result['result']['chosen_time']['start']}")
            else:
                print(f"   ✗ {result['summary']}: {result['error']}")

    except Exception as e:
        print(f"\n❌ 操作失败: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
