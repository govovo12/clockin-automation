"""
任務模組：判斷今天是否為國定假日
"""

import os
from workspace.tools.loader.json_loader import load_json
from workspace.config.paths import DATA_DIR
from workspace.config.error_code import ResultCode
from workspace.tools.printer.debug_printer import debug_log
from workspace.tools.time.time_utils import today_str   # ✅ 改成用工具


def check_holiday(context: dict):
    """
    判斷今天是否為國定假日
    :param context: 控制器傳入的 context
    :return: (ResultCode, dict)
    """
    debug = context.get("debug", False)
    today = today_str("%Y%m%d")  # ✅ 使用 time_utils，固定台灣時區
    year = today[:4]
    holiday_path = os.path.join(DATA_DIR, f"{year}.json")


    # 呼叫工具讀取 JSON
    code, data = load_json(holiday_path)
    if code != ResultCode.SUCCESS:
        return code, context  # 直接往上拋工具層錯誤碼

    # 找今天的紀錄
    today_info = next((d for d in data if d.get("date") == today), None)

    # Debug 輸出
    debug_log(debug, "holiday_task", f"今天的日期: {today}")
    debug_log(debug, "holiday_task", f"json讀到的今天紀錄: {today_info}")

    # 判斷是否假日
    if today_info and today_info.get("isHoliday", False):
        return ResultCode.task_skip_holiday, context

    return ResultCode.SUCCESS, context
