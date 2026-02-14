---
name: dingtalk-group-message
description: Send text messages to DingTalk groups via webhook robots. Use when the user asks to send notifications to DingTalk, mentions "钉钉消息" (DingTalk message), "通知钉钉群" (notify DingTalk group), or "钉钉提醒" (DingTalk reminder). This skill sends task completion notifications, alerts, or any text messages to DingTalk groups using signed webhook authentication.
---

# DingTalk Group Message

Send text messages to DingTalk groups via webhook robots with signature authentication.

## Quick Start

To send a message, you need:

1. **DingTalk Webhook URL** - Get from your group robot settings
2. **Secret Key** - Get from your group robot security settings

Set environment variables:
```bash
export DINGTALK_WEBHOOK_URL="https://oapi.dingtalk.com/robot/send?access_token=YOUR_TOKEN"
export DINGTALK_SECRET="SECYOUR_SECRET_KEY"
```

Send a message:
```bash
python scripts/send_message.py "任务完成：数据导出成功"
```

## Usage Patterns

### Task Completion Notification

When a task completes, notify the DingTalk group:
```bash
python scripts/send_message.py "[完成] 数据处理任务\n文件已保存到 output 文件夹"
```

### Simple Reminder

Send a quick reminder:
```bash
python scripts/send_message.py "会议将在10分钟后开始"
```

### Multi-line Message

Use `\n` for line breaks:
```bash
python scripts/send_message.py "任务报告\n\n状态：已完成\n耗时：5分钟\n文件：3个"
```

## Getting Webhook Credentials

1. Open DingTalk group settings
2. Add "Group Robot" (群机器人)
3. Select "Custom" robot
4. Copy Webhook URL
5. Enable "Signature" security (加签)
6. Copy the Secret key

## Script Parameters

The `scripts/send_message.py` script accepts:

- **Positional argument**: Message content (required)
- **Environment variable `DINGTALK_WEBHOOK_URL`**: Webhook URL
- **Environment variable `DINGTALK_SECRET`**: Signature secret key

## Structured Task Notification (New!)

Send structured task notifications with task name, status, and details:

```bash
# Task completed successfully
python scripts/send_task_notification.py --task "数据导出" --status "success" --message "已导出1000条记录" --duration "5分钟"

# Task failed
python scripts/send_task_notification.py --task "数据处理" --status "failure" --message "数据库连接超时" --duration "30秒"

# Task in progress
python scripts/send_task_notification.py --task "备份任务" --status "progress" --message "正在压缩文件" --extra "进度: 50%"

# With extra information
python scripts/send_task_notification.py --task "文件上传" --status "success" --message "上传完成" --duration "2分钟" --extra "文件: report.csv"
```

**Message format preview:**
```
✅ 任务通知

📌 任务名称：数据导出
📊 状态：成功

📝 详情：已导出1000条记录
⏱️ 耗时：5分钟

🕒 时间：2026-01-21 14:30:25
```

**Available status types:**
- `success` ✅ - 任务成功完成
- `failure` ❌ - 任务失败
- `error` ⚠️ - 任务错误
- `warning` ⚡ - 警告信息
- `progress` 🔄 - 任务进行中
- `pending` ⏳ - 等待处理
- `info` ℹ️ - 一般信息

## Response

- Success: Returns exit code 0 with `✓ 消息发送成功`
- Failure: Returns exit code 1 with error message
