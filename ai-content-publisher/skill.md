---
name: management-content-publisher
description: 自动生成高质量管理内容。专注团队管理和个人管理领域，目标读者为35-55岁职场人士（Team Leader、创业者、中高层管理者）。支持多种输出格式（HTML、Word、Markdown），按日期自动组织文件路径。根据时间段智能选择内容类型（早8点=管理技巧、午12点=实战案例、晚6点=深度思考），生成吸引人且实用的标题。可选发布到微信公众号草稿箱。当用户说"生成管理文章"、"写今天的公众号内容"、"管理内容自动发布"时使用。复用 wechat-tech-writer、wechat-article-formatter、wechat-draft-publisher、docx skills。
allowed-tools: WebSearch, Skill, Bash, Read, Write, AskUserQuestion
---

# 管理内容自动生成系统

自动搜索管理领域最新资讯、智能选题、生成高质量文章。内容专注对35-55岁职场人士（Team Leader、创业者、中高层管理者）有价值的管理智慧。

**架构说明**：本系统复用以下 skills：
- `wechat-tech-writer`：负责文章内容生成（可选）
- `wechat-article-formatter`：负责格式化为微信HTML（可选）
- `wechat-draft-publisher`：负责发布到草稿箱（可选）
- `docx`：负责生成Word文档
- `dingtalk-group-message`：负责发送完成通知（可选）

本系统专注于：热点获取、智能选题、时间策略、多格式输出、本地文档保存、可选发布。

**重要变化**：
- **不再强制发布到草稿箱**：用户可以选择仅本地保存
- **支持多种输出格式**：HTML、Word、Markdown
- **按日期组织文件**：便于管理和查找
- **可选钉钉通知**：任务完成后自动通知

**📸 封面图策略**（仅在发布到草稿箱时需要）：
- **禁止使用AI生成**：不再使用 `canvas-design` skill 生成封面图
- **从封面库选择**：使用 `assets/covers/` 中的预设封面
- 选择流程：调用 `scripts/select_cover.py` 根据内容类型选择合适的封面
- 上传到微信素材库：调用 `wechat-draft-publisher` 时自动上传封面

## 核心特性

- **文章模式**：支持标准模式和深度模式
  - **标准模式**（默认）：800-1000字管理文章，适合日常发布
  - **深度模式**：2000字深度分析，适合专题文章
- **多格式输出**：支持多种输出格式
  - **HTML格式**：适配微信公众号发布（使用wechat-article-formatter）
  - **Word格式**：生成.docx文档，方便本地编辑（使用docx）
  - **Markdown格式**：保留原始内容，便于后续处理
- **智能路径组织**：按日期自动组织输出目录
  - 路径格式：`output/YYYY-MM-DD/文章标题.扩展名`
  - 示例：`output/2026-01-21/孩子说我不会怎么办_成长型思维.docx`
- **可选草稿箱发布**：自动发布到微信公众号草稿箱（可选）
  - 使用wechat-draft-publisher skill
  - 需要用户提供封面图和配置信息
- **时间段策略**：根据发布时间自动选择内容类型
  - 早8点：管理技巧/方法论
  - 中午12点：实战案例/具体做法
  - 晚上6点：深度思考/战略思维
- **智能标题生成**：吸引人且符合实际，避免标题党
- **48小时时效性检查**：确保内容是最新的
- **智能过滤**：自动排除无关信息，聚焦管理价值
- **每次1篇**：专注质量而非数量

## 目标读者

- **Team Leader/管理者**：需要提升团队管理和领导力
- **创业者**：需要获取管理经验和实战案例
- **中高层管理者**：需要深度思考和战略洞察
- **职场进阶者**：需要实用的管理技巧和方法

## 触发条件

当用户说以下类似话术时触发：
- "帮我生成今天的管理文章"
- "写今天的公众号内容"
- "管理内容自动发布"
- "生成团队管理文章"
- "搜索管理资讯并发布"

## 执行流程

### 步骤1：判断时间段和内容类型

```python
from datetime import datetime
from scripts.title_generator import get_time_slot_type, TIME_SLOT_CONTENT

# 获取当前时间和目标类型
target_type, time_slot = get_time_slot_type()
time_info = TIME_SLOT_CONTENT[time_slot]

print(f"当前时间: {datetime.now().strftime('%H:%M')}")
print(f"时段: {time_slot}")
print(f"内容类型: {time_info['description']}")
print(f"内容重点: {time_info['focus']}")
print(f"目标读者: {time_info['target_audience']}")
```

**时间段映射**：
- 6:00-11:00 → `morning` → 管理技巧/方法论
- 11:00-16:00 → `afternoon` → 实战案例/具体做法
- 16:00-6:00 → `evening` → 深度思考/战略思维

### 步骤2：获取当前日期并获取热点

```bash
# 确认当前日期
date_str=$(date +"%Y年%m月%d日")
echo "今天是: $date_str"

# 获取热点
cd /c/Users/wangj/.claude/skills/ai-content-publisher
python3 scripts/fetch_hotspots.py
```

**热点来源**：
- 管理类媒体和博客（哈佛商业评论、36Kr管理专栏、虎嗅管理、知乎管理话题）
- 创业和管理社区（经管之家、创业者社区）
- WebSearch主动搜索（团队管理、领导力、个人管理等关键词）

**重要**：只获取48小时内的热点，确保内容是最新的。

### 步骤3：智能选题（选择1篇）

```bash
python3 scripts/selector.py
```

**选题策略**：
1. **根据时间段确定目标类型**（管理技巧/实战案例/深度思考）
2. **过滤排除**：排除无关信息（技术细节、代码实现等）
3. **针对性评分**：优先选择匹配目标类型的高分话题，聚焦管理价值
4. **选择最佳**：只选择1个评分最高的选题

选中话题保存到：`cache/selected_topic.json`

### 步骤4：生成吸引人的标题

```python
from scripts.title_generator import generate_title

# 读取选中的话题
import json
with open('cache/selected_topic.json', 'r') as f:
    topic = json.load(f)

# 生成标题（会根据内容类型自动选择合适的模板）
generated_title = generate_title(topic, topic['content_type'])

print(f"生成标题: {generated_title}")
```

**标题生成原则**：
- ✅ 包含具体数字（"3个技巧"、"5步搞定"）
- ✅ 直接利益点（"让你效率提升10倍"）
- ✅ 明确具体（不模糊）
- ✅ 适当长度（避免被截断）
- ✅ 符合实际（标题与内容匹配）
- ❌ 避免标题党（"震惊！"、"必看！"等）

### 步骤5：生成文章内容

使用 **wechat-tech-writer** 的 `generate.py` 脚本生成文章：

```bash
# 标准模式（默认）
python3 /c/Users/wangj/wechat_article_skills/wechat-tech-writer/generate.py \
  --topic "$TOPIC_TITLE" \
  --url "$TOPIC_URL" \
  --type "$CONTENT_TYPE" \
  --output "$OUTPUT_DIR" \
  --mode standard

# 深度模式（2000字专题文章）
python3 /c/Users/wangj/wechat_article_skills/wechat-tech-writer/generate.py \
  --topic "$TOPIC_TITLE" \
  --url "$TOPIC_URL" \
  --type "$CONTENT_TYPE" \
  --output "$OUTPUT_DIR" \
  --mode deep
```

**模式说明**：
- `standard`：800-1000字，标准科普文章（定时任务使用）
- `deep`：2000字，深度分析文章（手动触发特殊需求时使用）

将生成的文章保存到：
```
output/{日期}/
├── {文章标题}.md
```

### 步骤5.5：确定输出格式（新增）

在生成文章后，需要确定输出格式。使用AskUserQuestion工具询问用户：

```
请选择输出格式：
- HTML：适配微信公众号发布（美化格式）
- Word：生成.docx文档（方便本地编辑）
- Markdown：保留原始内容
- 多种格式：同时生成多种格式
```

**格式选择建议**：
- 如果要发布到微信公众号 → 选择HTML或多种格式
- 如果要本地保存和编辑 → 选择Word
- 如果要后续处理 → 选择Markdown
- 如果不确定 → 选择多种格式（HTML + Word + Markdown）

### 步骤5.6：按日期组织输出路径（新增）

自动创建以日期命名的目录结构：

```bash
# 获取当前日期
date_str=$(date +"%Y-%m-%d")  # 示例：2026-01-21

# 创建输出目录
mkdir -p "output/$date_str"
```

**输出路径规则**：
- 所有输出文件保存在 `output/YYYY-MM-DD/` 目录下
- 文件名使用文章标题，去除特殊字符
- 多篇文章保存在同一日期目录下，便于管理

**示例目录结构**：
```
output/
└── 2026-01-21/
    ├── 孩子说我不会怎么办_成长型思维.md
    ├── 孩子说我不会怎么办_成长型思维.docx
    ├── 孩子说我不会怎么办_成长型思维.html
    ├── 培养成长型思维的三个黄金时刻.md
    ├── 培养成长型思维的三个黄金时刻.docx
    └── 培养成长型思维的三个黄金时刻.html
```

### 步骤5.7：根据选择的格式生成文件（新增）

#### 生成Word格式（使用docx skill）

如果用户选择Word格式，使用python-docx库生成：

```python
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

# 读取Markdown文件内容
with open(f'output/{date_str}/{article_title}.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 创建Word文档
doc = Document()

# 设置默认字体
style = doc.styles['Normal']
font = style.font
font.name = 'Arial'
font.size = Pt(12)

# 解析Markdown并添加到Word文档
# ...（具体的转换逻辑）

# 保存Word文档
doc.save(f'output/{date_str}/{clean_title}.docx')
```

**Word格式化要点**：
- 标题使用Heading样式（Heading 1, 2, 3）
- 正文使用Arial字体，12pt
- 表格添加边框和表头样式
- 列表使用Word的标准列表格式
- 代码块使用等宽字体

#### 生成HTML格式（使用wechat-article-formatter skill）

如果用户选择HTML格式，使用wechat-article-formatter转换：

```bash
python -X utf8 ~/.claude/skills/wechat-article-formatter/scripts/markdown_to_html.py \
  --input "output/{date_str}/{article_title}.md" \
  --output "output/{date_str}/{article_title}.html"
```

**注意**：Windows系统需要使用 `python -X utf8` 来避免编码错误。

#### 生成Markdown格式

Markdown格式是原始内容，默认已保存，无需额外处理。

### 步骤5.8：询问是否发布到草稿箱（新增）

在生成文件后，询问用户是否需要发布到微信公众号草稿箱：

```
是否需要发布到微信公众号草稿箱？
- 是：继续执行发布流程
- 否：跳过发布，仅保存本地文件
```

**⚠️ 重要**：
- 发布到草稿箱需要额外的配置（封面图、作者信息等）
- 如果用户不需要草稿箱功能，不要强制发布
- 只在用户明确要求时才调用wechat-draft-publisher skill

### 步骤5.9：从封面库选择封面图（⚠️ 仅在发布到草稿箱时需要）

```bash
# 根据内容类型从封面库选择封面
python3 scripts/select_cover.py "$CONTENT_TYPE" "output/{日期}/article/"
```

**封面选择规则**：
- `new_tool` → `tool_*.png`（蓝色AI工具、深色编码、橙色生产力）
- `tutorial` → `tutorial_*.png`（绿色学习）
- `industry_news` → `news_*.png`（蓝色数据、紫色分析）

封面复制为：`output/{日期}/cover.png`

**⚠️ 严禁**：
- 禁止使用 `/canvas-design` 生成封面
- 禁止使用任何AI生成封面
- 如果 `select_cover.py` 失败，必须报错退出

### 步骤6：格式化HTML（仅在需要发布到草稿箱时执行）

**⚠️ 注意**：如果用户已经在步骤5.7中选择了HTML格式，此步骤可跳过。

使用 **wechat-article-formatter** 转换：

```bash
# Windows系统需要使用 -X utf8 参数
python -X utf8 ~/.claude/skills/wechat-article-formatter/scripts/markdown_to_html.py \
  --input "output/{date_str}/{article_title}.md" \
  --output "output/{date_str}/{article_title}_wechat.html"
```

### 步骤7：发布到草稿箱（可选，仅在用户要求时执行）

**⚠️ 重要**：只在步骤5.8中用户明确选择"是"时才执行此步骤。

使用 **wechat-draft-publisher** 发布：

```bash
python3 /c/Users/wangj/.claude/skills/wechat-draft-publisher/publisher.py \
  --title "{文章标题}" \
  --content "output/{date_str}/{article_title}_wechat.html" \
  --cover "output/{date_str}/cover.png" \
  --author "阳桃AI干货"
```

### 步骤8：发送完成通知（新增）

使用 **dingtalk-group-message** skill 发送任务完成通知：

```bash
cd ~/.claude/skills/dingtalk-group-message

# 设置环境变量
export DINGTALK_WEBHOOK_URL="https://oapi.dingtalk.com/robot/send?access_token=YOUR_TOKEN"
export DINGTALK_SECRET="SECYOUR_SECRET_KEY"

# 发送任务通知
python -X utf8 scripts/send_task_notification.py \
  --task "微信公众号文章生成" \
  --status "success" \
  --message "已成功生成{文章数量}篇主题文章。格式：{输出格式}。文件位置：output/{日期}/"
```

**通知内容示例**：
```
✅ 任务通知

📌 任务名称：微信公众号文章生成
📊 状态：成功

📝 详情：已成功生成2篇成长型思维主题文章Word格式：
1. 孩子说我不会怎么办（实用对话策略）
2. 培养成长型思维的三个黄金时刻（失败挑战努力）

📂 文件位置：output/2026-01-21/

🕒 时间：2026-01-21 21:25:54
```

**注意**：如果用户未配置钉钉webhook，此步骤可跳过。

### 步骤9：完成总结（更新）

```
✅ AI内容生成完成

生成时间：{当前时间}
内容类型：{类型}
输出格式：{HTML/Word/Markdown/多种}

【本地文件】
标题：{完整标题}
字数：{字数}字
格式：{输出格式}
位置：output/{日期}/

【微信公众号】
标题：{完整标题}
状态：{已发布到草稿箱 / 仅本地保存}
Media ID：{media_id（如果已发布）}

---
```

**如果没有发布到草稿箱**：
```
✅ AI内容生成完成（本地保存）

生成时间：{当前时间}
内容类型：{类型}

【本地文件】
路径：output/{日期}/
├── {文章标题}.md
├── {文章标题}.docx（如果选择Word格式）
└── {文章标题}.html（如果选择HTML格式）

提示：如需发布到微信公众号，请手动使用微信编辑器导入HTML文件。
```

**如果已发布到草稿箱**：
```
✅ AI内容生成完成（已发布到草稿箱）

生成时间：{当前时间}
内容类型：{类型}

【本地文件】
路径：output/{日期}/
├── {文章标题}.md
├── {文章标题}.docx
└── {文章标题}.html

【微信公众号】
标题：{完整标题}
字数：{字数}字
状态：已发布到草稿箱
Media ID：{media_id}

---
请前往微信公众号后台查看草稿：
https://mp.weixin.qq.com
```

## 标题写作参考

### 好标题的要素

| 要素 | 说明 | 示例 |
|------|------|------|
| 具体数字 | "3个技巧"、"5步搞定" | "3步用LangChain搭建AI应用" |
| 直接利益 | "让...效率提升..." | "Claude Code：让开发者效率提升3倍" |
| 明确具体 | 不模糊，有针对性 | "OpenAI o3：AI开发者需要知道的3个变化" |
| 适当长度 | 避免被截断 | 微信限制64字节（约20个汉字） |
| 符合实际 | 标题与内容匹配 | 不夸大、不模糊 |

### 标题模板

**管理技巧类**：
- `{number}个{管理技能}技巧，让团队效率提升{X倍}`
- `提升{管理技能}的{number}个方法`
- `{管理技能}进阶：{number}个实用技巧`

**实战案例类**：
- `从{公司/案例}学到的{number}个管理教训`
- `{number}步打造{理想团队状态}`
- `真实案例：如何解决{管理痛点}`

**深度思考类**：
- `深度思考：{管理话题}的{number}个关键洞察`
- `{管理话题}：从{现象}到{本质}`
- `重新理解{管理话题}：{新视角}`

### 避免标题党

❌ **不要用**：
- "震惊！"、"必看！"、"惊呆了！"
- "你绝对想不到..."
- 过度承诺
- 故意模糊

✅ **应该用**：
- 实事求是
- 突出价值
- 明确具体
- 适度吸引

## 配置文件

### config/sources.yaml
- RSS源列表
- GitHub配置
- 时效性设置（48小时）
- 每次获取数量限制

## 输出目录

```
output/
└── {日期}/                       # 按日期组织（示例：2026-01-21）
    ├── {文章标题}.md             # Markdown原始内容
    ├── {文章标题}.docx           # Word格式（如果选择）
    ├── {文章标题}.html           # HTML格式（如果选择）
    └── cover.png                 # 封面图（仅发布到草稿箱时需要）

cache/
├── hotspots.json                 # 原始热点
└── selected_topic.json           # 选中的话题（单个）
```

**目录组织原则**：
- 每天的文章保存在同一日期目录下
- 多篇文章共享同一个日期目录
- 文件名使用文章标题，便于识别
- Markdown格式始终保留，便于后续处理
- Word和HTML格式根据用户选择生成

## 定时任务配置

### Crontab 配置

```bash
# 编辑定时任务
crontab -e

# 添加以下内容（早8点、中午12点、晚上6点）
0 8,12,18 * * * cd /c/Users/wangj && claude skill ai-content-publisher >> /var/log/ai-content.log 2>&1
```

### Cron 表达式说明

```
┌───────────── 分钟 (0-59)
│  ┌────────── 小时 (0-23)
│  │   ┌────── 日期 (1-31)
│  │   │  ┌─── 月份 (1-12)
│  │   │  │ ┌ 星期 (0-7)
│  │   │  │ │
*  *  *  *  *  命令
```

- `0 8,12,18 * * *` = 每天 8:00、12:00、18:00 执行
- `>> /var/log/ai-content.log` = 日志追加到文件
- `2>&1` = 错误也重定向到日志

## 质量标准

### 内容质量要求

- **原创性**：用自己的语言重新组织，不照搬原文
- **准确性**：事实和数据必须可靠
- **实用性**：必须有具体价值，对读者有帮助
- **可读性**：语言自然流畅，适合公众号风格
- **字数要求**：800-1000字（标准模式）
- **深度模式**：2000字（专题文章）

### 标题质量要求

- **长度限制**：不超过64字节（约20个汉字）
- **吸引力**：让人想点击，但不夸张
- **信息量**：包含核心信息，让读者知道会学到什么
- **匹配度**：标题与内容完全一致

## 注意事项

1. **⚠️ 封面图强制要求**（仅在发布到草稿箱时）：
   - **必须**从封面库选择（`assets/covers/`）
   - **禁止**使用 `/canvas-design` 生成封面
   - **禁止**使用任何AI生成封面
   - 封面选择失败则报错退出，不继续发布

2. **⚠️ 草稿箱发布是可选的**：
   - 不强制发布到草稿箱
   - 在步骤5.8询问用户是否需要发布
   - 只在用户明确要求时才调用wechat-draft-publisher
   - 如果用户只需本地文件，跳过发布流程

3. **输出格式选择**：
   - 使用AskUserQuestion工具询问用户需求
   - 支持HTML、Word、Markdown多种格式
   - 根据用户选择生成相应格式
   - 推荐默认生成Word格式（最通用）

4. **路径组织规范**：
   - 所有文件保存在 `output/YYYY-MM-DD/` 目录下
   - 使用日期作为文件夹名称
   - 文件名使用文章标题，去除特殊字符
   - 多篇文章共享同一日期目录

5. **日期检查**：所有搜索操作前必须先确认当前日期
6. **时效性**：只使用48小时内的热点
7. **时间段策略**：根据时间自动选择合适的内容类型
8. **质量第一**：宁可少发，也要保证质量
9. **标题规范**：吸引人但不标题党
10. **Windows编码问题**：使用python时添加 `-X utf8` 参数避免中文乱码

## 参考资源

### 标题写作技巧
- [10倍点击量：2025年的标题生成器](https://www.iweaver.ai/zh/guide/headline-generator-in-2025/)
- [技术文章如何取标题、封面、配图](https://cloud.tencent.com/developer/article/2277070)
- [如何打造爆款文章标题？把握1个公式，9个套路，5个细节](https://www.digitaling.com/articles/893297.html)
- [AI生成公众号推文神器：3分钟打造爆款内容的秘密武器](https://www.uecloud.net/geo/article/Zj5)
