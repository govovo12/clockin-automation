# workspace/tasks/login/clockin_task.py
"""
打卡任務：Step 7
"""

from urllib.parse import urlsplit
from workspace.config.error_code import ResultCode
from workspace.tools.request import http_client
from workspace.config.http_headers import DEFAULT_HEADERS
from workspace.tools.printer.debug_printer import debug_log


def _origin_from(url: str) -> str:
    """從 URL 解析出 Origin (scheme + host)，例如 https://goodtimesdaka.com"""
    parts = urlsplit(url)
    return f"{parts.scheme}://{parts.netloc}" if parts.scheme and parts.netloc else ""


def do_clockin(context: dict):
    """
    嘗試進行打卡
    - 使用 context 內的 clock_url、clockin_token
    - payload 必須帶 _token
    - 成功回傳 (ResultCode.SUCCESS, dict)
    - 失敗回傳 (錯誤碼, None)

    🔑 新版系統要求：
    - POST /attendance/clock_in 必須帶 Referer = /attendance/ClockIn
    - 必須帶 Origin = https://goodtimesdaka.com
    - 不要再手動塞 X-XSRF-TOKEN，瀏覽器表單提交沒有這個 header
    """
    url = context.get("clock_url")
    clockin_token = context.get("clockin_token")
    debug = context.get("debug", False)

    if not url or not clockin_token:
        return ResultCode.task_clockin_no_token, None

    # payload，只需要 _token
    data = {"_token": clockin_token}

    # -------------------------------
    # Headers：新版 Referer 與 Origin 規則
    # -------------------------------
    headers = DEFAULT_HEADERS.copy()
    headers["Referer"] = context.get("CLOCK_PAGE_URL") or url
    headers["Origin"] = _origin_from(url)
    # ⚠️ 不要再手動塞 X-XSRF-TOKEN，Cookie 由 Session 自動帶

    # Debug 印細節
    debug_log(debug, "clockin_task", f"打卡 URL: {url}")
    debug_log(debug, "clockin_task", f"payload: {data}")
    debug_log(debug, "clockin_task", f"headers: {headers}")

    if debug:
        cookies = http_client.get_cookies()
        debug_log(debug, "clockin_task", f"當前 cookies: {cookies}")

    # 發送 POST 請求
    code, resp = http_client.post(url, data=data, headers=headers)

    # Debug 輸出
    if resp is not None:
        debug_log(debug, "clockin_task", f"HTTP 狀態碼: {resp.status_code}")
        preview = resp.text if len(resp.text) < 500 else resp.text[:500] + "...(truncated)"
        debug_log(debug, "clockin_task", f"API 回應內容:\n{preview}")
    else:
        debug_log(debug, "clockin_task", "沒有收到伺服器回應")

    if code != ResultCode.SUCCESS or resp is None:
        return code, None

    # 嘗試解析 JSON
    try:
        data = resp.json()
    except Exception as e:
        debug_log(debug, "clockin_task", f"JSON 解析失敗: {e}")
        return ResultCode.task_clockin_json_error, None

    records = data.get("table_data", {}).get("original", {}).get("data", [])
    debug_log(debug, "clockin_task", f"解析到的紀錄數: {len(records)}")

    if not records:
        return ResultCode.task_clockin_no_records, None

    first = records[0]
    debug_log(debug, "clockin_task", f"第一筆紀錄: {first}")

    if not first.get("id"):
        return ResultCode.task_clockin_no_id, None

    # 回傳四個必要欄位
    result = {
        "id": first.get("id"),
        "date": first.get("clock_in_at"),
        "work_time": first.get("work_time"),
        "off_work_time": first.get("off_work_time"),
    }

    return ResultCode.SUCCESS, result
