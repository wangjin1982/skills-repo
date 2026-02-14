# 飞书文档操作 Skill (Feishu Docs)

一个用于创建、编辑和管理飞书文档的Claude Code Skill。

## 功能特性

✅ **创建文档** - 从头创建新的飞书文档
✅ **内容添加** - 支持从Markdown文件导入内容
✅ **格式支持** - 标题（H1/H2/H3）、文本、列表等
✅ **批量操作** - 支持批量创建多个文档
✅ **文档搜索** - 根据关键词搜索文档
✅ **命令行工具** - 提供便捷的CLI工具
✅ **Python API** - 完整的Python客户端库

## 快速开始

### 1. 配置飞书应用

首先，你需要在飞书开放平台创建应用并配置权限：

1. 访问 [飞书开放平台](https://open.feishu.cn)
2. 创建"企业自建应用"
3. 在"权限管理"中添加以下权限：
   - `docx:document` - 文档基础权限
   - `docx:document:create` - 创建文档
   - `docx:document:update` - 更新文档（必需！）
   - `docx:document:readonly` - 查看文档
4. 保存并记录 App ID 和 App Secret

### 2. 安装依赖

```bash
pip install requests
```

### 3. 使用Python API

```python
import sys
sys.path.append('/home/aiops/.claude/skills/feishu-docs/scripts')

from feishu_api import FeishuDocClient

# 初始化客户端
client = FeishuDocClient(
    app_id="your_app_id",
    app_secret="your_app_secret"
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
print(client.get_document_url(doc_id))
```

### 4. 使用命令行工具

```bash
cd ~/.claude/skills/feishu-docs

# 从Markdown创建文档
python scripts/create_from_markdown.py \
  --app-id "your_app_id" \
  --app-secret "your_app_secret" \
  --title "文档标题" \
  --markdown-file "path/to/content.md"

# 搜索文档
python scripts/search_docs.py \
  --app-id "your_app_id" \
  --app-secret "your_app_secret" \
  "搜索关键词"
```

## 目录结构

```
feishu-docs/
├── SKILL.md                      # Skill主文档
├── README.md                     # 本文件
├── LICENSE.txt                   # MIT许可证
├── examples.py                   # 使用示例代码
├── scripts/                      # 工具脚本
│   ├── feishu_api.py            # 核心API客户端
│   ├── create_from_markdown.py  # 创建文档工具
│   └── search_docs.py           # 搜索文档工具
└── config/                       # 配置文件
    └── feishu_config.example.txt # 配置文件示例
```

## 使用场景

### 场景1: 从Markdown创建文档

将Markdown格式的文档转换为飞书文档：

```python
client = FeishuDocClient(app_id="...", app_secret="...")
doc_id = client.create_document("技术文档")
client.add_content_from_markdown(doc_id, "tech_doc.md")
```

### 场景2: 批量创建文档

批量创建多个文档：

```bash
python scripts/create_from_markdown.py \
  --app-id "xxx" \
  --app-secret "yyy" \
  --batch batch_list.txt
```

`batch_list.txt` 格式：
```
文档1|path/to/doc1.md
文档2|path/to/doc2.md
文档3|path/to/doc3.md
```

### 场景3: 搜索文档

查找包含特定关键词的文档：

```python
results = client.search_documents("项目计划")
for doc in results:
    print(f"{doc['title']}: {doc['document_id']}")
```

## 常见问题

### Q: 创建的文档只有标题没有内容？

**A:** 这通常是因为缺少 `docx:document:update` 权限。

解决方法：
1. 登录飞书开放平台
2. 找到你的应用
3. 添加 `docx:document:update` 权限
4. 保存并重新发布应用
5. 等待5-10分钟使权限生效

### Q: API返回400错误 "invalid param"？

**A:** 检查以下几点：
- 确保 `block_type` 使用数字（1, 2, 3）而不是字符串
- 文本段落使用 `block_type: 2`
- 标题1使用 `block_type: 1`
- 标题2使用 `block_type: 2`，但用 `heading2` 字段

### Q: API返回429错误？

**A:** 这是频率限制错误。

解决方法：
- 增加批次间的延迟时间
- 减小每批的块数量
- 使用 `time.sleep()` 在请求间添加延迟

## 核心概念

### 块类型（Block Types）

飞书文档由不同类型的"块"组成：

| block_type | 类型 | 说明 | 示例 |
|------------|------|------|------|
| 1 | heading1 | 一级标题 | `# 标题` |
| 2 | heading2/text | 二级标题或文本 | `## 标题` 或普通文本 |
| 3 | heading3 | 三级标题 | `### 标题` |

### 块的数据结构

```python
# 文本块
{
    "block_type": 2,
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
            {"text_run": {"content": "标题"}}
        ]
    }
}
```

## API限制

- **频率限制**: 每秒最多3次请求
- **批量大小**: 建议每批20-50个块
- **Token有效期**: 2小时（自动刷新）

## 最佳实践

1. **分批处理** - 大文档分成多批添加，避免超时
2. **错误处理** - 捕获异常并记录失败的操作
3. **延迟控制** - 批次间添加0.2-0.5秒延迟
4. **权限检查** - 确保应用有所有必需的权限
5. **配置管理** - 使用配置文件管理凭证

## 贡献

欢迎提交问题和改进建议！

## 许可证

MIT License - 详见 [LICENSE.txt](LICENSE.txt)

## 相关资源

- [飞书开放平台](https://open.feishu.cn)
- [飞书文档API文档](https://open.feishu.cn/document/server-docs/docs/docs/docx-v1/docx-overview)
- [Claude Code文档](https://docs.claude.com/en/docs/claude-code)

## 更新日志

### v1.0.0 (2026-01-01)
- ✅ 初始版本发布
- ✅ 支持创建文档和添加内容
- ✅ 支持从Markdown导入
- ✅ 提供Python API和CLI工具
- ✅ 完整的文档和示例

---

**作者**: Claude Code AI Assistant
**创建时间**: 2026-01-01
**Skill版本**: 1.0.0
