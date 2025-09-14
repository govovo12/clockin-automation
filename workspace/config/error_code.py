# workspace/config/error_code.py
"""
錯誤碼集中管理
- 工具錯誤碼 (1000-1999)
- 任務錯誤碼 (2000-2999)
- 控制器錯誤碼 (3000-3999)
"""


class ResultCode:
    SUCCESS = 0

    # ---------------- 工具錯誤碼 (1000-1999) ----------------
    tools_env_not_found = 1001
    tools_env_load_failed = 1002
    tools_http_request_failed = 1003
    tools_http_invalid_response = 1004
    tools_response_parse_failed = 1005
    tools_response_missing_key = 1006
    tools_response_invalid_format = 1007
    tools_response_token_failed = 1008
    tools_response_token_missing = 1009
    tools_http_request_timeout   = 1010
    tools_http_connection_error  = 1011
    tools_http_unknown_error     = 1012
    tools_json_not_found   = 1013  # 找不到 JSON 檔案
    tools_json_parse_error = 1014  # JSON 格式錯誤
    tools_json_unknown_err = 1015  # JSON 讀取未知錯誤
    tools_telegram_request_failed = 1016      # Telegram API 請求失敗 (例如網路錯誤)
    tools_telegram_invalid_response = 1017    # Telegram 回應非 200 或格式錯誤

    # ---------------- 任務錯誤碼 (2000-2999) ----------------
    task_env_missing_key = 2001
    task_login_failed = 2002
    task_time_check_failed = 2005
    task_clockin_no_token = 2006
    task_clockin_invalid_response = 2007
    task_clockin_no_id = 2008
    task_clockin_no_records = 2009
    task_clockin_json_error = 2010
    task_login_token_parse_error = 2011  # 無法解析 login 頁面的 _token
    task_skip_holiday = 2012   # 今天是國定假日，不需要打卡
    task_skip_leave   = 2013   # 今天是自訂請假日，不需要打卡
    task_telegram_missing_key = 2014       # 缺少必要的環境變數 (TOKEN 或 CHAT_ID)
    task_telegram_invalid_enable = 2015    # ENABLE_TELEGRAM 值不合法
    task_notify_disabled = 2016   # 通知未開啟，不執行通知模組

    # ---------------- 控制器錯誤碼 (3000-3999) ----------------
    ctrl_success = 3000
    ctrl_failed  = 3001
    ctrl_schedule_success = 3002   # 今日為工作日，正常打卡

# ---------------- 分類集合 ----------------
SUCCESS_CODES = {ResultCode.SUCCESS,
                 ResultCode.ctrl_success,
                 ResultCode.ctrl_schedule_success, 
                 }

TOOL_ERROR_CODES = {
    ResultCode.tools_env_not_found,
    ResultCode.tools_env_load_failed,
    ResultCode.tools_http_request_failed,
    ResultCode.tools_http_invalid_response,
    ResultCode.tools_response_parse_failed,
    ResultCode.tools_response_missing_key,
    ResultCode.tools_response_invalid_format,
    ResultCode.tools_response_token_failed,
    ResultCode.tools_response_token_missing,
    ResultCode.tools_http_request_timeout,
    ResultCode.tools_http_connection_error,
    ResultCode.tools_http_unknown_error,
    ResultCode.tools_json_not_found,      
    ResultCode.tools_json_parse_error,    
    ResultCode.tools_json_unknown_err,    
    ResultCode.tools_telegram_request_failed,
    ResultCode.tools_telegram_invalid_response,
    
}

TASK_ERROR_CODES = {
    ResultCode.task_env_missing_key,
    ResultCode.task_login_failed,
    ResultCode.task_time_check_failed,
    ResultCode.task_clockin_no_token,
    ResultCode.task_clockin_invalid_response,
    ResultCode.task_clockin_no_id,        
    ResultCode.task_clockin_no_records,   
    ResultCode.task_clockin_json_error,
    ResultCode.task_login_token_parse_error,
    ResultCode.task_skip_holiday,     
    ResultCode.task_skip_leave, 
    ResultCode.task_telegram_missing_key,
    ResultCode.task_telegram_invalid_enable,
    ResultCode.task_notify_disabled,  
}

CTRL_ERROR_CODES = {
    ResultCode.ctrl_failed,    
}
GENERIC_ERROR_CODES = set()


# ---------------- 訊息區 ----------------
ERROR_MESSAGES = {
    ResultCode.SUCCESS: "操作成功",
    # 工具錯誤訊息
    ResultCode.tools_env_not_found: "找不到 .env 檔案",
    ResultCode.tools_env_load_failed: ".env 載入失敗",
    ResultCode.tools_http_request_failed: "HTTP 請求失敗",
    ResultCode.tools_http_invalid_response: "HTTP 回應狀態碼無效",
    ResultCode.tools_response_parse_failed: "回應解析失敗（JSON 格式錯誤）",
    ResultCode.tools_response_missing_key: "回應缺少必要欄位",
    ResultCode.tools_response_invalid_format: "回應格式錯誤（非預期型別）",
    ResultCode.tools_response_token_failed: "從 HTML/JS 抓取 _token 失敗",
    ResultCode.tools_response_token_missing: "HTML/JS 回應缺少 _token",
    ResultCode.tools_http_request_timeout: "HTTP 請求超時",
    ResultCode.tools_http_connection_error: "網路連線失敗（DNS 或伺服器拒絕）",
    ResultCode.tools_http_unknown_error: "HTTP 請求發生未知錯誤",
    ResultCode.tools_json_not_found: "找不到 JSON 檔案",
    ResultCode.tools_json_parse_error: "JSON 格式錯誤或解析失敗",
    ResultCode.tools_json_unknown_err: "讀取 JSON 發生未知錯誤",
    ResultCode.tools_telegram_request_failed: "Telegram API 請求失敗",
    ResultCode.tools_telegram_invalid_response: "Telegram 回應無效或解析失敗",


    # 任務錯誤訊息
    ResultCode.task_env_missing_key: "必要環境變數缺失",
    ResultCode.task_login_failed: "登入失敗（帳號密碼錯誤或伺服器拒絕）",
    ResultCode.task_time_check_failed: "時間判斷失敗",
    ResultCode.task_clockin_no_token: "打卡回應缺少必要的 token",
    ResultCode.task_clockin_invalid_response: "打卡回應格式錯誤",
    ResultCode.task_clockin_no_id: "打卡回應缺少 id",
    ResultCode.task_clockin_no_records: "打卡回應沒有任何紀錄",
    ResultCode.task_clockin_json_error: "打卡回應 JSON 格式錯誤或解析失敗",
    ResultCode.task_login_token_parse_error:"無法解析login頁面的_token",
    ResultCode.task_skip_holiday: "今日為國定假日，不需打卡",
    ResultCode.task_skip_leave: "今日為自訂請假日，不需打卡",
    ResultCode.task_telegram_missing_key: "缺少必要的環境變數 (TELEGRAM_BOT_TOKEN 或 TELEGRAM_CHAT_ID)",
    ResultCode.task_telegram_invalid_enable: "ENABLE_TELEGRAM 值不合法，請設定為 true/false",
    ResultCode.task_notify_disabled: "通知未開啟，不執行通知模組",

    # 控制器錯誤訊息
    ResultCode.ctrl_success: "控制器流程成功",
    ResultCode.ctrl_schedule_success: "今日為工作日，正常打卡",   # ✅ 新增
    ResultCode.ctrl_failed: "控制器流程失敗",

}
