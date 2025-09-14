"""
JSON Loader 工具
單一職責：讀取 JSON 檔案並回傳 dict
"""

import json
from workspace.config.error_code import ResultCode


def load_json(file_path: str):
    """
    讀取 JSON 檔案
    :param file_path: JSON 檔案的完整路徑
    :return: (ResultCode, dict 或 None)
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return ResultCode.SUCCESS, data
    except FileNotFoundError:
        return ResultCode.tools_json_not_found, None

    except json.JSONDecodeError:
        return ResultCode.tools_response_parse_failed, None
    except Exception:
        return ResultCode.tools_http_unknown_error, None
