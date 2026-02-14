---
name: ai-daily-news
description: 自动生成AI领域每日资讯日报，使用WebSearch搜索最新AI资讯（模型发布、应用突破、产业投资），提炼5条关键摘要，生成精美HTML卡片页面。当用户请求生成AI日报、AI资讯汇总、今日AI新闻时使用此技能。
---

# AI资讯日报生成器

自动搜集AI领域最新资讯，生成精美的HTML日报页面。

## 核心工作流程

### 1. 获取当前日期

**关键要求：必须使用真实系统时间，禁止虚构日期。**

```python
from datetime import datetime
current_date = datetime.now().strftime('%Y年%m月%d日')
```

### 2. 执行多维度搜索

使用 WebSearch 工具执行至少 **3-5次** 不同关键词的搜索，确保信息全面性。参考 [search_strategy.md](references/search_strategy.md) 获取完整搜索策略。

**关键搜索维度**：

- **模型发布**：搜索 "AI模型发布 2025"、"大语言模型 最新"、"LLM launch"
- **应用突破**：搜索 "AI应用突破"、"生成式AI 应用"、"AI deployment"
- **产业投资**：搜索 "AI融资投资"、"AI startup funding"、"AI公司并购"

**搜索要求**：
- ✅ 必须使用 WebSearch 工具，禁止模拟数据
- ✅ 每次搜索使用不同关键词
- ✅ 中英文搜索结合，确保覆盖国内外资讯
- ✅ 关注时效性，优先选择24-48小时内的资讯

### 3. 信息提取与筛选

从搜索结果中提取关键信息，筛选出 **最重要的5条资讯**。

**筛选标准**：
- 时效性：优先选择最新资讯
- 权威性：来自知名科技媒体、官方公告
- 重要性：对AI行业有显著影响
- 多样性：覆盖模型、应用、投资等不同类型

**提取信息字段**：
- `title`: 资讯标题（简洁有力）
- `summary`: 资讯摘要（50-100字，说明核心事件和影响）
- `source`: 信息来源（媒体名称）
- `url`: 原文链接（如有）

### 4. 生成JSON数据

将筛选后的资讯组织成JSON格式，保存为临时文件：

```json
{
  "date": "2025年12月14日",
  "news_items": [
    {
      "title": "资讯标题",
      "summary": "资讯摘要，包含核心事件和影响",
      "source": "来源媒体",
      "url": "https://example.com/news"
    }
  ]
}
```

**重要**：确保有且仅有5条资讯。

### 5. 生成HTML报告（可同时导出PNG）

使用 `scripts/generate_report.py` 脚本生成HTML页面：

**仅生成HTML**：
```bash
python scripts/generate_report.py <news_json_path> <output_html_path>
```

**同时生成HTML和PNG**（推荐）：
```bash
python scripts/generate_report.py <news_json_path> <output_html_path> --export-png
```

**自定义PNG路径和宽度**：
```bash
python scripts/generate_report.py <news_json_path> <output_html_path> --export-png --output-png <png_path> --width 600
```

**指定微信二维码**（���于公众号推广）：
```bash
# 自动查找 assets/weixin_qr.png 或 assets/weixin_qr.jpg
python scripts/generate_report.py <news_json_path> <output_html_path>

# 指定自定义二维码路径
python scripts/generate_report.py <news_json_path> <output_html_path> --qr-code /path/to/qrcode.png
```

**二维码设置说明**：
- 将您的微信公众号二维码图片命名为 `weixin_qr.png` 或 `weixin_qr.jpg`
- 放置在skill目录的 `assets/` 文件夹下
- 二维码会自动显示在日报右下角，方便读者扫码关注
- 图片格式支持：PNG、JPG、GIF（建议正方形，尺寸200x200像素）
- 如果未提供二维码，将显示默认的手机图标占位符

**输出路径建议**：
- 使用用户的临时目录或当前工作目录
- 文件名格式：`ai_daily_news_YYYYMMDD.html` / `ai_daily_news_YYYYMMDD.png`

### 6. 导出PNG长图（可选）

如果已生成HTML，可以使用独立的导出脚本：

```bash
python scripts/export_to_png.py <html_path> <png_path>
```

**依赖要求**：
- 需要安装 `html2image` 库：`pip install html2image`
- 首次运行会自动下载Chrome/Chromium（如果系统未安装）

### 7. 打开浏览器展示

生成HTML后，**必须**提供文件的完整绝对路径，并使用系统默认浏览器打开：

**Windows**:
```bash
start <html_file_path>
```

**macOS**:
```bash
open <html_file_path>
```

**Linux**:
```bash
xdg-open <html_file_path>
```

## 输出格式说明

生成的日报支持两种格式：

### HTML格式
- 🎨 **精美设计**：深色科技风、卡片式布局
- 📱 **响应式**：支持桌面和移动端
- 🔗 **可点击链接**：每条资讯包含原文链接
- 📅 **日期标注**：显示生成日期

### PNG格式（长图）
- 📸 **高清截图**：基于Chrome渲染，完美还原HTML样式
- 🖼️ **分享友好**：适合社交媒体分享、保存归档
- 📏 **标准尺寸**：600px宽度，适配主流平台
- 🔤 **清晰排版**：保留所有文字和布局细节

## 质量保证

- ❌ **禁止使用模拟数据** - 所有资讯必须来自真实 WebSearch 结果
- ❌ **禁止虚构日期** - 必须使用 `datetime.now()` 获取真实日期
- ✅ **确保信息准确** - 摘要需准确反映原文内容
- ✅ **保证多样性** - 5条资讯应覆盖不同类型和来源

## 示例用法

**用户请求**：
- "帮我生成今天的AI资讯日报"
- "创建AI日报"
- "今日AI新闻汇总"
- "生成AI日报并导出为图片"

**执行流程**：
1. 获取当前日期：2025年12月28日
2. 执行5次WebSearch搜索不同关键词
3. 提取并筛选5条最重要资讯
4. 生成JSON数据文件
5. 调用脚本生成HTML（可同时生成PNG）
6. 在浏览器中打开HTML文件
7. 向用户报告文件路径（包括PNG路径）

## 参考资源

- **搜索策略详解**：[search_strategy.md](references/search_strategy.md)
- **HTML生成脚本**：[generate_report.py](scripts/generate_report.py)
- **PNG导出脚本**：[export_to_png.py](scripts/export_to_png.py)
