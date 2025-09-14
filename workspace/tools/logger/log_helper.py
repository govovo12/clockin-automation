# workspace/tools/logger/log_helper.py
"""
Log Helper 工具模組
由呼叫者決定 log_file，要不要覆蓋檔案
"""

import logging


def get_logger(log_file: str, name: str = "workspace_logger", overwrite: bool = True):
    """
    建立一個 logger，輸出到指定檔案
    :param log_file: log 檔路徑
    :param name: logger 名稱
    :param overwrite: True=覆蓋舊檔, False=累加
    :return: logger 物件
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # 避免重複加 handler
    if not logger.handlers:
        mode = "w" if overwrite else "a"
        file_handler = logging.FileHandler(log_file, mode=mode, encoding="utf-8")
        file_handler.setLevel(logging.INFO)

        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

    return logger
