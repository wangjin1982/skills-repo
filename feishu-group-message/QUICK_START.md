# 飞书群消息通知 Skill - 快速开始

## 5分钟快速上手

### 步骤1：创建通知器（30秒）

```python
from feishu_group_messenger import create_messenger

messenger = create_messenger(
    app_id="your_app_id",
    app_secret="your_app_secret"
)
```

### 步骤2：发送第一条消息（1分钟）

```python
result = messenger.send_task_notification(
    chat_id="oc_your_chat_id",
    task_name="测试任务",
    status="success"
)

if result['success']:
    print("✅ 发送成功！")
```

### 步骤3：发送更丰富的通知（2分钟）

```python
result = messenger.send_rich_task_notification(
    chat_id="oc_your_chat_id",
    task_name="数据导入任务",
    status="success",
    details="成功导入1000条记录",
    metrics={
        "记录数": "1000",
        "耗时": "3.5秒"
    },
    links={
        "查看数据": "https://feishu.cn/base/xxx"
    }
)
```

## 常用代码片段

### 任务完成通知

```python
messenger.send_task_notification(
    chat_id="oc_xxx",
    task_name="任务名称",
    status="success",  # 或 "failed", "warning"
    details="任务详情"
)
```

### 带数据的通知

```python
messenger.send_rich_task_notification(
    chat_id="oc_xxx",
    task_name="数据报告",
    status="success",
    metrics={
        "总记录": "1000",
        "成功": "950",
        "失败": "50"
    },
    links={"查看": "https://..."}
)
```

### 简单文本消息

```python
messenger.send_text(
    chat_id="oc_xxx",
    message="这是一条提醒消息"
)
```

### 错误通知

```python
messenger.send_task_notification(
    chat_id="oc_xxx",
    task_name="任务名称",
    status="failed",
    details="失败原因描述"
)
```

## 完整示例

```python
from feishu_group_messenger import create_messenger

# 1. 创建通知器
messenger = create_messenger(app_id, app_secret)

# 2. 任务开始
messenger.send_text(chat_id, "🔄 开始处理...")

# 3. 执行任务
try:
    result = do_something()

    # 4. 成功通知
    messenger.send_rich_task_notification(
        chat_id=chat_id,
        task_name="我的任务",
        status="success",
        metrics={"处理量": "100"},
        links={"查看": "https://..."}
    )
except Exception as e:
    # 5. 失败通知
    messenger.send_task_notification(
        chat_id=chat_id,
        task_name="我的任务",
        status="failed",
        details=str(e)
    )
```

## 消息状态类型

| 状态 | 图标 | 使用场景 |
|------|------|----------|
| `success` | ✅ | 任务成功完成 |
| `failed` | ❌ | 任务失败 |
| `warning` | ⚠️ | 任务完成但有警告 |

## 获取必要信息

### APP_ID 和 APP_SECRET
1. 登录飞书开放平台 (https://open.feishu.cn)
2. 创建应用或使用现有应用
3. 在应用凭证页面获取

### Chat ID
1. 打开飞书群聊
2. 点击群设置
3. 查看群信息中的群ID

## 配置机器人权限

1. 在飞书开放平台启用"机器人"能力
2. 将机器人添加到群聊
3. 在群设置中授予机器人发送消息权限

## 常见问题速查

**Q: 消息发送失败？**
- 检查机器人是否在群中
- 检查 chat_id 格式（通常以"oc_"开头）
- 检查 APP_ID 和 APP_SECRET

**Q: 如何@某人？**
使用富文本消息的 `at` 标签

**Q: 发送频率限制？**
避免短时间内发送大量消息，建议合并发送

## 完整文档

- `README.md` - 详细使用指南
- `skill.md` - 完整功能文档
- `example.py` - 10个实际使用示例

## 技术支持

遇到问题？查看：
1. 文档中的错误处理部分
2. example.py 中的实际案例
3. feishu_group_messenger.py 中的注释
