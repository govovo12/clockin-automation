# workspace/tasks/notify/telegram_message_task.py
"""
通知控制器 Step 2
將 schedule_controller_code / login_controller_code 轉換為訊息字串
"""

from workspace.config.error_code import ERROR_MESSAGES, ResultCode


def translate_codes_to_messages(tg_context: dict):
    """
    把數字代碼轉換成人類可讀訊息
    :param tg_context: Telegram 專用 context
    :return: (ResultCode, dict) 包含處理後的字串
    """
    result = {}

    # 1. schedule_controller_code → 錯誤碼轉文字
    schedule_code = tg_context.get("schedule_controller_code")
    if schedule_code is not None:
        schedule_msg = ERROR_MESSAGES.get(schedule_code, f"未知代碼 {schedule_code}")
        result["schedule_controller_code"] = schedule_msg

    # 2. login_controller_code → 判斷打卡成功 / 失敗
    login_code = tg_context.get("login_controller_code")
    if login_code is not None:
        if login_code == ResultCode.SUCCESS:
            result["login_controller_code"] = "打卡成功"
        else:
            result["login_controller_code"] = "打卡失敗"

    return ResultCode.SUCCESS, result
