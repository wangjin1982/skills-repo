@echo off
setlocal

REM 设置环境变量
set DINGTALK_WEBHOOK_URL=https://oapi.dingtalk.com/robot/send?access_token=2c53af85cf548a854f9dd3939f3d43949217bd496e4b33c24b19e13dcfbd5dc2
set DINGTALK_SECRET=SEC9245a75149221c420f9446417020f6fc35f8ea9a7436d020d3e2ac0f78197ada

REM 运行 Python 脚本
python scripts\create_todo.py --subject "测试待办任务" --description "这是通过 dingtalk-todo skill 创建的测试任务"

endlocal
