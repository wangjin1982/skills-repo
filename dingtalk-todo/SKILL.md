---
name: dingtalk-todo
description: Create personal todo tasks in DingTalk. Use when the user asks to create todo items, tasks, or reminders in DingTalk. Supports both enterprise app API (for real todos) and webhook notification method (instant setup).
---

# DingTalk Todo

Create personal todo tasks in DingTalk with multiple implementation methods.

## Quick Start

### Method 1: Webhook Message (Instant Setup, No Enterprise App)

Send structured todo messages via webhook (simpler, works immediately).

**Setup:**
```bash
export DINGTALK_WEBHOOK_URL="https://oapi.dingtalk.com/robot/send?access_token=YOUR_TOKEN"
export DINGTALK_SECRET="SECYOUR_SECRET_KEY"
```

**Usage:**
```bash
python scripts/create_todo.py --subject "完成项目报告" --description "包含Q4数据分析"
```

### Method 2: Enterprise App (Real Todo, Requires Setup)

Create real todo tasks using DingTalk enterprise app API.

**Prerequisites:**
1. Create DingTalk enterprise internal app
2. Get AppKey and AppSecret
3. Apply for todo permission

**Setup:**
```bash
export DINGTALK_APP_KEY="your_app_key"
export DINGTALK_APP_SECRET="your_app_secret"
export DINGTALK_OPERATOR_ID="your_union_id"
```

**Usage:**
```bash
python scripts/create_todo.py --subject "完成项目报告" --description "包含Q4数据分析"
```

## Auto-fallback

The skill automatically detects available credentials:
- If enterprise app credentials found → Use real todo API
- If webhook credentials found → Use webhook message
- If both available → Prefer enterprise app API

## Getting Enterprise App Credentials

See `references/setup-guide.md` for detailed instructions.

## Usage Examples

### Basic Todo
```bash
python scripts/create_todo.py --subject "编写测试用例"
```

### Todo with Description
```bash
python scripts/create_todo.py --subject "代码审查" --description "审查PR #123的功能实现"
```

## Configuration

### Environment Variables

| Variable | Required | Method | Description |
|----------|----------|--------|-------------|
| DINGTALK_WEBHOOK_URL | Method 1 | Webhook | Group robot webhook URL |
| DINGTALK_SECRET | Method 1 | Webhook | Webhook signature secret |
| DINGTALK_APP_KEY | Method 2 | Enterprise App | App key from DingTalk |
| DINGTALK_APP_SECRET | Method 2 | Enterprise App | App secret from DingTalk |
| DINGTALK_OPERATOR_ID | Method 2 | Enterprise App | Operator's UnionId |
