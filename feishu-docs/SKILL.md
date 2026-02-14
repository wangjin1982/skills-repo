---
name: feishu-docs
description: "飞书文档创建、编辑和管理工具。支持创建文档、添加内容、搜索文档、编辑文档块等操作。当用户需要创建飞书文档、编辑飞书文档、或在飞书文档中添加内容时使用此Skill。"
license: MIT
---

# 飞书文档操作 Skill (Feishu Docs Management)

## 概述

这个Skill提供了完整的飞书文档操作能力，包括创建文档、添加内容、搜索文档、编辑文档等功能。基于飞书开放平台API，支持应用级权限和用户级权限两种认证方式。

## 前置要求

### 1. 飞书应用配置

在使用此Skill之前，需要先在飞书开放平台创建应用并配置权限：

1. 访问 [飞书开放平台](https://open.feishu.cn)
2. 创建企业自建应用
3. 配置以下权限：
   - `docx:document` - 文档基础权限
   - `docx:document:create` - 创建文档
   - `docx:document:update` - 更新文档内容（必需！）
   - `docx:document:readonly` - 查看文档
   - `drive:drive` - 云文档权限

4. 获取并记录：
   - App ID
   - App Secret

### 2. 环境要求

- Python 3.6+
- requests 库

安装依赖：
```bash
pip install requests
```

## 核心功能

### 1. 创建文档并添加内容

这是最常用的功能，可以从Markdown文件创建飞书文档。

**工作流程：**

1. 准备Markdown格式的内容文件
2. 使用Python脚本创建文档并添加内容
3. 获取文档分享链接

**关键参数说明：**

- `block_type` - 飞书文档块类型（数字代码）：
  - `1` - 一级标题 (heading1)
  - `2` - 二级标题 (heading2) 或 文本段落 (text)
  - `3` - 三级标题 (heading3)
  - `13` - 文本段落

**正确的API格式：**

```python
# 文本段落
{
    "block_type": 2,  # 使用2作为文本段落
    "text": {
        "elements": [
            {"text_run": {"content": "文本内容"}}
        ]
    }
}

# 一级标题
{
    "block_type": 1,
    "heading1": {
        "elements": [
            {"text_run": {"content": "标题内容"}}
        ]
    }
}

# 二级标题
{
    "block_type": 2,  # 注意：heading2也是用2
    "heading2": {
        "elements": [
            {"text_run": {"content": "二级标题"}}
        ]
    }
}
```

### 2. 搜索文档

根据标题搜索飞书文档。

### 3. 编辑文档

更新现有文档的内容块。

## 使用指南

### 场景1：从Markdown创建飞书文档

**步骤：**

1. 确保已配置飞书应用凭证
2. 使用提供的Python脚本

```bash
cd ~/.claude/skills/feishu-docs
python scripts/create_from_markdown.py \
  --app-id "your_app_id" \
  --app-secret "your_app_secret" \
  --title "文档标题" \
  --markdown-file "path/to/content.md"
```

**示例代码（在Python中）：**

```python
import sys
sys.path.append('/home/aiops/.claude/skills/feishu-docs')

from scripts.feishu_api import FeishuDocClient

# 初始化客户端
client = FeishuDocClient(
    app_id="cli_a9d176668a38dbc9",
    app_secret="jDB6hdclWymSvK0lXVH0Bd0CgtfCJT6T"
)

# 创建文档并添加内容
doc_id = client.create_document("我的文档标题")
client.add_content_from_markdown(doc_id, "path/to/content.md")

# 获取文档链接
print(f"文档链接: https://feishu.cn/docx/{doc_id}")
```

### 场景2：批量创建文档

```python
from scripts.feishu_api import FeishuDocClient

client = FeishuDocClient(app_id="...", app_secret="...")

# 批量创建
documents = [
    ("文档1", "/path/to/doc1.md"),
    ("文档2", "/path/to/doc2.md"),
    ("文档3", "/path/to/doc3.md"),
]

for title, md_file in documents:
    doc_id = client.create_document(title)
    client.add_content_from_markdown(doc_id, md_file)
    print(f"创建完成: {title} - https://feishu.cn/docx/{doc_id}")
```

### 场景3：搜索并更新文档

```python
from scripts.feishu_api import FeishuDocClient

client = FeishuDocClient(app_id="...", app_secret="...")

# 搜索文档
docs = client.search_documents("关键词")
for doc in docs:
    print(f"找到: {doc['title']} - {doc['document_id']}")

# 更新文档内容
doc_id = "xxx"
client.update_text_block(doc_id, block_id, "新内容")
```

## 重要提示

### 权限问题

如果遇到 "block not support to create" 或 "invalid param" 错误：

1. **检查权限配置**
   - 确保在飞书开放平台开启了 `docx:document:update` 权限
   - 保存并重新发布应用

2. **等待权限生效**
   - 权限更新后可能需要等待几分钟
   - 重启MCP服务（如果使用）

3. **验证参数格式**
   - 确保 `block_type` 使用正确的数字代码
   - 文本内容必须放在 `elements` 数组中

### API调用限制

- 飞书API有频率限制：每秒最多3次请求
- 建议批量操作时添加适当的延迟
- 大量内容建议分批添加，每批20-50个块

### 内容格式转换

**Markdown到飞书块类型的映射：**

| Markdown | 飞书块类型 | block_type |
|----------|-----------|------------|
| `# 标题` | heading1 | 1 |
| `## 标题` | heading2 | 2 |
| `### 标题` | heading3 | 3 |
| `- 列表` | text (带"• ") | 2 |
| 普通文本 | text | 2 |
| `**粗体**` | text | 2 |
| 空行 | text (空内容) | 2 |

## 常见问题

### Q1: 创建的文档只有标题没有内容？

**A:** 这通常是因为缺少 `docx:document:update` 权限。请：
1. 登录飞书开放平台
2. 找到你的应用
3. 在权限管理中添加 `docx:document:update`
4. 保存并重新发布应用
5. 等待5-10分钟后重试

### Q2: API返回 400 错误 "invalid param"？

**A:** 检查以下几点：
- 确保 `block_type` 使用数字而不是字符串
- 检查 `elements` 数组的格式是否正确
- 验证 `text_run` 对象的结构

### Q3: API返回 429 错误？

**A:** 这是频率限制错误。解决方案：
- 减少请求频率
- 添加延迟（如 `time.sleep(0.5)`）
- 使用批量接口而非逐个添加

### Q4: 如何获取现有文档的ID？

**A:**
- 方法1：从文档链接中提取（`feishu.cn/docx/{document_id}`）
- 方法2：使用搜索功能 `client.search_documents("关键词")`
- 方法3：在飞书文档中点击"分享"，查看链接中的ID

## 工具脚本

Skill目录下提供了以下工具脚本：

### `scripts/feishu_api.py`
核心API客户端类，封装了所有飞书文档操作。

### `scripts/create_from_markdown.py`
命令行工具，从Markdown文件创建飞书文档。

### `scripts/search_docs.py`
搜索飞书文档。

### `scripts/update_doc.py`
更新现有文档内容。

## 配置文件

### `config/feishu_config.example`
配置文件示例，包含：
- App ID
- App Secret
- API域名（默认：https://open.feishu.cn）

## 最佳实践

1. **内容分段**
   - 长文档建议分成多个批次添加
   - 每批20-50个块
   - 添加延迟避免触发频率限制

2. **错误处理**
   - 捕获并记录API错误
   - 失败后等待一段时间重试
   - 保存已成功添加的内容位置

3. **性能优化**
   - 使用批量API而非逐个添加
   - 复用token（有效期2小时）
   - 缓存常用操作的结果

4. **权限管理**
   - 应用权限适合自动化任务
   - 用户权限适合个人文档操作
   - 根据场景选择合适的权限类型

## 参考资源

- [飞书开放平台文档](https://open.feishu.cn/document)
- [飞书文档API文档](https://open.feishu.cn/document/server-docs/docs/docs/docx-v1/docx-overview)
- [MCP协议规范](https://modelcontextprotocol.io/)

## 更新日志

### v1.0.0 (2026-01-01)
- ✅ 支持创建文档
- ✅ 支持添加文本内容
- ✅ 支持标题格式（H1/H2/H3）
- ✅ 支持从Markdown导入
- ✅ 支持搜索文档
- ✅ 完整的错误处理
- ✅ 命令行工具

## 许可证

MIT License - 详见 LICENSE.txt
