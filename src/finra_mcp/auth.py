"""Authentication helpers for FINRA API requests."""

from __future__ import annotations

from collections.abc import Mapping

from finra_mcp.errors import MissingCredentialsError


def bearer_auth_headers(token: str | None) -> dict[str, str]:
    """Return FINRA Bearer authentication headers for a token."""
    if not token:
        return {}
    return {"Authorization": f"Bearer {token}"}


def require_bearer_token(token: str | None) -> str:
    """Return a token or raise a clear credential error."""
    if token:
        return token
    raise MissingCredentialsError(
        "FINRA_API_TOKEN is required for this FINRA Query API request. "
        "Set FINRA_API_TOKEN in the environment or pass api_token explicitly."
    )


def merge_auth_headers(headers: Mapping[str, str] | None, token: str | None) -> dict[str, str]:
    merged = dict(headers or {})
    merged.update(bearer_auth_headers(token))
    return merged
