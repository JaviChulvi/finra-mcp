# Response Validation

Use this reference to verify that FINRA MCP responses match the request.

## Catalog Responses

Check:

- `status` is `ok`.
- `source` is expected, usually `bundled_catalog` for non-live catalog calls.
- Dataset entries contain `group`, `dataset`, endpoint patterns, and titles.
- Group filters are honored: every returned dataset belongs to the requested
  group.
- `include_variants=false` returns logical datasets rather than every variant.

## Metadata Responses

Check:

- `status` is `ok`.
- `dataset.group` and `dataset.name` match the request.
- `metadata.fields` is present and each field has a `name`.
- `field_count` matches the number of fields when both are present.
- `partition_fields` and `primary_id_field` are carried through if FINRA
  exposes them.

When metadata is unavailable from FINRA but a bundled fallback is returned,
state the source clearly.

## Data Query Responses

Check:

- `status` is `ok`.
- `status_code` is a successful HTTP status.
- `data` is a list for dataset queries unless the endpoint semantics differ.
- Each sampled record contains the requested `fields`.
- No unrequested field expectation is asserted unless FINRA returned extra
  fields by documented endpoint behavior.
- `pagination.limit` matches the requested limit when FINRA returns the header.
- `pagination.offset` matches the requested offset when FINRA returns the
  header.
- `pagination.total` is non-negative when present.
- `dataset.group` and `dataset.name` match the request when present.

## Filter Responses

For `compareFilters`, inspect sampled rows and verify the condition:

- `EQUAL`: every sampled row has the exact requested value.
- `NOT_EQUAL`: sampled rows do not contain the excluded value.
- range comparisons: sampled values are directionally consistent with the
  comparison.
- `IN`: sampled values belong to the requested set.

For `dateRangeFilters`, check date fields are within the requested bounds when
the response includes those fields.

For `domainFilters`, check sampled values belong to the requested domain set.

If the response does not include the filtered field, say the filter was sent but
cannot be independently verified from the returned projection.

## Pagination Responses

For `query_dataset_paginated`, check:

- `page_count` is no larger than `max_pages`.
- `record_count` equals the length of `records`.
- Each page has a distinct page number.
- Offsets advance coherently by page size or returned FINRA pagination values.
- Aggregated records are consistent with per-page `record_count` values.
- Early stop is justified by fewer returned rows than requested, total reached,
  or max pages reached.

## Async Responses

For async start, check:

- HTTP status indicates accepted or successful start.
- Response contains a request id, location, check-status link, or status URL.
- The dataset identity matches the request when present.

For async status, check:

- Status values such as queued, running, complete, failed, or expired are
  reported plainly.
- `resultLink` is present before calling download.
- Expiration timestamps are surfaced when available.

For download, check:

- The URL is HTTP(S).
- The response status is successful.
- The returned data is parseable according to the content: JSON/list, CSV text,
  or another FINRA-provided format.

## Error Responses

Check:

- `status` is `error`.
- `error` names the local or FINRA error class.
- `message` explains the failure.
- FINRA `details` are preserved when available.
- Request ids are reported when present.

Do not convert an error response into a successful data result. Explain what was
verified about the failure path.
