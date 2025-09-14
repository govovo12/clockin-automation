# workspace/tools/env_loader.py
"""
Env Loader 工具模組
負責載入與讀取 .env 檔案
"""

import os
from dotenv import load_dotenv
from workspace.config.paths import ROOT_DIR
from workspace.config.error_code import ResultCode


def load_env() -> int:
    """
    嘗試載入 .env 檔案
    :return: ResultCode.SUCCESS 或對應錯誤碼
    """
    env_path = os.path.join(ROOT_DIR, ".env")
    if not os.path.exists(env_path):
        return ResultCode.tools_env_not_found

    success = load_dotenv(env_path)
    if not success:
        return ResultCode.tools_env_load_failed

    return ResultCode.SUCCESS


def get_env(key: str, default=None):
    """
    安全取得環境變數
    :param key: 環境變數名稱
    :param default: 預設值（可選）
    :return: 變數值 | None
    """
    return os.getenv(key, default)
