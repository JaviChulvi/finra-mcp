from __future__ import annotations

import asyncio
from typing import Any

import pytest

from finra_mcp.tools import equity, finra_content, firm, fixed_income, registration


def run(coro: Any) -> Any:
    return asyncio.run(coro)


@pytest.mark.parametrize(
    ("module", "query_name", "list_name", "group"),
    [
        (equity, "query_equity_dataset", "list_equity_datasets", "otcMarket"),
        (
            fixed_income,
            "query_fixed_income_dataset",
            "list_fixed_income_datasets",
            "fixedIncomeMarket",
        ),
        (
            finra_content,
            "query_finra_content_dataset",
            "list_finra_content_datasets",
            "finra",
        ),
        (firm, "query_firm_dataset", "list_firm_datasets", "firm"),
        (
            registration,
            "query_registration_dataset",
            "list_registration_datasets",
            "registration",
        ),
    ],
)
def test_convenience_wrappers_are_thin(
    monkeypatch: pytest.MonkeyPatch,
    module: Any,
    query_name: str,
    list_name: str,
    group: str,
) -> None:
    async def fake_query_dataset_with_filters(
        actual_group: str,
        dataset: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        return {"group": actual_group, "dataset": dataset, "kwargs": kwargs}

    async def fake_list_query_api_datasets(
        group: str | None = None,
        include_variants: bool = True,
    ) -> dict[str, Any]:
        return {"group": group, "include_variants": include_variants}

    monkeypatch.setattr(module, "query_dataset_with_filters", fake_query_dataset_with_filters)
    monkeypatch.setattr(module, "list_query_api_datasets", fake_list_query_api_datasets)

    query_response = run(getattr(module, query_name)("sampleDataset", fields=["fieldA"], limit=2))
    list_response = run(getattr(module, list_name)(include_variants=False))

    assert query_response["group"] == group
    assert query_response["dataset"] == "sampleDataset"
    assert query_response["kwargs"]["fields"] == ["fieldA"]
    assert query_response["kwargs"]["limit"] == 2
    assert list_response == {"group": group, "include_variants": False}
