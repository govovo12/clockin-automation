"""
Telegram 控制器
Step 1: 建立 Telegram 專用 context
Step 2: 翻譯代碼為訊息字串
Step 3: 發送 Telegram 通知
"""

# 🟢 任務模組
from workspace.tasks.notify.telegram_context_task import build_telegram_context
from workspace.tasks.notify.telegram_message_task import translate_codes_to_messages
from workspace.tasks.notify.telegram_send_task import send_telegram_notification

# 🟠 工具模組
from workspace.tools.printer.error_printer import print_result
from workspace.tools.printer.debug_printer import print_context

# 🔵 Config
from workspace.config.error_code import ResultCode


def run_telegram_flow(main_context: dict):
    """
    Telegram 通知流程控制器
    Step 1: 建立 Telegram 專用 context
    Step 2: 翻譯代碼為訊息字串
    Step 3: 發送 Telegram 通知
    :param main_context: 總控制器傳來的 context
    :return: ResultCode
    """
    context = {}

    # Step 1
    print("Step 1: 建立 Telegram 專用 context")
    code, tg_data = build_telegram_context(main_context)
    print_result(code)
    if code != ResultCode.SUCCESS:
        return code
    context.update(tg_data)

    if context.get("debug", False):
        print_context(True, "Step 1 結束時", context)

    # Step 2
    print("Step 2: 翻譯代碼為訊息字串")
    code, translated = translate_codes_to_messages(context)
    print_result(code)
    if code != ResultCode.SUCCESS:
        return code
    context.update(translated)

    if context.get("debug", False):
        print_context(True, "Step 2 結束時", context)

    # Step 3
    print("Step 3: 發送 Telegram 通知")
    code = send_telegram_notification(context)
    print_result(code)
    if code != ResultCode.SUCCESS:
        return code

    if context.get("debug", False):
        print_context(True, "Step 3 結束時", context)

    # ✅ 全部成功
    return ResultCode.SUCCESS
