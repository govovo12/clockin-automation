# workspace/tools/logger/stdout_tee.py
"""
Stdout Tee 工具模組
-----------------------------------
把所有 print() / stdout / stderr 同步輸出到主控台與 log 檔。

目前搭配 paths.generate_log_path()：
- 每天一個檔案，例如：2025-9-15.log
- 每次程式重新執行時會覆蓋舊檔
"""

import sys, io
from workspace.config import paths

_log_fp = None

class _Tee(io.TextIOBase):
    def __init__(self, *streams):
        self._streams = streams
    def write(self, s):
        for st in self._streams:
            st.write(s)
        return len(s)
    def flush(self):
        for st in self._streams:
            try:
                st.flush()
            except Exception:
                pass

def enable_stdout_logging(log_path: str | None = None,
                          overwrite: bool = True,
                          also_stderr: bool = True) -> str:
    """
    啟用 Tee，將 print()、stdout、stderr 同步輸出到 log 檔與主控台
    :param log_path: 指定 log 檔案路徑，若為 None 則自動產生
                     預設由 paths.generate_log_path() 生成「每天一檔」
    :param overwrite: True=覆蓋舊檔 (每日重新啟動會清空)，False=累加
    :param also_stderr: True=stderr 也會被 Tee
    :return: 使用中的 log 檔路徑
    """
    global _log_fp
    if log_path is None:
        log_path = paths.generate_log_path()  # 預設每天一檔
    mode = "w" if overwrite else "a"
    _log_fp = open(log_path, mode=mode, encoding="utf-8")
    sys.stdout = _Tee(sys.__stdout__, _log_fp)
    if also_stderr:
        sys.stderr = _Tee(sys.__stderr__, _log_fp)
    return log_path

def disable_stdout_logging():
    """
    關閉 Tee，恢復原始 stdout/stderr
    """
    global _log_fp
    try:
        if _log_fp:
            _log_fp.flush()
            _log_fp.close()
    finally:
        _log_fp = None
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
