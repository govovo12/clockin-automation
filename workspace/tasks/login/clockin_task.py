# workspace/tasks/login/clockin_task.py
"""
打卡任務：Step 7
"""

from workspace.config.error_code import ResultCode
from workspace.tools.request import http_client
from workspace.config.http_headers import DEFAULT_HEADERS
from workspace.tools.printer.debug_printer import debug_log


def do_clockin(context: dict):
    """
    嘗試進行打卡
    - 使用 context 內的 clock_url、clockin_token
    - payload 必須帶 _token
    - 成功回傳 (ResultCode.SUCCESS, dict)
    - 失敗回傳 (錯誤碼, None)
    """
    url = context.get("clock_url")
    clockin_token = context.get("clockin_token")
    debug = context.get("debug", False)

    if not url or not clockin_token:
        return ResultCode.task_clockin_no_token, None

    # payload，只需要 _token
    data = {"_token": clockin_token}

    # headers：用 DEFAULT，再補 Referer / Origin / XSRF
    headers = DEFAULT_HEADERS.copy()
    headers["Referer"] = context.get("CLOCK_PAGE_URL") or url
    headers["Origin"] = "http://daka.bbnamg.com"

    xsrf_token = http_client.session.cookies.get("XSRF-TOKEN")
    if xsrf_token:
        headers["X-XSRF-TOKEN"] = xsrf_token

    # Debug 印細節
    debug_log(debug, "clockin_task", f"打卡 URL: {url}")
    debug_log(debug, "clockin_task", f"payload: {data}")
    headers_dbg = dict(headers)
    if "X-XSRF-TOKEN" in headers_dbg:
        headers_dbg["X-XSRF-TOKEN"] = "***MASKED***"
    debug_log(debug, "clockin_task", f"headers: {headers_dbg}")

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
