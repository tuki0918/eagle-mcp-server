"""
Item related tools for Eagle MCP Server.
"""

import os
from typing import Optional, List, Dict
from fastmcp import FastMCP
from utils.eagle_api import eagle_api_get, eagle_api_post


def register_item_tools(mcp: FastMCP):
    """Register item-related tools to the MCP server."""

    @mcp.tool
    async def add_item_from_url(
        url: str,
        name: str,
        folder_id: Optional[str] = None,
        website: Optional[str] = None,
        tags: Optional[List[str]] = None,
        star: Optional[int] = None,
        annotation: Optional[str] = None,
        modification_time: Optional[int] = None,
        headers: Optional[Dict[str, str]] = None,
    ):
        """
        Add an image from a URL to Eagle App.

        If you intend to add multiple items in a row, we suggest you use `add_items_from_urls`.

        Args:
            url: The URL of the image to be added. Supports http, https, base64
            name: The name of the image to be added
            folder_id: The ID of the folder to put the image in (optional)
            website: The address of the source of the image (optional)
            tags: Tags for the image (optional)
            star: The rating for the image (0-5) (optional)
            annotation: The annotation for the image (optional)
            modification_time: The creation date (ms) of the image (optional)
            headers: Customize the HTTP headers properties (optional)

        Returns:
            dict: Result of the add operation
        """
        payload = {"url": url, "name": name}
        if folder_id is not None:
            payload["folderId"] = folder_id
        if website is not None:
            payload["website"] = website
        if tags is not None:
            payload["tags"] = tags
        if star is not None:
            payload["star"] = star
        if annotation is not None:
            payload["annotation"] = annotation
        if modification_time is not None:
            payload["modificationTime"] = modification_time
        if headers is not None:
            payload["headers"] = headers
        return await eagle_api_post("/api/item/addFromURL", payload)

    @mcp.tool
    async def add_item_from_path(
        path: str,
        name: str,
        folder_id: Optional[str] = None,
        website: Optional[str] = None,
        tags: Optional[List[str]] = None,
        star: Optional[int] = None,
        annotation: Optional[str] = None,
    ):
        """
        Add a local file to Eagle App.

        If you intend to add multiple items in a row, we suggest you use `add_items_from_paths`.

        Args:
            path: The path of the local file
            name: The name of the image to be added
            folder_id: The ID of the folder to put the image in (optional)
            website: The address of the source of the image (optional)
            tags: Tags for the image (optional)
            star: The rating for the image (0-5) (optional)
            annotation: The annotation for the image (optional)

        Returns:
            dict: Result of the add operation
        """
        payload = {"path": path, "name": name}
        if folder_id is not None:
            payload["folderId"] = folder_id
        if website is not None:
            payload["website"] = website
        if tags is not None:
            payload["tags"] = tags
        if star is not None:
            payload["star"] = star
        if annotation is not None:
            payload["annotation"] = annotation
        return await eagle_api_post("/api/item/addFromPath", payload)

    @mcp.tool
    async def add_bookmark(
        url: str,
        name: str,
        folder_id: Optional[str] = None,
        tags: Optional[List[str]] = None,
        modification_time: Optional[int] = None,
    ):
        """
        Save the link in the URL form to Eagle App.

        Args:
            url: The URL of the bookmark to be added
            name: The name/title of the bookmark
            folder_id: The ID of the folder to put the bookmark in (optional)
            tags: Tags for the bookmark (optional)
            modification_time: The creation date (ms) of the bookmark (optional)

        Returns:
            dict: Result of the bookmark add operation
        """
        payload = {"url": url, "name": name}
        if folder_id is not None:
            payload["folderId"] = folder_id
        if tags is not None:
            payload["tags"] = tags
        if modification_time is not None:
            payload["modificationTime"] = modification_time
        return await eagle_api_post("/api/item/addBookmark", payload)

    @mcp.tool
    async def get_item_info(item_id: str):
        """
        Get Properties of the specified file.

        Including the file name, tags, categorizations, folders, dimensions, etc.

        Args:
            item_id: ID of the file

        Returns:
            dict: Item information including metadata
        """
        payload = {"id": item_id}
        return await eagle_api_get("/api/item/info", payload)

    @mcp.tool
    async def get_item_thumbnail(item_id: str):
        """
        Get the path of the thumbnail of the file specified.

        If you would like to get a batch of thumbnail paths,
        the combination of Library path + Object ID is recommended.

        Args:
            item_id: ID of the file

        Returns:
            dict: Thumbnail path information
        """
        payload = {"id": item_id}
        return await eagle_api_get("/api/item/thumbnail", payload)

    @mcp.tool
    async def get_item_list(
        limit: Optional[int] = 200,
        offset: Optional[int] = 0,
        order_by: Optional[str] = None,
        keyword: Optional[str] = None,
        ext: Optional[str] = None,
        tags: Optional[str] = None,
        folders: Optional[str] = None,
    ):
        """
        Get items that match the filter condition.

        Args:
            limit: The number of items to be displayed (1-200, default: 200)
            offset: Offset a collection of results from the api (default: 0)
            order_by: The sorting order. CREATEDATE, FILESIZE, NAME, RESOLUTION, add minus for descending
            keyword: Filter by the keyword
            ext: Filter by the extension type, e.g.: jpg, png
            tags: Filter by tags. Use , to divide different tags. E.g.: Design, Poster
            folders: Filter by Folders. Use , to divide folder IDs

        Returns:
            dict: List of items matching the criteria
        """
        payload = {"limit": limit, "offset": offset}
        if order_by is not None:
            payload["orderBy"] = order_by
        if keyword is not None:
            payload["keyword"] = keyword
        if ext is not None:
            payload["ext"] = ext
        if tags is not None:
            payload["tags"] = tags
        if folders is not None:
            payload["folders"] = folders
        return await eagle_api_get("/api/item/list", payload)

    @mcp.tool
    async def move_item_to_trash(item_ids: List[str]):
        """
        Move items to trash.

        Args:
            item_ids: List of item IDs to move to trash

        Returns:
            dict: Result of the move operation
        """
        payload = {"itemIds": item_ids}
        return await eagle_api_post("/api/item/moveToTrash", payload)

    @mcp.tool
    async def refresh_item_palette(item_id: str):
        """
        Re-analysis the color of the file.

        When changes to the original file were made, you can call this function
        to refresh the Color Analysis.

        Args:
            item_id: The item's ID

        Returns:
            dict: Result of the refresh operation
        """
        payload = {"id": item_id}
        return await eagle_api_post("/api/item/refreshPalette", payload)

    @mcp.tool
    async def refresh_item_thumbnail(item_id: str):
        """
        Re-generate the thumbnail of the file used to display in the List.

        When changes to the original file were made, you can call this function
        to re-generate the thumbnail, the color analysis will also be made.

        Args:
            item_id: The item's ID

        Returns:
            dict: Result of the refresh operation
        """
        payload = {"id": item_id}
        return await eagle_api_post("/api/item/refreshThumbnail", payload)

    @mcp.tool
    async def update_item(
        item_id: str,
        tags: Optional[List[str]] = None,
        annotation: Optional[str] = None,
        url: Optional[str] = None,
        star: Optional[int] = None,
    ):
        """
        Modify data of specified fields of the item.

        Args:
            item_id: The ID of the item to be modified
            tags: Tags for the item (optional)
            annotation: Annotations for the item (optional)
            url: The source url (optional)
            star: Ratings (0-5) (optional)

        Returns:
            dict: Result of the update operation
        """
        payload = {"id": item_id}
        if tags is not None:
            payload["tags"] = tags
        if annotation is not None:
            payload["annotation"] = annotation
        if url is not None:
            payload["url"] = url
        if star is not None:
            payload["star"] = star
        return await eagle_api_post("/api/item/update", payload)

    @mcp.tool
    async def get_item_source(item_id: str):
        """
        Get the source path of the file specified.

        Args:
            item_id: ID of the file

        Returns:
            dict: Source path information or error
        """
        payload = {"id": item_id}

        # Get library info first
        library = await eagle_api_get("/api/library/info")
        if library.get("status") != "success":
            return {"status": "error", "message": "Failed to fetch eagle info"}

        # Get item info
        item = await eagle_api_get("/api/item/info", payload)
        if item.get("status") != "success":
            return {"status": "error", "message": "Failed to fetch item info"}

        # Construct source path
        source_path = construct_source_path(library, item)
        if source_path is None:
            return {"status": "error", "message": "Failed to fetch source path"}

        return {"status": "success", "data": {"source": source_path}}


def construct_source_path(library: dict, item: dict) -> str | None:
    """
    Construct the source path for an item based on library and item info.
    """
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
