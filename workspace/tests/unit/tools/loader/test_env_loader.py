import pytest
import workspace.tools.loader.env_loader as env_loader
from workspace.config.error_code import ResultCode

# 檔案級標記
pytestmark = [pytest.mark.unit, pytest.mark.tools, pytest.mark.loader]


def test_load_env_file_not_found(tmp_path, monkeypatch):
    """反向測試: 沒有 .env 檔案"""
    # 模擬讓 ROOT_DIR 指向空目錄
    monkeypatch.setattr(env_loader, "ROOT_DIR", str(tmp_path))

    code = env_loader.load_env()
    assert code == ResultCode.tools_env_not_found


def test_load_env_file_exists_and_valid(tmp_path, monkeypatch):
    """正向測試: .env 存在且可正確載入"""
    env_file = tmp_path / ".env"
    env_file.write_text("MY_KEY=123\n")

    monkeypatch.setattr(env_loader, "ROOT_DIR", str(tmp_path))

    code = env_loader.load_env()
    assert code == ResultCode.SUCCESS
    assert env_loader.get_env("MY_KEY") == "123"


def test_load_env_file_exists_but_empty(tmp_path, monkeypatch):
    """邊界測試: .env 存在但內容空"""
    env_file = tmp_path / ".env"
    env_file.write_text("")  # 空檔案

    monkeypatch.setattr(env_loader, "ROOT_DIR", str(tmp_path))

    code = env_loader.load_env()
    # python-dotenv 對空檔案 load 會回傳 False
    assert code == ResultCode.tools_env_load_failed


def test_get_env_with_default(monkeypatch):
    """邊界測試: 變數不存在時，應回傳 default"""
    monkeypatch.delenv("NOT_EXIST_KEY", raising=False)
    value = env_loader.get_env("NOT_EXIST_KEY", default="fallback")
    assert value == "fallback"
