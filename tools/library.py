"""
Library management tools for Eagle MCP Server
"""
from typing import Dict, Any
from fastmcp import FastMCP
from utils.eagle_api import eagle_api_get, eagle_api_post

def register_library_tools(mcp: FastMCP):
    """Register library management MCP tools"""
    
    @mcp.tool()
    async def get_library_info() -> Dict[str, Any]:
        """Get information about the current library."""
        return await eagle_api_get("/api/library/info")

    @mcp.tool()
    async def get_library_history() -> Dict[str, Any]:
        """Get the list of libraries recently opened by the Application."""
        return await eagle_api_get("/api/library/history")

    @mcp.tool()
    async def switch_library(library_path: str) -> Dict[str, Any]:
        """
        Switch the library currently opened by Eagle.
        
        Args:
            library_path: Path to the library to switch to
        """
        payload = {"libraryPath": library_path}
        return await eagle_api_post("/api/library/switch", payload)

    @mcp.tool()
    async def get_library_icon(library_path: str) -> Dict[str, Any]:
        """
        Obtain the icon of the specified Library.
        Note: This endpoint is deprecated in the original Eagle API.
        
        Args:
            library_path: Path to the library
        """
        params = {"libraryPath": library_path}
        result = await eagle_api_get("/api/library/icon", params, is_binary=True)
        
        if isinstance(result, dict) and result.get("status") == "error":
            return result
            
        # For binary results, we need to handle differently in MCP context
        # Return a success message with info about the binary data
        return {
            "status": "success", 
            "message": "Library icon retrieved successfully (binary data)",
            "data": {"type": "binary_image"}
        }