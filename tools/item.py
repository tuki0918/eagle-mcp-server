import os
from typing import Optional, List, Dict, Annotated
from pydantic import Field
from fastmcp import FastMCP
from utils.eagle_api import eagle_api_get, eagle_api_post


def register_item_tools(mcp: FastMCP):
    """Register item-related tools to the MCP server."""

    @mcp.tool(
        tags={"Item", "disabled"},
        meta={"reference": "https://api.eagle.cool/item/add-from-url"},
    )
    async def add_item_from_url(
        url: Annotated[
            str,
            Field(
                description="The URL of the image to be added. Supports http, https, base64"
            ),
        ],
        name: Annotated[str, Field(description="The name of the image to be added")],
        folder_id: Annotated[
            Optional[str], Field(description="The ID of the folder to put the image in")
        ] = None,
        # NOTE: APIのドキュメントによっては、項目名がurlの場合がある
        website: Annotated[
            Optional[str], Field(description="The address of the source of the image")
        ] = None,
        tags: Annotated[
            Optional[List[str]], Field(description="Tags for the image")
        ] = None,
        # NOTE: APIのドキュメントによっては、記載されていない場合がある。実際には利用可能
        star: Annotated[
            Optional[int],
            Field(description="The rating for the image (0-5)", ge=0, le=5),
        ] = None,
        annotation: Annotated[
            Optional[str], Field(description="The annotation for the image")
        ] = None,
        modification_time: Annotated[
            Optional[int], Field(description="The creation date (ms) of the image")
        ] = None,
        headers: Annotated[
            Optional[Dict[str, str]],
            Field(description="Customize the HTTP headers properties"),
        ] = None,
    ):
        """
        Add an image from a URL to Eagle App.

        If you intend to add multiple items in a row, we suggest you use `add_items_from_urls`.

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

    @mcp.tool(
        tags={"Item", "disabled"},
        meta={"reference": "https://api.eagle.cool/item/add-from-urls"},
    )
    async def add_items_from_urls(
        items: Annotated[
            List[Dict],
            Field(
                description="List of items to add from URLs. Each item should contain url, name, and optional fields like website, tags, star, annotation, modification_time, headers"
            ),
        ],
        folder_id: Annotated[
            Optional[str],
            Field(description="The ID of the folder to put the images in"),
        ] = None,
    ):
        """
        Add multiple images from URLs to Eagle App.

        Each item in the items list should be a dictionary with the following structure:
        - url (required): The URL of the image
        - name (required): The name of the image
        - website (optional): The source website
        - tags (optional): List of tags
        - star (optional): Rating 0-5
        - annotation (optional): Annotation text
        - modification_time (optional): Creation date in ms
        - headers (optional): Custom HTTP headers

        Returns:
            dict: Result of the batch add operation
        """
        payload = {"items": items}
        if folder_id is not None:
            payload["folderId"] = folder_id
        return await eagle_api_post("/api/item/addFromURLs", payload)

    @mcp.tool(
        tags={"Item"},
        meta={"reference": "https://api.eagle.cool/item/add-from-path"},
    )
    async def add_item_from_path(
        path: Annotated[str, Field(description="The path of the local file")],
        name: Annotated[str, Field(description="The name of the image to be added")],
        folder_id: Annotated[
            Optional[str], Field(description="The ID of the folder to put the image in")
        ] = None,
        # NOTE: APIのドキュメントによっては、項目名がurlの場合がある
        website: Annotated[
            Optional[str], Field(description="The address of the source of the image")
        ] = None,
        tags: Annotated[
            Optional[List[str]], Field(description="Tags for the image")
        ] = None,
        # NOTE: APIのドキュメントによっては、記載されていない場合がある。実際には利用可能
        star: Annotated[
            Optional[int],
            Field(description="The rating for the image (0-5)", ge=0, le=5),
        ] = None,
        annotation: Annotated[
            Optional[str], Field(description="The annotation for the image")
        ] = None,
    ):
        """
        Add a local file to Eagle App.

        If you intend to add multiple items in a row, we suggest you use `add_items_from_paths`.

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

    @mcp.tool(
        tags={"Item", "disabled"},
        meta={"reference": "https://api.eagle.cool/item/add-from-paths"},
    )
    async def add_items_from_paths(
        # NOTE: ドキュメントがおそらく間違っている。
        items: Annotated[
            List[Dict],
            Field(
                description="List of items to add from local paths. Each item should contain path, name, and optional fields like website, tags, star, annotation"
            ),
        ],
        folder_id: Annotated[
            Optional[str],
            Field(description="The ID of the folder to put the images in"),
        ] = None,
    ):
        """
        Add multiple local files to Eagle App.

        Each item in the items list should be a dictionary with the following structure:
        - path (required): The local file path
        - name (required): The name of the image
        - website (optional): The source website
        - tags (optional): List of tags
        - star (optional): Rating 0-5
        - annotation (optional): Annotation text

        Returns:
            dict: Result of the batch add operation
        """
        payload = {"items": items}
        if folder_id is not None:
            payload["folderId"] = folder_id
        return await eagle_api_post("/api/item/addFromPaths", payload)

    @mcp.tool(
        tags={"Item", "disabled"},
        meta={"reference": "https://api.eagle.cool/item/add-bookmark"},
        enabled=False,
    )
    async def add_bookmark(
        url: Annotated[str, Field(description="The URL of the bookmark to be added")],
        # NOTE: base64が指定されていない場合は、URL遷移先のページのタイトルが反映される
        name: Annotated[str, Field(description="The name/title of the bookmark")],
        # NOTE: 未指定の場合はURL遷移先のページのスクリーンショットが反映される
        base64: Annotated[
            Optional[str],
            Field(
                description="The thumbnail of the bookmark. Must be in base64 format."
            ),
        ] = None,
        folder_id: Annotated[
            Optional[str],
            Field(description="The ID of the folder to put the bookmark in"),
        ] = None,
        tags: Annotated[
            Optional[List[str]], Field(description="Tags for the bookmark")
        ] = None,
        modification_time: Annotated[
            Optional[int], Field(description="The creation date (ms) of the bookmark")
        ] = None,
    ):
        """
        Save the link in the URL form to Eagle App.

        Returns:
            dict: Result of the bookmark add operation
        """
        payload = {"url": url, "name": name}
        if base64 is not None:
            payload["base64"] = base64
        if folder_id is not None:
            payload["folderId"] = folder_id
        if tags is not None:
            payload["tags"] = tags
        if modification_time is not None:
            payload["modificationTime"] = modification_time
        return await eagle_api_post("/api/item/addBookmark", payload)

    @mcp.tool(
        tags={"Item"},
        meta={"reference": "https://api.eagle.cool/item/info"},
    )
    async def get_item_info(
        item_id: Annotated[str, Field(description="ID of the file")],
    ):
        """
        Get Properties of the specified file.

        Including the file name, tags, categorizations, folders, dimensions, etc.

        Returns:
            dict: Item information including metadata
        """
        payload = {"id": item_id}
        return await eagle_api_get("/api/item/info", payload)

    @mcp.tool(
        tags={"Item", "disabled"},
        meta={"reference": "https://api.eagle.cool/item/thumbnail"},
        enabled=False,
    )
    async def get_item_thumbnail(
        item_id: Annotated[str, Field(description="ID of the file")],
    ):
        """
        Get the path of the thumbnail of the file specified.

        If you would like to get a batch of thumbnail paths,
        the combination of Library path + Object ID is recommended.

        Returns:
            dict: Thumbnail path information
        """
        payload = {"id": item_id}
        return await eagle_api_get("/api/item/thumbnail", payload)

    @mcp.tool(
        tags={"Item"},
        meta={"reference": "https://api.eagle.cool/item/list"},
    )
    async def get_item_list(
        limit: Annotated[
            Optional[int],
            Field(
                description="The number of items to be displayed (1-200)", ge=1, le=200
            ),
        ] = 200,
        offset: Annotated[
            Optional[int],
            Field(description="Offset a collection of results from the api", ge=0),
        ] = 0,
        order_by: Annotated[
            Optional[str],
            Field(
                description="The sorting order. CREATEDATE, FILESIZE, NAME, RESOLUTION, add minus for descending"
            ),
        ] = None,
        keyword: Annotated[
            Optional[str], Field(description="Filter by the keyword")
        ] = None,
        ext: Annotated[
            Optional[str],
            Field(description="Filter by the extension type, e.g.: jpg, png"),
        ] = None,
        tags: Annotated[
            Optional[str],
            Field(
                description="Filter by tags. Use , to divide different tags. E.g.: Design, Poster"
            ),
        ] = None,
        folders: Annotated[
            Optional[str],
            Field(description="Filter by Folders. Use , to divide folder IDs"),
        ] = None,
    ):
        """
        Get items that match the filter condition.

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

    @mcp.tool(
        tags={"Item"},
        meta={"reference": "https://api.eagle.cool/item/api-item-movetotrash"},
    )
    async def move_item_to_trash(
        item_ids: Annotated[
            List[str], Field(description="List of item IDs to move to trash")
        ],
    ):
        """
        Move items to trash.

        Returns:
            dict: Result of the move operation
        """
        payload = {"itemIds": item_ids}
        return await eagle_api_post("/api/item/moveToTrash", payload)

    @mcp.tool(
        tags={"Item", "disabled"},
        meta={"reference": "https://api.eagle.cool/item/refresh-palette"},
        enabled=False,
    )
    async def refresh_item_palette(
        item_id: Annotated[str, Field(description="The item's ID")],
    ):
        """
        Re-analysis the color of the file.

        When changes to the original file were made, you can call this function
        to refresh the Color Analysis.

        Returns:
            dict: Result of the refresh operation
        """
        payload = {"id": item_id}
        return await eagle_api_post("/api/item/refreshPalette", payload)

    @mcp.tool(
        tags={"Item", "disabled"},
        meta={"reference": "https://api.eagle.cool/item/refresh-thumbnail"},
        enabled=False,
    )
    async def refresh_item_thumbnail(
        item_id: Annotated[str, Field(description="The item's ID")],
    ):
        """
        Re-generate the thumbnail of the file used to display in the List.

        When changes to the original file were made, you can call this function
        to re-generate the thumbnail, the color analysis will also be made.

        Returns:
            dict: Result of the refresh operation
        """
        payload = {"id": item_id}
        return await eagle_api_post("/api/item/refreshThumbnail", payload)

    @mcp.tool(
        tags={"Item"},
        meta={"reference": "https://api.eagle.cool/item/update"},
    )
    async def update_item(
        item_id: Annotated[str, Field(description="The ID of the item to be modified")],
        tags: Annotated[
            Optional[List[str]], Field(description="Tags for the item")
        ] = None,
        annotation: Annotated[
            Optional[str], Field(description="Annotations for the item")
        ] = None,
        url: Annotated[Optional[str], Field(description="The source url")] = None,
        star: Annotated[
            Optional[int], Field(description="Ratings (0-5)", ge=0, le=5)
        ] = None,
        # NOTE: APIのドキュメントに項目が無く、API経由での更新できない
        # name: ...
        # folders: ...
    ):
        """
        Modify data of specified fields of the item.

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

    @mcp.tool(
        tags={"Item"},
    )
    async def get_item_source(
        item_id: Annotated[str, Field(description="ID of the file")],
    ):
        """
        Get the source path of the file specified.

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
