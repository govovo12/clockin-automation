# workspace/tools/printer/error_printer.py
"""
Error Printer 工具模組
負責統一輸出錯誤碼與訊息
（Log 的寫入交給 stdout_tee 負責，不在這裡重複）
"""

from workspace.config.error_code import (
    ResultCode,
    ERROR_MESSAGES,
    SUCCESS_CODES,
    TOOL_ERROR_CODES,
    TASK_ERROR_CODES,
    CTRL_ERROR_CODES,
)


def print_result(code: int):
    """
    根據錯誤碼輸出統一格式訊息
    """
    msg = ERROR_MESSAGES.get(code, f"未知錯誤碼: {code}")

    if code in SUCCESS_CODES:
        print(f"[✅ 成功] code={code} msg={msg}")
        return

    if code in TOOL_ERROR_CODES:
        print(f"[❌ 工具失敗] code={code} msg={msg}")
        return

    if code in TASK_ERROR_CODES:
        print(f"[❌ 任務失敗] code={code} msg={msg}")
        return

    if code in CTRL_ERROR_CODES:
        print(f"[❌ 控制器失敗] code={code} msg={msg}")
        return

    print(f"[❌ 未知失敗] code={code} msg={msg}")
