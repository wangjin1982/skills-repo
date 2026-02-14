# 飞书文档 Skill - 快速使用指南

## 📋 Skill位置

```
/home/aiops/.claude/skills/feishu-docs/
```

## 🎯 核心功能

这个Skill提供了完整的飞书文档操作能力：

1. ✅ **创建文档** - 创建新的飞书文档
2. ✅ **添加内容** - 从Markdown导入或手动添加内容
3. ✅ **搜索文档** - 根据关键词搜索文档
4. ✅ **批量操作** - 批量创建多个文档

## 🚀 快速开始

### 方法1: 在Python代码中使用

```python
import sys
sys.path.append('/home/aiops/.claude/skills/feishu-docs/scripts')

from feishu_api import FeishuDocClient

# 初始化客户端
client = FeishuDocClient(
    app_id="cli_a9d176668a38dbc9",  # 替换为你的App ID
    app_secret="jDB6hdclWymSvK0lXVH0Bd0CgtfCJT6T"  # 替换为你的App Secret
)

# 创建文档
doc_id = client.create_document("我的文档")

# 添加内容
blocks = [
    {"block_type": 1, "heading1": {"elements": [{"text_run": {"content": "标题"}}]}},
    {"block_type": 2, "text": {"elements": [{"text_run": {"content": "内容"}}]}}
]
client.add_blocks(doc_id, blocks)

# 获取链接
url = client.get_document_url(doc_id)
print(f"文档链接: {url}")
```

### 方法2: 使用命令行工具

```bash
cd /home/aiops/.claude/skills/feishu-docs

# 从Markdown创建文档
python scripts/create_from_markdown.py \
  --app-id "cli_a9d176668a38dbc9" \
  --app-secret "jDB6hdclWymSvK0lXVH0Bd0CgtfCJT6T" \
  --title "文档标题" \
  --markdown-file "content.md"

# 搜索文档
python scripts/search_docs.py \
  --app-id "cli_a9d176668a38dbc9" \
  --app-secret "jDB6hdclWymSvK0lXVH0Bd0CgtfCJT6T" \
  "搜索关键词"
```

### 方法3: 在Claude Code中使用

直接告诉Claude Code：

```
请帮我创建一个飞书文档，标题是"项目计划"，内容在 /path/to/plan.md
```

Claude Code会自动调用feishu-docs Skill完成任务。

## 📚 重要概念

### 块类型（Block Types）

飞书文档由"块"组成，每个块有一个类型：

| 块类型 | block_type | 说明 | Markdown对应 |
|--------|-----------|------|--------------|
| 一级标题 | 1 | heading1 | `# 标题` |
| 二级标题 | 2 | heading2 | `## 标题` |
| 三级标题 | 3 | heading3 | `### 标题` |
| 文本段落 | 2 | text | 普通文本 |

**注意**: 二级标题(heading2)和文本(text)都使用 `block_type: 2`，区别在于使用的字段名。

### 正确的块格式

```python
# ✅ 正确 - 文本段落
{
    "block_type": 2,
    "text": {
        "elements": [
            {"text_run": {"content": "这是文本"}}
        ]
    }
}

# ✅ 正确 - 一级标题
{
    "block_type": 1,
    "heading1": {
        "elements": [
            {"text_run": {"content": "这是标题"}}
        ]
    }
}

# ✅ 正确 - 二级标题
{
    "block_type": 2,
    "heading2": {
        "elements": [
            {"text_run": {"content": "这是二级标题"}}
        ]
    }
}
```

## 💡 使用场景

### 场景1: 从现有文档创建飞书文档

```python
client = FeishuDocClient(app_id="...", app_secret="...")
doc_id = client.create_document("技术文档")
client.add_content_from_markdown(doc_id, "technical_doc.md")
print(f"创建成功: {client.get_document_url(doc_id)}")
```

### 场景2: 批量创建文档

创建一个文本文件 `batch.txt`：
```
项目文档1|/path/to/doc1.md
项目文档2|/path/to/doc2.md
会议记录|/path/to/meeting.md
```

运行批量创建：
```bash
python scripts/create_from_markdown.py \
  --app-id "xxx" \
  --app-secret "yyy" \
  --batch batch.txt
```

### 场景3: 搜索和管理文档

```python
client = FeishuDocClient(app_id="...", app_secret="...")

# 搜索文档
results = client.search_documents("项目")
for doc in results:
    print(f"{doc['title']}: {doc['document_id']}")

# 获取文档信息
doc_id = "xxx"
info = client.get_document_info(doc_id)
print(f"标题: {info['title']}")
```

## ⚠️ 常见问题

### Q1: "创建文档失败" 或 "block not support to create"

**原因**: 缺少 `docx:document:update` 权限

**解决**:
1. 访问 https://open.feishu.cn
2. 找到你的应用
3. 添加权限: `docx:document:update`
4. 保存并重新发布
5. 等待5-10分钟

### Q2: "invalid param" 错误

**原因**: 块格式不正确

**解决**: 检查以下几点
- `block_type` 必须是数字（1, 2, 3）
- 文本段落使用 `block_type: 2` + `text` 字段
- 标题使用对应的字段（`heading1`, `heading2`, `heading3`）
- `elements` 必须是数组

### Q3: API频率限制（429错误）

**原因**: 请求太频繁

**解决**:
- 添加延迟: `time.sleep(0.5)`
- 减小批次大小
- 使用批量API

## 🧪 测试Skill

运行快速测试：

```bash
cd /home/aiops/.claude/skills/feishu-docs
python quick_test.py
```

这会：
1. ✅ 测试客户端初始化
2. ✅ 测试创建文档
3. ✅ 测试添加内容
4. ✅ 测试获取链接

## 📖 学习资源

1. **README.md** - 完整的功能说明
2. **SKILL.md** - 详细的Skill文档
3. **examples.py** - 7个使用示例
4. **scripts/feishu_api.py** - API客户端源码

## 🎓 示例代码速查

```python
# 初始化
from feishu_api import FeishuDocClient
client = FeishuDocClient(app_id="...", app_secret="...")

# 创建文档
doc_id = client.create_document("标题")

# 添加单个块
client.add_blocks(doc_id, [{
    "block_type": 2,
    "text": {"elements": [{"text_run": {"content": "内容"}}]}
}])

# 从Markdown添加
success, fail = client.add_content_from_markdown(
    doc_id, "file.md", batch_size=20, delay=0.2
)

# 搜索文档
results = client.search_documents("关键词")

# 获取信息
info = client.get_document_info(doc_id)
blocks = client.get_document_blocks(doc_id)

# 获取链接
url = client.get_document_url(doc_id)
```

## ✨ 最佳实践

1. **使用配置文件** - 避免硬编码凭证
2. **批量处理** - 大文档分批添加（20-50块/批）
3. **错误处理** - 捕获并记录异常
4. **延迟控制** - 批次间添加0.2-0.5秒延迟
5. **权限检查** - 确保有所有必需权限

## 🔗 相关链接

- 飞书开放平台: https://open.feishu.cn
- 飞书文档API: https://open.feishu.cn/document/server-docs/docs/docs/docx-v1/docx-overview
- Skill目录: `/home/aiops/.claude/skills/feishu-docs/`

---

**创建时间**: 2026-01-01
**版本**: 1.0.0
**作者**: Claude Code AI Assistant
