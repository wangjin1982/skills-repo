# 钉钉企业应用申请指南

本文指南介绍如何创建钉钉企业内部应用并获取待办权限。

## 前置条件

1. 拥有一个钉钉企业账号（可以创建免费企业）
2. 有企业管理员权限

## 步骤一：创建企业内部应用

1. **登录钉钉开放平台**
   - 访问：https://open.dingtalk.com/
   - 使用钉钉账号登录

2. **进入应用开发**
   - 点击顶部菜单「应用开发」
   - 选择「企业内部开发」
   - 点击「创建应用」

3. **填写应用信息**
   - 应用名称：例如「待办助手」
   - 应用描述：例如「个人待办任务管理工具」
   - 应用图标：上传或使用默认图标

4. **创建完成**
   - 记下应用的 **AppKey** 和 **AppSecret**
   - 在应用详情页面可以查看

## 步骤二：申请待办权限

1. **进入权限管理**
   - 在应用详情页面
   - 点击左侧菜单「权限管理」

2. **搜索待办权限**
   - 搜索关键词：「待办」或「todo」
   - 找到以下权限并申请：
     - `todo:task:read` - 读取待办任务
     - `todo:task:write` - 写入待办任务

3. **提交审核**
   - 勾选需要的权限
   - 点击「申请权限」
   - 填写申请理由：「用于个人待办任务管理」

4. **等待审核**
   - 企业内部应用通常自动通过
   - 稍等片刻后刷新页面即可

## 步骤三：获取 UnionId

### 方法一：通过开发者后台查询

1. 在应用详情页面
2. 点击左侧菜单「开发管理」
3. 找到「接口调试工具」
4. 选择接口「获取用户信息」
5. 输入你的 userId（钉钉账号）
6. 调用接口即可获取 UnionId

### 方法二：通过代码获取

```python
import requests

def get_unionid(access_token, userid):
    """
    获取用户的 UnionId

    Args:
        access_token: 应用访问令牌
        userid: 钉钉用户 ID

    Returns:
        UnionId
    """
    url = f"https://api.dingtalk.com/v1.0/contact/users/{userid}"
    headers = {
        "x-acs-dingtalk-access-token": access_token
    }

    response = requests.get(url, headers=headers)
    result = response.json()

    if result.get('unionId'):
        return result['unionId']
    else:
        print(f"获取 UnionId 失败: {result}")
        return None
```

## 步骤四：配置环境变量

将获取到的凭证配置到环境变量中：

### Windows (PowerShell)

```powershell
$env:DINGTALK_APP_KEY="your_app_key"
$env:DINGTALK_APP_SECRET="your_app_secret"
$env:DINGTALK_OPERATOR_ID="your_union_id"
```

### Windows (CMD)

```cmd
set DINGTALK_APP_KEY=your_app_key
set DINGTALK_APP_SECRET=your_app_secret
set DINGTALK_OPERATOR_ID=your_union_id
```

### Linux/macOS

```bash
export DINGTALK_APP_KEY="your_app_key"
export DINGTALK_APP_SECRET="your_app_secret"
export DINGTALK_OPERATOR_ID="your_union_id"
```

## 步骤五：测试验证

```bash
python scripts/create_todo.py --subject "测试任务" --description "这是测试企业应用模式的待办任务"
```

## 常见问题

### Q1: 没有企业账号怎么办？

可以创建免费企业：
1. 打开钉钉客户端
2. 点击「+」→「创建/加入企业」
3. 选择「创建企业」
4. 选择「免费试用」或「个人版」
5. 完成创建即可

### Q2: 权限申请被拒绝怎么办？

企业内部应用的待办权限通常自动通过，如果被拒绝：
1. 检查是否有管理员权限
2. 确认企业类型（部分企业类型可能有权限限制）
3. 联系钉钉客服

### Q3: 如何获取 UserId？

UserId 是钉钉用户的唯一标识，可以通过以下方式获取：
1. 在钉钉客户端中查看个人资料
2. 使用「通讯录录权限」接口获取
3. 让管理员在企业管理后台查看

## 参考链接

- [钉钉开放平台](https://open.dingtalk.com/)
- [企业内部开发文档](https://open.dingtalk.com/document/orgapp/tutorial/overview-1)
- [待办 API 文档](https://open.dingtalk.com/document/orgapp-server/asynchronous-creation-of-enterprise-todo-tasks)
