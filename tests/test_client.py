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


def test_result_download_is_isolated_and_rejects_unsafe_destinations(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import socket

    monkeypatch.setattr(
        socket,
        "getaddrinfo",
        lambda *args, **kwargs: [
            (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("93.184.216.34", 443))
        ],
    )

    async def main() -> None:
        calls = []

        def handler(request: httpx.Request) -> httpx.Response:
            calls.append(request)
            assert request.url.host == "93.184.216.34"
            assert request.headers["host"] == "results.example.test"
            assert request.extensions["sni_hostname"] == "results.example.test"
            assert "authorization" not in request.headers
            assert "cookie" not in request.headers
            assert request.url.query == b"signature=a%2Fb&expires=123"
            return httpx.Response(200, text="ok")

        real_client = httpx.AsyncClient
        injected = real_client(
            headers={"Authorization": "Bearer injected", "Cookie": "secret=x"},
            transport=httpx.MockTransport(handler),
        )

        def download_client(**kwargs: Any) -> httpx.AsyncClient:
            assert kwargs["follow_redirects"] is False
            assert kwargs["trust_env"] is False
            return real_client(transport=httpx.MockTransport(handler), **kwargs)

        client = FinraQueryClient(
            FinraConfig(api_token="secret", result_hosts=["results.example.test"]),
            http_client=injected,
        )
        monkeypatch.setattr(httpx, "AsyncClient", download_client)
        for url in (
            "http://results.example.test/x",
            "https://evil.test/x",
            "https://127.0.0.1/x",
            "https://results.example.test@evil.test/x",
        ):
            with pytest.raises(ValueError):
                await client.download_async_query_result(url)
        result = await client.download_async_query_result(
            "https://results.example.test/x?signature=a%2Fb&expires=123"
        )
        assert result.data == "ok"
        assert len(calls) == 1
        await injected.aclose()

    run(main())


def test_result_download_does_not_follow_redirects(monkeypatch: pytest.MonkeyPatch) -> None:
    import socket

    monkeypatch.setattr(
        socket,
        "getaddrinfo",
        lambda *args, **kwargs: [
            (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("93.184.216.34", 443))
        ],
    )

    async def main() -> None:
        real_client = httpx.AsyncClient

        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(302, headers={"location": "http://127.0.0.1/"})

        def download_client(**kwargs: Any) -> httpx.AsyncClient:
            return real_client(transport=httpx.MockTransport(handler), **kwargs)

        injected = real_client(transport=httpx.MockTransport(handler))
        client = FinraQueryClient(
            FinraConfig(result_hosts=["results.example.test"]), http_client=injected
        )
        monkeypatch.setattr(httpx, "AsyncClient", download_client)
        with pytest.raises(ValueError, match="redirect"):
            await client.download_async_query_result("https://results.example.test/x")
        await injected.aclose()

    run(main())


@pytest.mark.parametrize("address", ["127.0.0.1", "10.0.0.1", "169.254.169.254", "::1"])
def test_result_download_rejects_private_dns(monkeypatch: pytest.MonkeyPatch, address: str) -> None:
    import socket

    async def main() -> None:
        real_client = httpx.AsyncClient
        calls = []

        def handler(request: httpx.Request) -> httpx.Response:
            calls.append(request)
            return httpx.Response(200, text="private response")

        monkeypatch.setattr(
            socket,
            "getaddrinfo",
            lambda *args, **kwargs: [(socket.AF_INET, socket.SOCK_STREAM, 6, "", (address, 443))],
        )
        monkeypatch.setattr(
            httpx,
            "AsyncClient",
            lambda **kwargs: real_client(transport=httpx.MockTransport(handler), **kwargs),
        )
        client = FinraQueryClient(
            FinraConfig(result_hosts=["results.example.test"]), http_client=real_client()
        )
        try:
            with pytest.raises(ValueError, match="public"):
                await client.download_async_query_result("https://results.example.test/file")
            assert not calls
        finally:
            await client.close()

    run(main())
