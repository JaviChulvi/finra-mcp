# FINRA MCP

Read-only Python MCP server for the FINRA Query API, built with FastMCP.

This server exposes metadata-driven tools for the Query API datasets listed in
the FINRA Developer Center catalog. It is intentionally scoped to FINRA Query
API data access only.

## Scope And Read-Only Guarantee

Included:

- FINRA Query API dataset discovery.
- Query API metadata.
- Read-only data queries through `GET`.
- Read-only search/filter requests through `POST`.
- Query API pagination helpers.
- Query API async request workflow.
- Thin convenience wrappers for major dataset groups.

Excluded:

- Submission API.
- Notification API.
- fileX.
- Any operation that submits, mutates, uploads, acknowledges, subscribes,
  unsubscribes, deletes, or sends data.

The server validates POST payloads and only allows FINRA Query API read-only
search/filter keys: `compareFilters`, `dateRangeFilters`, `domainFilters`,
`fields`, `limit`, `offset`, `sortFields`, and `async`.

## Supported Dataset Groups

The bundled catalog snapshot is generated from the official FINRA Developer
Center docs and metadata endpoints.

| Query API group | Area |
| --- | --- |
| `otcMarket` | Equity |
| `fixedIncomeMarket` | Fixed Income |
| `finra` | FINRA Content |
| `firm` | Firm |
| `registration` | Registration |

See [docs/query_api_inventory.md](docs/query_api_inventory.md) for the full
dataset inventory and field list, and
[docs/tool_reference.md](docs/tool_reference.md) for every MCP tool.

## Installation With Conda

```bash
conda env create -f environment.yml
conda activate finra-mcp
```

## Installation With Pip

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

## Installation With uv

```bash
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"
```

## Environment Variables

Create a local `.env` or export variables in your shell. Do not commit
credentials.

```bash
export FINRA_API_TOKEN="your-finra-api-token"
export FINRA_BASE_URL="https://api.finra.org"
export FINRA_TIMEOUT="30"
```

Variables:

- `FINRA_API_TOKEN`: Bearer token for authenticated FINRA Query API calls.
- `FINRA_BASE_URL`: optional, defaults to `https://api.finra.org`.
- `FINRA_TIMEOUT`: optional HTTP timeout in seconds, defaults to `30`.
- `FINRA_RESULT_HOSTS`: comma-separated exact, trusted result hostnames. Configure the
  hostname supplied by FINRA for your signed results before downloading; no hosts are
  trusted by default. Only HTTPS on port 443 is allowed, and redirects are rejected.
  DNS must resolve exclusively to public addresses; the connection is pinned to a
  validated address while preserving the original Host header and TLS identity.

Metadata endpoints may be publicly accessible for some datasets, but data,
`/datasets`, and most firm/registration datasets require valid FINRA
credentials and entitlements.

For more detail on how to interpret `MissingCredentialsError` versus FINRA
`401` responses, see
[docs/tool_reference.md](docs/tool_reference.md#public-and-authenticated-access).

## Run The MCP Server

```bash
finra-mcp
```

Equivalent:

```bash
python -m finra_mcp.server
```

FastMCP runs over stdio by default, which is the expected transport for most MCP
client configurations.

## MCP Client Configuration

Example MCP client entry:

```json
{
  "mcpServers": {
    "finra-query-api": {
      "command": "finra-mcp",
      "env": {
        "FINRA_API_TOKEN": "your-finra-api-token",
        "FINRA_BASE_URL": "https://api.finra.org"
      }
    }
  }
}
```

If the package is not installed as a console script, use:

```json
{
  "mcpServers": {
    "finra-query-api": {
      "command": "python",
      "args": ["-m", "finra_mcp.server"],
      "env": {
        "FINRA_API_TOKEN": "your-finra-api-token"
      }
    }
  }
}
```

## Tool Examples

List Query API groups:

```json
{
  "tool": "list_query_api_groups",
  "arguments": {}
}
```

List Equity datasets:

```json
{
  "tool": "list_equity_datasets",
  "arguments": {
    "include_variants": true
  }
}
```

Get metadata:

```json
{
  "tool": "get_dataset_metadata",
  "arguments": {
    "group": "otcMarket",
    "dataset": "regShoDaily"
  }
}
```

Query with selected fields:

```json
{
  "tool": "query_dataset_get",
  "arguments": {
    "group": "otcMarket",
    "dataset": "regShoDaily",
    "fields": ["tradeReportDate", "marketCode"],
    "limit": 5
  }
}
```

Query with filters:

```json
{
  "tool": "query_dataset_with_filters",
  "arguments": {
    "group": "otcMarket",
    "dataset": "weeklySummary",
    "domain_filters": [
      {
        "fieldName": "tierIdentifier",
        "values": ["T1"]
      }
    ],
    "fields": ["weekStartDate", "tierIdentifier", "totalWeeklyTradeCount"],
    "limit": 100
  }
}
```

Fetch a record by id:

```json
{
  "tool": "get_dataset_record_by_id",
  "arguments": {
    "group": "registration",
    "dataset": "registrationValidationIndividual",
    "record_id": "12345"
  }
}
```

## Pagination

FINRA Query API responses can include headers such as:

- `Record-Total`
- `Record-Offset`
- `Record-Limit`
- `Total-Records-On-Page`
- `Record-Max-Limit`
- `Response-Payload-Max-Size`
- `FINRA-api-request-id`

The tools parse these into the `pagination` object.

Example paginated call:

```json
{
  "tool": "query_dataset_paginated",
  "arguments": {
    "group": "fixedIncomeMarket",
    "dataset": "treasuryDailyAggregates",
    "page_size": 1000,
    "max_pages": 3,
    "method": "POST"
  }
}
```

## Async Query Workflow

Start an async request:

```json
{
  "tool": "start_async_query",
  "arguments": {
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
}
```

Poll status:

```json
{
  "tool": "get_async_query_status",
  "arguments": {
    "group": "otcMarket",
    "dataset": "weeklySummary",
    "request_id": "0ba2c6e6-c13b-4a47-989a-c47106ab98ce"
  }
}
```

Download result:

```json
{
  "tool": "download_async_query_result",
  "arguments": {
    "result_link": "https://presigned-result-url"
  }
}
```

FINRA recommends polling async status no more than once per minute.

## FINRA Credentials And Test Data

FINRA credentials and dataset entitlements are managed through the FINRA API
Console. Public, firm, and mock credentials have different access rights. The
Developer Center docs note that mock datasets append `Mock` to the dataset name,
and some datasets also expose historic variants. For production-like testing,
FINRA recommends using its QA Test environment where available.

The server never hardcodes credentials and `.env` is ignored by git.

## Troubleshooting

`FINRA_API_TOKEN is required`:

Set `FINRA_API_TOKEN` for data queries, `/datasets`, record lookup, and async
status requests.

`Unauthorized` or HTTP `401`:

The token is missing, invalid, expired, or for a different FINRA environment.

HTTP `403`:

The credential is valid but lacks entitlement for the dataset.

HTTP `429`:

The FINRA API rate-limited the request. Reduce frequency, narrow filters, or use
async requests for large result sets.

Large or timed-out synchronous queries:

Use filters, smaller pages, or `start_async_query`.

Metadata fields differ from the bundled catalog:

The bundled snapshot is documentation-driven. Use `get_dataset_metadata` to read
the current FINRA metadata endpoint.

## Development

Run tests:

```bash
pytest
```

Format and lint:

```bash
ruff format
ruff check
```

Official FINRA links:

- https://developer.finra.org/products/query-api
- https://developer.finra.org/docs
- https://developer.finra.org/catalog
