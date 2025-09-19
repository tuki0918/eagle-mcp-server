"""
Folder management tools for Eagle MCP Server
"""
from typing import Optional, Dict, Any
from fastmcp import FastMCP
from utils.eagle_api import eagle_api_get, eagle_api_post

def register_folder_tools(mcp: FastMCP):
    """Register folder management MCP tools"""
    
    @mcp.tool()
    async def create_folder(folder_name: str, parent: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a folder. The created folder will be put at the bottom of the folder list of the current library.
        
        Args:
            folder_name: Name of the folder
            parent: ID of the parent folder (optional)
        """
        payload = {"folderName": folder_name}
        if parent:
            payload["parent"] = parent
        return await eagle_api_post("/api/folder/create", payload)

    @mcp.tool()
    async def update_folder(
        folder_id: str, 
        new_name: Optional[str] = None,
        new_description: Optional[str] = None,
        new_color: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update the specified folder.
        
        Args:
            folder_id: The folder's ID
            new_name: The new name of the folder (optional)
            new_description: The new description of the folder (optional)
            new_color: The new color of the folder - "red","orange","green","yellow","aqua","blue","purple","pink" (optional)
        """
        payload = {"folderId": folder_id}
        if new_name:
            payload["newName"] = new_name
        if new_description:
            payload["newDescription"] = new_description
        if new_color:
            payload["newColor"] = new_color
        return await eagle_api_post("/api/folder/update", payload)

    @mcp.tool()
    async def get_folder_list() -> Dict[str, Any]:
        """Get the list of folders of the current library."""
        return await eagle_api_get("/api/folder/list")