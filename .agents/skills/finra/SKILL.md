---
name: finra
description: "Use when Codex needs to work with the FINRA Query API MCP server: discovering FINRA datasets, inspecting metadata and field names, building read-only GET/POST query arguments, handling pagination and async Query API workflows, interpreting FINRA authentication or entitlement errors, validating returned data shape, or explaining safe usage of the FINRA MCP tools without using Submission API, Notification API, fileX, uploads, or write operations."
---

# FINRA MCP

Use this skill to operate the FINRA Query API MCP server safely and accurately.
The server is read-only and exposes dataset discovery, metadata, query,
pagination, async, and group convenience tools.

## Core Rules

- Use only Query API read-only workflows.
- Do not use or propose Submission API, Notification API, fileX, uploads,
  acknowledgements, subscriptions, sends, creates, updates, deletes, or other
  mutating operations.
- Inspect catalog or metadata before constructing non-trivial queries.
- Request only fields needed for the task.
- Use small limits unless the user explicitly needs larger result sets.
- Treat `MissingCredentialsError` as local credential absence.
- Treat FINRA `401` responses as authentication or entitlement failures unless
  there is separate evidence of a tool bug.
- Distinguish tool execution from data access: a tool can work correctly while
  FINRA denies access to a restricted endpoint.
- Report enough evidence for the user to understand what was verified: tool
  name, dataset, status, field shape, counts, filters, pagination, and access
  errors.

## Workflow

1. Identify whether the user needs discovery, metadata, records, filtered data,
   pagination, or async results.
2. Use catalog tools for broad discovery and metadata tools for field-level
   decisions.
3. Build query arguments from known FINRA Query API keys only.
4. Validate the response against the request before summarizing it.
5. For restricted endpoints, stop at the credential or entitlement boundary and
   explain what token or access is missing.

## Tool Selection

Read [references/tool-selection.md](references/tool-selection.md) when choosing
among generic tools and convenience wrappers, or when mapping a user request to
specific MCP calls.

Use generic tools when the user names a FINRA group and dataset directly. Use
convenience wrappers when the user asks by domain area, such as equity, fixed
income, FINRA content, firm, or registration.

## Query Construction

Use only these POST payload keys:

- `compareFilters`
- `dateRangeFilters`
- `domainFilters`
- `fields`
- `limit`
- `offset`
- `sortFields`
- `async`

Normalize user intent into these keys. If the user asks for write-like behavior,
state that the MCP server is read-only and do not call a mutating endpoint.

For details on filter types, field selection, pagination, and async workflow
checks, read [references/response-validation.md](references/response-validation.md).

## Access Handling

Read [references/access-and-errors.md](references/access-and-errors.md) when a
tool returns `MissingCredentialsError`, `FinraAuthenticationError`, `401`, or an
unexpected FINRA error body.

When credentials are missing or insufficient, do not keep retrying equivalent
restricted calls. Record which tool and dataset were blocked, then ask for a
valid `FINRA_API_TOKEN` and any necessary FINRA entitlements if the user needs
live restricted data.

## Verification Standard

Validate correctness directly from each response:

- `status` is `ok` for successful data access.
- `dataset.group` and `dataset.name` match the request when present.
- Returned records contain the requested fields.
- Filtered responses satisfy the filter condition for sampled rows.
- Pagination metadata matches the requested `limit` and `offset`.
- Paginated calls advance offsets and aggregate record counts coherently.
- Metadata field names match the query fields used later.
- Async start returns an accepted status and a status URL or request id.
- Downloaded async results are parseable as the returned content type.

If a result is credential-blocked, verify the error type and explain the access
boundary instead of presenting it as a data result.

## Reporting

Prefer concise, evidence-based summaries:

- List tools called and the outcome category: data returned, metadata returned,
  catalog returned, credential-blocked, entitlement-blocked, or input error.
- Mention representative fields and counts, not full records, unless the user
  asks for raw output.
- Call out any unverified requirement explicitly.
- Never claim all live data tools are verified when some endpoints only returned
  credential or entitlement errors.
