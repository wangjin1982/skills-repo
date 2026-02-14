# 微信公众号草稿发布器 - UTF-8编码修复

## 🎯 问题描述

使用原始的 `publisher.py` 推送文章到微信公众号草稿箱时，**中文字符显示为乱码**。

## 🔍 问题原因

微信公众号API需要**UTF-8编码**的JSON数据，但Python的 `json.dumps()` 默认使用 `ensure_ascii=True`，会将非ASCII字符转义为Unicode序列（如 `\u4e2d\u6587`），导致中文显示异常。

## ✅ 解决方案

### 关键修复代码

**原始代码**（有中文乱码问题）：
```python
response = requests.post(url, params=params, json=article_data)
```

**修复后的代码**：
```python
headers = {'Content-Type': 'application/json; charset=utf-8'}

response = requests.post(
    url,
    params=params,
    data=json.dumps(article_data, ensure_ascii=False).encode('utf-8'),
    headers=headers
)
```

### 修复要点

1. **`ensure_ascii=False`**：让JSON输出包含原始UTF-8字符而不是Unicode转义序列
2. **`.encode('utf-8')`**：手动将字符串编码为UTF-8字节
3. **设置Content-Type**：明确告知服务器使用UTF-8编码

## 📝 使用示例

### 方法1：使用修复后的脚本

```bash
python publisher_fixed.py \
  --title "时间管理法" \
  --content article.html \
  --author "大金" \
  --cover cover.png
```

### 方法2：直接使用Python代码

```python
import requests
import json

# 读取HTML内容
with open('article.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# API配置
access_token = "your_access_token"
cover_media_id = "your_cover_media_id"

# 构建数据
article_data = {
    "articles": [{
        "title": "时间管理法",
        "author": "大金",
        "digest": "让孩子从被催促到自主管理时间",
        "content": html_content,
        "thumb_media_id": cover_media_id,
        "show_cover_pic": 1,
        "need_open_comment": 1,
        "only_fans_can_comment": 0
    }]
}

# 发送请求（关键修复）
url = "https://api.weixin.qq.com/cgi-bin/draft/add"
params = {"access_token": access_token}
headers = {'Content-Type': 'application/json; charset=utf-8'}

response = requests.post(
    url,
    params=params,
    data=json.dumps(article_data, ensure_ascii=False).encode('utf-8'),
    headers=headers
)

result = response.json()
print(result)
```

## ✅ 验证结果

修复后，微信公众号草稿箱中的文章：
- ✅ 标题正确显示中文
- ✅ 正文内容正确显示中文
- ✅ 格式保持正常
- ✅ 封面图正常显示

## 🔄 更新现有脚本

将所有使用 `requests.post(..., json=...)` 的代码替换为：

```python
# 旧代码（有乱码问题）
requests.post(url, json=data)

# 新代码（修复乱码）
requests.post(
    url,
    data=json.dumps(data, ensure_ascii=False).encode('utf-8'),
    headers={'Content-Type': 'application/json; charset=utf-8'}
)
```

## 📚 相关文件

- **原始脚本**：`publisher.py`（有中文乱码问题）
- **修复脚本**：`publisher_fixed.py`（UTF-8编码正确）
- **配置文件**：`~/.wechat-publisher/config.json`

## 🎓 经验总结

1. **中文内容必须使用UTF-8编码**
2. **`ensure_ascii=False` 是关键**
3. **手动 `.encode('utf-8')` 确保正确编码**
4. **设置明确的 Content-Type header**

## 📅 更新日期

2026-01-29

---

**修复状态**：✅ 已验证并测试成功
