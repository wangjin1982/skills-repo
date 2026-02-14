# 钉钉待办 API 调研报告

## 概述

本文档介绍钉钉待办相关的 API 接口，用于创建真正的待办任务。

## API 类型

### 1. 企业内部应用待办 API

创建真正的待办任务，需要企业内部应用权限。

#### API 端点

```
POST https://api.dingtalk.com/v1.0/todo/tasks/create
```

#### 请求头

```http
x-acs-dingtalk-access-token: {access_token}
Content-Type: application/json
```

#### 请求体

```json
{
  "subject": "任务标题",
  "description": "任务描述",
  "creatorId": "创建者UnionId",
  "executorIds": ["执行者UnionId"],
  "detailUrl": {
    "appUrl": "dingtalk://...",
    "pcUrl": "https://..."
  },
  "dueTime": 1737878400000,
  "priority": "high"
}
```

#### 参数说明

| 参数 | 类型 | 必填 | 说明 |
|-----|------|-----|------|
| subject | String | 是 | 任务标题 |
| description | String | 否 | 任务描述 |
| creatorId | String | 是 | 创建者的 UnionId |
| executorIds | Array[String] | 是 | 执行者的 UnionId 列表 |
| detailUrl | Object | 否 | 任务详情链接 |
| dueTime | Number | 否 | 截止时间（毫秒时间戳） |
| priority | String | 否 | 优先级：high/medium/low |

#### 获取 AccessToken

```python
import requests

def get_access_token(app_key, app_secret):
    url = "https://api.dingtalk.com/v1.0/oauth2/accessToken"
    data = {
        "appKey": app_key,
        "appSecret": app_secret
    }
    response = requests.post(url, json=data)
    return response.json()['accessToken']
```

#### 获取 UnionId

```python
def get_user_info(access_token, userid):
    url = "https://api.dingtalk.com/v1.0/contact/users/{userid}"
    headers = {
        "x-acs-dingtalk-access-token": access_token
    }
    response = requests.get(url, headers=headers)
    return response.json()['unionId']
```

## 实现示例

### 创建待办任务

```python
import requests
import json

def create_todo(access_token, subject, description, creator_id, executor_ids):
    url = "https://api.dingtalk.com/v1.0/todo/tasks/create"

    headers = {
        "x-acs-dingtalk-access-token": access_token,
        "Content-Type": "application/json"
    }

    data = {
        "subject": subject,
        "description": description,
        "creatorId": creator_id,
        "executorIds": executor_ids
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()
```

## 权限要求

企业应用需要申请以下权限：

- 待办任务读写权限：`todo:task:read` 和 `todo:task:write`

## 参考资料

- [钉钉开放平台 - 待办 API 文档](https://open.dingtalk.com/document/orgapp-server/asynchronous-creation-of-enterprise-todo-tasks)
- [钉钉开放平台 - OAuth 2.0](https://open.dingtalk.com/document/orgapp-mini-protocol/obtain-user-token)
- [钉钉开放平台 - 获取用户信息](https://open.dingtalk.com/document/orgapp-mini-protocol/dingtalk-retrieve-user-information)
