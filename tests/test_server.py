from __future__ import annotations

import asyncio

from finra_mcp.server import CONVENIENCE_TOOLS, GENERIC_TOOLS, create_server


def test_server_registers_expected_readonly_tools() -> None:
    async def main() -> None:
        mcp = create_server()
        tools = await mcp.list_tools(run_middleware=False)
        names = {tool.name for tool in tools}

        expected = {tool.__name__ for tool in [*GENERIC_TOOLS, *CONVENIENCE_TOOLS]}
        assert expected <= names
        assert len(names) == len(expected)
        forbidden = {
            "create",
            "update",
            "delete",
            "submit",
            "acknowledge",
            "upload",
            "subscribe",
            "unsubscribe",
            "send",
        }
        assert names.isdisjoint(forbidden)

    asyncio.run(main())
