# workspace/tasks/login/time_check_task.py
"""
任務模組：取得當前時間（台北時區）
"""

from datetime import datetime
import pytz
from workspace.config.error_code import ResultCode
from workspace.tools.printer.debug_printer import debug_log


def get_current_time(context: dict):
    """
    取得台北當前時間
    :param context: dict
    :return: (錯誤碼, datetime 或 None)
    """
    try:
        tz = pytz.timezone("Asia/Taipei")
        taipei_now = datetime.now(tz)

        # Debug 印時間
        debug = context.get("debug", False)
        debug_log(debug, "time_check_task", f"現在台北時間: {taipei_now.strftime('%Y-%m-%d %H:%M:%S')}")

        return ResultCode.SUCCESS, taipei_now
    except Exception as e:
        debug_log(context.get("debug", False), "time_check_task", f"取得時間失敗: {e}")
        return ResultCode.task_env_missing_key, None
