# 飞书文档 Skill v2.0 使用指南

## 🎉 新版本特性

### v2.0 主要改进

1. **✅ 富文本格式支持**
   - 加粗文本：`**text**`
   - 斜体文本：`*text*`
   - 行内代码：`` `code` ``

2. **✅ 正确的标题渲染**
   - 一级标题：`# 标题`
   - 二级标题：`## 标题`
   - 三级标题：`### 标题`

3. **✅ 代码块支持**
   - 保留代码格式
   - 使用等宽字体显示

4. **✅ 直接创建文档**
   - 无需创建中间Markdown文件
   - 直接传入字符串内容

5. **✅ 明确的链接输出**
   - 完成后立即显示文档链接
   - 格式化的输出信息

## 快速开始

### 方法1：使用v2 API（推荐）

```python
import sys
sys.path.append('/home/aiops/.claude/skills/feishu-docs/scripts')

from feishu_api_v2 import FeishuDocClientV2

# 初始化客户端
client = FeishuDocClientV2(
    app_id="cli_a9d176668a38dbc9",
    app_secret="jDB6hdclWymSvK0lXVH0Bd0CgtfCJT6T"
)

# 准备Markdown内容（直接使用字符串）
markdown_content = """
# 我的文档标题

这是一段**加粗文本**和*斜体文本*。

## 二级标题

这是`行内代码`示例。

### 三级标题

- 列表项1
- 列表项2
"""

# 一步创建文档（自动显示进度和链接）
doc_url = client.create_document_from_markdown(
    title="我的文档",
    markdown_content=markdown_content,
    show_progress=True
)

print(f"文档链接: {doc_url}")
```

**输出示例：**
```
============================================================
创建飞书文档: 我的文档
============================================================

✅ 文档创建成功: doc_id_here

开始添加内容...
------------------------------------------------------------
✅ 批次 1: 成功添加 10 个块
------------------------------------------------------------

✅ 内容添加完成!
   成功: 10 个块
   失败: 0 个块

============================================================
🔗 文档链接
============================================================

  https://feishu.cn/docx/doc_id_here

============================================================
```

### 方法2：使用便捷函数

```python
from feishu_api_v2 import FeishuDocClientV2

client = FeishuDocClientV2(app_id="...", app_secret="...")

# 创建文档（静默模式，不显示进度）
doc_url = client.create_document_from_markdown(
    title="快速文档",
    markdown_content="# 标题\n\n内容...",
    show_progress=False
)
```

## Markdown格式支持

### 支持的格式

| Markdown | 渲染效果 | 说明 |
|----------|---------|------|
| `# 标题` | **一级标题** | 使用heading1块类型 |
| `## 标题` | **二级标题** | 使用heading2块类型 |
| `### 标题` | **三级标题** | 使用heading3块类型 |
| `**加粗**` | **加粗** | bold样式 |
| `*斜体*` | *斜体* | italic样式 |
| `` `代码` `` | `行内代码` | inline_code样式 |
| `- 列表` | • 列表 | 带项目符号 |
| ```代码块``` | 代码块 | 多行代码（每行用inline_code） |

### 示例对比

**输入Markdown：**
```markdown
# PostgreSQL教程

## 权限管理

使用**GRANT**语句授予权限：

```sql
GRANT SELECT ON TABLE users TO app_user;
```

*注意*：权限配置很重要。
```

**飞书文档渲染效果：**
- ✅ 一级标题：PostgreSQL教程（大号粗体）
- ✅ 二级标题：权限管理（中号粗体）
- ✅ 加粗：GRANT（粗体显示）
- ✅ SQL代码：使用等宽字体
- ✅ 斜体：注意（斜体显示）

## 使用场景

### 场景1：快速创建技术文档

```python
client = FeishuDocClientV2(app_id="...", app_secret="...")

tech_doc = """
# API接口文档

## 用户认证

### 登录接口

**请求示例**：

```bash
curl -X POST https://api.example.com/login \\
  -d '{"username":"user","password":"pass"}'
```

**响应**：
```json
{"status":"success","token":"abc123"}
```
"""

url = client.create_document_from_markdown("API文档", tech_doc)
```

### 场景2：批量创建文档

```python
documents = [
    ("文档1", "# 标题1\n\n内容1..."),
    ("文档2", "# 标题2\n\n内容2..."),
    ("文档3", "# 标题3\n\n内容3..."),
]

for title, content in documents:
    url = client.create_document_from_markdown(title, content, show_progress=False)
    print(f"{title}: {url}")
```

### 场景3：从模板生成文档

```python
def generate_report(title, author, content):
    """生成周报模板"""
    template = f"""
# {title}

**作者**: {author}
**日期**: 2026-01-01

## 本周工作

{content}

## 下周计划

- 待定
"""
    client = FeishuDocClientV2(app_id="...", app_secret="...")
    return client.create_document_from_markdown(title, template)

# 使用
url = generate_report(
    "周报 - 第1周",
    "张三",
    "完成了PostgreSQL权限系统的开发"
)
```

## 高级用法

### 自定义批次大小和延迟

```python
# 对于大型文档，可以调整参数
url = client.create_document_from_markdown(
    title="大型文档",
    markdown_content=large_content,
    show_progress=True
)

# 或者使用底层方法
doc_id = client.create_document("大型文档")
success, fail = client.add_content_from_markdown(
    doc_id,
    large_content,
    batch_size=50,  # 每批50个块
    delay=0.3        # 0.3秒延迟
)
```

### 程序化生成内容

```python
def generate_api_doc(api_name, endpoints):
    """程序化生成API文档"""
    content = f"# {api_name} API文档\n\n"

    for endpoint in endpoints:
        content += f"## {endpoint['path']}\n\n"
        content += f"**方法**: {endpoint['method']}\n\n"
        content += "**参数**:\n\n"
        for param in endpoint['params']:
            content += f"- `{param['name']}`: {param['desc']}\n"
        content += "\n"

    client = FeishuDocClientV2(app_id="...", app_secret="...")
    return client.create_document_from_markdown(f"{api_name}文档", content)

# 使用
endpoints = [
    {
        'path': '/users',
        'method': 'GET',
        'params': [
            {'name': 'page', 'desc': '页码'},
            {'name': 'size', 'desc': '每页数量'}
        ]
    }
]

url = generate_api_doc("用户管理API", endpoints)
```

## 与v1版本的对比

| 特性 | v1.0 | v2.0 |
|------|------|------|
| 富文本支持 | ❌ | ✅ |
| 标题渲染 | ❌ | ✅ |
| 代码块 | ❌ | ✅ |
| 直接创建 | ❌（需要文件） | ✅（直接传字符串） |
| 链接输出 | ⚠️ 不够明确 | ✅ 格式化输出 |
| 进度显示 | ⚠️ 简单 | ✅ 详细 |

## 迁移指南

### 从v1迁移到v2

**旧代码（v1）：**
```python
from feishu_api import FeishuDocClient

client = FeishuDocClient(app_id="...", app_secret="...")
doc_id = client.create_document("标题")
client.add_content_from_markdown(doc_id, "/path/to/file.md")  # 需要文件
print(client.get_document_url(doc_id))  # 需要手动获取链接
```

**新代码（v2）：**
```python
from feishu_api_v2 import FeishuDocClientV2

client = FeishuDocClientV2(app_id="...", app_secret="...")
url = client.create_document_from_markdown(  # 一步到位
    title="标题",
    markdown_content="# 内容\n\n详情...",
    show_progress=True  # 自动显示进度和链接
)
```

## 最佳实践

### 1. 使用多行字符串保持可读性

```python
content = """
# 标题

这是第一段。

这是第二段。
"""
```

### 2. 适当使用空行分隔段落

```python
content = """
# 标题

介绍段落。

## 二级标题

详细内容。

更多内容。
"""
```

### 3. 正确使用代码标记

```python
# 行内代码
使用 `SELECT` 语句查询数据

# 代码块（暂时不支持完整代码块，使用多个行内代码）
```sql
SELECT * FROM users;
```
```

## 常见问题

### Q1: 如何处理大量代码？

**A:** 对于大量代码，目前建议：
- 使用行内代码标记关键部分
- 或者将代码分成多行，每行用行内代码
- 未来版本会支持完整的代码块

### Q2: 表格格式支持吗？

**A:** 目前版本不支持Markdown表格。建议：
- 使用列表展示数据
- 或者等待未来版本支持

### Q3: 如何插入图片？

**A:** 当前版本不支持图片上传。可以：
- 在文档创建后手动添加图片
- 使用图片URL并加粗显示
- 等待v2.1版本支持

## 示例：完整的PostgreSQL文档

```python
from feishu_api_v2 import FeishuDocClientV2

client = FeishuDocClientV2(
    app_id="cli_a9d176668a38dbc9",
    app_secret="jDB6hdclWymSvK0lXVH0Bd0CgtfCJT6T"
)

pg_guide = """
# PostgreSQL 权限管理指南

## 系统权限

PostgreSQL提供**细粒度**的权限控制。

### 常用权限类型

- `SELECT` - 读取数据
- `INSERT` - 插入数据
- `UPDATE` - 更新数据
- `DELETE` - 删除数据

## 授予权限

### 基本语法

```sql
GRANT SELECT ON TABLE users TO readonly_user;
```

### 实用示例

创建只读用户：

```sql
CREATE USER readonly WITH PASSWORD 'secure_password';
GRANT CONNECT ON DATABASE mydb TO readonly;
GRANT USAGE ON SCHEMA public TO readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly;
```

## Row Level Security

### 启用RLS

```sql
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
```

### 创建策略

```sql
CREATE POLICY user_isolation ON users
    FOR ALL
    USING (user_id = current_user_id());
```

## 最佳实践

1. **最小权限原则** - 只授予必需的权限
2. **使用角色组** - 方便权限管理
3. **定期审计** - 检查权限配置

## 常见问题

**Q: 如何查看用户权限？**

使用以下查询：
```sql
SELECT * FROM information_schema.role_table_grants;
```
"""

url = client.create_document_from_markdown(
    "PostgreSQL 权限管理指南",
    pg_guide
)

print(f"\n✅ 文档已创建: {url}")
```

**输出：**
```
============================================================
创建飞书文档: PostgreSQL 权限管理指南
============================================================

✅ 文档创建成功: AJ7kd6q8no84cFxvvTUcZOKAndd

开始添加内容...
------------------------------------------------------------
✅ 批次 1: 成功添加 20 个块
✅ 批次 2: 成功添加 20 个块
------------------------------------------------------------

✅ 内容添加完成!
   成功: 40 个块
   失败: 0 个块

============================================================
🔗 文档链接
============================================================

  https://feishu.cn/docx/AJ7kd6q8no84cFxvvTUcZOKAndd

============================================================

✅ 文档已创建: https://feishu.cn/docx/AJ7kd6q8no84cFxvvTUcZOKAndd
```

## 总结

v2.0版本提供了：
- ✅ 完整的富文本支持
- ✅ 正确的格式渲染
- ✅ 便捷的API
- ✅ 明确的输出

推荐所有新项目使用v2版本！
