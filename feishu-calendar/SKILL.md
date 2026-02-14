---
name: feishu-calendar
description: "飞书智能日历管理工具。读取现有日程，智能分析空闲时间，自动将新日程安排到合适的时间段。当用户提到需要安排会议、添加日程、或者提到有哪些事情需要处理时使用此Skill。"
license: MIT
---

# 飞书智能日历管理 Skill (Feishu Smart Calendar)

## 概述

这是一个智能日历管理工具，能够：
- 读取飞书日历中的现有日程
- 智能分析空闲时间段
- 自动将新日程安排到最合适的时间
- 支持批量添加多个日程
- 考虑工作时间和最小间隔要求

## 核心功能

### 1. 智能单日程添加
自动找到最合适的空闲时间段，添加单个日程。

### 2. 批量日程添加
一次性添加多个日程，系统会智能分配时间，避免冲突。

### 3. 日程查看
查看未来指定天数内的所有日程安排。

### 4. 空闲时间查询
查找指定时间范围内的所有空闲时间段。

## 前置要求

### 1. 飞书应用配置

需要在飞书开放平台配置以下权限：
- `calendar:calendar` - 日历基础权限
- `calendar:calendar.event` - 日程事件权限
- `calendar:calendar.event:readonly` - 查看日程
- `calendar:calendar.event:create` - 创建日程

### 2. 环境要求
- Python 3.6+
- requests 库

## 使用指南

### 方式1: Python代码集成

```python
import sys
sys.path.append('/home/aiops3/.claude/skills/feishu-calendar')

from scripts.feishu_calendar_manager import FeishuSmartCalendar

# 加载配置
import json
with open("/home/aiops3/.claude/feishu_config.json", "r") as f:
    config = json.load(f)

# 初始化管理器
manager = FeishuSmartCalendar(
    app_id=config["app_id"],
    app_secret=config["app_secret"],
    domain=config["domain"]
)

# 智能添加单个日程
result = manager.smart_add_event(
    summary="团队周会",
    duration_minutes=60,
    description="讨论本周工作进展",
    location="会议室A"
)

print(f"日程已安排在: {result['chosen_time']['start']}")
print(f"其他可选时间: {result['alternative_slots']}")

# 批量添加多个日程
events_to_add = [
    {
        "summary": "代码评审",
        "duration_minutes": 30,
        "description": "评审新功能代码"
    },
    {
        "summary": "客户沟通",
        "duration_minutes": 45,
        "description": "讨论项目需求"
    }
]

results = manager.batch_add_events(events_to_add)
for result in results:
    if result["success"]:
        print(f"✓ {result['summary']}: {result['result']['chosen_time']['start']}")
```

### 方式2: 命令行快速测试

```bash
cd /home/aiops3/.claude/skills/feishu-calendar/scripts
python3 feishu_calendar_manager.py
```

## 智能调度算法

### 工作时间
- 默认工作时间: 9:00 - 18:00
- 可以通过修改 `work_start_hour` 和 `work_end_hour` 自定义

### 时间间隔
- 两个日程之间默认保留 15 分钟间隔
- 可以通过 `min_gap_minutes` 自定义

### 调度策略
1. 读取未来N天（默认7天）的所有日程
2. 识别每天的工作时间内的空闲时段
3. 过滤掉小于所需时长的时段
4. 如果指定了首选时间，选择最接近的空闲时段
5. 否则选择最早的可用时段

### 时间冲突处理
- 自动避开已有日程
- 保证日程之间有足够的间隔
- 只在工作时间内安排日程
- 不会安排到过去的时间

## 配置选项

### 自定义工作时间
```python
manager.work_start_hour = 9   # 早上9点开始
manager.work_end_hour = 18    # 晚上6点结束
```

### 自定义最小间隔
```python
manager.min_gap_minutes = 15  # 日程之间保留15分钟
```

### 自定义搜索范围
```python
# 在未来30天内寻找合适的时间
result = manager.smart_add_event(
    summary="季度总结会议",
    duration_minutes=120,
    days_to_search=30  # 搜索未来30天
)
```

### 指定首选时间
```python
from datetime import datetime, timedelta

# 希望安排在明天下午2点
preferred_time = datetime.now() + timedelta(days=1)
preferred_time = preferred_time.replace(hour=14, minute=0)

result = manager.smart_add_event(
    summary="产品评审",
    duration_minutes=90,
    preferred_time=preferred_time  # 会尝试找最接近这个时间的空闲段
)
```

## 使用场景示例

### 场景1: 用户说"我明天要开3个会"

```python
# 提取会议信息
events = [
    {"summary": "产品需求评审", "duration_minutes": 60, "description": "讨论Q1产品规划"},
    {"summary": "技术方案讨论", "duration_minutes": 90, "description": "新架构技术方案"},
    {"summary": "每周团队例会", "duration_minutes": 30, "description": "团队周例会"}
]

# 批量智能安排
results = manager.batch_add_events(events)

# 向用户反馈
for result in results:
    if result["success"]:
        time_info = result['result']['chosen_time']
        print(f"✅ {result['summary']} 已安排在 {time_info['start']}")
```

### 场景2: 用户说"帮我找个时间做代码评审"

```python
# 智能安排
result = manager.smart_add_event(
    summary="代码评审",
    duration_minutes=45,
    description="评审新功能代码"
)

# 向用户展示建议
print(f"为您找到以下时间:")
print(f"推荐: {result['chosen_time']['start']} - {result['chosen_time']['end']}")
print(f"\n其他可选时间:")
for i, slot in enumerate(result['alternative_slots'][:3], 1):
    print(f"{i}. {slot['start']} - {slot['end']}")
```

### 场景3: 用户说"查看我明天的日程"

```python
from datetime import datetime, timedelta

# 获取主日历
calendar_id = manager.get_primary_calendar_id()

# 明天的时间范围
tomorrow_start = datetime.now().replace(hour=0, minute=0, second=0) + timedelta(days=1)
tomorrow_end = tomorrow_start + timedelta(days=1)

# 获取日程
events = manager.get_events(
    calendar_id,
    int(tomorrow_start.timestamp()),
    int(tomorrow_end.timestamp())
)

# 展示给用户
print(f"明天您有 {len(events)} 个日程:")
for event in events:
    start_time = datetime.fromtimestamp(int(event['start_time']['timestamp']))
    end_time = datetime.fromtimestamp(int(event['end_time']['timestamp']))
    print(f"- {event['summary']}")
    print(f"  {start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}")
```

## API参考

### FeishuSmartCalendar 类

#### `__init__(app_id, app_secret, domain)`
初始化日历管理器

#### `smart_add_event(summary, duration_minutes, description, location, preferred_time, days_to_search)`
智能添加单个日程
- **summary**: 日程标题
- **duration_minutes**: 持续时间（分钟）
- **description**: 描述（可选）
- **location**: 地点（可选）
- **preferred_time**: 首选时间（可选）
- **days_to_search**: 搜索未来多少天（默认7天）

返回:
```python
{
    "event": {...},  # 飞书返回的日程对象
    "chosen_time": {
        "start": "2026-01-09 10:00:00",
        "end": "2026-01-09 11:00:00"
    },
    "alternative_slots": [...]  # 其他可选时间段
}
```

#### `batch_add_events(events_to_add)`
批量添加日程
- **events_to_add**: 日程列表，每个元素包含 summary, duration_minutes, description, location

返回:
```python
[
    {
        "success": True,
        "summary": "会议名称",
        "result": {...}
    },
    ...
]
```

#### `get_events(calendar_id, start_time, end_time)`
获取指定时间范围内的日程

#### `find_free_slots(events, start_date, end_date, duration_minutes)`
查找空闲时间段

## 常见问题

### Q1: 如何修改工作时间?
```python
manager.work_start_hour = 8   # 早上8点
manager.work_end_hour = 20    # 晚上8点
```

### Q2: 如果没有找到合适的时间怎么办?
系统会抛出异常，建议增加 `days_to_search` 参数:
```python
result = manager.smart_add_event(
    summary="重要会议",
    duration_minutes=120,
    days_to_search=14  # 在未来14天内寻找
)
```

### Q3: 如何跳过周末?
当前版本会包括周末。如果需要跳过周末，可以在调用前检查日期:
```python
from datetime import datetime

def is_weekday(dt):
    return dt.weekday() < 5  # 0-4 是周一到周五

# 可以在 find_free_slots 中添加过滤逻辑
```

### Q4: 如何处理全天事件?
当前版本主要处理有具体时间的事件。全天事件可以设置为工作时间段的整个时间:
```python
result = manager.smart_add_event(
    summary="年度总结",
    duration_minutes=540,  # 9小时 (9:00-18:00)
)
```

## 最佳实践

1. **批量操作**: 如果要添加多个日程，使用 `batch_add_events` 而不是多次调用 `smart_add_event`
2. **时间范围**: 对于重要且可以延后的日程，增加 `days_to_search` 参数
3. **首选时间**: 如果用户提到具体时间偏好，使用 `preferred_time` 参数
4. **用户确认**: 在创建日程前，向用户展示建议的时间并获得确认
5. **错误处理**: 始终捕获异常并向用户提供友好的错误信息

## 更新日志

### v1.0.0 (2026-01-08)
- ✅ 智能日程调度算法
- ✅ 批量日程添加
- ✅ 空闲时间查询
- ✅ 支持首选时间
- ✅ 自动避免时间冲突
- ✅ 工作时间配置
- ✅ 完整的错误处理

## 许可证

MIT License
