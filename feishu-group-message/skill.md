---
name: feishu-group-message
description: "通过飞书机器人向飞书群组发送通知消息。适用于任务完成后的消息通知机制。支持文本消息、富文本消息、任务通知等多种消息类型。简单易用，专为自动化任务通知设计。"
---

# 飞书群消息通知 Skill

## 概述

本Skill提供了向飞书群组发送通知消息的完整解决方案，特别适用于任务完成后的自动化通知场景。

## 核心功能

### 1. 文本消息
- 发送纯文本消息到飞书群
- 简单直接，适合快速通知

### 2. 富文本消息
- 发送格式化的富文本消息
- 支持标题、加粗、斜体、链接等
- 更美观专业的展示效果

### 3. 任务通知
- 专门为任务完成通知设计
- 自动添加状态图标（✅❌⚠️）
- 支持详细信息、链接、指标等

### 4. 批量通知
- 支持向多个群组发送消息
- 支持多种消息类型组合

## 使用场景

### 场景1：任务完成通知
```python
# 数据处理完成后通知
messenger.send_task_notification(
    chat_id="oc_xxx",
    task_name="数据导入任务",
    status="success",
    details="成功导入 1000 条记录",
    links={"查看数据": "https://feishu.cn/base/xxx"}
)
```

### 场景2：错误报告
```python
# 任务失败时通知
messenger.send_task_notification(
    chat_id="oc_xxx",
    task_name="API请求任务",
    status="failed",
    details="连接超时，请检查网络设置"
)
```

### 场景3：批量报告
```python
# 富文本格式展示详细报告
messenger.send_rich_task_notification(
    chat_id="oc_xxx",
    task_name="每日数据汇总",
    status="success",
    metrics={
        "总记录数": "10,000",
        "新增记录": "500",
        "处理时间": "2.3秒"
    },
    links={
        "查看详情": "https://feishu.cn/base/xxx",
        "下载报告": "https://example.com/report.pdf"
    }
)
```

### 场景4：自定义消息
```python
# 发送自定义文本消息
messenger.send_text(
    chat_id="oc_xxx",
    message="提醒：明天上午10点开始系统维护"
)
```

## 消息类型说明

### 文本消息 (send_text)
最简单的消息类型，适合纯文本通知。

**特点：**
- 简单直接
- 无格式限制
- 适合快速通知

**示例输出：**
```
✅ 数据导入已完成
成功导入 1000 条记录
```

### 富文本消息 (send_post)
格式化消息，支持多种文本样式。

**特点：**
- 支持加粗、斜体
- 支持链接
- 支持多种文本标签
- 更美观专业

**支持标签：**
- `text`: 普通文本
- `a`: 链接
- `at`: @某人
- `img`: 图片
- `emoji`: 表情

### 任务通知 (send_task_notification)
专为任务通知设计的快捷方法。

**状态类型：**
- `success`: ✅ 成功
- `failed`: ❌ 失败
- `warning`: ⚠️ 警告

**自动格式化：**
- 自动添加状态图标
- 自动组织消息结构
- 自动格式化链接

### 富文本任务通知 (send_rich_task_notification)
更美观的任务通知格式。

**额外功能：**
- 支持指标展示（metrics）
- 更丰富的格式化选项
- 适合重要报告

## 快速开始

### 最简单的用法

```python
from feishu_group_messenger import create_messenger

# 创建通知器
messenger = create_messenger(
    app_id="your_app_id",
    app_secret="your_app_secret"
)

# 发送任务完成通知
result = messenger.send_task_notification(
    chat_id="oc_xxx",
    task_name="数据导入",
    status="success"
)

if result['success']:
    print("✅ 消息发送成功")
else:
    print(f"❌ 发送失败: {result['error']}")
```

### 推荐配置

```python
# 创建通知器（可复用）
messenger = create_messenger(
    app_id="cli_a9d176668a38dbc9",
    app_secret="jDB6hdclWymSvK0lXVH0Bd0CgtfCJT6T"
)

# 任务完成后通知
result = messenger.send_rich_task_notification(
    chat_id="oc_1750c0544dad49b14f940312bd78c5c7",
    task_name="飞书多维表格创建",
    status="success",
    details="成功创建 5 个多维表格，包含 27 条记录",
    metrics={
        "表格数量": "5",
        "总记录数": "27",
        "处理时间": "15秒"
    },
    links={
        "全球生物医药动态": "https://feishu.cn/base/xxx",
        "中国生物医药进展": "https://feishu.cn/base/yyy"
    }
)
```

## 配置说明

### 获取群聊ID (chat_id)

**方法1：从群设置中获取**
1. 打开飞书群聊
2. 点击群设置
3. 查看群信息，复制群ID

**方法2：从API获取**
使用飞书开放平台API获取用户的群列表

### 配置应用权限

**必需权限：**
- `im:message` - 发送消息权限
- `im:message:group_at_msg` - 群@消息权限（可选）

**配置步骤：**
1. 登录飞书开放平台
2. 创建应用或使用现有应用
3. 启用"机器人"能力
4. 获取 APP_ID 和 APP_SECRET
5. 添加应用到群聊
6. 在群设置中授予机器人发送消息权限

## 返回值说明

所有发送方法返回统一的格式：

```python
{
    "success": True,           # 是否成功
    "message_id": "om_xxx",    # 消息ID（成功时）
    "error": None              # 错误信息（失败时）
}
```

## 错误处理

### 常见错误

**1. 权限不足**
```
Code 99991663: app not in chat
```
解决：将机器人添加到群聊

**2. 令牌无效**
```
Code 99991668: invalid token
```
解决：检查 APP_ID 和 APP_SECRET

**3. 群ID错误**
```
Code 7003: invalid chat id
```
解决：确认 chat_id 格式正确

### 错误处理最佳实践

```python
result = messenger.send_task_notification(
    chat_id="oc_xxx",
    task_name="测试任务",
    status="success"
)

if result['success']:
    print(f"✅ 消息已发送: {result['message_id']}")
else:
    print(f"❌ 发送失败: {result['error']}")
    # 可以根据错误类型进行重试或其他处理
```

## 最佳实践

### 1. 复用通知器实例
```python
# ✅ 推荐：创建一次，多次使用
messenger = create_messenger(app_id, app_secret)
messenger.send_text(chat_id, "消息1")
messenger.send_text(chat_id, "消息2")
```

### 2. 使用任务通知方法
```python
# ✅ 推荐：使用专门的方法
messenger.send_task_notification(
    chat_id,
    task_name="任务名称",
    status="success",
    details="详细信息"
)
```

### 3. 提供详细信息
```python
# ✅ 推荐：包含有用的上下文信息
messenger.send_rich_task_notification(
    chat_id,
    task_name="数据导入",
    status="success",
    details="成功从CSV导入数据",
    metrics={"记录数": "1000", "耗时": "5秒"},
    links={"查看数据": "https://..."}
)
```

### 4. 错误处理
```python
# ✅ 推荐：总是检查返回结果
result = messenger.send_text(chat_id, message)
if not result['success']:
    print(f"发送失败: {result['error']}")
    # 记录日志或重试
```

## API 参考

### FeishuGroupMessenger

#### 初始化
```python
messenger = FeishuGroupMessenger(
    app_id: str,           # 飞书应用ID
    app_secret: str,       # 飞书应用密钥
    domain: str = "https://open.feishu.cn"  # API域名
)
```

#### 方法

##### `send_text(chat_id: str, message: str) -> Dict`
发送文本消息

**参数:**
- `chat_id`: 群聊ID
- `message`: 消息内容

**返回:** 发送结果字典

##### `send_post(chat_id: str, title: str, content: List[Dict]) -> Dict`
发送富文本消息

**参数:**
- `chat_id`: 群聊ID
- `title`: 消息标题
- `content`: 内容列表

**返回:** 发送结果字典

##### `send_task_notification(chat_id, task_name, status, details, links) -> Dict`
发送任务完成通知

**参数:**
- `chat_id`: 群聊ID
- `task_name`: 任务名称
- `status`: 任务状态 ("success", "failed", "warning")
- `details`: 详细信息（可选）
- `links`: 相关链接字典（可选）

**返回:** 发送结果字典

##### `send_rich_task_notification(chat_id, task_name, status, details, links, metrics) -> Dict`
发送富文本任务完成通知

**参数:**
- `chat_id`: 群聊ID
- `task_name`: 任务名称
- `status`: 任务状态
- `details`: 详细信息（可选）
- `links`: 相关链接字典（可选）
- `metrics`: 指标字典（可选）

**返回:** 发送结果字典

## 限制和注意事项

1. **频率限制**：飞书API有调用频率限制，避免短时间内大量发送
2. **消息长度**：单条消息有长度限制，超长消息会被截断
3. **权限要求**：机器人必须被添加到群聊中才能发送消息
4. **群聊ID格式**：chat_id格式必须正确，通常以"oc_"开头

## 示例

### 示例1：数据处理任务通知
```python
# 完整的数据处理通知流程
messenger = create_messenger(app_id, app_secret)

# 任务开始
messenger.send_text(chat_id, "🔄 开始处理数据...")

# 处理数据...
# process_data()

# 任务完成
messenger.send_rich_task_notification(
    chat_id=chat_id,
    task_name="数据处理任务",
    status="success",
    details="成功处理CSV文件",
    metrics={
        "输入文件": "data.csv",
        "记录数": "1000",
        "耗时": "3.5秒"
    },
    links={
        "查看结果": "https://feishu.cn/base/xxx"
    }
)
```

### 示例2：错误处理和重试
```python
import time

def send_with_retry(messenger, chat_id, message, max_retries=3):
    """带重试的消息发送"""
    for attempt in range(max_retries):
        result = messenger.send_text(chat_id, message)

        if result['success']:
            return True

        if attempt < max_retries - 1:
            print(f"发送失败，{2**attempt}秒后重试...")
            time.sleep(2**attempt)

    return False

# 使用
success = send_with_retry(messenger, chat_id, "重要通知")
```

### 示例3：批量通知多个群
```python
# 向多个群发送通知
chat_ids = [
    "oc_xxx1",
    "oc_xxx2",
    "oc_xxx3"
]

for chat_id in chat_ids:
    result = messenger.send_task_notification(
        chat_id=chat_id,
        task_name="系统维护通知",
        status="warning",
        details="今晚10点进行系统维护，预计持续2小时"
    )
    print(f"群 {chat_id}: {'✅' if result['success'] else '❌'}")
```

## 与其他Skill配合使用

本Skill特别适合与其他Skill配合使用，作为任务完成的通知机制：

### 与feishu-bitable配合
```python
from feishu_bitable_manager import create_manager
from feishu_group_messenger import create_messenger

# 创建管理器和通知器
bitable_manager = create_manager(app_id, app_secret)
messenger = create_messenger(app_id, app_secret)

# 导入数据到多维表格
result = bitable_manager.import_csv_to_bitable("data.csv", "我的数据")

# 发送通知
if result['success']:
    messenger.send_rich_task_notification(
        chat_id="oc_xxx",
        task_name="数据导入到飞书多维表格",
        status="success",
        details=f"成功导入 {result['written']} 条记录",
        metrics={
            "写入记录": str(result['written']),
            "验证记录": str(result['verified']),
            "清理空记录": str(result['cleanup']['empty'])
        },
        links={"查看数据": result['url']}
    )
```

### 与数据处理流程配合
```python
def process_and_notify(csv_file, table_name, chat_id):
    """处理数据并发送通知的完整流程"""
    messenger = create_messenger(app_id, app_secret)

    try:
        # 发送开始通知
        messenger.send_text(chat_id, f"🔄 开始处理: {table_name}")

        # 处理数据
        result = bitable_manager.import_csv_to_bitable(csv_file, table_name)

        # 发送完成通知
        if result['success']:
            messenger.send_rich_task_notification(
                chat_id=chat_id,
                task_name=table_name,
                status="success",
                metrics={
                    "记录数": str(result['written']),
                    "验证数": str(result['verified'])
                },
                links={"查看": result['url']}
            )
        else:
            messenger.send_task_notification(
                chat_id=chat_id,
                task_name=table_name,
                status="failed",
                details=result.get('error', '未知错误')
            )

    except Exception as e:
        messenger.send_task_notification(
            chat_id=chat_id,
            task_name=table_name,
            status="failed",
            details=str(e)
        )
```

## 总结

本Skill提供了一个简单而强大的飞书群消息通知解决方案，特别适合作为自动化任务的通知机制。

**优势：**
- ✅ 简单易用，API直观
- ✅ 支持多种消息类型
- ✅ 专为任务通知设计
- ✅ 良好的错误处理
- ✅ 可与其他Skill配合

**适用性：**
- 任务完成通知
- 批量任务报告
- 错误告警
- 进度更新
- 系统监控
