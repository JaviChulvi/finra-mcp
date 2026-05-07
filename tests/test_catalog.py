from __future__ import annotations

from finra_mcp.discovery.catalog import fields_from_catalog, find_dataset, list_datasets, list_groups


def test_catalog_lists_required_groups() -> None:
    groups = {group["group"] for group in list_groups()}

    assert {"otcMarket", "fixedIncomeMarket", "finra", "firm", "registration"} <= groups


def test_catalog_contains_many_dataset_variants() -> None:
    datasets = list_datasets(include_variants=True)
    variant_count = sum(len(dataset["variants"]) for dataset in datasets)

    assert len(datasets) >= 40
    assert variant_count >= 75


def test_find_dataset_by_variant_name() -> None:
    dataset = find_dataset("otcMarket", "weeklySummaryMock")

    assert dataset is not None
    assert dataset["dataset"] == "weeklySummary"
    assert dataset["selected_variant"]["kind"] == "mock"


def test_fields_from_catalog_uses_metadata_snapshot() -> None:
    fields = fields_from_catalog("otcMarket", "regShoDaily")

    assert "tradeReportDate" in {field["name"] for field in fields}
