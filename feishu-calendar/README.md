# 飞书智能日历管理 Skill

这是一个Claude Code的Skill，用于智能管理飞书日历。

## 快速开始

### 1. 测试基本功能

```bash
cd /home/aiops3/.claude/skills/feishu-calendar/scripts
python3 feishu_calendar_manager.py
```

### 2. 在Claude中使用

当用户说类似以下内容时，Claude会自动调用此Skill：

- "我明天要开会，帮我安排一下"
- "查看我下周的日程"
- "帮我找个时间做代码评审"
- "我有3个会议需要安排"

### 3. 手动调用

你也可以在Python代码中直接使用：

```python
import sys
sys.path.append('/home/aiops3/.claude/skills/feishu-calendar')

from scripts.feishu_calendar_manager import FeishuSmartCalendar
import json

# 加载配置
with open("/home/aiops3/.claude/feishu_config.json", "r") as f:
    config = json.load(f)

# 初始化
manager = FeishuSmartCalendar(
    app_id=config["app_id"],
    app_secret=config["app_secret"],
    domain=config["domain"]
)

# 智能添加日程
result = manager.smart_add_event(
    summary="团队周会",
    duration_minutes=60,
    description="讨论本周工作"
)

print(f"日程已安排在: {result['chosen_time']['start']}")
```

## 主要功能

1. **智能调度**: 自动分析现有日程，找到最合适的空闲时间
2. **批量添加**: 一次性添加多个日程，自动避免冲突
3. **灵活配置**: 支持自定义工作时间、最小间隔等
4. **智能建议**: 提供多个可选时间段供用户选择

## 配置

飞书应用配置存储在: `/home/aiops3/.claude/feishu_config.json`

## 文档

详细文档请查看 [SKILL.md](./SKILL.md)

## 许可证

MIT
