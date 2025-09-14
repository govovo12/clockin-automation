# workspace/tools/printer/debug_printer.py
"""
Debug Printer 工具
統一 debug 輸出格式，避免各模組重複寫 if debug 判斷
"""

def debug_log(debug: bool, tag: str, message: str):
    """
    Debug 輔助工具
    - debug: True 才會輸出
    - tag: 模組名稱或步驟名稱
    - message: 要印出的訊息
    """
    if not debug:
        return
    print(f"[DEBUG][{tag}] {message}")


def print_context(debug: bool, step_name: str, context: dict, mask_keys=None):
    """
    專門印 context 內容的 Debug 工具
    - debug: True 才會輸出
    - step_name: 例如 "Step 1 結束時"
    - context: 當前流程的 context dict
    - mask_keys: 需要隱藏值的 key list (例如 ["CLOCK_PASSWORD"])
    """
    if not debug:
        return

    print(f"[DEBUG] {step_name} context內容:")
    for key, value in context.items():
        if mask_keys and key in mask_keys:
            value = "******"
        print(f"    {key} = {value}")
