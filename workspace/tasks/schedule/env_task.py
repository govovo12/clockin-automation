"""
任務模組：讀取 .env 的 debug 值
"""

from workspace.tools.loader.env_loader import load_env, get_env
from workspace.config.error_code import ResultCode


def load_debug_flag(context: dict):
    """
    從 .env 讀取 debug 值並放入 context
    :param context: 控制器傳入的 context
    :return: (ResultCode, dict)
    """
    # 載入 .env
    code = load_env()
    if code != ResultCode.SUCCESS:
        return code, context

    debug_value = get_env("debug")
    if debug_value is None:
        return ResultCode.task_env_missing_key, context

    # 轉成布林，統一格式
    debug = str(debug_value).lower() in ["1", "true", "yes"]
    context["debug"] = debug

    return ResultCode.SUCCESS, context
