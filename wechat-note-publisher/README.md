# 微信公众号笔记发布器

全局通用Skill，将Obsidian笔记自动发布到微信公众号草稿箱。

## 🎯 功能特点

- ✅ 自动提取并上传封面图到微信
- ✅ Markdown转美化HTML（支持代码高亮）
- ✅ 自动截断标题（微信API限制）
- ✅ UTF-8编码支持（中文无乱码）
- ✅ 多配置文件支持（适合多环境）
- ✅ 跨平台兼容（macOS/Linux/Windows）

## 📦 安装

```bash
# 已安装到全局skill位置
~/.claude/skills/wechat-note-publisher/
```

## ⚙️ 配置

### 1. 创建配置文件

```bash
# 复制模板
cp ~/.claude/skills/wechat-note-publisher/config.default.json \
   ~/.wechat-publish-config.json

# 编辑配置，填入你的信息
nano ~/.wechat-publish-config.json
```

### 2. 配置示例

```json
{
  "server": {
    "host": "你的服务器IP",
    "port": 5000,
    "timeout": 30
  },
  "wechat": {
    "app_id": "wx你的AppID",
    "app_secret": "你的AppSecret",
    "account_name": "公众号名称"
  },
  "publish": {
    "default_author": "作者名",
    "title_max_length": 10,
    "cover_required": true
  }
}
```

## 🚀 使用方法

### 方式一：通过Claude Skill（推荐）

```
发布笔记 [[你的笔记.md]]
```

### 方式二：命令行直接调用

```bash
# 发布笔记
python3 ~/.claude/skills/wechat-note-publisher/scripts/publish.py \
  "笔记路径.md" "可选标题" "可选作者"

# 创建封面图
python3 ~/.claude/skills/wechat-note-publisher/scripts/create_cover.py \
  "主标题" "副标题" "作者" "输出.png"
```

## 📝 工作流程

```
1. 准备笔记
   ↓
2. 添加封面图（可选自动生成）
   ↓
3. 触发"发布笔记"
   ↓
4. 自动完成所有步骤
   ↓
5. 文章出现在公众号草稿箱
```

## 📁 配置文件搜索顺序

```
1. ~/.wechat-publish-config.json       ← 推荐位置
2. ~/.claude/skills/wechat-note-publisher/config.json
3. 当前vault/.wechat-config.json       ← 项目特定配置
4. 默认配置
```

## 🌟 高级用法

### 多个公众号

为每个公众号创建不同的配置文件：

```bash
~/.wechat-publish-config-account1.json
~/.wechat-publish-config-account2.json
```

### 不同vault使用不同配置

在vault根目录创建 `.wechat-config.json` 覆盖全局配置。

### 封面图可选

设置 `cover_required: false` 使封面图变为可选。

## 🔧 故障排查

| 问题 | 解决方案 |
|------|---------|
| 未找到配置文件 | 创建 `~/.wechat-publish-config.json` |
| 封面图上传失败 | 检查图片路径是否正确 |
| 中文乱码 | 确保服务器使用 Stable Token API |
| 标题过长 | 自动截断，或调整 `title_max_length` |

## 📄 许可

MIT License

## 🤝 贡献

欢迎提交问题和改进建议！
