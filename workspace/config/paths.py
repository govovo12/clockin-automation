# workspace/config/paths.py
"""
Paths 工具模組
統一管理專案路徑，避免硬寫路徑
可以透過 ROOT_DEPTH 調整往上跳幾層
"""

import os
import sys
from datetime import datetime

# --- 可調整的變數 ---
ROOT_DEPTH = 2  # 往上跳幾層 (預設: 2 層，從 config → workspace → project_root)

if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
    # PyInstaller 打包模式
    ROOT_DIR = sys._MEIPASS
else:
    # 原始碼模式
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = current_dir
    for _ in range(ROOT_DEPTH):
        root_dir = os.path.dirname(root_dir)
    ROOT_DIR = root_dir

# --- 常用路徑 ---
ENV_FILE = os.path.join(ROOT_DIR, ".env")
WORKSPACE_DIR = os.path.join(ROOT_DIR, "workspace")
DATA_DIR = os.path.join(WORKSPACE_DIR, "data")  # 新增 data 資料夾

# --- Log 資料夾 ---
LOG_DIR = os.path.join(ROOT_DIR, "log")
os.makedirs(LOG_DIR, exist_ok=True)  # 確保 log 資料夾存在


def generate_log_path() -> str:
    """
    依照當前日期產生 log 檔名，例如 2025-9-15.log
    每次執行會覆蓋舊檔
    """
    now = datetime.now()
    filename = f"{now.year}-{now.month}-{now.day}.log"
    return os.path.join(LOG_DIR, filename)
