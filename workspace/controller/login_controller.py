# workspace/controller/login_controller.py
"""
登入流程控制器：Step 式流程
"""

# 🟢 任務模組（依 Step 順序）
from workspace.tasks.login.env_check_task import check_env_vars             # Step 1: 載入並檢查環境變數
from workspace.tasks.login.get_login_token_task import do_get_login_token   # Step 2: 取得登入頁 (cookie + login _token)
from workspace.tasks.login.login_task import do_login                       # Step 3: 登入
from workspace.tasks.login.get_clockin_token_task import get_clockin_token  # Step 4: 抓取打卡 _token
from workspace.tasks.login.time_check_task import get_current_time          # Step 5: 取得當前時間
from workspace.tasks.login.path_select_task import select_clock_path        # Step 6: 根據時間選擇打卡路徑
from workspace.tasks.login.clockin_task import do_clockin                   # Step 7: 嘗試打卡
from workspace.tasks.login.clockin_format_task import format_clockin_msg    # Step 8: 格式化打卡訊息

# 🟠 工具模組
from workspace.tools.printer.error_printer import print_result
from workspace.tools.printer.debug_printer import print_context

# 🔵 Config 模組
from workspace.config.error_code import ResultCode



def step1_check_env(context: dict):
    """Step 1: 載入並檢查環境變數"""
    print("Step 1: 讀取環境變數並檢查")
    code, envs = check_env_vars()
    if code != ResultCode.SUCCESS:
        print_result(code)
        return code, context

    context.update(envs)
    print_result(code)
    return ResultCode.SUCCESS, context


def step2_get_login_page(context: dict):
    """Step 2: 取得登入頁 (cookie + login _token)"""
    print("Step 2: 取得登入頁")
    code, context = do_get_login_token(context)
    if code != ResultCode.SUCCESS:
        print_result(code)
        return code, context

    print_result(code)
    return ResultCode.SUCCESS, context


def step3_do_login(context: dict):
    """Step 3: 登入"""
    print("Step 3: 登入")
    code, _ = do_login(context)
    if code != ResultCode.SUCCESS:
        print_result(code)
        return code, context

    print_result(code)
    return ResultCode.SUCCESS, context


def step4_get_token(context: dict):
    """Step 4: 從首頁抓取打卡用的 _token"""
    print("Step 4: 抓取打卡 _token")
    code, token = get_clockin_token(context)
    if code != ResultCode.SUCCESS:
        print_result(code)
        return code, context

    context["clockin_token"] = token
    print_result(code)
    return ResultCode.SUCCESS, context


def step5_get_time(context: dict):
    """Step 5: 取得當前時間"""
    print("Step 5: 取得當前時間")
    code, now = get_current_time(context)
    if code != ResultCode.SUCCESS:
        print_result(code)
        return code, context

    context["current_time"] = now
    print_result(code)
    return ResultCode.SUCCESS, context


def step6_select_path(context: dict):
    """Step 6: 根據時間選擇打卡路徑"""
    print("Step 6: 選擇打卡路徑")
    code, result = select_clock_path(context)
    if code != ResultCode.SUCCESS:
        print_result(code)
        return code, context

    context.update(result)
    context.pop("CLOCK_IN_URL", None)
    context.pop("CLOCK_OUT_URL", None)

    print_result(code)
    return ResultCode.SUCCESS, context


def step7_do_clockin(context: dict):
    """Step 7: 嘗試打卡"""
    print("Step 7: 嘗試打卡")
    code, result = do_clockin(context)
    if code != ResultCode.SUCCESS:
        print_result(code)
        return code, context

    # 控制器來塞資料
    context["clockin_summary"] = result

    print_result(code)
    return ResultCode.SUCCESS, context


def step8_format_msg(context: dict):
    """Step 8: 格式化打卡訊息"""
    print("Step 8: 格式化打卡訊息")
    result = format_clockin_msg(context)

    # 塞回 context
    context.update(result)

    # 成功訊息（這裡不需要錯誤碼，因為能跑到這裡就代表成功）
    print("[✅ 打卡訊息]", context["clockin_msg"])
    return ResultCode.SUCCESS, context


def run_login_flow():
    """最外層：登入控制流程"""
    context = {}

    # Step 1
    code, context = step1_check_env(context)
    if code != ResultCode.SUCCESS:
        return code, context
    print_context(context.get("debug", False), "Step 1 結束時", context, mask_keys=["CLOCK_PASSWORD"])

    # Step 2
    code, context = step2_get_login_page(context)
    if code != ResultCode.SUCCESS:
        return code, context
    print_context(context.get("debug", False), "Step 2 結束時", context, mask_keys=["CLOCK_PASSWORD"])

    # Step 3
    code, context = step3_do_login(context)
    if code != ResultCode.SUCCESS:
        return code, context
    print_context(context.get("debug", False), "Step 3 結束時", context, mask_keys=["CLOCK_PASSWORD"])

    # Step 4
    code, context = step4_get_token(context)
    if code != ResultCode.SUCCESS:
        return code, context
    print_context(context.get("debug", False), "Step 4 結束時", context, mask_keys=["CLOCK_PASSWORD"])

    # Step 5
    code, context = step5_get_time(context)
    if code != ResultCode.SUCCESS:
        return code, context
    print_context(context.get("debug", False), "Step 5 結束時", context, mask_keys=["CLOCK_PASSWORD"])

    # Step 6
    code, context = step6_select_path(context)
    if code != ResultCode.SUCCESS:
        return code, context
    print_context(context.get("debug", False), "Step 6 結束時", context, mask_keys=["CLOCK_PASSWORD"])

    # 檢查 dry_run
    if context.get("dry_run", False):
        context["clockin_msg"] = "流程成功（dry run 模式，未執行打卡動作）"
        print_result(ResultCode.SUCCESS)
        print("[✅ 打卡訊息]", context["clockin_msg"])
        return ResultCode.SUCCESS, context

    # Step 7
    code, context = step7_do_clockin(context)
    if code != ResultCode.SUCCESS:
        return code, context
    print_context(context.get("debug", False), "Step 7 結束時", context, mask_keys=["CLOCK_PASSWORD"])

    # Step 8
    code, context = step8_format_msg(context)
    if code != ResultCode.SUCCESS:
        return code, context
    print_context(context.get("debug", False), "Step 8 結束時", context, mask_keys=["CLOCK_PASSWORD"])

    # ✅ 全部成功：回傳 success 與 Step 7 塞進 context 的 clockin_msg
    return ResultCode.SUCCESS, {"clockin_msg": context.get("clockin_msg")}

