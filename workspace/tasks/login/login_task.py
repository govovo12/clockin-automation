# workspace/tasks/login/login_task.py
"""
任務模組：登入並取得 Cookie Token
"""

from urllib.parse import urlsplit
from workspace.tools.request import http_client
from workspace.config.error_code import ResultCode
from workspace.config.http_headers import DEFAULT_HEADERS
from workspace.tools.printer.debug_printer import debug_log


def _origin_from(url: str) -> str:
    parts = urlsplit(url)
    if not parts.scheme or not parts.netloc:
        return ""
    return f"{parts.scheme}://{parts.netloc}"


def do_login(context: dict):
    """
    使用 Step 2 存入的 login_token 與 login_action_url 做登入
    不再重複 GET /login，也不再手動拼 Cookie
    """
    login_action_url = context.get("login_action_url") or context.get("CLOCK_LOGIN_URL")
    referer_url = context.get("CLOCK_LOGIN_URL") or login_action_url

    username = context.get("CLOCK_USERNAME")
    password = context.get("CLOCK_PASSWORD")
    login_token = context.get("login_token")
    debug = context.get("debug", False)

    # 必要值檢查
    if not all([login_action_url, username, password, login_token]):
        debug_log(debug, "login_task", f"缺少必要參數: "
                   f"login_action_url={bool(login_action_url)}, "
                   f"username={bool(username)}, "
                   f"password={bool(password)}, "
                   f"login_token={bool(login_token)}")
        return ResultCode.task_env_missing_key, None

    # POST payload
    payload = {
        "_token": login_token,
        "username": username,
        "password": password,
    }

    # headers：先用 DEFAULT，再補 Referer / Origin / XSRF
    headers = DEFAULT_HEADERS.copy()
    headers["Referer"] = referer_url
    headers["Origin"] = _origin_from(referer_url)

    xsrf_token = http_client.session.cookies.get("XSRF-TOKEN")
    if xsrf_token:
        headers["X-XSRF-TOKEN"] = xsrf_token

    # Debug 輸出
    debug_log(debug, "login_task", f"POST URL: {login_action_url}")
    debug_log(debug, "login_task", f"payload: {{'_token': '***MASKED***', 'username': '{username}', 'password': '***MASKED***'}}")
    headers_dbg = dict(headers)
    if "X-XSRF-TOKEN" in headers_dbg:
        headers_dbg["X-XSRF-TOKEN"] = "***MASKED***"
    debug_log(debug, "login_task", f"headers: {headers_dbg}")

    if debug:
        cookies = http_client.get_cookies()
        debug_log(debug, "login_task", f"目前 cookies: {cookies}")

    # 發送 POST 請求
    code, resp = http_client.post(login_action_url, data=payload, headers=headers)

    # Debug 回應
    if debug:
        cookies = http_client.get_cookies()
        debug_log(debug, "login_task", f"目前 cookies: {cookies}")

        if resp is not None:
            debug_log(debug, "login_task", f"狀態碼: {resp.status_code}")
            preview = resp.text if len(resp.text) < 400 else resp.text[:400] + "...(truncated)"
            debug_log(debug, "login_task", f"回應內容預覽:\n{preview}")
        else:
            debug_log(debug, "login_task", "沒有收到伺服器回應")

    if code != ResultCode.SUCCESS or resp is None:
        return code, None

    debug_log(debug, "login_task", "登入成功，Session 已保存 Cookies")
    return ResultCode.SUCCESS, {}
