# workspace/config/http_headers.py

# ⚠️ 注意：
# 這裡的 DEFAULT_HEADERS 是新版系統用「模仿瀏覽器表單提交」的版本。
# - Accept / Content-Type：模仿真瀏覽器
# - User-Agent / Accept-Language：固定常用值
# - Referer / Cookie / X-XSRF-TOKEN 等屬於「動態」資訊，
#   會在 task 執行時由程式碼補上，不要硬寫在這裡。

DEFAULT_HEADERS = {
    # 模仿真瀏覽器 UA（固定值，不會動態改）
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/140.0.0.0 Safari/537.36"
    ),

    # 語言偏好（固定值）
    "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",

    # 接收內容類型（模仿瀏覽器，固定值）
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;q=0.9,"
        "image/avif,image/webp,image/apng,*/*;q=0.8,"
        "application/signed-exchange;v=b3;q=0.7"
    ),

    # 表單提交格式（固定值）
    # ⚠️ 這裡不要加 charset=UTF-8，因為真瀏覽器不會帶
    "Content-Type": "application/x-www-form-urlencoded",
}

# ➜ 動態補上的部分（不要寫死在 DEFAULT_HEADERS）：
#   - Referer：由 task 依當前 URL 填入
#   - Cookie：由 requests.Session 自動帶
#   - X-XSRF-TOKEN：由程式碼從 cookie 讀取後補上
