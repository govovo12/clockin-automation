# workspace/tasks/login/clockin_format_task.py
"""
Step 8: 格式化打卡紀錄
"""

from workspace.tools.printer.debug_printer import debug_log


def format_clockin_msg(context: dict):
    """將打卡紀錄轉換成中文訊息，回傳 dict"""
    debug = context.get("debug", False)
    summary = context.get("clockin_summary", {})

    date = summary.get("date", "未知日期")
    work_time = summary.get("work_time") or "尚未打卡"
    off_time = summary.get("off_work_time")

    if off_time:
        msg = f"{date} 打卡成功，上班 {work_time}，下班 {off_time}"
    else:
        msg = f"{date} 打卡成功，上班 {work_time}，下班尚未打卡"

    # debug 模式印訊息
    debug_log(debug, "clockin_format_task", f"組成的打卡訊息: {msg}")

    return {"clockin_msg": msg}
