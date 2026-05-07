"""FINRA Query API error types and response mapping."""

from __future__ import annotations

from typing import Any


class FinraError(Exception):
    """Base exception for FINRA MCP errors."""


class MissingCredentialsError(FinraError):
    """Raised when a request requires FINRA credentials but none are configured."""


class FinraAPIError(FinraError):
    """Raised for FINRA API failures."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
        request_id: str | None = None,
        details: Any | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.request_id = request_id
        self.details = details

    def to_dict(self) -> dict[str, Any]:
        return {
            "error": self.__class__.__name__,
            "message": self.message,
            "status_code": self.status_code,
            "request_id": self.request_id,
            "details": self.details,
        }


class FinraAuthenticationError(FinraAPIError):
    """Raised for missing, invalid, or expired credentials."""


class FinraAuthorizationError(FinraAPIError):
    """Raised when credentials are valid but insufficient for a dataset."""


class FinraValidationError(FinraAPIError):
    """Raised for invalid FINRA Query API parameters or payloads."""


class FinraRateLimitError(FinraAPIError):
    """Raised when the FINRA API rate-limits a request."""


class ReadOnlyViolationError(FinraError):
    """Raised when a payload or tool request is outside read-only Query API scope."""


def _body_message(body: Any) -> str | None:
    if isinstance(body, dict):
        for key in ("message", "statusDescription", "error", "title", "detail"):
            value = body.get(key)
            if value:
                return str(value)
    if isinstance(body, str) and body.strip():
        return body.strip()
    return None


def finra_error_from_response(
    *,
    status_code: int,
    body: Any,
    request_id: str | None = None,
) -> FinraAPIError:
    """Create a typed FINRA exception for an HTTP response."""
    message = _body_message(body) or f"FINRA API request failed with HTTP {status_code}"
    kwargs = {"status_code": status_code, "request_id": request_id, "details": body}

    if status_code == 401:
        return FinraAuthenticationError(message, **kwargs)
    if status_code == 403:
        return FinraAuthorizationError(message, **kwargs)
    if status_code == 429:
        return FinraRateLimitError(message, **kwargs)
    if status_code in {400, 404, 409, 422}:
        return FinraValidationError(message, **kwargs)
    return FinraAPIError(message, **kwargs)
