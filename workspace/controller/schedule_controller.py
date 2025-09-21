# workspace/controller/schedule_controller.py
"""
子控制器：行程判斷 (Schedule Controller)
- Step 1: 載入 .env 並讀取 debug 值
- Step 2: 判斷國定假日
- Step 3: 判斷自訂請假日
"""

# 🟢 任務模組（依 Step 順序）
from workspace.tasks.schedule.env_task import load_debug_flag              # Step 1
from workspace.tasks.schedule.holiday_task import check_holiday           # Step 2
from workspace.tasks.schedule.leave_task import check_leave               # Step 3

# 🟠 工具模組
from workspace.tools.printer.debug_printer import print_context
from workspace.tools.printer.error_printer import print_result

# 🔵 Config 模組
from workspace.config.error_code import ResultCode


def run_schedule_check():
    """
    行程判斷流程
    :return: (ResultCode, dict) - code 與 context
    """
    context = {}
    context["skip_login"] = False   # 預設 False

    # Step 1: 載入 env 並取得 debug
    print("Step 1: 讀取環境變數 debug")
    code, context = load_debug_flag(context)
    print_result(code)
    if code != ResultCode.SUCCESS:
        context["skip_login"] = True   # 出錯 → 不用跑登入
        return code, context
    if context.get("debug", False):
        print_context(True, "Step 1 結束時", context)

    # Step 2: 判斷國定假日
    print("Step 2: 判斷國定假日")
    code, context = check_holiday(context)
    print_result(code)
    if code != ResultCode.SUCCESS:
        context["skip_login"] = True   # 假日 / 出錯 → 不跑登入
        return code, context
    if context.get("debug", False):
        print_context(True, "Step 2 結束時", context)

    # Step 3: 判斷自訂請假日
    print("Step 3: 判斷自訂請假日")
    code, context = check_leave(context)
    print_result(code)
    if code != ResultCode.SUCCESS:
        context["skip_login"] = True   # 請假 / 出錯 → 不跑登入
        return code, context
    if context.get("debug", False):
        print_context(True, "Step 3 結束時", context)

    # ✅ 全部成功 → 控制器成功碼
    context["skip_login"] = False
    return ResultCode.ctrl_schedule_success, context
