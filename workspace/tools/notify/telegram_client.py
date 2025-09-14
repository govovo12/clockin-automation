"""
Telegram Client 工具模組
-----------------------------------
負責呼叫 Telegram Bot API 傳送訊息
不帶業務邏輯，單純封裝 HTTP 請求
"""

import requests
from workspace.config.error_code import ResultCode


def send_message(token: str, chat_id: str, text: str, timeout: int = 10, parse_mode: str = None):
    """
    傳送訊息到 Telegram
    :param token: Bot Token
    :param chat_id: 目標 Chat ID
    :param text: 訊息文字
    :param timeout: 請求逾時秒數 (預設 10 秒)
    :param parse_mode: 訊息格式 (HTML / MarkdownV2)
    :return: (ResultCode, response | None)
    """
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
    }

    if parse_mode:
        payload["parse_mode"] = parse_mode  # ✅ 新增格式設定

    try:
        resp = requests.post(url, data=payload, timeout=timeout)
    except requests.exceptions.RequestException:
        return ResultCode.tools_telegram_request_failed, None



    if resp.status_code != 200:
        return ResultCode.tools_telegram_invalid_response, resp

    try:
        data = resp.json()
    except ValueError:
        return ResultCode.tools_telegram_invalid_response, resp

    if not data.get("ok"):
        return ResultCode.tools_telegram_invalid_response, resp

    return ResultCode.SUCCESS, resp
