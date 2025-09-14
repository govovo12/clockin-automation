# workspace/tasks/schedule/leave_task.py
"""
任務模組：判斷今天是否為自訂請假日
"""

import os
import datetime
from workspace.config.paths import DATA_DIR
from workspace.config.error_code import ResultCode
from workspace.tools.loader.json_loader import load_json
from workspace.tools.printer.debug_printer import debug_log


def check_leave(context: dict):
    """
    讀取 leaves.json，若今天在清單內則回傳 task_skip_leave，否則 SUCCESS
    - 僅在 context['debug'] 為 True 時輸出兩行 debug：
      1) 今天的日期
      2) json 讀到的日期清單
    :return: (ResultCode, dict)
    """
    debug = context.get("debug", False)
    today = datetime.date.today().strftime("%Y-%m-%d")
    leave_path = os.path.join(DATA_DIR, "leaves.json")

    code, data = load_json(leave_path)
    if code != ResultCode.SUCCESS:
        # 讀檔/解析出錯時，直接把工具層錯誤碼往上拋
        return code, context

    leaves = (data or {}).get("leaves", []) or []

    # Debug：只印你要的兩行
    debug_log(debug, "leave_task", f"今天的日期: {today}")
    debug_log(debug, "leave_task", f"json讀到的日期: {leaves}")

    if today in leaves:
        return ResultCode.task_skip_leave, context

    return ResultCode.SUCCESS, context
