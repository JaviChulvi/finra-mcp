from __future__ import annotations

import asyncio
from typing import Any

import pytest

from finra_mcp.models import PaginationHeaders, QueryResult
from finra_mcp.server import CONVENIENCE_TOOLS, GENERIC_TOOLS, create_server
from finra_mcp.tools import query


def run(coro: Any) -> Any:
    return asyncio.run(coro)


class PublicToolSmokeClient:
    calls: list[tuple[str, tuple[Any, ...], dict[str, Any]]]

    def __init__(self) -> None:
        self.calls = []

    async def __aenter__(self) -> PublicToolSmokeClient:
        return self

    async def __aexit__(self, *exc_info: object) -> None:
        return None

    def _result(
        self,
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

    async def list_datasets(self, *args: Any, **kwargs: Any) -> QueryResult:
        self.calls.append(("list_datasets", args, kwargs))
        return self._result([{"datasetGroup": "otcMarket", "datasetName": "regShoDaily"}])

    async def get_metadata(self, *args: Any, **kwargs: Any) -> QueryResult:
        self.calls.append(("get_metadata", args, kwargs))
        return self._result(
            {
                "datasetGroup": "otcMarket",
                "datasetName": "regShoDaily",
                "fields": [{"name": "tradeReportDate"}, {"name": "marketCode"}],
                "partitionFields": ["tradeReportDate"],
                "primaryIdField": "tradeReportDate",
            }
        )

    async def query_dataset_get(self, *args: Any, **kwargs: Any) -> QueryResult:
        self.calls.append(("query_dataset_get", args, kwargs))
        return self._result(
            [{"tradeReportDate": "2026-05-06", "marketCode": "B"}],
            total=1,
            limit=kwargs.get("limit"),
            offset=kwargs.get("offset", 0),
            returned=1,
        )

    async def query_dataset_post_readonly(self, *args: Any, **kwargs: Any) -> QueryResult:
        self.calls.append(("query_dataset_post_readonly", args, kwargs))
        payload = args[2] if len(args) > 2 else {}
        return self._result(
            [{"marketCode": "B", "payload_keys": sorted(payload)}],
            total=1,
            limit=payload.get("limit"),
            offset=payload.get("offset", 0),
            returned=1,
        )

    async def get_record_by_id(self, *args: Any, **kwargs: Any) -> QueryResult:
        self.calls.append(("get_record_by_id", args, kwargs))
        return self._result({"firmCrdNumber": args[2]})

    async def start_async_query(self, *args: Any, **kwargs: Any) -> QueryResult:
        self.calls.append(("start_async_query", args, kwargs))
        return self._result(
            {"requestId": "req-1"},
            status_code=202,
            location="/async-requests/group/otcMarket/name/regShoDaily/req-1",
        )

    async def get_async_query_status(self, *args: Any, **kwargs: Any) -> QueryResult:
        self.calls.append(("get_async_query_status", args, kwargs))
        return self._result(
            {
                "requestId": "req-1",
                "status": "complete",
                "resultLink": "https://example.test/result.csv",
                "expires": "2026-05-07T12:00:00Z",
            }
        )

    async def download_async_query_result(self, *args: Any, **kwargs: Any) -> QueryResult:
        self.calls.append(("download_async_query_result", args, kwargs))
        return self._result("tradeReportDate,marketCode\n2026-05-06,B\n")


PUBLIC_TOOL_SMOKE_ARGS: dict[str, dict[str, Any]] = {
    "download_async_query_result": {"result_link": "https://example.test/result.csv"},
    "get_async_query_status": {
        "group": "otcMarket",
        "dataset": "regShoDaily",
        "request_id": "req-1",
    },
    "get_dataset_details": {
        "group": "otcMarket",
        "dataset": "regShoDaily",
        "include_metadata": False,
    },
    "get_dataset_fields": {"group": "otcMarket", "dataset": "regShoDaily"},
    "get_dataset_metadata": {"group": "otcMarket", "dataset": "regShoDaily"},
    "get_dataset_record_by_id": {
        "group": "firm",
        "dataset": "firmProfile",
        "record_id": "123",
    },
    "list_equity_datasets": {"include_variants": False},
    "list_finra_content_datasets": {"include_variants": False},
    "list_firm_datasets": {"include_variants": False},
    "list_fixed_income_datasets": {"include_variants": False},
    "list_query_api_datasets": {"group": "otcMarket", "include_variants": False},
    "list_query_api_groups": {},
    "list_registration_datasets": {"include_variants": False},
    "query_dataset_get": {
        "group": "otcMarket",
        "dataset": "regShoDaily",
        "fields": ["tradeReportDate", "marketCode"],
        "limit": 1,
    },
    "query_dataset_paginated": {
        "group": "otcMarket",
        "dataset": "regShoDaily",
        "fields": ["marketCode"],
        "page_size": 1,
        "max_pages": 1,
        "method": "POST",
    },
    "query_dataset_post_readonly": {
        "group": "otcMarket",
        "dataset": "regShoDaily",
        "payload": {"fields": ["marketCode"], "limit": 1},
    },
    "query_dataset_with_filters": {
        "group": "otcMarket",
        "dataset": "regShoDaily",
        "fields": ["marketCode"],
        "limit": 1,
    },
    "query_equity_dataset": {
        "dataset": "regShoDaily",
        "fields": ["marketCode"],
        "limit": 1,
    },
    "query_finra_content_dataset": {
        "dataset": "finraRulebook",
        "fields": ["ruleNumber"],
        "limit": 1,
    },
    "query_firm_dataset": {
        "dataset": "firmProfile",
        "fields": ["firmCrdNumber"],
        "limit": 1,
    },
    "query_fixed_income_dataset": {
        "dataset": "treasuryDailyAggregates",
        "fields": ["reportDate"],
        "limit": 1,
    },
    "query_registration_dataset": {
        "dataset": "registrationValidationIndividual",
        "fields": ["crdNumber"],
        "limit": 1,
    },
    "start_async_query": {
        "group": "otcMarket",
        "dataset": "regShoDaily",
        "payload": {"limit": 1},
    },
}


async def call_public_tool(tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    mcp = create_server()
    result = await mcp.call_tool(tool_name, arguments, run_middleware=False)
    assert result.structured_content is not None
    return result.structured_content


def test_server_registers_expected_readonly_tools() -> None:
    async def main() -> None:
        mcp = create_server()
        tools = await mcp.list_tools(run_middleware=False)
        names = {tool.name for tool in tools}

        expected = {tool.__name__ for tool in [*GENERIC_TOOLS, *CONVENIENCE_TOOLS]}
        assert expected <= names
        assert len(names) == len(expected)
        forbidden = {
            "create",
            "update",
            "delete",
            "submit",
            "acknowledge",
            "upload",
            "subscribe",
            "unsubscribe",
            "send",
        }
        assert names.isdisjoint(forbidden)

    asyncio.run(main())


def test_all_registered_tools_have_public_smoke_coverage() -> None:
    expected = {tool.__name__ for tool in [*GENERIC_TOOLS, *CONVENIENCE_TOOLS]}

    assert set(PUBLIC_TOOL_SMOKE_ARGS) == expected


@pytest.mark.parametrize("tool_name", sorted(PUBLIC_TOOL_SMOKE_ARGS))
def test_public_tool_smoke(
    monkeypatch: pytest.MonkeyPatch,
    tool_name: str,
) -> None:
    stub = PublicToolSmokeClient()
    monkeypatch.setattr(query, "FinraQueryClient", lambda: stub)

    response = run(call_public_tool(tool_name, PUBLIC_TOOL_SMOKE_ARGS[tool_name]))

    assert response["status"] == "ok"
