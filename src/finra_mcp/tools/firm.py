"""Thin Firm group wrappers for the FINRA Query API."""

from __future__ import annotations

from typing import Any

from finra_mcp.tools.query import list_query_api_datasets, query_dataset_with_filters

FIRM_GROUP = "firm"


async def list_firm_datasets(include_variants: bool = True) -> dict[str, Any]:
    """List Firm Query API datasets in the `firm` group."""
    return await list_query_api_datasets(group=FIRM_GROUP, include_variants=include_variants)


async def query_firm_dataset(
    dataset: str,
    compare_filters: list[dict[str, Any]] | None = None,
    date_range_filters: list[dict[str, Any]] | None = None,
    domain_filters: list[dict[str, Any]] | None = None,
    fields: list[str] | None = None,
    limit: int | None = None,
    offset: int | None = None,
    sort_fields: list[dict[str, Any] | str] | None = None,
) -> dict[str, Any]:
    """Query a Firm dataset through the generic Query API implementation."""
    return await query_dataset_with_filters(
        FIRM_GROUP,
        dataset,
        compare_filters=compare_filters,
        date_range_filters=date_range_filters,
        domain_filters=domain_filters,
        fields=fields,
        limit=limit,
        offset=offset,
        sort_fields=sort_fields,
    )
