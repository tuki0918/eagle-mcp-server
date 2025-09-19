#!/usr/bin/env python3
"""
Eagle MCP Server - A Model Context Protocol server for Eagle App
Migrated from fastapi-mcp to FastMCP 2.0 for stdio transport
"""

from fastmcp import FastMCP
from tools.connection import register_connection_tools
from tools.application import register_application_tools
from tools.folder import register_folder_tools
from tools.item import register_item_tools
from tools.library import register_library_tools

# Initialize FastMCP server
mcp = FastMCP("Eagle MCP Server", "An MCP server for Eagle App")

# Register all tool groups
register_connection_tools(mcp)
register_application_tools(mcp)
register_folder_tools(mcp)
register_item_tools(mcp)
register_library_tools(mcp)

if __name__ == "__main__":
    # Run the MCP server using stdio transport
    mcp.run()
