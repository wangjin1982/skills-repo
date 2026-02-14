# 飞书群消息通知 Skill - 使用指南

## 概述

本Skill提供了向飞书群组发送通知消息的完整解决方案。特别适合用于任务完成后的自动化通知。

## 快速开始

### 安装和配置

```python
from feishu_group_messenger import create_messenger

# 创建通知器实例
messenger = create_messenger(
    app_id="your_app_id",
    app_secret="your_app_secret"
)
```

### 发送第一条消息

```python
# 发送简单的任务完成通知
result = messenger.send_task_notification(
    chat_id="oc_your_chat_id",
    task_name="测试任务",
    status="success"
)

if result['success']:
    print("✅ 消息发送成功")
else:
    print(f"❌ 发送失败: {result['error']}")
```

## 核心API

### 1. send_text - 发送文本消息

最简单的消息发送方式。

```python
result = messenger.send_text(
    chat_id="oc_xxx",
    message="这是一条测试消息"
)
```

**使用场景：**
- 简单提醒
- 快速通知
- 状态更新

### 2. send_task_notification - 发送任务通知

专为任务完成设计的通知方法（推荐使用）。

```python
result = messenger.send_task_notification(
    chat_id="oc_xxx",
    task_name="数据导入任务",
    status="success",              # "success", "failed", "warning"
    details="成功导入 1000 条记录",  # 可选
    links={                         # 可选
        "查看数据": "https://feishu.cn/base/xxx"
    }
)
```

**自动添加的状态图标：**
- `success` → ✅
- `failed` → ❌
- `warning` → ⚠️

### 3. send_rich_task_notification - 发送富文本任务通知

更美观的任务通知，支持指标展示。

```python
result = messenger.send_rich_task_notification(
    chat_id="oc_xxx",
    task_name="数据处理任务",
    status="success",
    details="成功从CSV导入并清洗数据",
    metrics={                        # 可选
        "总记录数": "1000",
        "有效记录": "950",
        "处理时间": "3.5秒"
    },
    links={                          # 可选
        "查看数据": "https://feishu.cn/base/xxx",
        "下载报告": "https://example.com/report.pdf"
    }
)
```

**消息格式示例：**
```
✅ 数据处理任务 - 已完成

📋 详情: 成功从CSV导入并清洗数据

📊 数据统计:
• 总记录数: 1000
• 有效记录: 950
• 处理时间: 3.5秒

🔗 相关链接:
• 查看数据
• 下载报告
```

### 4. send_post - 发送富文本消息

完全自定义的富文本消息。

```python
content = [
    {"tag": "text", "text": "重要通知：", "style": ["bold"]},
    {"tag": "text", "text": "\n\n"},
    {"tag": "text", "text": "系统将于今晚"},
    {"tag": "text", "text": "10点", "style": ["bold", "italic"]},
    {"tag": "text", "text": "进行维护\n\n"},
    {"tag": "a", "text": "查看详情", "href": "https://example.com"}
]

result = messenger.send_post(
    chat_id="oc_xxx",
    title="系统维护通知",
    content=content
)
```

## 实用示例

### 示例1：数据处理流程通知

```python
def process_data_with_notification(csv_file, table_name, chat_id):
    """处理数据并发送通知"""

    # 任务开始
    messenger.send_text(chat_id, f"🔄 开始处理: {table_name}")

    try:
        # 处理数据
        result = bitable_manager.import_csv_to_bitable(csv_file, table_name)

        if result['success']:
            # 成功通知
            messenger.send_rich_task_notification(
                chat_id=chat_id,
                task_name=table_name,
                status="success",
                metrics={
                    "写入": str(result['written']),
                    "验证": str(result['verified']),
                    "清理空记录": str(result['cleanup']['empty'])
                },
                links={"查看": result['url']}
            )
        else:
            # 失败通知
            messenger.send_task_notification(
                chat_id=chat_id,
                task_name=table_name,
                status="failed",
                details=result.get('error')
            )

    except Exception as e:
        # 异常通知
        messenger.send_task_notification(
            chat_id=chat_id,
            task_name=table_name,
            status="failed",
            details=str(e)
        )
```

### 示例2：批量任务通知

```python
def batch_task_notification(chat_id, tasks):
    """批量任务完成通知"""

    success_count = 0
    failed_tasks = []

    for task_name, task_result in tasks:
        if task_result['success']:
            success_count += 1
        else:
            failed_tasks.append(task_name)

    # 发送汇总报告
    messenger.send_rich_task_notification(
        chat_id=chat_id,
        task_name="批量任务执行",
        status="success" if not failed_tasks else "warning",
        metrics={
            "总任务数": str(len(tasks)),
            "成功": str(success_count),
            "失败": str(len(failed_tasks))
        },
        details=f"失败任务: {', '.join(failed_tasks)}" if failed_tasks else None
    )
```

### 示例3：定时任务报告

```python
def daily_report_notification(chat_id, stats):
    """每日统计报告"""

    messenger.send_rich_task_notification(
        chat_id=chat_id,
        task_name=f"每日数据报告 - {stats['date']}",
        status="success",
        details="今日数据处理完成",
        metrics={
            "新增用户": str(stats['new_users']),
            "活跃用户": str(stats['active_users']),
            "数据处理量": str(stats['data_processed']),
            "API调用次数": str(stats['api_calls'])
        },
        links={
            "详细报告": stats['report_url'],
            "数据看板": stats['dashboard_url']
        }
    )
```

### 示例4：错误告警

```python
def error_alert(chat_id, error_info):
    """发送错误告警"""

    messenger.send_task_notification(
        chat_id=chat_id,
        task_name=f"错误告警 - {error_info['module']}",
        status="failed",
        details=error_info['message'],
        links={
            "查看日志": error_info['log_url'],
            "错误追踪": error_info['trace_url']
        }
    )
```

### 示例5：进度更新

```python
def progress_update(chat_id, current, total, task_name):
    """发送进度更新"""

    percentage = (current / total) * 100

    messenger.send_text(
        chat_id=chat_id,
        message=f"📊 {task_name} 进度: {current}/{total} ({percentage:.1f}%)"
    )
```

## 返回值处理

所有发送方法都返回统一格式的字典：

```python
{
    "success": True,           # bool: 是否成功
    "message_id": "om_xxx",    # str: 消息ID（成功时）
    "error": None              # str: 错误信息（失败时）
}
```

### 推荐的错误处理模式

```python
result = messenger.send_task_notification(
    chat_id="oc_xxx",
    task_name="测试任务",
    status="success"
)

if result['success']:
    print(f"✅ 消息已发送: {result['message_id']}")
    # 可以记录消息ID用于后续追踪
else:
    print(f"❌ 发送失败: {result['error']}")
    # 可以根据错误类型进行重试或其他处理
    # 例如记录到日志、发送备用通知等
```

## 与其他Skill配合

### 配合 feishu-bitable Skill

```python
from feishu_bitable_manager import create_manager
from feishu_group_messenger import create_messenger

# 创建实例
bitable = create_manager(app_id, app_secret)
messenger = create_messenger(app_id, app_secret)

# 导入数据并通知
csv_files = [
    ("data1.csv", "表格1"),
    ("data2.csv", "表格2"),
    ("data3.csv", "表格3")
]

results = []
for csv_file, table_name in csv_files:
    result = bitable.import_csv_to_bitable(csv_file, table_name)
    results.append((table_name, result))

# 发送汇总通知
success_count = sum(1 for _, r in results if r['success'])

messenger.send_rich_task_notification(
    chat_id="oc_xxx",
    task_name="批量导入多维表格",
    status="success" if success_count == len(results) else "warning",
    metrics={
        "总数": str(len(results)),
        "成功": str(success_count)
    },
    links={
        r[0]: r[1]['url']
        for r in results
        if r[1]['success']
    }
)
```

### 配合数据处理任务

```python
def data_pipeline_with_notification(chat_id):
    """完整的数据处理流程"""

    messenger = create_messenger(app_id, app_secret)

    # 阶段1：数据收集
    messenger.send_text(chat_id, "🔄 阶段1/3: 收集数据...")
    # collect_data()

    # 阶段2：数据处理
    messenger.send_text(chat_id, "🔄 阶段2/3: 处理数据...")
    # process_data()

    # 阶段3：数据导入
    messenger.send_text(chat_id, "🔄 阶段3/3: 导入数据...")
    result = bitable.import_csv_to_bitable("data.csv", "数据表")

    # 最终通知
    if result['success']:
        messenger.send_rich_task_notification(
            chat_id=chat_id,
            task_name="数据处理流程",
            status="success",
            details="所有阶段完成",
            links={"查看结果": result['url']}
        )
```

## 常见问题

### Q: 如何获取群聊ID (chat_id)？

**方法1：从群设置获取**
1. 打开飞书群聊
2. 点击右上角"..."
3. 查看群信息，复制群ID

**方法2：从消息链接获取**
群消息链接中包含chat_id，格式通常为：`https://feishu.cn/cinema/chat_id`

### Q: 消息发送失败怎么办？

**检查清单：**
1. ✅ 机器人是否已添加到群聊
2. ✅ APP_ID 和 APP_SECRET 是否正确
3. ✅ chat_id 格式是否正确（通常以"oc_"开头）
4. ✅ 机器人是否有发送消息权限

**常见错误：**
- `Code 99991663`: 机器人不在群中 → 将机器人添加到群
- `Code 99991668`: 令牌无效 → 检查凭证
- `Code 7003`: chat_id无效 → 确认ID格式

### Q: 有发送频率限制吗？

是的，飞书API有频率限制。建议：
- 避免在短时间内发送大量消息
- 批量消息考虑合并发送
- 使用适当的时间间隔

### Q: 支持@人吗？

支持，可以使用富文本消息的 `at` 标签：

```python
content = [
    {"tag": "at", "text": "@张三", "user_id": "ou_xxx"},
    {"tag": "text", "text": " 请查看上述消息"}
]

messenger.send_post(chat_id, "消息标题", [content])
```

### Q: 可以发送图片吗？

可以，使用富文本消息的 `img` 标签：

```python
content = [
    {"tag": "img", "image_key": "img_xxx"},
    {"tag": "text", "text": "\n图片说明"}
]

messenger.send_post(chat_id, "图片消息", [content])
```

### Q: 消息长度有限制吗？

是的，单条消息有长度限制。建议：
- 文本消息不超过2000字符
- 富文本消息内容适度
- 超长内容考虑拆分或使用链接

## 最佳实践

### 1. 复用实例

```python
# ✅ 推荐：创建一次，多次使用
messenger = create_messenger(app_id, app_secret)

for task in tasks:
    messenger.send_task_notification(chat_id, task['name'], task['status'])
```

### 2. 提供有用的上下文

```python
# ✅ 推荐：包含详细信息
messenger.send_rich_task_notification(
    chat_id,
    task_name="数据导入",
    status="success",
    details="成功从CSV导入",
    metrics={"记录数": "1000", "耗时": "5秒"},
    links={"查看": url}
)
```

### 3. 适当的错误处理

```python
# ✅ 推荐：检查返回值
result = messenger.send_text(chat_id, message)
if not result['success']:
    # 记录日志
    logger.error(f"消息发送失败: {result['error']}")
    # 尝试备用通知方式
    send_backup_notification(message)
```

### 4. 合理使用消息类型

```python
# 简单通知 → send_text
messenger.send_text(chat_id, "任务开始")

# 任务完成 → send_task_notification
messenger.send_task_notification(chat_id, "任务名", "success")

# 详细报告 → send_rich_task_notification
messenger.send_rich_task_notification(
    chat_id, "报告", "success",
    metrics={...}, links={...}
)
```

### 5. 批量操作时合并消息

```python
# ❌ 不推荐：发送多条消息
for item in items:
    messenger.send_text(chat_id, f"处理: {item}")

# ✅ 推荐：合并成一条消息
summary = "\n".join([f"• {item}" for item in items])
messenger.send_text(chat_id, f"批量处理完成:\n{summary}")
```

## 进阶技巧

### 1. 消息模板

```python
def create_notification_template(task_name, status, **kwargs):
    """创建标准化的通知模板"""

    base = {
        "chat_id": kwargs.get('chat_id'),
        "task_name": task_name,
        "status": status
    }

    if status == "success":
        base.update({
            "details": kwargs.get('details'),
            "metrics": kwargs.get('metrics'),
            "links": kwargs.get('links')
        })
    else:
        base.update({
            "details": kwargs.get('error_details')
        })

    return base

# 使用
template = create_notification_template(
    "数据导入",
    "success",
    chat_id="oc_xxx",
    details="完成",
    metrics={"记录数": "100"},
    links={"查看": "https://..."}
)

messenger.send_task_notification(**template)
```

### 2. 重试机制

```python
def send_with_retry(messenger, method, max_retries=3, **kwargs):
    """带重试的消息发送"""

    for attempt in range(max_retries):
        result = method(**kwargs)

        if result['success']:
            return result

        if attempt < max_retries - 1:
            wait_time = 2 ** attempt  # 指数退避
            print(f"发送失败，{wait_time}秒后重试...")
            time.sleep(wait_time)

    return result

# 使用
send_with_retry(
    messenger,
    messenger.send_task_notification,
    chat_id="oc_xxx",
    task_name="重要通知",
    status="success"
)
```

### 3. 消息队列

```python
class MessageQueue:
    """简单的消息队列"""

    def __init__(self, messenger):
        self.messenger = messenger
        self.queue = []

    def add(self, method, **kwargs):
        """添加消息到队列"""
        self.queue.append((method, kwargs))

    def send_all(self):
        """发送所有消息"""
        results = []
        for method, kwargs in self.queue:
            result = method(**kwargs)
            results.append(result)
        self.queue.clear()
        return results

# 使用
mq = MessageQueue(messenger)
mq.add(messenger.send_text, chat_id="oc_xxx", message="消息1")
mq.add(messenger.send_text, chat_id="oc_xxx", message="消息2")
results = mq.send_all()
```

## 技术支持

如有问题，请参考：
- `skill.md`：完整的Skill文档
- `feishu_group_messenger.py`：源代码和注释
- `example.py`：完整的使用示例
