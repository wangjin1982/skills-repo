# 微信公众号笔记发布器 (WeChat Note Publisher)

## 概述

将Obsidian笔记自动转换并发布到微信公众号草稿箱的**全局通用Skill**。

**完整工作流程：**
```
笔记 → 提取封面图 → 上传图到微信 → MD转HTML → 上传服务器 → 发布草稿箱
```

---

## 触发条件

当用户使用以下任一方式时触发：

- "发布笔记 [[note.md]]"
- "发布这篇文章"
- "Publish note [[note.md]]"
- "推送笔记到公众号 [[note.md]]"
- "发到公众号 [[note.md]]"
- @wechat-note-publisher

---

## 功能特性

1. **自动提取封面图** - 从笔记中提取第一张图片作为封面
2. **上传封面到微信** - 获取 `thumb_media_id` 用于公众号文章
3. **Markdown转HTML** - 转换为适配公众号的美化HTML
4. **上传到云服务器** - 将HTML文件上传到云服务器
5. **发布到草稿箱** - 通过云服务器调用微信API发布

---

## 快速开始

### 1. 配置文件

创建配置文件 `~/.wechat-publish-config.json`：

```json
{
  "server": {
    "host": "你的服务器IP",
    "port": 5000,
    "timeout": 30
  },
  "wechat": {
    "app_id": "你的微信AppID",
    "app_secret": "你的微信AppSecret",
    "account_name": "公众号名称"
  },
  "publish": {
    "default_author": "作者名",
    "title_max_length": 10,
    "cover_required": true
  }
}
```

### 2. 创建封面图（如需要）

```bash
python3 ~/.claude/skills/wechat-note-publisher/scripts/create_cover.py \
  "主标题" "副标题" "作者" "输出路径.png"
```

示例：
```bash
python3 ~/.claude/skills/wechat-note-publisher/scripts/create_cover.py \
  "思考的技术" "第一章：转换思路" "大前研一" \
  "管理学经典/思考的技术/cover_chapter1.png"
```

### 3. 在笔记中添加封面图

```markdown
# 文章标题

![封面图](cover_chapter1.png)

> 标签和其他内容...
```

### 4. 发布笔记

```
发布笔记 [[管理学经典/卓有成效的管理者/第1章.md]]
```

---

## 配置文件搜索顺序

脚本按以下顺序查找配置文件：

1. `~/.wechat-publish-config.json` - 用户配置（推荐）
2. `~/.claude/skills/wechat-note-publisher/config.json` - 全局配置
3. 当前vault `/.wechat-config.json` - 项目配置
4. 使用默认配置

---

## 实现细节

### 标题处理
- 从笔记第一个一级标题提取
- 自动截断到配置的长度（默认10个中文字符）
- 移除emoji和特殊字符

### 封面图处理
- 查找笔记中第一张本地图片
- 上传到微信获取 `thumb_media_id`
- 如果配置为必需且没有图片，则报错

### HTML转换
- 使用带UTF-8编码的转换
- 添加公众号适配CSS样式
- 支持代码高亮、表格、引用等

### 编码处理（关键）
- 上传HTML: `Content-Type: text/html; charset=utf-8`
- 发送JSON: `ensure_ascii=False` + `.encode('utf-8')`

---

## 文件结构

```
~/.claude/skills/wechat-note-publisher/
├── SKILL.md                    # 本文件
├── config.default.json         # 默认配置模板
└── scripts/
    ├── publish.py              # 主发布脚本
    └── create_cover.py         # 封面图生成工具
```

---

## 注意事项

1. **封面图**: 默认必需，可在配置中设置 `cover_required: false`
2. **标题长度**: 默认10个中文字符，可在配置中调整
3. **封面图比例**: 建议使用 2.35:1 (900x500)
4. **编码**: 所有关键步骤使用UTF-8编码
5. **服务器**: 需确保云服务器正常运行

---

## 服务器部署

云服务器需部署:
- `app.py` - Flask服务，处理发布请求
- `config.json` - 服务器配置文件
- 使用 `python app.py` 启动服务

服务器API使用 **Stable Access Token** 确保中文正确显示。

---

## 多环境使用

### 不同vault使用不同配置

在vault根目录创建 `.wechat-config.json`：

```json
{
  "server": {
    "host": "另一台服务器IP",
    "port": 5000
  },
  "publish": {
    "default_author": "另一个作者名"
  }
}
```

### 多个公众号

创建多个配置文件，使用时指定：
```bash
export WECHAT_CONFIG_PATH="~/.wechat-config-account1.json"
python3 publish.py note.md
```

---

## 故障排查

### 问题：找不到配置文件
```
警告: 未找到配置文件，使用默认配置
```
**解决**: 创建 `~/.wechat-publish-config.json`

### 问题：封面图上传失败
```
✗ 未找到封面图
```
**解决**: 在笔记中添加图片引用或设置 `cover_required: false`

### 问题：中文乱码
**解决**: 确保服务器使用 `Stable Access Token` API

---

## 依赖项

- Python 3.6+
- requests (`pip install requests`)
- PIL/Pillow (`pip install Pillow`)
- pandoc (可选，用于更好的Markdown转换)

---

## 许可

MIT License - 可自由使用和修改
