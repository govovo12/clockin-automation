# workspace/tools/response/parser.py
"""
Response Parser 工具模組
負責解析 API 回應並回傳錯誤碼
"""
import re
from workspace.config.error_code import ResultCode


def parse_json(resp):
    """
    嘗試將 response 轉換為 JSON
    :param resp: requests.Response
    :return: (錯誤碼, dict 或 None)
    """
    try:
        data = resp.json()
        if not isinstance(data, dict):
            return ResultCode.tools_response_invalid_format, None
        return ResultCode.SUCCESS, data
    except Exception:
        return ResultCode.tools_response_parse_failed, None


def require_key(data: dict, key: str):
    """
    檢查 JSON 裡是否存在必要欄位
    :param data: dict
    :param key: 必要欄位名稱
    :return: (錯誤碼, value 或 None)
    """
    if key not in data:
        return ResultCode.tools_response_missing_key, None
    return ResultCode.SUCCESS, data[key]




def parse_token_from_html(resp):
    """
    從 HTML 或 JS response 內容提取 _token
    :param resp: requests.Response
    :return: (錯誤碼, token 或 None)
    """
    try:
        html = resp.text

        # 1. 嘗試從 hidden input 抓 (for /login 頁面)
        match = re.search(r'name="_token"\s+value="([^"]+)"', html)
        if match:
            return ResultCode.SUCCESS, match.group(1)

        # 2. 嘗試從 JavaScript data 抓 (for 首頁打卡頁)
        match = re.search(r"'_token'\s*:\s*'([^']+)'", html)
        if match:
            return ResultCode.SUCCESS, match.group(1)

        return ResultCode.tools_response_token_missing, None

    except Exception:
        return ResultCode.tools_response_token_failed, None
