"""
HTTP Client 工具模組
統一管理 GET / POST 請求，並回傳錯誤碼
"""

import requests
from requests.exceptions import RequestException, Timeout, ConnectionError
from workspace.config.error_code import ResultCode

# 建立全域 Session，自動保存 cookie
session = requests.Session()


def get_cookies():
    """回傳目前 session 的 cookies dict（不印）"""
    return session.cookies.get_dict()


def get(url: str, params=None, headers=None, timeout=10):
    try:
        resp = session.get(url, params=params, headers=headers, timeout=timeout)

        if resp.status_code != 200:
            return ResultCode.tools_http_invalid_response, resp
        return ResultCode.SUCCESS, resp

    except Timeout:
        return ResultCode.tools_http_request_timeout, None
    except ConnectionError:
        return ResultCode.tools_http_connection_error, None
    except RequestException:
        return ResultCode.tools_http_request_failed, None
    except Exception:
        return ResultCode.tools_http_unknown_error, None


def post(url: str, data=None, headers=None, timeout=10):
    try:
        resp = session.post(url, data=data, headers=headers, timeout=timeout)

        if resp.status_code != 200:
            return ResultCode.tools_http_invalid_response, resp
        return ResultCode.SUCCESS, resp

    except Timeout:
        return ResultCode.tools_http_request_timeout, None
    except ConnectionError:
        return ResultCode.tools_http_connection_error, None
    except RequestException:
        return ResultCode.tools_http_request_failed, None
    except Exception:
        return ResultCode.tools_http_unknown_error, None
