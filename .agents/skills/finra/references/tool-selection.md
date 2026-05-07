# Tool Selection

Use this reference to choose the right FINRA MCP tool.

## Discovery Tools

- `list_query_api_groups`: Use first when the user asks what dataset groups are
  available.
- `list_query_api_datasets`: Use for datasets in one group or all groups. Keep
  `live=false` unless the user specifically needs FINRA's live `/datasets`
  endpoint and credentials are configured.
- `get_dataset_details`: Use when the user names a dataset and needs catalog
  description, endpoint patterns, variants, or optional metadata.
- `get_dataset_metadata`: Use when field definitions, partition fields, primary
  id fields, or FINRA's live metadata shape matter.
- `get_dataset_fields`: Use when constructing queries and only field names or
  field metadata are needed.

## Query Tools

- `query_dataset_get`: Use for simple read-only data access with selected
  fields, limit, offset, sort fields, or extra query params.
- `query_dataset_post_readonly`: Use when the user provides an explicit FINRA
  Query API filter payload.
- `query_dataset_with_filters`: Use when Codex is translating user intent into
  compare, date range, domain, field, pagination, or sort arguments.
- `query_dataset_paginated`: Use when the user needs multiple pages or asks to
  retrieve more than one page of results.
- `get_dataset_record_by_id`: Use only when the dataset has a record id concept
  and the user provides an id. Expect credentials or entitlements for many
  record endpoints.

## Async Tools

- `start_async_query`: Use for Query API requests that should run
  asynchronously. Prefer POST unless the user explicitly needs GET semantics.
- `get_async_query_status`: Use only after an async request id or status URL is
  available. This may require `FINRA_API_TOKEN`.
- `download_async_query_result`: Use only for HTTP(S) result links returned by
  FINRA async status or otherwise trusted by the user.

## Convenience Wrappers

These are thin wrappers around generic query/list tools with the group fixed:

- `list_equity_datasets`, `query_equity_dataset`: `otcMarket`
- `list_fixed_income_datasets`, `query_fixed_income_dataset`:
  `fixedIncomeMarket`
- `list_finra_content_datasets`, `query_finra_content_dataset`: `finra`
- `list_firm_datasets`, `query_firm_dataset`: `firm`
- `list_registration_datasets`, `query_registration_dataset`: `registration`

Use wrappers when the user speaks in domain terms. Use generic tools when the
group is already explicit or when comparing behavior across groups.

## Tool Choice Heuristics

- For "what exists?", use list tools.
- For "what fields can I query?", use metadata or fields tools.
- For "give me rows", use query tools.
- For "filter by X", use `query_dataset_with_filters` unless the user supplied
  a complete payload, then use `query_dataset_post_readonly`.
- For "get the next page", use `query_dataset_get` or
  `query_dataset_with_filters` with offset if only one page is needed; use
  `query_dataset_paginated` for multiple pages.
- For "run this large query", use async start, then status, then download when
  credentials permit.
