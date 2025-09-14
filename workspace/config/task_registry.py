# workspace/config/task_registry.py
"""
Task Registry (方法 A 架構版)

這裡集中管理所有任務的註冊，分區如下：
- task       : 一般任務
- controller : 控制器
- tool       : 工具
"""

from workspace.controller.login_controller import run_login_flow
from workspace.controller.schedule_controller import run_schedule_check
from workspace.controller.telegram_controller import run_telegram_flow
from workspace.controller.main_controller import run_main_flow

TASK_REGISTRY = {
    "task": {
        # e.g. "001": task_001.run,
    },
    "controller": {
        "login": run_login_flow,            # 登入流程控制器
        "schedule": run_schedule_check,     # 新增：行程判斷控制器
        "telegram": run_telegram_flow,      # Telegram 控制器
        "main": run_main_flow,   # ✅ 新增總控制器
    },
    "tool": {
        # e.g. "abc": tool_abc.run,
    },
}

def get_task(category: str, name: str):
    """
    從註冊表取得對應的任務函式
    :param category: "task" | "controller" | "tool"
    :param name: 任務或工具 ID
    :return: 可執行的函式 or None
    """
    return TASK_REGISTRY.get(category, {}).get(name)
