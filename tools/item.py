"""
Item management tools for Eagle MCP Server
"""
from typing import Optional, List, Any, Dict
from fastmcp import FastMCP
from utils.eagle_api import eagle_api_get, eagle_api_post
import os

def register_item_tools(mcp: FastMCP):
    """Register item management MCP tools"""
    
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
    async def add_item_from_url(url: str, name: Optional[str] = None, website: Optional[str] = None, tags: Optional[List[str]] = None, annotation: Optional[str] = None, folder_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Add an image from a URL to Eagle App. If you intend to add multiple items in a row, we suggest you use `add_items_from_urls`.
        
        Args:
            url: URL of the image to add
            name: Custom name for the item (optional)
            website: Website URL associated with the item (optional)
            tags: List of tags for the item (optional)
            annotation: Annotation text for the item (optional)
            folder_id: ID of the folder to add the item to (optional)
        """
        payload = {"url": url}
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
        return await eagle_api_post("/api/item/addFromURL", payload)

    @mcp.tool()
    async def add_items_from_urls(items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Add multiple images from URLs to Eagle App.
        
        Args:
            items: List of dictionaries with URL and optional metadata (name, website, tags, annotation, folderId)
        """
        payload = {"items": items}
        return await eagle_api_post("/api/item/addFromURLs", payload)

    @mcp.tool()
    async def add_items_from_paths(items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Add multiple local files to Eagle App.
        
        Args:
            items: List of dictionaries with path and optional metadata (name, website, tags, annotation, folderId)
        """
        payload = {"items": items}
        return await eagle_api_post("/api/item/addFromPaths", payload)

    @mcp.tool()
    async def add_bookmark(url: str, name: Optional[str] = None, base64: Optional[str] = None, tags: Optional[List[str]] = None, folder_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Save the link in the URL form to Eagle App.
        
        Args:
            url: URL to bookmark
            name: Custom name for the bookmark (optional)
            base64: Base64 encoded thumbnail image (optional)
            tags: List of tags for the bookmark (optional)
            folder_id: ID of the folder to add the bookmark to (optional)
        """
        payload = {"url": url}
        if name:
            payload["name"] = name
        if base64:
            payload["base64"] = base64
        if tags:
            payload["tags"] = tags
        if folder_id:
            payload["folderId"] = folder_id
        return await eagle_api_post("/api/item/addBookmark", payload)

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
    async def get_item_thumbnail(item_id: str) -> Dict[str, Any]:
        """
        Get the path of the thumbnail of the file specified. If you would like to get a batch of thumbnail paths, the combination of Library path + Object ID is recommended.
        
        Args:
            item_id: The item's ID
        """
        params = {"id": item_id}
        return await eagle_api_get("/api/item/thumbnail", params)

    @mcp.tool()
    async def get_item_source(item_id: str) -> Dict[str, Any]:
        """
        Get the source file information for a specific item.
        
        Args:
            item_id: The item's ID
        """
        # Get library info and item info to construct source path
        library = await eagle_api_get("/api/library/info")
        if library.get("status") != "success":
            return {"status": "error", "message": "Failed to fetch eagle info"}

        item = await eagle_api_get("/api/item/info", {"id": item_id})
        if item.get("status") != "success":
            return {"status": "error", "message": "Failed to fetch item info"}

        source_path = _construct_source_path(library, item)
        if source_path is None:
            return {"status": "error", "message": "Failed to fetch source path"}

        return {"status": "success", "data": {"source": source_path}}

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
    async def refresh_item_palette(item_id: str) -> Dict[str, Any]:
        """
        Re-analysis the color of the file. When changes to the original file were made, you can call this function to refresh the Color Analysis.
        
        Args:
            item_id: The item's ID
        """
        payload = {"id": item_id}
        return await eagle_api_post("/api/item/refreshPalette", payload)

    @mcp.tool()
    async def refresh_item_thumbnail(item_id: str) -> Dict[str, Any]:
        """
        Re-generate the thumbnail of the file used to display in the List. When changes to the original file were made, you can call this function to re-generate the thumbnail, the color analysis will also be made.
        
        Args:
            item_id: The item's ID
        """
        payload = {"id": item_id}
        return await eagle_api_post("/api/item/refreshThumbnail", payload)

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


def _construct_source_path(library: dict, item: dict) -> str | None:
    """Helper function to construct the source path for an item"""
    try:
        library_path = library["data"]["library"]["path"]
        item_id = item["data"]["id"]
        item_name = item["data"]["name"]
        item_ext = item["data"]["ext"]

        return os.path.join(
            library_path, "images", f"{item_id}.info", f"{item_name}.{item_ext}"
        )
    except KeyError:
        return None