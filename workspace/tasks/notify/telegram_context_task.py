"""
通知控制器 Step 1
組合 Telegram 專用資料
- 從「總控制器」傳來的 main_context 抽取:
  schedule_controller_code, login_controller_code, clockin_msg, debug
- 從 .env 讀取 (使用 env_loader):
  TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, ENABLE_TELEGRAM
- 不直接修改 context，僅回傳 (ResultCode, dict)
"""

from workspace.tools.loader.env_loader import load_env, get_env
from workspace.config.error_code import ResultCode


def _validate_enable(value: str) -> bool:
    """ENABLE_TELEGRAM 僅接受 'true' 或 'false'（不分大小寫）"""
    return value.lower() in ("true", "false")


def build_telegram_context(main_context: dict):
    """
    :param main_context: 總控制器傳來的 context（不會被修改）
    :return: (ResultCode, dict) 只回傳需要給 Telegram 的資料
    """
    # 1) 先載入 .env
    code = load_env()
    if code != ResultCode.SUCCESS:
        return code, {}

    # 2) 從 main_context 抽取四個關鍵值
    result = {
        "debug": main_context.get("debug", False),
        "schedule_controller_code": main_context.get("schedule_controller_code"),
        "login_controller_code": main_context.get("login_controller_code"),
        "clockin_msg": main_context.get("clockin_msg"),
    }

    # 3) 讀取 .env
    token = get_env("TELEGRAM_BOT_TOKEN")
    chat_id = get_env("TELEGRAM_CHAT_ID")
    enable_raw = get_env("ENABLE_TELEGRAM", "false")

    # 4) 驗證必須值
    if not token or not chat_id:
        return ResultCode.task_telegram_missing_key, {}

    if not _validate_enable(enable_raw):
        return ResultCode.task_telegram_invalid_enable, {}

    enable = (enable_raw.lower() == "true")

    # 5) 合併 env 值
    result.update({
        "TELEGRAM_BOT_TOKEN": token,
        "TELEGRAM_CHAT_ID": chat_id,
        "ENABLE_TELEGRAM": enable,
    })

    return ResultCode.SUCCESS, result
