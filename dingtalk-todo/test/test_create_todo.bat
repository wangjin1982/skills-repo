@echo off
REM 钉钉待办任务测试脚本
REM 用于测试 DingTalk Todo Skill 的功能

echo ========================================
echo 钉钉待办任务测试脚本
echo ========================================
echo.

REM 检查环境变量
echo [检查] 验证环境变量...
if not defined DINGTALK_WEBHOOK_URL (
    echo [警告] 未设置 DINGTALK_WEBHOOK_URL 环境变量
    echo [提示] 请先设置环境变量：
    echo   set DINGTALK_WEBHOOK_URL=https://oapi.dingtalk.com/robot/send?access_token=YOUR_TOKEN
    echo   set DINGTALK_SECRET=SECYOUR_SECRET_KEY
    echo.
    pause
    exit /b 1
)

if not defined DINGTALK_SECRET (
    echo [警告] 未设置 DINGTALK_SECRET 环境变量
    echo [提示] 请先设置环境变量：
    echo   set DINGTALK_SECRET=SECYOUR_SECRET_KEY
    echo.
    pause
    exit /b 1
)

echo [OK] 环境变量检查通过
echo.

REM 测试 1：基础待办任务
echo ========================================
echo 测试 1：基础待办任务（仅标题）
echo ========================================
python scripts\create_todo.py --subject "测试任务1 - 编写测试用例"
echo.
pause

REM 测试 2：带描述的待办任务
echo ========================================
echo 测试 2：带描述的待办任务
echo ========================================
python scripts\create_todo.py --subject "测试任务2 - 代码审查" --description "审查PR #123的功能实现，包括边界条件处理"
echo.
pause

REM 测试 3：多行描述
echo ========================================
echo 测试 3：多行描述的待办任务
echo ========================================
python scripts\create_todo.py --subject "测试任务3 - 文档编写" --description "编写API文档，包括：1. 接口说明 2. 参数列表 3. 返回值 4. 错误码"
echo.
pause

echo ========================================
echo 所有测试完成！
echo ========================================
echo.
echo 请检查钉钉群是否收到待办消息。
echo.
pause
