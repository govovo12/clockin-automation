# workspace/tasks/login/env_check_task.py
"""
任務模組：檢查並組合環境變數
"""

import os
from dotenv import load_dotenv
from workspace.config.error_code import ResultCode
from workspace.tools.printer.debug_printer import debug_log


def _to_bool(val: str) -> bool:
    """把環境變數的字串安全轉成布林值"""
    return str(val).strip().lower() in {"1", "true", "t", "yes", "y", "on"}


def check_env_vars():
    """
    檢查必要的環境變數，並組成完整 URL
    :return: (錯誤碼, dict 或 None)
    """
    load_dotenv()

    base_keys = [
        "CLOCK_PROTOCOL",
        "CLOCK_HOST",
        "CLOCK_LOGIN_PATH",
        "CLOCK_IN_PATH",
        "CLOCK_OUT_PATH",
        "CLOCK_PAGE_PATH",
        "CLOCK_USERNAME",
        "CLOCK_PASSWORD",
        "debug",
    ]

    # 確認所有 key 都存在
    missing_keys = [k for k in base_keys if not os.getenv(k)]
    if missing_keys:
        return ResultCode.task_env_missing_key, None

    # 組 base url
    base_url = f"{os.getenv('CLOCK_PROTOCOL')}{os.getenv('CLOCK_HOST')}"

    # 新增 dry_run
    dry_run = _to_bool(os.getenv("DRY_RUN", "false"))

    # 組合需要的值
    selected_values = {
        "CLOCK_USERNAME": os.getenv("CLOCK_USERNAME"),
        "CLOCK_PASSWORD": os.getenv("CLOCK_PASSWORD"),
        "CLOCK_LOGIN_URL": f"{base_url}{os.getenv('CLOCK_LOGIN_PATH')}",
        "CLOCK_IN_URL": f"{base_url}{os.getenv('CLOCK_IN_PATH')}",
        "CLOCK_OUT_URL": f"{base_url}{os.getenv('CLOCK_OUT_PATH')}",
        "CLOCK_PAGE_URL": f"{base_url}{os.getenv('CLOCK_PAGE_PATH')}",
        "debug": _to_bool(os.getenv("debug")),
        "dry_run": dry_run,
    }

    # Debug 輸出（密碼照原樣印，因為你之前要求不要遮罩）
    debug_log(selected_values["debug"], "env_check_task", "讀取到的環境變數：")
    for k, v in selected_values.items():
        debug_log(selected_values["debug"], "env_check_task", f"  {k} = {v}")

    return ResultCode.SUCCESS, selected_values
