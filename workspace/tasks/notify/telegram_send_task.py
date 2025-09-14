"""
通知控制器 Step 3
判斷是否啟用通知並呼叫 Telegram 工具發送訊息
"""

from workspace.config.error_code import ResultCode
from workspace.tools.notify.telegram_client import send_message


def send_telegram_notification(tg_context: dict):
    """
    發送 Telegram 通知
    :param tg_context: Telegram 專用 context
    :return: ResultCode
    """
    # Step 1: 判斷 ENABLE_TELEGRAM
    if not tg_context.get("ENABLE_TELEGRAM", False):
        return ResultCode.task_notify_disabled

    # Step 2: 準備參數
    token = tg_context.get("TELEGRAM_BOT_TOKEN")
    chat_id = tg_context.get("TELEGRAM_CHAT_ID")

    schedule_msg = tg_context.get("schedule_controller_code", "")
    login_msg = tg_context.get("login_controller_code", "")
    clockin_msg = tg_context.get("clockin_msg", "")

    # ✅ 組合專業格式訊息 (HTML 模式)
    text = (
        "📢 <b>打卡通知</b>\n"
        "────────────────────\n"
        f"📅 {schedule_msg}\n"
        f"✅ {login_msg}\n"
        f"🕒 {clockin_msg}\n"
    )

    # Step 3: 呼叫 Telegram API
    code, _ = send_message(token, chat_id, text, parse_mode="HTML")

    # 轉傳工具回來的錯誤碼
    return code
