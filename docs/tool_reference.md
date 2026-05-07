# FINRA MCP Tool Reference

This server exposes read-only tools for the FINRA Query API only. It does not
implement FINRA Submission API, Notification API, fileX, or any write operation.
POST is used only for FINRA Query API search/filter payloads.

Official sources:

- https://developer.finra.org/products/query-api
- https://developer.finra.org/docs
- https://developer.finra.org/catalog
- https://api.finra.org/datasets
- https://api.finra.org/metadata/group/{group}/name/{dataset}

## Dataset Groups

The bundled catalog snapshot contains these Query API groups:

| Group | Convenience area | Logical datasets | Dataset names including mock/historic variants |
| --- | --- | ---: | ---: |
| `otcMarket` | Equity | 8 | 17 |
| `fixedIncomeMarket` | Fixed Income | 10 | 20 |
| `finra` | FINRA Content | 2 | 4 |
| `firm` | Firm | 5 | 10 |
| `registration` | Registration | 16 | 29 |

Full dataset inventory and metadata field lists are maintained in
[query_api_inventory.md](query_api_inventory.md). The runtime metadata tools can
fetch the latest field definitions from FINRA with
`/metadata/group/{group}/name/{dataset}`.

## Public And Authenticated Access

FINRA Query API access depends on the dataset and operation. Some catalog,
metadata, and public data endpoints can be checked without credentials. Other
endpoints require `FINRA_API_TOKEN`, and some authenticated calls also require
FINRA account entitlements for the requested dataset.

If `FINRA_API_TOKEN` is not configured, token-gated tools return
`MissingCredentialsError` before sending the FINRA request. If a token is
configured but FINRA rejects the request or the account lacks entitlement, the
tool returns `FinraAuthenticationError` with FINRA's `401` response details.
Treat those responses as access failures, not proof that the MCP tool is broken.

## Filter Payload

The generic POST tools accept only these read-only FINRA Query API keys:

- `compareFilters`
- `dateRangeFilters`
- `domainFilters`
- `fields`
- `limit`
- `offset`
- `sortFields`
- `async`

Example payload:

```json
{
  "compareFilters": [
    {
      "fieldName": "marketCode",
      "compareType": "EQUAL",
      "fieldValue": "OTC"
    }
  ],
  "fields": ["tradeReportDate", "marketCode"],
  "limit": 100,
  "offset": 0,
  "sortFields": [
    {
      "fieldName": "tradeReportDate",
      "sortOrder": "DESC"
    }
  ]
}
```

## Generic Tools

### `list_query_api_groups`

Description: Lists Query API groups from the bundled catalog snapshot.

Arguments: none.

Example input:

```json
{}
```

Example output:

```json
{
  "status": "ok",
  "source": "bundled_catalog",
  "groups": [
    {
      "group": "otcMarket",
      "label": "Equity",
      "dataset_count": 8,
      "dataset_name_count": 17
    }
  ]
}
```

Group support: all discovered groups.

Filter support: no.

Pagination support: no.

Async support: no.

### `list_query_api_datasets`

Description: Lists datasets from the bundled catalog. With `live=true`, calls
FINRA `/datasets` and requires `FINRA_API_TOKEN`.

Arguments:

- `group`: optional FINRA dataset group.
- `include_variants`: include production, mock, and historic names. Default `true`.
- `live`: call FINRA `/datasets` instead of the bundled catalog. Default `false`.

Example input:

```json
{
  "group": "otcMarket",
  "include_variants": true
}
```

Example output:

```json
{
  "status": "ok",
  "source": "bundled_catalog",
  "group": "otcMarket",
  "datasets": [
    {
      "group": "otcMarket",
      "dataset": "weeklySummary",
      "title": "Weekly Summary",
      "variant_count": 3
    }
  ]
}
```

Group support: all discovered groups.

Filter support: no.

Pagination support: no.

Async support: no.

### `get_dataset_details`

Description: Returns catalog details for a dataset name and can include live
metadata.

Arguments:

- `group`: FINRA dataset group.
- `dataset`: dataset name or variant name.
- `include_metadata`: fetch metadata endpoint. Default `false`.

Example input:

```json
{
  "group": "otcMarket",
  "dataset": "regShoDaily",
  "include_metadata": true
}
```

Example output:

```json
{
  "status": "ok",
  "source": "bundled_catalog",
  "dataset": {
    "group": "otcMarket",
    "dataset": "regShoDaily",
    "title": "Reg SHO Daily Short Sale Volume"
  }
}
```

Group support: all discovered groups and any runtime group/name pair.

Filter support: no.

Pagination support: no.

Async support: no.

### `get_dataset_metadata`

Description: Calls `/metadata/group/{group}/name/{dataset}` and returns field
definitions, partition fields, primary id field when present, and support flags.

Arguments:

- `group`: FINRA dataset group.
- `dataset`: dataset name.

Example input:

```json
{
  "group": "otcMarket",
  "dataset": "regShoDaily"
}
```

Example output:

```json
{
  "status": "ok",
  "source": "finra_metadata_endpoint",
  "metadata": {
    "dataset_group": "OTCMARKET",
    "dataset_name": "REGSHODAILY",
    "field_count": 7,
    "fields": [
      {
        "name": "tradeReportDate",
        "type": "Date",
        "format": "yyyy-MM-dd"
      }
    ]
  }
}
```

Group support: all Query API datasets with a metadata endpoint.

Filter support: no.

Pagination support: no.

Async support: no.

### `get_dataset_fields`

Description: Returns only field metadata and field names for a dataset.

Arguments:

- `group`: FINRA dataset group.
- `dataset`: dataset name.

Example input:

```json
{
  "group": "fixedIncomeMarket",
  "dataset": "treasuryDailyAggregates"
}
```

Example output:

```json
{
  "status": "ok",
  "field_names": ["reportingDate", "productType", "totalTradeCount"],
  "field_count": 3
}
```

Group support: all Query API datasets.

Filter support: no.

Pagination support: no.

Async support: no.

### `query_dataset_get`

Description: Runs a read-only GET query against
`/data/group/{group}/name/{dataset}`.

Arguments:

- `group`: FINRA dataset group.
- `dataset`: dataset name.
- `fields`: optional list of fields to return.
- `limit`: optional record limit.
- `offset`: optional record offset.
- `sort_fields`: optional comma-style sort field list.
- `extra_params`: optional extra Query API query parameters.

Example input:

```json
{
  "group": "otcMarket",
  "dataset": "regShoDaily",
  "fields": ["tradeReportDate", "marketCode"],
  "limit": 5
}
```

Example output:

```json
{
  "status": "ok",
  "status_code": 200,
  "data": [],
  "pagination": {
    "total": 0,
    "limit": 5,
    "request_id": "..."
  }
}
```

Group support: all Query API datasets that support GET.

Filter support: fields, limit, offset, sort query parameters.

Pagination support: parses `Record-Total`, `Record-Limit`, `Record-Offset`,
`Total-Records-On-Page`, `Record-Max-Limit`, and request id headers.

Async support: use `start_async_query`.

### `query_dataset_post_readonly`

Description: Runs a read-only POST search/filter request against a Query API
dataset. Payloads with non-Query-API or mutating keys are rejected before HTTP.

Arguments:

- `group`: FINRA dataset group.
- `dataset`: dataset name.
- `payload`: read-only Query API filter payload.

Example input:

```json
{
  "group": "otcMarket",
  "dataset": "regShoDaily",
  "payload": {
    "dateRangeFilters": [
      {
        "fieldName": "tradeReportDate",
        "startDate": "2026-01-01",
        "endDate": "2026-01-31"
      }
    ],
    "limit": 100
  }
}
```

Example output:

```json
{
  "status": "ok",
  "status_code": 200,
  "data": [],
  "pagination": {
    "limit": 100
  }
}
```

Group support: all Query API datasets that support read-only POST search.

Filter support: full read-only FINRA Query API filter payload.

Pagination support: yes.

Async support: payload may include `"async": true`, or use `start_async_query`.

### `get_dataset_record_by_id`

Description: Calls `/data/group/{group}/name/{dataset}/id/{id}` for datasets
that support single-record access.

Arguments:

- `group`: FINRA dataset group.
- `dataset`: dataset name.
- `record_id`: primary id value.

Example input:

```json
{
  "group": "registration",
  "dataset": "registrationValidationIndividual",
  "record_id": "12345"
}
```

Example output:

```json
{
  "status": "ok",
  "data": {
    "id": "12345"
  }
}
```

Group support: datasets whose metadata indicates single-record support.

Filter support: no.

Pagination support: no.

Async support: no.

### `query_dataset_with_filters`

Description: Builds a valid read-only Query API POST payload from separate
filter arguments and executes it.

Arguments:

- `group`
- `dataset`
- `compare_filters`
- `date_range_filters`
- `domain_filters`
- `fields`
- `limit`
- `offset`
- `sort_fields`
- `async_request`

Example input:

```json
{
  "group": "otcMarket",
  "dataset": "weeklySummary",
  "domain_filters": [
    {
      "fieldName": "tierIdentifier",
      "values": ["T1"]
    }
  ],
  "fields": ["weekStartDate", "tierIdentifier", "totalWeeklyTradeCount"],
  "limit": 1000
}
```

Example output:

```json
{
  "status": "ok",
  "data": [],
  "pagination": {
    "limit": 1000
  }
}
```

Group support: all Query API datasets.

Filter support: compare, date range, domain, fields, sort, limit, offset.

Pagination support: yes.

Async support: set `async_request=true` or use `start_async_query`.

### `query_dataset_paginated`

Description: Fetches multiple pages from a dataset and returns records plus page
metadata.

Arguments:

- `group`
- `dataset`
- `page_size`: default `1000`.
- `max_pages`: default `10`.
- `start_offset`: default `0`.
- `fields`
- `compare_filters`
- `date_range_filters`
- `domain_filters`
- `sort_fields`
- `method`: `GET` or `POST`, default `POST`.

Example input:

```json
{
  "group": "fixedIncomeMarket",
  "dataset": "treasuryDailyAggregates",
  "page_size": 1000,
  "max_pages": 3,
  "method": "POST"
}
```

Example output:

```json
{
  "status": "ok",
  "page_count": 2,
  "record_count": 1500,
  "pages": [
    {
      "page": 1,
      "offset": 0,
      "record_count": 1000
    }
  ]
}
```

Group support: all Query API datasets with paged data access.

Filter support: yes for POST; fields, limit, offset for GET.

Pagination support: yes.

Async support: no, use async tools for large jobs.

### `start_async_query`

Description: Starts an asynchronous read-only Query API request. FINRA returns
HTTP `202` and a `Location` header for polling.

Arguments:

- `group`
- `dataset`
- `payload`: optional read-only filter payload.
- `method`: `GET` or `POST`, default `POST`.

Example input:

```json
{
  "group": "otcMarket",
  "dataset": "weeklySummary",
  "payload": {
    "limit": 100000,
    "domainFilters": [
      {
        "fieldName": "tierIdentifier",
        "values": ["T1"]
      }
    ]
  }
}
```

Example output:

```json
{
  "status": "ok",
  "status_code": 202,
  "async_status_url": "/async-requests/group/otcMarket/name/weeklySummary/..."
}
```

Group support: all Query API datasets that support async.

Filter support: full read-only payload.

Pagination support: async response headers are parsed when provided.

Async support: starts async workflow.

### `get_async_query_status`

Description: Polls `/async-requests/group/{group}/name/{dataset}/{requestId}`.

Arguments:

- `group`
- `dataset`
- `request_id`

Example input:

```json
{
  "group": "otcMarket",
  "dataset": "weeklySummary",
  "request_id": "0ba2c6e6-c13b-4a47-989a-c47106ab98ce"
}
```

Example output:

```json
{
  "status": "ok",
  "async_status": "complete",
  "result_link": "https://...",
  "expires": "2026-05-07T12:00:00Z"
}
```

Group support: all async Query API requests.

Filter support: no.

Pagination support: FINRA includes headers when status is complete.

Async support: polls async workflow.

### `download_async_query_result`

Description: GETs the pre-signed result link returned by a completed async
status request.

Arguments:

- `result_link`: pre-signed HTTP(S) URL from `get_async_query_status`.

Example input:

```json
{
  "result_link": "https://example-presigned-url"
}
```

Example output:

```json
{
  "status": "ok",
  "status_code": 200,
  "data": "csv-or-json-result"
}
```

Group support: any completed async result link.

Filter support: no.

Pagination support: no.

Async support: completes async workflow.

## Convenience Tools

The convenience tools are thin wrappers over `list_query_api_datasets` and
`query_dataset_with_filters`. They do not duplicate query logic or hardcode
schemas.

| Tool | Fixed group | Description |
| --- | --- | --- |
| `list_equity_datasets` | `otcMarket` | List Equity datasets. |
| `query_equity_dataset` | `otcMarket` | Query an Equity dataset. |
| `list_fixed_income_datasets` | `fixedIncomeMarket` | List Fixed Income datasets. |
| `query_fixed_income_dataset` | `fixedIncomeMarket` | Query a Fixed Income dataset. |
| `list_finra_content_datasets` | `finra` | List FINRA Content datasets. |
| `query_finra_content_dataset` | `finra` | Query a FINRA Content dataset. |
| `list_firm_datasets` | `firm` | List Firm datasets. |
| `query_firm_dataset` | `firm` | Query a Firm dataset. |
| `list_registration_datasets` | `registration` | List Registration datasets. |
| `query_registration_dataset` | `registration` | Query a Registration dataset. |

Support matrix:

| Tool | Dataset group support | Filter support | Pagination support | Async support |
| --- | --- | --- | --- | --- |
| `list_equity_datasets` | `otcMarket` | No | No | No |
| `query_equity_dataset` | `otcMarket` | Compare, date range, domain, fields, sort, limit, offset | Yes | Use generic async tools |
| `list_fixed_income_datasets` | `fixedIncomeMarket` | No | No | No |
| `query_fixed_income_dataset` | `fixedIncomeMarket` | Compare, date range, domain, fields, sort, limit, offset | Yes | Use generic async tools |
| `list_finra_content_datasets` | `finra` | No | No | No |
| `query_finra_content_dataset` | `finra` | Compare, date range, domain, fields, sort, limit, offset | Yes | Use generic async tools |
| `list_firm_datasets` | `firm` | No | No | No |
| `query_firm_dataset` | `firm` | Compare, date range, domain, fields, sort, limit, offset | Yes | Use generic async tools |
| `list_registration_datasets` | `registration` | No | No | No |
| `query_registration_dataset` | `registration` | Compare, date range, domain, fields, sort, limit, offset | Yes | Use generic async tools |

List wrapper arguments:

- `include_variants`: include production, mock, and historic names. Default `true`.

Query wrapper arguments:

- `dataset`
- `compare_filters`
- `date_range_filters`
- `domain_filters`
- `fields`
- `limit`
- `offset`
- `sort_fields`

Example input:

```json
{
  "dataset": "weeklySummary",
  "fields": ["weekStartDate", "tierIdentifier"],
  "limit": 100
}
```

Example output:

```json
{
  "status": "ok",
  "dataset": {
    "group": "otcMarket",
    "name": "weeklySummary"
  },
  "data": []
}
```

Filter support: same as `query_dataset_with_filters`.

Pagination support: parses Query API pagination headers.

Async support: use generic async tools.

Common dataset examples:

Equity:

```json
{
  "tool": "query_equity_dataset",
  "arguments": {
    "dataset": "weeklySummary",
    "fields": ["weekStartDate", "tierIdentifier", "totalWeeklyTradeCount"],
    "limit": 100
  }
}
```

Fixed Income:

```json
{
  "tool": "query_fixed_income_dataset",
  "arguments": {
    "dataset": "treasuryDailyAggregates",
    "fields": ["reportingDate", "totalTradeCount"],
    "limit": 100
  }
}
```

FINRA Content:

```json
{
  "tool": "query_finra_content_dataset",
  "arguments": {
    "dataset": "finraRulebook",
    "fields": ["ruleNumber", "ruleTitle"],
    "limit": 25
  }
}
```

Firm:

```json
{
  "tool": "query_firm_dataset",
  "arguments": {
    "dataset": "firmProfile",
    "fields": ["firmCrdNumber", "firmName"],
    "limit": 10
  }
}
```

Registration:

```json
{
  "tool": "query_registration_dataset",
  "arguments": {
    "dataset": "branchList",
    "fields": ["firmCrdNumber", "branchCrdNumber"],
    "limit": 10
  }
}
```
