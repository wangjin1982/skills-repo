# 钉钉个人待办 API 可行性分析

## 研究结论

**钉钉不提供纯个人的待办 API**。即使是"个人待办"API，也需要企业应用才能调用。

---

## API 信息

### 接口地址
```
POST https://api.dingtalk.com/v1.0/todo/users/{userid}/personalTasks
```

### 请求头
```http
x-acs-dingtalk-access-token: {access_token}
Content-Type: application/json
```

### 请求参数
```json
{
  "subject": "任务标题",
  "description": "任务描述",
  "detailUrl": "https://your-domain.com/task/123",  // 必填
  "dueTime": 1735689600000,
  "sourceId": "unique_task_id_123"
}
```

---

## 必需条件

### 1. 企业内部应用 ✅ 必需
- 需要在钉钉开放平台创建企业内部应用
- 获取 AppKey 和 AppSecret

### 2. access_token ✅ 必需
```python
# 获取企业内部应用的 access_token
GET https://oapi.dingtalk.com/gettoken?appkey={appkey}&appsecret={appsecret}
```

### 3. userid ✅ 必需
- 执行者的钉钉 userid
- 需要通过通讯录 API 获取

### 4. detailUrl ✅ 必填（2024年2月1日起）
- 必须提供任务详情页面的 URL
- 不能为空或 null

---

## 权限要求

企业应用需要申请以下权限：
- 待办任务写入权限

---

## Python 调用示例

```python
import requests
import time

def get_access_token(app_key, app_secret):
    """获取 access_token"""
    url = "https://oapi.dingtalk.com/gettoken"
    params = {
        "appkey": app_key,
        "appsecret": app_secret
    }
    response = requests.get(url, params=params)
    return response.json()['access_token']

def create_personal_todo(access_token, userid, subject, detail_url):
    """创建个人待办任务"""
    url = f"https://api.dingtalk.com/v1.0/todo/users/{userid}/personalTasks"

    headers = {
        "Content-Type": "application/json",
        "x-acs-dingtalk-access-token": access_token
    }

    data = {
        "subject": subject,
        "detailUrl": detail_url,  # 必填
        "description": "任务描述",
        "dueTime": int(time.time() * 1000) + 86400000
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()
```

---

## 关键限制

### ❌ 没有纯个人 API
- 所有待办 API 都需要企业应用
- 个人开发者无法直接调用

### ❌ detailUrl 必填
- 必须有自己的服务器托管详情页
- 不能使用钉钉内置页面

### ❌ 需要企业账号
- 必须有企业（可以创建免费企业）
- 需要企业管理员权限申请应用

---

## 替代方案

### 方案 1：使用企业应用（推荐）
- 创建免费企业
- 创建企业内部应用
- 申请待办权限
- 调用真正的待办 API

**优点**：真正的待办任务
**缺点**：需要配置，需要 detailUrl

### 方案 2：继续使用 Webhook 消息（当前）
- 无需企业应用
- 发送结构化消息
- 用户手动添加到待办

**优点**：简单快捷
**缺点**：不是真正的待办

### 方案 3：使用其他待办工具
- 滴答清单
- TickTick
- Microsoft To Do
- 提供真正的个人 API

---

## 参考资料

- [钉钉开放平台 - 创建钉钉个人待办任务](https://open.dingtalk.com/document/development/api-createpersonaltodotask)
- [获取企业内部应用的 access_token](https://open.dingtalk.com/document/development/obtain-orgapp-token)
- [钉钉 API - Apifox](https://dingtalk.apifox.cn/api-141426946)
