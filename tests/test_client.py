from __future__ import annotations

import asyncio
import json
from typing import Any

import httpx
import pytest

from finra_mcp.client import (
    FinraQueryClient,
    async_status_path,
    data_path,
    metadata_path,
    parse_pagination_headers,
    record_path,
)
from finra_mcp.config import FinraConfig
from finra_mcp.errors import (
    FinraAuthenticationError,
    FinraRateLimitError,
)
from finra_mcp.models import QueryPayload


def run(coro: Any) -> Any:
    return asyncio.run(coro)


def make_client(handler: httpx.MockTransport) -> FinraQueryClient:
    http_client = httpx.AsyncClient(
        base_url="https://api.finra.test",
        transport=handler,
    )
    return FinraQueryClient(
        FinraConfig(api_token="secret", base_url="https://api.finra.test"), http_client=http_client
    )


def test_path_builders_quote_components() -> None:
    assert (
        data_path("fixed Income", "name/with/slash")
        == "/data/group/fixed%20Income/name/name%2Fwith%2Fslash"
    )
    assert record_path("g", "n", "id/1") == "/data/group/g/name/n/id/id%2F1"
    assert metadata_path("g", "n") == "/metadata/group/g/name/n"
    assert async_status_path("g", "n", "r/1") == "/async-requests/group/g/name/n/r%2F1"


def test_parse_pagination_headers() -> None:
    headers = httpx.Headers(
        {
            "record-total": "123",
            "record-limit": "10",
            "record-offset": "20",
            "total-records-on-page": "10",
            "finra-api-request-id": "req-1",
            "location": "/async-requests/group/g/name/n/req-1",
        }
    )

    parsed = parse_pagination_headers(headers)

    assert parsed.total == 123
    assert parsed.limit == 10
    assert parsed.offset == 20
    assert parsed.returned == 10
    assert parsed.request_id == "req-1"
    assert parsed.location == "/async-requests/group/g/name/n/req-1"


def test_get_dataset_sends_bearer_and_query_params() -> None:
    async def main() -> None:
        def handler(request: httpx.Request) -> httpx.Response:
            assert request.method == "GET"
            assert request.url.path == "/data/group/otcMarket/name/regShoDaily"
            assert request.url.params["limit"] == "5"
            assert request.headers["authorization"] == "Bearer secret"
            return httpx.Response(
                200,
                json=[{"symbol": "ABC"}],
                headers={"record-total": "1", "record-limit": "5"},
            )

        client = make_client(httpx.MockTransport(handler))
        result = await client.query_dataset_get("otcMarket", "regShoDaily", limit=5)

        assert result.data == [{"symbol": "ABC"}]
        assert result.pagination.total == 1
        await client.close()

    run(main())


def test_metadata_can_be_requested_without_token() -> None:
    async def main() -> None:
        def handler(request: httpx.Request) -> httpx.Response:
            assert request.method == "GET"
            assert request.url.path == "/metadata/group/otcMarket/name/regShoDaily"
            assert "authorization" not in request.headers
            return httpx.Response(200, json={"fields": [{"name": "tradeReportDate"}]})

        http_client = httpx.AsyncClient(
            base_url="https://api.finra.test",
            transport=httpx.MockTransport(handler),
        )
        client = FinraQueryClient(
            FinraConfig(api_token=None, base_url="https://api.finra.test"),
            http_client=http_client,
        )

        result = await client.get_metadata("otcMarket", "regShoDaily")

        assert result.data["fields"][0]["name"] == "tradeReportDate"
        await client.close()

    run(main())


def test_data_requests_can_run_without_token_for_public_datasets() -> None:
    async def main() -> None:
        def handler(request: httpx.Request) -> httpx.Response:
            assert request.url.path == "/data/group/otcMarket/name/regShoDaily"
            assert "authorization" not in request.headers
            return httpx.Response(
                200,
                json=[{"marketCode": "B"}],
                headers={"record-total": "1", "record-limit": "1"},
            )

        http_client = httpx.AsyncClient(
            base_url="https://api.finra.test",
            transport=httpx.MockTransport(handler),
        )
        client = FinraQueryClient(
            FinraConfig(api_token=None, base_url="https://api.finra.test"),
            http_client=http_client,
        )

        result = await client.query_dataset_get("otcMarket", "regShoDaily", limit=1)

        assert result.data == [{"marketCode": "B"}]
        await client.close()

    run(main())


def test_post_readonly_payload_validation_and_serialization() -> None:
    async def main() -> None:
        def handler(request: httpx.Request) -> httpx.Response:
            payload = json.loads(request.content.decode())
            assert payload == {
                "compareFilters": [
                    {"fieldName": "marketCode", "compareType": "EQUAL", "fieldValue": "OTC"}
                ],
                "limit": 1,
            }
            return httpx.Response(200, json=[{"ok": True}])

        client = make_client(httpx.MockTransport(handler))
        payload = QueryPayload(
            compareFilters=[
                {"fieldName": "marketCode", "compareType": "EQUAL", "fieldValue": "OTC"}
            ],
            limit=1,
        )
        result = await client.query_dataset_post_readonly("otcMarket", "regShoDaily", payload)

        assert result.data == [{"ok": True}]
        await client.close()

    run(main())


def test_start_async_query_sets_async_flag() -> None:
    async def main() -> None:
        def handler(request: httpx.Request) -> httpx.Response:
            payload = json.loads(request.content.decode())
            assert payload["async"] is True
            return httpx.Response(
                202,
                json={"requestId": "req-123"},
                headers={"location": "/async-requests/group/g/name/n/req-123"},
            )

        client = make_client(httpx.MockTransport(handler))
        result = await client.start_async_query("g", "n", {"limit": 5})

        assert result.status_code == 202
        assert result.pagination.location == "/async-requests/group/g/name/n/req-123"
        await client.close()

    run(main())


def test_error_mapping() -> None:
    async def main() -> None:
        def auth_handler(_: httpx.Request) -> httpx.Response:
            return httpx.Response(
                401, json={"message": "Unauthorized"}, headers={"finra-api-request-id": "r1"}
            )

        client = make_client(httpx.MockTransport(auth_handler))
        with pytest.raises(FinraAuthenticationError) as exc_info:
            await client.query_dataset_get("g", "n")
        assert exc_info.value.request_id == "r1"
        await client.close()

        def rate_handler(_: httpx.Request) -> httpx.Response:
            return httpx.Response(429, json={"message": "Too many requests"})

        client = make_client(httpx.MockTransport(rate_handler))
        with pytest.raises(FinraRateLimitError):
            await client.query_dataset_get("g", "n")
        await client.close()

    run(main())
