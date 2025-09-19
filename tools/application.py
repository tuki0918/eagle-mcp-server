"""
Application tools for Eagle MCP Server
"""
from typing import Dict, Any
from fastmcp import FastMCP
from utils.eagle_api import eagle_api_get

def register_application_tools(mcp: FastMCP):
    """Register application-related MCP tools"""
    
    @mcp.tool()
    async def get_application_info() -> Dict[str, Any]:
        """
        Get detailed information on the Eagle App currently running. 
        In most cases, this could be used to determine whether certain functions are available on the user's device.
        """
        return await eagle_api_get("/api/application/info")