"""
工具模組：時間工具 (time_utils)
統一管理台灣時區的時間，避免 UTC 與本地混淆
"""

from datetime import datetime, date
import pytz

# 固定使用台灣時區
_TZ = pytz.timezone("Asia/Taipei")


def now() -> datetime:
    """
    取得台灣時區的 datetime
    :return: datetime 物件
    """
    return datetime.now(_TZ)


def today_str(fmt: str = "%Y%m%d") -> str:
    """
    取得今天日期字串（台灣時間）
    :param fmt: 日期格式，預設 YYYYMMDD
    :return: 日期字串
    """
    return now().strftime(fmt)


def today_date() -> date:
    """
    取得今天的 date 物件（台灣時間）
    :return: date 物件
    """
    return now().date()

def from_timestamp(ts: int | float) -> datetime:
    """
    把 timestamp (epoch 秒數, UTC 基準) 轉換成台灣時區的 datetime
    :param ts: 秒數 (int 或 float)
    :return: datetime (Asia/Taipei)
    """
    return datetime.fromtimestamp(ts, _TZ)