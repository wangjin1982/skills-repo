---
name: train-invoice-merger
description: "合并火车票电子发票PDF，按时间排序并生成打印友好的合并文件。当用户提供火车票发票ZIP文件或说'合并发票'、'整理火车票'、'发票按时间排序'时使用此技能。"
license: MIT
---

# 火车票发票合并工具

## 功能说明

自动处理火车票电子发票（PDF格式），按乘车时间排序并合并成一个便于打印的PDF文件。每页放置2张发票以节省纸张。

## 使用场景

当用户提供以下场景之一时使用：
- 多个ZIP压缩包包含火车票发票PDF
- 需要合并发票用于报销或存档
- 需要按时间顺序整理发票
- 希望每页打印多张发票以节省纸张

**触发词**：
- "合并发票"、"合并火车票"
- "整理发票"、"整理火车票"
- "发票按时间排序"
- "处理火车票PDF"

## 依赖要求

- Python 3.x
- PyMuPDF: `pip install PyMuPDF`
- reportlab: `pip install reportlab`
- pillow: `pip install pillow`

## 操作步骤

### 1. 解压ZIP文件

扫描当前目录下所有 `.zip` 文件并解压：

```bash
mkdir -p extracted
for f in *.zip; do unzip -q "$f" -d extracted/; done
```

### 2. 提取发票信息

使用pdfplumber提取每张PDF的关键信息（日期、路线、价格）。

### 3. 按时间排序

根据乘车日期对发票进行升序排序。

### 4. 合并PDF

创建新PDF，每页放置2张发票，按排序结果排列。

### 5. 输出文件

生成格式为 `火车票发票_合并_YYYYMMDD_to_YYYYMMDD.pdf` 的文件。

## 执行脚本

可以使用内置脚本自动完成所有步骤：

```bash
python3 ~/.claude/skills/train-invoice-merger/scripts/merge_train_invoices.py
```

## 注意事项

- 脚本会在当前目录查找 `.zip` 文件
- 临时文件会在处理完成后自动清理
- 原始ZIP文件不会被修改
- 输出PDF与输入文件在同一目录
