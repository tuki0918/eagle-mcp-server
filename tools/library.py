"""
Library related tools for Eagle MCP Server.
"""

from fastmcp import FastMCP
from utils.eagle_api import eagle_api_get, eagle_api_post


def register_library_tools(mcp: FastMCP):
    """Register library-related tools to the MCP server."""

    @mcp.tool
    async def get_library_info():
        """
        Get detailed information of the library currently running.

        The function can be used to obtain details such as `All Folders`,
        `All Smart Folders`, `All Tag Groups`, `Quick Access` and etc.

        Returns:
            dict: Library information including folders, tags, etc.
        """
        return await eagle_api_get("/api/library/info")

    @mcp.tool
    async def get_library_history():
        """
        Get the list of libraries recently opened by the Application.

        Returns:
            dict: List of recently opened libraries
        """
        return await eagle_api_get("/api/library/history")

    @mcp.tool
    async def switch_library(library_path: str):
        """
        Switch the library currently opened by Eagle.

        Args:
            library_path: The path of the library

        Returns:
            dict: Result of library switch operation
        """
        payload = {"libraryPath": library_path}
        return await eagle_api_post("/api/library/switch", payload)

    @mcp.tool
    async def get_library_icon(library_path: str):
        """
        Obtain the icon of the specified Library.

        Note: This function is deprecated and returns binary data info.

        Args:
            library_path: The path of the library

        Returns:
            dict: Information about the binary icon data
        """
        payload = {"libraryPath": library_path}
        result = await eagle_api_get("/api/library/icon", payload, is_binary=True)

        if isinstance(result, dict) and result.get("status") == "error":
            return result

        content, content_type = result
        # For MCP, we'll return the content type and a note about binary data
        return {
            "status": "success",
            "data": {
                "content_type": content_type,
                "data_size": len(content),
                "note": "Binary icon data available but not displayed in text format",
            },
        }
