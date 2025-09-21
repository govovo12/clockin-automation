"""
單元測試：time_utils 工具
驗證台灣時區轉換是否正確
"""

import pytest
from datetime import datetime
import pytz
from workspace.tools.time.time_utils import now, today_str, today_date

# 一行式檔案級標記
pytestmark = [pytest.mark.unit, pytest.mark.tools, pytest.mark.time]


def test_now_timezone(monkeypatch):
    """
    模擬 UTC 2025-09-20 23:50，驗證轉換成台灣 2025-09-21 07:50
    """
    fake_utc = datetime(2025, 9, 20, 23, 50, tzinfo=pytz.UTC)

    class FakeDatetime(datetime):
        @classmethod
        def now(cls, tz=None):
            return fake_utc.astimezone(tz) if tz else fake_utc

    monkeypatch.setattr("workspace.tools.time.time_utils.datetime", FakeDatetime)

    tw_now = now()
    assert tw_now.year == 2025
    assert tw_now.month == 9
    assert tw_now.day == 21
    assert tw_now.hour == 7
    assert tw_now.minute == 50


def test_today_str_and_date(monkeypatch):
    """
    模擬 UTC 2025-09-20 23:50，驗證 date 與字串格式正確
    """
    fake_utc = datetime(2025, 9, 20, 23, 50, tzinfo=pytz.UTC)

    class FakeDatetime(datetime):
        @classmethod
        def now(cls, tz=None):
            return fake_utc.astimezone(tz) if tz else fake_utc

    monkeypatch.setattr("workspace.tools.time.time_utils.datetime", FakeDatetime)

    assert today_date().strftime("%Y-%m-%d") == "2025-09-21"
    assert today_str("%Y%m%d") == "20250921"

def test_from_timestamp():
    """
    驗證 timestamp 轉台灣時間是否正確
    UTC 2025-09-20 23:50 = 台灣 2025-09-21 07:50
    """
    # 先算一個 UTC timestamp
    fake_utc = datetime(2025, 9, 20, 23, 50, tzinfo=pytz.UTC)
    ts = int(fake_utc.timestamp())

    from workspace.tools.time.time_utils import from_timestamp
    tw_dt = from_timestamp(ts)

    assert tw_dt.year == 2025
    assert tw_dt.month == 9
    assert tw_dt.day == 21
    assert tw_dt.hour == 7
    assert tw_dt.minute == 50
