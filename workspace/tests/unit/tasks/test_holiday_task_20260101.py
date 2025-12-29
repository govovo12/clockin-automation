import pytest
from unittest.mock import patch

import workspace.tasks.schedule.holiday_task as holiday_task
from workspace.tasks.schedule.holiday_task import check_holiday
from workspace.config.error_code import ResultCode


pytestmark = [
    pytest.mark.unit,
    pytest.mark.task,
    pytest.mark.holiday,
]


def test_20260101_should_skip_holiday():
    context = {"debug": True}

    with patch.object(
        holiday_task,
        "today_str",
        return_value="20260101"
    ):
        code, _ = check_holiday(context)

    assert code == ResultCode.task_skip_holiday
