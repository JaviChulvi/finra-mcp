from __future__ import annotations

import asyncio
from typing import Any

import pytest

from finra_mcp.models import PaginationHeaders, QueryResult
from finra_mcp.tools import query


def run(coro: Any) -> Any:
    return asyncio.run(coro)


class StubClient:
    def __init__(self, results: list[QueryResult] | None = None) -> None:
        self.results = results or []
        self.calls: list[tuple[str, tuple[Any, ...], dict[str, Any]]] = []

    async def __aenter__(self) -> StubClient:
        return self

    async def __aexit__(self, *exc_info: object) -> None:
        return None

    def next_result(self) -> QueryResult:
        return self.results.pop(0)

    async def get_metadata(self, *args: Any, **kwargs: Any) -> QueryResult:
        self.calls.append(("get_metadata", args, kwargs))
        return self.next_result()

    async def query_dataset_post_readonly(self, *args: Any, **kwargs: Any) -> QueryResult:
        self.calls.append(("query_dataset_post_readonly", args, kwargs))
        return self.next_result()

    async def query_dataset_get(self, *args: Any, **kwargs: Any) -> QueryResult:
        self.calls.append(("query_dataset_get", args, kwargs))
        return self.next_result()

    async def get_record_by_id(self, *args: Any, **kwargs: Any) -> QueryResult:
        self.calls.append(("get_record_by_id", args, kwargs))
        return self.next_result()

    async def start_async_query(self, *args: Any, **kwargs: Any) -> QueryResult:
        self.calls.append(("start_async_query", args, kwargs))
        return self.next_result()

    async def get_async_query_status(self, *args: Any, **kwargs: Any) -> QueryResult:
        self.calls.append(("get_async_query_status", args, kwargs))
        return self.next_result()

    async def download_async_query_result(self, *args: Any, **kwargs: Any) -> QueryResult:
        self.calls.append(("download_async_query_result", args, kwargs))
        return self.next_result()


def result(
    data: Any,
    *,
    status_code: int = 200,
    total: int | None = None,
    limit: int | None = None,
    offset: int | None = None,
    returned: int | None = None,
    location: str | None = None,
) -> QueryResult:
    return QueryResult(
        data=data,
        status_code=status_code,
        pagination=PaginationHeaders(
            total=total,
            limit=limit,
            offset=offset,
            returned=returned,
            location=location,
        ),
    )


def test_list_groups_and_datasets_from_catalog() -> None:
    groups = query.list_query_api_groups()
    datasets = run(query.list_query_api_datasets(group="otcMarket"))

    assert groups["status"] == "ok"
    assert any(group["group"] == "otcMarket" for group in groups["groups"])
    assert datasets["status"] == "ok"
    assert len(datasets["datasets"]) >= 8


def test_get_dataset_fields_uses_metadata(monkeypatch: pytest.MonkeyPatch) -> None:
    stub = StubClient(
        [
            result(
                {
                    "datasetGroup": "otcMarket",
                    "datasetName": "regShoDaily",
                    "fields": [{"name": "tradeReportDate"}, {"name": "marketCode"}],
                }
            )
        ]
    )
    monkeypatch.setattr(query, "FinraQueryClient", lambda: stub)

    response = run(query.get_dataset_fields("otcMarket", "regShoDaily"))

    assert response["status"] == "ok"
    assert response["field_names"] == ["tradeReportDate", "marketCode"]
    assert stub.calls[0][0] == "get_metadata"


def test_query_dataset_with_filters_builds_readonly_post(monkeypatch: pytest.MonkeyPatch) -> None:
    stub = StubClient([result([{"marketCode": "OTC"}], total=1, limit=1, offset=0, returned=1)])
    monkeypatch.setattr(query, "FinraQueryClient", lambda: stub)

    response = run(
        query.query_dataset_with_filters(
            "otcMarket",
            "regShoDaily",
            compare_filters=[
                {"fieldName": "marketCode", "compareType": "EQUAL", "fieldValue": "OTC"}
            ],
            fields=["marketCode"],
            limit=1,
        )
    )

    assert response["status"] == "ok"
    assert response["data"] == [{"marketCode": "OTC"}]
    call = stub.calls[0]
    assert call[0] == "query_dataset_post_readonly"
    assert call[1][0:2] == ("otcMarket", "regShoDaily")
    assert call[1][2]["compareFilters"][0]["fieldName"] == "marketCode"
    assert call[1][2]["fields"] == ["marketCode"]


def test_post_tool_rejects_non_readonly_payload() -> None:
    response = run(query.query_dataset_post_readonly("firm", "firmProfile", {"submit": True}))

    assert response["status"] == "error"
    assert response["error"] == "ReadOnlyViolationError"


def test_paginated_query_collects_pages(monkeypatch: pytest.MonkeyPatch) -> None:
    stub = StubClient(
        [
            result([{"id": 1}, {"id": 2}], total=3, limit=2, offset=0, returned=2),
            result([{"id": 3}], total=3, limit=2, offset=2, returned=1),
        ]
    )
    monkeypatch.setattr(query, "FinraQueryClient", lambda: stub)

    response = run(
        query.query_dataset_paginated(
            "otcMarket",
            "regShoDaily",
            page_size=2,
            max_pages=5,
            method="GET",
        )
    )

    assert response["status"] == "ok"
    assert response["record_count"] == 3
    assert response["page_count"] == 2
    assert stub.calls[1][2]["offset"] == 2


def test_async_tools(monkeypatch: pytest.MonkeyPatch) -> None:
    stub = StubClient(
        [
            result(None, status_code=202, location="/async-requests/group/g/name/n/req"),
            result(
                {
                    "requestId": "req",
                    "status": "complete",
                    "resultLink": "https://example.test/result.csv",
                    "expires": "2026-05-07T12:00:00Z",
                }
            ),
            result("a,b\n1,2\n"),
        ]
    )
    monkeypatch.setattr(query, "FinraQueryClient", lambda: stub)

    start = run(query.start_async_query("g", "n", {"limit": 10}))
    status = run(query.get_async_query_status("g", "n", "req"))
    downloaded = run(query.download_async_query_result("https://example.test/result.csv"))

    assert start["async_status_url"] == "/async-requests/group/g/name/n/req"
    assert status["async_status"] == "complete"
    assert status["result_link"] == "https://example.test/result.csv"
    assert downloaded["data"] == "a,b\n1,2\n"


@pytest.mark.parametrize("argument,value", [
    ("compare_filters", [{"fieldName": "x"}]),
    ("date_range_filters", [{"fieldName": "x"}]),
    ("domain_filters", [{"fieldName": "x"}]),
    ("sort_fields", [{"fieldName": "x", "sortType": "ASC"}]),
])
def test_paginated_get_rejects_unsupported_arguments(
    monkeypatch: pytest.MonkeyPatch, argument: str, value: list[Any]
) -> None:
    stub = StubClient([result([])])
    monkeypatch.setattr(query, "FinraQueryClient", lambda: stub)
    response = run(query.query_dataset_paginated("g", "n", method="GET", **{argument: value}))
    assert response["status"] == "error"
    assert argument in response["message"]
    assert not stub.calls


def test_paginated_get_transmits_string_sort_fields(monkeypatch: pytest.MonkeyPatch) -> None:
    stub = StubClient([result([])])
    monkeypatch.setattr(query, "FinraQueryClient", lambda: stub)
    response = run(query.query_dataset_paginated("g", "n", method="GET", sort_fields=["x"]))
    assert response["status"] == "ok"
    assert stub.calls[0][2]["sort_fields"] == ["x"]
