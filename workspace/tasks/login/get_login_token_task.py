# workspace/tasks/login/get_login_token_task.py
"""
任務模組：抓取登入頁面的 CSRF _token 與 form action
"""

from urllib.parse import urljoin
from bs4 import BeautifulSoup
from workspace.tools.request import http_client
from workspace.config.error_code import ResultCode
from workspace.config.http_headers import DEFAULT_HEADERS
from workspace.tools.printer.debug_printer import debug_log


def do_get_login_token(context: dict):
    """
    嘗試抓取 login 頁面的 _token 與 form action
    - 成功時，把 _token 存進 context["login_token"]
             並把 form action(完整 URL) 存進 context["login_action_url"]
    - 失敗時，回傳對應錯誤碼
    """
    url = context.get("CLOCK_LOGIN_URL")
    debug = context.get("debug", False)
    if not url:
        return ResultCode.task_env_missing_key, context

    # headers：用 DEFAULT，再補 Referer / XSRF
    headers = DEFAULT_HEADERS.copy()
    headers["Referer"] = url
    xsrf_token = http_client.session.cookies.get("XSRF-TOKEN")
    if xsrf_token:
        headers["X-XSRF-TOKEN"] = xsrf_token

    # Step 1: GET login 頁
    code, resp = http_client.get(url, headers=headers)
    debug_log(debug, "get_login_token", f"URL: {url}")

    if resp is not None:
        debug_log(debug, "get_login_token", f"狀態碼: {resp.status_code}")
        preview = resp.text if len(resp.text) < 300 else resp.text[:300] + "...(truncated)"
        debug_log(debug, "get_login_token", f"回應預覽:\n{preview}")

        # ✅ 只在 debug=True 時印 cookies
        if debug:
            cookies = http_client.get_cookies()
            debug_log(debug, "get_login_token", f"目前 cookies: {cookies}")
    else:
        debug_log(debug, "get_login_token", "沒有收到伺服器回應")

    if code != ResultCode.SUCCESS or resp is None:
        return code, context  # 底層工具會回傳正確錯誤碼

    # Step 2: 解析 HTML 找 hidden input 與 form action
    try:
        soup = BeautifulSoup(resp.text, "html.parser")
        token_input = soup.find("input", {"name": "_token"})
        login_token = token_input.get("value") if token_input else None

        form = token_input.find_parent("form") if token_input else soup.find("form")
        action = form.get("action") if form and form.has_attr("action") else None
        login_action_url = urljoin(url, action) if action else url  # 沒 action 就退回原本 URL

        if not login_token:
            debug_log(debug, "get_login_token", "找不到 _token")
            return ResultCode.task_login_token_parse_error, context

    except Exception as e:
        debug_log(debug, "get_login_token", f"解析 login 頁面失敗: {e}")
        return ResultCode.task_login_token_parse_error, context

    # Step 3: 寫回 context
    context["login_token"] = login_token
    context["login_action_url"] = login_action_url

    debug_log(debug, "get_login_token", f"抓到 login _token: {login_token}")
    debug_log(debug, "get_login_token", f"解析到 login action URL: {login_action_url}")

    return ResultCode.SUCCESS, context
