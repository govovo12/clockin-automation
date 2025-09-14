# workspace/tasks/clock/path_select_task.py
"""
任務模組：根據時間選擇打卡路徑
"""

from workspace.config.error_code import ResultCode
from workspace.tools.printer.debug_printer import debug_log


def select_clock_path(context: dict):
    """
    根據當前時間選擇要使用的打卡路徑
    :param context: dict (必須包含 current_time, CLOCK_IN_URL, CLOCK_OUT_URL, debug)
    :return: (錯誤碼, {"clock_url": str} 或 None)
    """
    try:
        now = context.get("current_time")
        in_url = context.get("CLOCK_IN_URL")
        out_url = context.get("CLOCK_OUT_URL")
        debug = context.get("debug", False)

        # 基本檢查
        if not all([now, in_url, out_url]):
            return ResultCode.task_env_missing_key, None

        # 判斷 clock path
        if now.hour < 12:
            clock_path = in_url
        else:
            clock_path = out_url

        # Debug 模式印出結果
        debug_log(debug, "path_select_task", f"選擇的打卡路徑: {clock_path}")

        # ✅ 改成回傳 clock_url，和 Step 6 一致
        return ResultCode.SUCCESS, {"clock_url": clock_path}

    except Exception:
        return ResultCode.task_env_missing_key, None
