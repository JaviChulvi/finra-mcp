from __future__ import annotations

import pytest

from finra_mcp.config import FinraConfig


def test_config_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FINRA_API_TOKEN", "token-123")
    monkeypatch.setenv("FINRA_BASE_URL", "https://api.example.test/")
    monkeypatch.setenv("FINRA_TIMEOUT", "7.5")

    config = FinraConfig.from_env()

    assert config.api_token == "token-123"
    assert config.base_url == "https://api.example.test"
    assert config.timeout == 7.5


def test_config_rejects_non_url_base() -> None:
    with pytest.raises(ValueError, match="HTTP"):
        FinraConfig(base_url="api.finra.org")
