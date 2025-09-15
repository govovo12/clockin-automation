# workspace/tasks/login/get_clockin_token_task.py
"""
任務模組：抓取打卡首頁 _token
"""

from workspace.config.error_code import ResultCode
from workspace.tools.request import http_client
from workspace.tools.response import parser
from workspace.config.http_headers import DEFAULT_HEADERS
from workspace.tools.printer.debug_printer import debug_log


def get_clockin_token(context: dict):
    """
    從首頁 API 抓取打卡需要的 _token
    - Input: context (必須有 CLOCK_PAGE_URL, debug)
    - Output: (錯誤碼, token 或 None)

    🔑 新版系統要求：
    - GET /attendance/ClockIn 必須帶 Referer = /login
    - 不要再手動塞 X-XSRF-TOKEN，Session cookie 就會自動帶
    """
    url = context.get("CLOCK_PAGE_URL")
    debug = context.get("debug", False)

    if not url:
        return ResultCode.tools_http_invalid_response, None

    # -------------------------------
    # Headers：新版 Referer 檢查
    # - 打卡頁 (ClockIn) 必須從 login 頁來
    # -------------------------------
    headers = DEFAULT_HEADERS.copy()
    headers["Referer"] = context.get("CLOCK_LOGIN_URL", url)

    # 1. 發送 GET 請求（Session 自動帶 Cookie）
    code, resp = http_client.get(url, headers=headers)

    # Debug 輸出
    debug_log(debug, "get_clockin_token", f"URL: {url}")
    if resp is not None:
        debug_log(debug, "get_clockin_token", f"狀態碼: {resp.status_code}")
        preview = resp.text if len(resp.text) < 300 else resp.text[:300] + "...(truncated)"
        debug_log(debug, "get_clockin_token", f"回應預覽:\n{preview}")

        if debug:
            cookies = http_client.get_cookies()
            debug_log(debug, "get_clockin_token", f"目前 cookies: {cookies}")
    else:
        debug_log(debug, "get_clockin_token", "沒有收到伺服器回應")

    if code != ResultCode.SUCCESS or resp is None:
        return code, None

    # 2. 從 HTML 抽取 _token
    code, token = parser.parse_token_from_html(resp)
    if code != ResultCode.SUCCESS:
        return code, None

    # Debug 印 token 與 cookies
    debug_log(debug, "get_clockin_token", f"抓到的 _token: {token}")
    if debug:
        cookies = http_client.get_cookies()
        debug_log(debug, "get_clockin_token", f"當前 cookies: {cookies}")

    return ResultCode.SUCCESS, token
