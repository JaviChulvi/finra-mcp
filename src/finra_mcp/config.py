"""Configuration loading for the FINRA MCP server."""

from __future__ import annotations

import os

from pydantic import BaseModel, Field, field_validator


class FinraConfig(BaseModel):
    """Runtime configuration for FINRA Query API access."""

    api_token: str | None = Field(default=None)
    base_url: str = Field(default="https://api.finra.org")
    timeout: float = Field(default=30.0, gt=0)

    @field_validator("base_url")
    @classmethod
    def normalize_base_url(cls, value: str) -> str:
        value = value.strip().rstrip("/")
        if not value.startswith(("http://", "https://")):
            raise ValueError("FINRA_BASE_URL must be an HTTP(S) URL")
        return value

    @classmethod
    def from_env(cls) -> FinraConfig:
        """Load configuration from environment variables."""
        timeout = os.getenv("FINRA_TIMEOUT")
        return cls(
            api_token=os.getenv("FINRA_API_TOKEN") or None,
            base_url=os.getenv("FINRA_BASE_URL") or "https://api.finra.org",
            timeout=float(timeout) if timeout else 30.0,
        )
