# -*- coding: utf-8 -*-
"""发送任务完成通知到飞书群"""

from feishu_group_messenger import create_messenger

# 创建通知器
messenger = create_messenger(
    app_id='cli_a9d176668a38dbc9',
    app_secret='jDB6hdclWymSvK0lXVH0Bd0CgtfCJT6T'
)

# 发送富文本任务完成通知
result = messenger.send_rich_task_notification(
    chat_id='oc_1750c0544dad49b14f940312bd78c5c7',
    task_name='微信公众号文章生成',
    status='success',
    details='成功生成《管理者的心智挑战》文章，共1100字，包含封面图和Word文档',
    metrics={
        '字数': '1100字',
        '第一部分': '800字',
        '封面图': '1024x1792px',
        'Word文档': '41KB'
    },
    links={
        '文档路径': r'C:\Users\wangj\Documents\微信公众号\wechat-skills-package\ai-content-publisher\output\doc\word\管理者的心智挑战_20260121.docx'
    }
)

if result['success']:
    print('[OK] 飞书消息发送成功')
    if result.get('message_id'):
        print(f'消息ID: {result["message_id"]}')
else:
    print(f'[ERROR] 发送失败: {result.get("error", "未知错误")}')
