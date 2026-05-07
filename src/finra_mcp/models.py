"""Pydantic models for FINRA Query API requests and responses."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from finra_mcp.errors import ReadOnlyViolationError

CompareType = Literal[
    "EQUAL",
    "NOT_EQUAL",
    "LESS",
    "LESS_OR_EQUAL",
    "GREATER",
    "GREATER_OR_EQUAL",
    "CONTAINS",
    "STARTS_WITH",
    "ENDS_WITH",
    "IN",
]


class CompareFilter(BaseModel):
    fieldName: str
    compareType: str
    fieldValue: Any


class DateRangeFilter(BaseModel):
    fieldName: str
    startDate: str | None = None
    endDate: str | None = None


class DomainFilter(BaseModel):
    fieldName: str
    values: list[Any] = Field(default_factory=list)

    @model_validator(mode="before")
    @classmethod
    def normalize_value_key(cls, data: Any) -> Any:
        if isinstance(data, dict) and "values" not in data and "fieldValues" in data:
            data = dict(data)
            data["values"] = data.pop("fieldValues")
        return data


class SortField(BaseModel):
    fieldName: str
    sortOrder: Literal["ASC", "DESC"] = "ASC"


class QueryPayload(BaseModel):
    """Read-only FINRA Query API filter payload."""

    model_config = ConfigDict(populate_by_name=True)

    compareFilters: list[CompareFilter | dict[str, Any]] | None = None
    dateRangeFilters: list[DateRangeFilter | dict[str, Any]] | None = None
    domainFilters: list[DomainFilter | dict[str, Any]] | None = None
    fields: list[str] | None = None
    limit: int | None = Field(default=None, ge=0)
    offset: int | None = Field(default=None, ge=0)
    sortFields: list[SortField | dict[str, Any] | str] | None = None
    async_: bool | None = Field(default=None, alias="async")

    @field_validator("fields")
    @classmethod
    def non_empty_fields(cls, value: list[str] | None) -> list[str] | None:
        if value is not None and any(not field for field in value):
            raise ValueError("fields must not contain empty names")
        return value

    def to_finra_payload(self, *, exclude_none: bool = True) -> dict[str, Any]:
        return self.model_dump(by_alias=True, exclude_none=exclude_none)


READ_ONLY_QUERY_KEYS = {
    "compareFilters",
    "dateRangeFilters",
    "domainFilters",
    "fields",
    "limit",
    "offset",
    "sortFields",
    "async",
}

FORBIDDEN_PAYLOAD_WORDS = {
    "acknowledge",
    "create",
    "delete",
    "mutate",
    "send",
    "submit",
    "subscribe",
    "unsubscribe",
    "update",
    "upload",
}


def validate_read_only_payload(payload: dict[str, Any]) -> None:
    """Reject non-Query-API or mutating POST payloads."""
    unknown = set(payload) - READ_ONLY_QUERY_KEYS
    if unknown:
        unknown_list = ", ".join(sorted(unknown))
        raise ReadOnlyViolationError(
            "POST payloads are restricted to read-only FINRA Query API search/filter keys. "
            f"Unsupported keys: {unknown_list}"
        )

    lowered_keys = {key.lower() for key in payload}
    forbidden = lowered_keys & FORBIDDEN_PAYLOAD_WORDS
    if forbidden:
        raise ReadOnlyViolationError(
            "Refusing a payload that appears to request a non-read-only operation: "
            + ", ".join(sorted(forbidden))
        )


class PaginationHeaders(BaseModel):
    """MCP-friendly FINRA pagination and request metadata."""

    total: int | None = None
    limit: int | None = None
    offset: int | None = None
    returned: int | None = None
    max_limit: int | None = None
    payload_max_size: int | None = None
    request_id: str | None = None
    data_api_version: str | None = None
    data_version: str | None = None
    location: str | None = None
    raw: dict[str, str] = Field(default_factory=dict)


class QueryResult(BaseModel):
    data: Any
    pagination: PaginationHeaders = Field(default_factory=PaginationHeaders)
    status_code: int
    headers: dict[str, str] = Field(default_factory=dict)
