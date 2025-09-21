"""
Application related tools for Eagle MCP Server.
"""

from fastmcp import FastMCP
from utils.eagle_api import eagle_api_get


def register_application_tools(mcp: FastMCP):
    """Register application-related tools to the MCP server."""

    @mcp.tool
    async def get_application_info():
        """
        Get detailed information on the Eagle App currently running.

        In most cases, this could be used to determine whether certain functions
        are available on the user's device.

        Returns:
            dict: Application information including version, platform, etc.
        """
        return await eagle_api_get("/api/application/info")
