"""Generic read-only FINRA Query API tool functions."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal

from finra_mcp.client import FinraQueryClient
from finra_mcp.discovery.catalog import (
    fields_from_catalog,
    find_dataset,
    list_datasets,
    list_groups,
    load_catalog,
)
from finra_mcp.discovery.metadata import field_names, normalize_metadata
from finra_mcp.errors import FinraError, ReadOnlyViolationError
from finra_mcp.models import QueryPayload, QueryResult, validate_read_only_payload


def _result_to_response(
    result: QueryResult,
    *,
    group: str | None = None,
    dataset: str | None = None,
    include_headers: bool = False,
) -> dict[str, Any]:
    response: dict[str, Any] = {
        "status": "ok",
        "status_code": result.status_code,
        "data": result.data,
        "pagination": result.pagination.model_dump(exclude_none=True),
    }
    if group is not None or dataset is not None:
        response["dataset"] = {"group": group, "name": dataset}
    if include_headers:
        response["headers"] = result.headers
    return response


def _error_to_response(error: Exception) -> dict[str, Any]:
    if isinstance(error, FinraError) and hasattr(error, "to_dict"):
        details = error.to_dict()  # type: ignore[attr-defined]
    else:
        details = {"error": error.__class__.__name__, "message": str(error)}
    return {"status": "error", **details}


def _coerce_payload(payload: Mapping[str, Any] | None) -> dict[str, Any]:
    body = dict(payload or {})
    validate_read_only_payload(body)
    return body


def _build_payload(
    *,
    compare_filters: list[dict[str, Any]] | None = None,
    date_range_filters: list[dict[str, Any]] | None = None,
    domain_filters: list[dict[str, Any]] | None = None,
    fields: list[str] | None = None,
    limit: int | None = None,
    offset: int | None = None,
    sort_fields: list[dict[str, Any] | str] | None = None,
    async_request: bool | None = None,
) -> dict[str, Any]:
    payload = QueryPayload(
        compareFilters=compare_filters,
        dateRangeFilters=date_range_filters,
        domainFilters=domain_filters,
        fields=fields,
        limit=limit,
        offset=offset,
        sortFields=sort_fields,
        async_=async_request,
    ).to_finra_payload()
    validate_read_only_payload(payload)
    return payload


def list_query_api_groups() -> dict[str, Any]:
    """List FINRA Query API dataset groups from the bundled catalog snapshot."""
    catalog = load_catalog()
    return {
        "status": "ok",
        "source": "bundled_catalog",
        "generated_at": catalog.get("generated_at"),
        "groups": list_groups(),
    }


async def list_query_api_datasets(
    group: str | None = None,
    include_variants: bool = True,
    live: bool = False,
) -> dict[str, Any]:
    """List FINRA Query API datasets from the catalog, or `/datasets` when live is true."""
    if not live:
        return {
            "status": "ok",
            "source": "bundled_catalog",
            "group": group,
            "datasets": list_datasets(group, include_variants=include_variants),
        }

    try:
        async with FinraQueryClient() as client:
            result = await client.list_datasets(group=group)
        return _result_to_response(result, group=group)
    except Exception as exc:
        return _error_to_response(exc)


async def get_dataset_details(
    group: str,
    dataset: str,
    include_metadata: bool = False,
) -> dict[str, Any]:
    """Return catalog details for one FINRA Query API dataset name."""
    details = find_dataset(group, dataset)
    if not details:
        details = {
            "group": group,
            "dataset": dataset,
            "description": None,
            "documentation_url": None,
            "data_endpoint": f"/data/group/{group}/name/{dataset}",
            "metadata_endpoint": f"/metadata/group/{group}/name/{dataset}",
            "notes": [
                "Dataset was not present in the bundled catalog; runtime metadata may still exist."
            ],
        }

    response: dict[str, Any] = {
        "status": "ok",
        "source": "bundled_catalog",
        "dataset": details,
    }
    if include_metadata:
        response["metadata"] = await get_dataset_metadata(group, dataset)
    return response


async def get_dataset_metadata(group: str, dataset: str) -> dict[str, Any]:
    """Fetch metadata from `/metadata/group/{group}/name/{dataset}`."""
    try:
        async with FinraQueryClient() as client:
            result = await client.get_metadata(group, dataset)
        metadata = normalize_metadata(result.data if isinstance(result.data, dict) else {})
        return {
            "status": "ok",
            "source": "finra_metadata_endpoint",
            "dataset": {"group": group, "name": dataset},
            "metadata": metadata,
            "pagination": result.pagination.model_dump(exclude_none=True),
        }
    except Exception as exc:
        fallback_fields = fields_from_catalog(group, dataset)
        if fallback_fields:
            return {
                "status": "ok",
                "source": "bundled_catalog_fallback",
                "dataset": {"group": group, "name": dataset},
                "metadata": {
                    "dataset_group": group,
                    "dataset_name": dataset,
                    "fields": fallback_fields,
                    "field_count": len(fallback_fields),
                },
                "warning": _error_to_response(exc),
            }
        return _error_to_response(exc)


async def get_dataset_fields(group: str, dataset: str) -> dict[str, Any]:
    """Return field metadata and field names for a FINRA Query API dataset."""
    metadata_response = await get_dataset_metadata(group, dataset)
    if metadata_response.get("status") != "ok":
        return metadata_response
    metadata = metadata_response.get("metadata", {})
    fields = metadata.get("fields", [])
    return {
        "status": "ok",
        "source": metadata_response.get("source"),
        "dataset": {"group": group, "name": dataset},
        "fields": fields,
        "field_names": field_names(metadata),
        "field_count": len(fields),
        "partition_fields": metadata.get("partition_fields")
        or metadata.get("partitionFields")
        or [],
        "primary_id_field": metadata.get("primary_id_field"),
    }


async def query_dataset_get(
    group: str,
    dataset: str,
    fields: list[str] | None = None,
    limit: int | None = None,
    offset: int | None = None,
    sort_fields: list[str] | None = None,
    extra_params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Run a read-only GET query against `/data/group/{group}/name/{dataset}`."""
    try:
        async with FinraQueryClient() as client:
            result = await client.query_dataset_get(
                group,
                dataset,
                fields=fields,
                limit=limit,
                offset=offset,
                sort_fields=sort_fields,
                extra_params=extra_params,
            )
        return _result_to_response(result, group=group, dataset=dataset)
    except Exception as exc:
        return _error_to_response(exc)


async def query_dataset_post_readonly(
    group: str,
    dataset: str,
    payload: dict[str, Any],
) -> dict[str, Any]:
    """Run a read-only POST search/filter Query API request."""
    try:
        body = _coerce_payload(payload)
        async with FinraQueryClient() as client:
            result = await client.query_dataset_post_readonly(group, dataset, body)
        return _result_to_response(result, group=group, dataset=dataset)
    except Exception as exc:
        return _error_to_response(exc)


async def get_dataset_record_by_id(group: str, dataset: str, record_id: str) -> dict[str, Any]:
    """Fetch a single dataset record by primary id."""
    try:
        async with FinraQueryClient() as client:
            result = await client.get_record_by_id(group, dataset, record_id)
        return _result_to_response(result, group=group, dataset=dataset)
    except Exception as exc:
        return _error_to_response(exc)


async def query_dataset_with_filters(
    group: str,
    dataset: str,
    compare_filters: list[dict[str, Any]] | None = None,
    date_range_filters: list[dict[str, Any]] | None = None,
    domain_filters: list[dict[str, Any]] | None = None,
    fields: list[str] | None = None,
    limit: int | None = None,
    offset: int | None = None,
    sort_fields: list[dict[str, Any] | str] | None = None,
    async_request: bool = False,
) -> dict[str, Any]:
    """Query a dataset using FINRA Query API filter payload fields."""
    try:
        payload = _build_payload(
            compare_filters=compare_filters,
            date_range_filters=date_range_filters,
            domain_filters=domain_filters,
            fields=fields,
            limit=limit,
            offset=offset,
            sort_fields=sort_fields,
            async_request=async_request or None,
        )
        async with FinraQueryClient() as client:
            result = await client.query_dataset_post_readonly(group, dataset, payload)
        return _result_to_response(result, group=group, dataset=dataset)
    except Exception as exc:
        return _error_to_response(exc)


async def query_dataset_paginated(
    group: str,
    dataset: str,
    page_size: int = 1000,
    max_pages: int = 10,
    start_offset: int = 0,
    fields: list[str] | None = None,
    compare_filters: list[dict[str, Any]] | None = None,
    date_range_filters: list[dict[str, Any]] | None = None,
    domain_filters: list[dict[str, Any]] | None = None,
    sort_fields: list[dict[str, Any] | str] | None = None,
    method: Literal["GET", "POST"] = "POST",
) -> dict[str, Any]:
    """Fetch multiple pages from a dataset using FINRA pagination headers."""
    if page_size < 1:
        return _error_to_response(ValueError("page_size must be greater than zero"))
    if max_pages < 1:
        return _error_to_response(ValueError("max_pages must be greater than zero"))

    method = method.upper()  # type: ignore[assignment]
    if method not in {"GET", "POST"}:
        return _error_to_response(ValueError("method must be GET or POST"))

    if method == "GET":
        for name, value in (("compare_filters", compare_filters),
                            ("date_range_filters", date_range_filters),
                            ("domain_filters", domain_filters)):
            if value:
                return _error_to_response(ValueError(f"GET does not support {name}; use POST"))
        if sort_fields and not all(isinstance(field, str) for field in sort_fields):
            return _error_to_response(
                ValueError("GET sort_fields must contain only strings; use POST")
            )

    pages: list[dict[str, Any]] = []
    records: list[Any] = []
    offset = start_offset
    try:
        async with FinraQueryClient() as client:
            for page_number in range(1, max_pages + 1):
                if method == "GET":
                    result = await client.query_dataset_get(
                        group,
                        dataset,
                        fields=fields,
                        limit=page_size,
                        offset=offset,
                        sort_fields=sort_fields,  # type: ignore[arg-type]
                    )
                else:
                    payload = _build_payload(
                        compare_filters=compare_filters,
                        date_range_filters=date_range_filters,
                        domain_filters=domain_filters,
                        fields=fields,
                        limit=page_size,
                        offset=offset,
                        sort_fields=sort_fields,
                    )
                    result = await client.query_dataset_post_readonly(group, dataset, payload)

                page_data = result.data if isinstance(result.data, list) else []
                page_info = {
                    "page": page_number,
                    "offset": offset,
                    "status_code": result.status_code,
                    "pagination": result.pagination.model_dump(exclude_none=True),
                    "record_count": len(page_data),
                }
                pages.append(page_info)
                records.extend(page_data)

                returned = (
                    result.pagination.returned
                    if result.pagination.returned is not None
                    else len(page_data)
                )
                effective_limit = result.pagination.limit or page_size
                total = result.pagination.total
                next_offset = (
                    result.pagination.offset if result.pagination.offset is not None else offset
                ) + effective_limit

                if returned < effective_limit:
                    break
                if total is not None and next_offset >= total:
                    break
                offset = next_offset

        return {
            "status": "ok",
            "dataset": {"group": group, "name": dataset},
            "method": method,
            "page_size": page_size,
            "page_count": len(pages),
            "records": records,
            "record_count": len(records),
            "pages": pages,
        }
    except Exception as exc:
        return _error_to_response(exc)


async def start_async_query(
    group: str,
    dataset: str,
    payload: dict[str, Any] | None = None,
    method: Literal["GET", "POST"] = "POST",
) -> dict[str, Any]:
    """Start an asynchronous read-only FINRA Query API request."""
    try:
        body = _coerce_payload(payload)
        async with FinraQueryClient() as client:
            result = await client.start_async_query(group, dataset, body, method=method)
        response = _result_to_response(result, group=group, dataset=dataset)
        response["async_status_url"] = result.pagination.location
        return response
    except Exception as exc:
        return _error_to_response(exc)


async def get_async_query_status(group: str, dataset: str, request_id: str) -> dict[str, Any]:
    """Poll an async FINRA Query API request status URL."""
    try:
        async with FinraQueryClient() as client:
            result = await client.get_async_query_status(group, dataset, request_id)
        response = _result_to_response(result, group=group, dataset=dataset)
        if isinstance(result.data, dict):
            response["result_link"] = result.data.get("resultLink")
            response["expires"] = result.data.get("expires")
            response["async_status"] = result.data.get("status")
        return response
    except Exception as exc:
        return _error_to_response(exc)


async def download_async_query_result(result_link: str) -> dict[str, Any]:
    """Download the pre-signed result link returned by a completed async query."""
    if not result_link.startswith(("https://", "http://")):
        return _error_to_response(
            ReadOnlyViolationError("result_link must be an HTTP(S) URL returned by async status")
        )
    try:
        async with FinraQueryClient() as client:
            result = await client.download_async_query_result(result_link)
        return _result_to_response(result)
    except Exception as exc:
        return _error_to_response(exc)
