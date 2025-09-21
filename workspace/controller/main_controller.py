"""
總控制器
Step 1: 載入 ENV (debug)
Step 2: 呼叫假日判斷控制器
Step 3: 呼叫登入控制器
Step 4: 呼叫 Telegram 控制器
"""

# 🟢 工具模組
from workspace.tools.loader.env_loader import load_env, get_env
from workspace.tools.printer.debug_printer import print_context

# 🟠 子控制器
from workspace.controller.schedule_controller import run_schedule_check
from workspace.controller.login_controller import run_login_flow
from workspace.controller.telegram_controller import run_telegram_flow

# 🔵 Config
from workspace.config.error_code import ResultCode


def run_main_flow():
    """
    總控制器流程
    Step 1: 載入 env -> 取得 debug
    Step 2: 呼叫假日判斷控制器
    Step 3: 呼叫登入控制器
    Step 4: 呼叫 Telegram 控制器
    """
    context = {}

    print("=== 開始執行打卡流程 ===")

    # Step 1: 載入 env -> 取得 debug
    print("===Step 1: 載入環境變數 debug===")
    code = load_env()
    if code != ResultCode.SUCCESS:
        return code   # ❌ env 出錯 → 直接停止

    debug = get_env("DEBUG", "false").lower() == "true"
    context["debug"] = debug
    if debug:
        print_context(debug, "Step 1 結束時", context)

    # Step 2: 假日 / 請假判斷
    print("===Step 2: 呼叫假日判斷控制器===")
    schedule_code, schedule_ctx = run_schedule_check()
    context.update(schedule_ctx)
    context["schedule_controller_code"] = schedule_code

    if debug:
        print_context(debug, "Step 2 結束時", context)

    # Step 3: 登入打卡（只有在 skip_login=False 時才跑）
    if not context.get("skip_login", False):
        print("===Step 3: 呼叫登入控制器===")
        login_code, login_result = run_login_flow()
        context["login_controller_code"] = login_code
        if isinstance(login_result, dict) and "clockin_msg" in login_result:
            context["clockin_msg"] = login_result["clockin_msg"]

        if debug:
            print_context(debug, "Step 3 結束時", context)
    else:
        print("===Step 3: 跳過登入打卡===")

    # Step 4: TG 通知（無論前面成功/失敗/跳過都會跑）
    print("===Step 4: 呼叫 Telegram 控制器===")
    tg_code = run_telegram_flow(context)
    if debug:
        print_context(debug, "Step 4 結束時", context)

    if tg_code != ResultCode.SUCCESS:
        return tg_code   # ❌ TG 出錯 → 停止

    return ResultCode.SUCCESS
