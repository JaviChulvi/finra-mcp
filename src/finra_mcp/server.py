"""FastMCP server exposing read-only FINRA Query API tools."""

from __future__ import annotations

from fastmcp import FastMCP

from finra_mcp import __version__
from finra_mcp.tools.query import (
    download_async_query_result,
    get_async_query_status,
    get_dataset_details,
    get_dataset_fields,
    get_dataset_metadata,
    get_dataset_record_by_id,
    list_query_api_datasets,
    list_query_api_groups,
    query_dataset_get,
    query_dataset_paginated,
    query_dataset_post_readonly,
    query_dataset_with_filters,
    start_async_query,
)


GENERIC_TOOLS = [
    list_query_api_groups,
    list_query_api_datasets,
    get_dataset_details,
    get_dataset_metadata,
    get_dataset_fields,
    query_dataset_get,
    query_dataset_post_readonly,
    get_dataset_record_by_id,
    query_dataset_with_filters,
    query_dataset_paginated,
    start_async_query,
    get_async_query_status,
    download_async_query_result,
]

CONVENIENCE_TOOLS = []


def create_server() -> FastMCP:
    """Create the FINRA Query API MCP server."""
    mcp = FastMCP(
        name="FINRA Query API",
        version=__version__,
        instructions=(
            "Read-only MCP server for the FINRA Query API. "
            "It supports dataset discovery, metadata, read-only GET/POST queries, "
            "record lookup, pagination, and async query result retrieval. "
            "Submission API, Notification API, fileX, and write operations are not implemented."
        ),
    )
    for tool in GENERIC_TOOLS:
        mcp.tool(tags={"finra", "query-api", "read-only"})(tool)
    for tool in CONVENIENCE_TOOLS:
        mcp.tool(tags={"finra", "query-api", "read-only", "convenience"})(tool)
    return mcp


mcp = create_server()


def main() -> None:
    """Run the FastMCP server over stdio by default."""
    mcp.run()


if __name__ == "__main__":
    main()
