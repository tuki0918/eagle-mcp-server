#!/usr/bin/env python3
"""
Eagle MCP Server - A Model Context Protocol server for Eagle App
Migrated from fastapi-mcp to FastMCP 2.0 for stdio transport
"""

import asyncio
from typing import Optional, List, Any, Dict
from fastmcp import FastMCP
from utils.eagle_api import eagle_api_get, eagle_api_post

# Initialize FastMCP server
mcp = FastMCP("Eagle MCP Server", "An MCP server for Eagle App")

# MCP Tools - Connection
@mcp.tool()
async def connect() -> Dict[str, str]:
    """Connect to Eagle MCP Server."""
    return {"status": "success", "message": "Connected!"}

# Application Tools
@mcp.tool()
async def get_application_info() -> Dict[str, Any]:
    """
    Get detailed information on the Eagle App currently running. 
    In most cases, this could be used to determine whether certain functions are available on the user's device.
    """
    return await eagle_api_get("/api/application/info")

# Folder Tools
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

# Item Tools
@mcp.tool()
async def add_item_from_path(path: str, name: Optional[str] = None, website: Optional[str] = None, tags: Optional[List[str]] = None, annotation: Optional[str] = None, folder_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Add an image from a local file path to Eagle App.
    
    Args:
        path: Local file path to add
        name: Custom name for the item (optional)
        website: Website URL associated with the item (optional)
        tags: List of tags for the item (optional)
        annotation: Annotation text for the item (optional)
        folder_id: ID of the folder to add the item to (optional)
    """
    payload = {"path": path}
    if name:
        payload["name"] = name
    if website:
        payload["website"] = website
    if tags:
        payload["tags"] = tags
    if annotation:
        payload["annotation"] = annotation
    if folder_id:
        payload["folderId"] = folder_id
    return await eagle_api_post("/api/item/addFromPath", payload)

@mcp.tool() 
async def get_item_info(item_id: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific item.
    
    Args:
        item_id: The item's ID
    """
    params = {"id": item_id}
    return await eagle_api_get("/api/item/info", params)

@mcp.tool()
async def get_item_source(item_id: str) -> Dict[str, Any]:
    """
    Get the source file information for a specific item.
    
    Args:
        item_id: The item's ID
    """
    params = {"id": item_id}
    return await eagle_api_get("/api/item/source", params)

@mcp.tool()
async def get_item_list(
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    order_by: Optional[str] = None,
    keyword: Optional[str] = None,
    ext: Optional[str] = None,
    tags: Optional[List[str]] = None,
    folders: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Get a list of items from the current library.
    
    Args:
        limit: Maximum number of items to return (optional)
        offset: Number of items to skip (optional)
        order_by: Sort order - CREATEDATE, FILESIZE, NAME, RESOLUTION (optional)
        keyword: Search keyword (optional)
        ext: File extension filter (optional)
        tags: Filter by tags (optional)
        folders: Filter by folder IDs (optional)
    """
    params = {}
    if limit is not None:
        params["limit"] = limit
    if offset is not None:
        params["offset"] = offset
    if order_by:
        params["orderBy"] = order_by
    if keyword:
        params["keyword"] = keyword
    if ext:
        params["ext"] = ext
    if tags:
        params["tags"] = tags
    if folders:
        params["folders"] = folders
    return await eagle_api_get("/api/item/list", params)

@mcp.tool()
async def move_item_to_trash(item_id: str) -> Dict[str, Any]:
    """
    Move an item to trash.
    
    Args:
        item_id: The item's ID
    """
    payload = {"id": item_id}
    return await eagle_api_post("/api/item/moveToTrash", payload)

@mcp.tool()
async def update_item(
    item_id: str,
    name: Optional[str] = None,
    annotation: Optional[str] = None,
    website: Optional[str] = None,
    tags: Optional[List[str]] = None,
    folder_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Update an item's metadata.
    
    Args:
        item_id: The item's ID
        name: New name for the item (optional)
        annotation: New annotation text (optional)
        website: New website URL (optional)
        tags: New tags list (optional)
        folder_id: New folder ID to move item to (optional)
    """
    payload = {"id": item_id}
    if name:
        payload["name"] = name
    if annotation:
        payload["annotation"] = annotation
    if website:
        payload["website"] = website
    if tags:
        payload["tags"] = tags
    if folder_id:
        payload["folderId"] = folder_id
    return await eagle_api_post("/api/item/update", payload)

# Library Tools
@mcp.tool()
async def get_library_info() -> Dict[str, Any]:
    """Get information about the current library."""
    return await eagle_api_get("/api/library/info")

if __name__ == "__main__":
    # Run the MCP server using stdio transport
    mcp.run()
