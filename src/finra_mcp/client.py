"""Reusable HTTP client for the read-only FINRA Query API."""

from __future__ import annotations

from collections.abc import Mapping
from contextlib import asynccontextmanager
from typing import Any
from urllib.parse import quote

import httpx

from finra_mcp.auth import bearer_auth_headers, require_bearer_token
from finra_mcp.config import FinraConfig
from finra_mcp.errors import finra_error_from_response
from finra_mcp.models import (
    PaginationHeaders,
    QueryPayload,
    QueryResult,
    validate_read_only_payload,
)


def _quote_path(value: str) -> str:
    return quote(value, safe="")


def data_path(group: str, dataset: str) -> str:
    return f"/data/group/{_quote_path(group)}/name/{_quote_path(dataset)}"


def record_path(group: str, dataset: str, record_id: str) -> str:
    return f"{data_path(group, dataset)}/id/{_quote_path(record_id)}"


def metadata_path(group: str, dataset: str) -> str:
    return f"/metadata/group/{_quote_path(group)}/name/{_quote_path(dataset)}"


def async_status_path(group: str, dataset: str, request_id: str) -> str:
    return (
        f"/async-requests/group/{_quote_path(group)}/name/{_quote_path(dataset)}/"
        f"{_quote_path(request_id)}"
    )


def _int_header(headers: httpx.Headers, *names: str) -> int | None:
    for name in names:
        value = headers.get(name)
        if value is None:
            continue
        try:
            return int(value)
        except ValueError:
            return None
    return None


def parse_pagination_headers(headers: httpx.Headers) -> PaginationHeaders:
    raw = {
        name: value
        for name, value in headers.items()
        if name.lower()
        in {
            "record-total",
            "record-count",
            "record-limit",
            "record-offset",
            "record-max-limit",
            "total-record-count",
            "total-records",
            "total-records-on-page",
            "response-payload-max-size",
            "finra-api-request-id",
            "x-request-id",
            "data-api-version",
            "data-version",
            "location",
        }
    }
    return PaginationHeaders(
        total=_int_header(headers, "record-total", "total-record-count", "total-records"),
        returned=_int_header(headers, "record-count", "total-records-on-page"),
        limit=_int_header(headers, "record-limit"),
        offset=_int_header(headers, "record-offset"),
        max_limit=_int_header(headers, "record-max-limit"),
        payload_max_size=_int_header(headers, "response-payload-max-size"),
        request_id=headers.get("finra-api-request-id") or headers.get("x-request-id"),
        data_api_version=headers.get("data-api-version"),
        data_version=headers.get("data-version"),
        location=headers.get("location"),
        raw=raw,
    )


class FinraQueryClient:
    """Async FINRA Query API client.

    The client only constructs Query API, metadata, dataset-discovery, and async-result
    URLs. It has no Submission API, Notification API, fileX, or mutating endpoints.
    """

    def __init__(
        self,
        config: FinraConfig | None = None,
        *,
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        self.config = config or FinraConfig.from_env()
        self._owned_client = http_client is None
        self._client = http_client or httpx.AsyncClient(
            base_url=self.config.base_url,
            timeout=self.config.timeout,
            headers={"Accept": "application/json", **bearer_auth_headers(self.config.api_token)},
        )

    async def close(self) -> None:
        if self._owned_client:
            await self._client.aclose()

    async def __aenter__(self) -> FinraQueryClient:
        return self

    async def __aexit__(self, *exc_info: object) -> None:
        await self.close()

    @asynccontextmanager
    async def session(self):
        try:
            yield self
        finally:
            await self.close()

    def _auth_headers(self, require_token: bool) -> dict[str, str]:
        if require_token:
            return bearer_auth_headers(require_bearer_token(self.config.api_token))
        return bearer_auth_headers(self.config.api_token)

    async def _request(
        self,
        method: str,
        path_or_url: str,
        *,
        require_token: bool = True,
        params: Mapping[str, Any] | None = None,
        json_payload: Mapping[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> QueryResult:
        request_headers = {"Accept": "application/json", **self._auth_headers(require_token)}
        if headers:
            request_headers.update(headers)
        response = await self._client.request(
            method,
            path_or_url,
            params={key: value for key, value in (params or {}).items() if value is not None},
            json=json_payload,
            headers=request_headers,
        )

        body: Any
        content_type = response.headers.get("content-type", "")
        if response.content and "application/json" in content_type:
            try:
                body = response.json()
            except ValueError:
                body = response.text
        elif response.content:
            body = response.text
        else:
            body = None

        pagination = parse_pagination_headers(response.headers)
        if response.is_error:
            raise finra_error_from_response(
                status_code=response.status_code,
                body=body,
                request_id=pagination.request_id,
            )
        return QueryResult(
            data=body,
            pagination=pagination,
            status_code=response.status_code,
            headers=dict(response.headers),
        )

    async def list_datasets(
        self,
        *,
        group: str | None = None,
        name: str | None = None,
    ) -> QueryResult:
        params = {"group": group, "name": name}
        return await self._request("GET", "/datasets", require_token=True, params=params)

    async def get_metadata(self, group: str, dataset: str) -> QueryResult:
        return await self._request("GET", metadata_path(group, dataset), require_token=False)

    async def query_dataset_get(
        self,
        group: str,
        dataset: str,
        *,
        fields: list[str] | None = None,
        limit: int | None = None,
        offset: int | None = None,
        sort_fields: list[str] | None = None,
        extra_params: Mapping[str, Any] | None = None,
    ) -> QueryResult:
        params: dict[str, Any] = dict(extra_params or {})
        params.update(
            {
                "fields": ",".join(fields) if fields else None,
                "limit": limit,
                "offset": offset,
                "sortFields": ",".join(sort_fields) if sort_fields else None,
            }
        )
        return await self._request(
            "GET", data_path(group, dataset), params=params, require_token=False
        )

    async def query_dataset_post_readonly(
        self,
        group: str,
        dataset: str,
        payload: QueryPayload | Mapping[str, Any],
    ) -> QueryResult:
        body = payload.to_finra_payload() if isinstance(payload, QueryPayload) else dict(payload)
        validate_read_only_payload(body)
        return await self._request(
            "POST",
            data_path(group, dataset),
            json_payload=body,
            require_token=False,
        )

    async def get_record_by_id(self, group: str, dataset: str, record_id: str) -> QueryResult:
        return await self._request(
            "GET", record_path(group, dataset, record_id), require_token=False
        )

    async def start_async_query(
        self,
        group: str,
        dataset: str,
        payload: QueryPayload | Mapping[str, Any] | None = None,
        *,
        method: str = "POST",
    ) -> QueryResult:
        method = method.upper()
        if method == "GET":
            body = payload.to_finra_payload() if isinstance(payload, QueryPayload) else payload
            if body:
                raise ValueError("Async GET does not support a payload; use POST")
            return await self._request(
                "GET",
                data_path(group, dataset),
                params={"async": "true"},
                require_token=False,
            )
        if method != "POST":
            raise ValueError("Async Query API requests must use GET or read-only POST")
        body = (
            payload.to_finra_payload() if isinstance(payload, QueryPayload) else dict(payload or {})
        )
        body["async"] = True
        validate_read_only_payload(body)
        return await self._request(
            "POST",
            data_path(group, dataset),
            json_payload=body,
            require_token=False,
        )

    async def get_async_query_status(
        self,
        group: str,
        dataset: str,
        request_id: str,
    ) -> QueryResult:
        return await self._request(
            "GET",
            async_status_path(group, dataset, request_id),
            require_token=True,
        )

    async def download_async_query_result(self, result_url: str) -> QueryResult:
        return await self._request("GET", result_url, require_token=False)
