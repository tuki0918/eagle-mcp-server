"""
Connection tools for Eagle MCP Server
"""
from typing import Dict
from fastmcp import FastMCP

def register_connection_tools(mcp: FastMCP):
    """Register connection-related MCP tools"""
    
    @mcp.tool()
    async def connect() -> Dict[str, str]:
        """Connect to Eagle MCP Server."""
        return {"status": "success", "message": "Connected!"}