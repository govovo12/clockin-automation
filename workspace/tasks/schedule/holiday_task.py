"""
任務模組：判斷今天是否為國定假日
"""

import datetime
import os
from workspace.tools.loader.json_loader import load_json
from workspace.config.paths import DATA_DIR
from workspace.config.error_code import ResultCode
from workspace.tools.printer.debug_printer import debug_log


def check_holiday(context: dict):
    """
    判斷今天是否為國定假日
    :param context: 控制器傳入的 context
    :return: (ResultCode, dict)
    """
    debug = context.get("debug", False)
    today = datetime.date.today().strftime("%Y%m%d")  # holiday.json 用 YYYYMMDD
    holiday_path = os.path.join(DATA_DIR, "2025.json")  # ✅ 修正路徑

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
