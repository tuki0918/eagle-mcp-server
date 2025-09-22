import asyncio
from fastmcp import FastMCP
from tools import (
    register_application_tools,
    register_folder_tools,
    register_library_tools,
    register_item_tools,
)

# Create the FastMCP server
mcp = FastMCP("Eagle MCP Server", instructions="An MCP server for Eagle")

# Register all tools
register_application_tools(mcp)
register_folder_tools(mcp)
register_library_tools(mcp)
register_item_tools(mcp)


async def main():
    """Run the MCP server with stdio transport"""
    await mcp.run_async()


if __name__ == "__main__":
    asyncio.run(main())
