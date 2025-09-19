"""
Item tools for Eagle MCP Server
"""
import os
from fastmcp import tool
from pydantic import BaseModel, Field
from typing import Annotated, Dict, Optional, List, Literal, Union
from enum import Enum
from utils.eagle_api import eagle_api_get, eagle_api_post


class AddBaseItem(BaseModel):
    name: Annotated[
        str, Field(..., description="Required, the name of the image to be added.")
    ]
    website: Annotated[
        Optional[str], Field(None, description="The Address of the source of the image")
    ]
    tags: Annotated[Optional[List[str]], Field(None, description="Tags for the image.")]
    star: Annotated[
        Optional[int], Field(None, ge=0, le=5, description="The rating for the image.")
    ]
    annotation: Annotated[
        Optional[str], Field(None, description="The annotation for the image.")
    ]


class AddBaseItemFromURL(AddBaseItem):
    url: Annotated[
        str,
        Field(
            ...,
            description="Required, the URL of the image to be added. Supports http, https, base64",
        ),
    ]
    modificationTime: Annotated[
        Optional[int],
        Field(
            None,
            description="The creation date (ms) of the image. The parameter can be used to alter the image's sorting order in Eagle.",
        ),
    ]
    headers: Annotated[
        Optional[Dict[str, str]],
        Field(
            None,
            description="Optional, customize the HTTP headers properties, this could be used to circumvent the security of certain websites.",
        ),
    ]


class AddBaseItemFromPath(AddBaseItem):
    path: Annotated[
        str, Field(..., description="Required, the path of the local file.")
    ]


class AddItemFromURLRequest(AddBaseItemFromURL):
    folderId: Annotated[
        Optional[str], Field(None, description="The ID of the folder to put")
    ]


class AddItemsFromURLsRequest(BaseModel):
    items: Annotated[
        List[AddBaseItemFromURL],
        Field(..., description="Required, list of items to be added"),
    ]
    folderId: Annotated[
        Optional[str], Field(None, description="The ID of the folder to put")
    ]


class AddItemFromPathRequest(AddBaseItemFromPath):
    folderId: Annotated[
        Optional[str], Field(None, description="The ID of the folder to put")
    ]


class AddItemsFromPathsRequest(BaseModel):
    items: Annotated[
        List[AddBaseItemFromPath],
        Field(..., description="Required, list of items to be added"),
    ]
    folderId: Annotated[
        Optional[str], Field(None, description="The ID of the folder to put")
    ]


class AddBookmarkRequest(BaseModel):
    url: Annotated[
        str,
        Field(
            ...,
            description="Required, the URL of the bookmark to be added",
        ),
    ]
    name: Annotated[
        str, Field(..., description="Required, the name/title of the bookmark")
    ]
    folderId: Annotated[
        Optional[str], Field(None, description="The ID of the folder to put")
    ]
    tags: Annotated[Optional[List[str]], Field(None, description="Optional, tags")]
    modificationTime: Annotated[
        Optional[int],
        Field(
            None,
            description="The creation date (ms) of the bookmark",
        ),
    ]


class GetItemInfoRequest(BaseModel):
    id: Annotated[
        str,
        Field(
            ...,
            description="ID of the file",
        ),
    ]


class GetItemThumbnailRequest(BaseModel):
    id: Annotated[
        str,
        Field(
            ...,
            description="ID of the file",
        ),
    ]


class OrderBy(str, Enum):
    CREATE_TIME = "CREATETIME"
    FILESIZE = "FILESIZE"
    NAME = "NAME"
    RESOLUTION = "RESOLUTION"


class OrderSort(str, Enum):
    ASC = "ASC"
    DESC = "DESC"


class GetItemListRequest(BaseModel):
    orderBy: Annotated[
        Optional[OrderBy], Field(None, description="Order by")
    ]
    orderSort: Annotated[
        Optional[OrderSort], Field(None, description="Order sort")
    ]
    keyword: Annotated[
        Optional[str],
        Field(
            None,
            description="Keyword search. The searching scopes include filename, annotation, tags, and directory name.",
        ),
    ]
    ext: Annotated[
        Optional[str],
        Field(
            None,
            description="Filter by file extension. Use `,` to divide different extensions. E.g.: `jpg, png`",
        ),
    ]
    tags: Annotated[
        Optional[str],
        Field(
            None,
            description="Filter by tags. Use `,` to divide different tags. E.g.: `Design, Poster`",
        ),
    ]
    folders: Annotated[
        Optional[str],
        Field(
            None,
            description="Filter by Folders. Use `,` to divide folder IDs. E.g.: `KAY6NTU6UYI5Q,KBJ8Z60O88VMG`",
        ),
    ]


class MoveItemToTrashRequest(BaseModel):
    itemIds: Annotated[
        List[str],
        Field(
            ...,
            description="Required, ID of the file",
        ),
    ]


class RefreshItemPaletteRequest(BaseModel):
    id: Annotated[
        str,
        Field(
            ...,
            description="The item's ID",
        ),
    ]


class RefreshItemThumbnailRequest(BaseModel):
    id: Annotated[
        str,
        Field(
            ...,
            description="The item's ID",
        ),
    ]


class UpdateItemRequest(BaseModel):
    id: Annotated[
        str,
        Field(
            ...,
            description="Required, the ID of the item to be modified",
        ),
    ]
    tags: Annotated[Optional[List[str]], Field(None, description="Optional, tags")]
    annotation: Annotated[
        Optional[str], Field(None, description="Optional, annotations")
    ]
    url: Annotated[Optional[str], Field(None, description="Optional, the source url")]
    star: Annotated[
        Optional[int], Field(None, ge=0, le=5, description="Optional, ratings")
    ]


class GetItemSourceRequest(BaseModel):
    id: Annotated[
        str,
        Field(
            ...,
            description="ID of the file",
        ),
    ]


@tool
async def add_item_from_url(data: AddItemFromURLRequest):
    """
    Add an image from a URL to Eagle App.
    
    If you intend to add multiple items in a row, we suggest you use `add_items_from_urls`.
    
    Args:
        data: Item data including URL, name, and optional metadata
        
    Returns:
        dict: Result of the add operation
    """
    payload = data.model_dump(exclude_none=True)
    return await eagle_api_post("/api/item/addFromURL", payload)


@tool
async def add_items_from_urls(data: AddItemsFromURLsRequest):
    """
    Add multiple images from URLs to Eagle App.
    
    Args:
        data: List of items to add from URLs with optional folder
        
    Returns:
        dict: Result of the batch add operation
    """
    payload = data.model_dump(exclude_none=True)
    payload["items"] = [item.model_dump(exclude_none=True) for item in data.items]
    return await eagle_api_post("/api/item/addFromURLs", payload)


@tool
async def add_item_from_path(data: AddItemFromPathRequest):
    """
    Add a local file to Eagle App.
    
    If you intend to add multiple items in a row, we suggest you use `add_items_from_paths`.
    
    Args:
        data: Item data including local file path, name, and optional metadata
        
    Returns:
        dict: Result of the add operation
    """
    payload = data.model_dump(exclude_none=True)
    return await eagle_api_post("/api/item/addFromPath", payload)


@tool
async def add_items_from_paths(data: AddItemsFromPathsRequest):
    """
    Add multiple local files to Eagle App.
    
    Args:
        data: List of items to add from local paths with optional folder
        
    Returns:
        dict: Result of the batch add operation
    """
    payload = data.model_dump(exclude_none=True)
    payload["items"] = [item.model_dump(exclude_none=True) for item in data.items]
    return await eagle_api_post("/api/item/addFromPaths", payload)


@tool
async def add_bookmark(data: AddBookmarkRequest):
    """
    Save the link in the URL form to Eagle App.
    
    Args:
        data: Bookmark data including URL, name, and optional metadata
        
    Returns:
        dict: Result of the bookmark add operation
    """
    payload = data.model_dump(exclude_none=True)
    return await eagle_api_post("/api/item/addBookmark", payload)


@tool
async def get_item_info(data: GetItemInfoRequest):
    """
    Get Properties of the specified file.
    
    Including the file name, tags, categorizations, folders, dimensions, etc.
    
    Args:
        data: Request with item ID
        
    Returns:
        dict: Item information including metadata
    """
    payload = data.model_dump(exclude_none=True)
    return await eagle_api_get("/api/item/info", payload)


@tool
async def get_item_thumbnail(data: GetItemThumbnailRequest):
    """
    Get the path of the thumbnail of the file specified.
    
    If you would like to get a batch of thumbnail paths, 
    the combination of Library path + Object ID is recommended.
    
    Args:
        data: Request with item ID
        
    Returns:
        dict: Thumbnail path information
    """
    payload = data.model_dump(exclude_none=True)
    return await eagle_api_get("/api/item/thumbnail", payload)


@tool
async def get_item_list(data: GetItemListRequest):
    """
    Get items that match the filter condition.
    
    Args:
        data: Filter criteria including keywords, extensions, tags, folders, etc.
        
    Returns:
        dict: List of items matching the criteria
    """
    payload = data.model_dump(exclude_none=True)
    return await eagle_api_get("/api/item/list", payload)


@tool
async def move_item_to_trash(data: MoveItemToTrashRequest):
    """
    Move items to trash.
    
    Args:
        data: Request with list of item IDs to move to trash
        
    Returns:
        dict: Result of the move operation
    """
    payload = data.model_dump(exclude_none=True)
    return await eagle_api_post("/api/item/moveToTrash", payload)


@tool
async def refresh_item_palette(data: RefreshItemPaletteRequest):
    """
    Re-analysis the color of the file.
    
    When changes to the original file were made, you can call this function 
    to refresh the Color Analysis.
    
    Args:
        data: Request with item ID
        
    Returns:
        dict: Result of the refresh operation
    """
    payload = data.model_dump(exclude_none=True)
    return await eagle_api_post("/api/item/refreshPalette", payload)


@tool
async def refresh_item_thumbnail(data: RefreshItemThumbnailRequest):
    """
    Re-generate the thumbnail of the file used to display in the List.
    
    When changes to the original file were made, you can call this function 
    to re-generate the thumbnail, the color analysis will also be made.
    
    Args:
        data: Request with item ID
        
    Returns:
        dict: Result of the refresh operation
    """
    payload = data.model_dump(exclude_none=True)
    return await eagle_api_post("/api/item/refreshThumbnail", payload)


@tool
async def update_item(data: UpdateItemRequest):
    """
    Modify data of specified fields of the item.
    
    Args:
        data: Item update data including ID and fields to modify
        
    Returns:
        dict: Result of the update operation
    """
    payload = data.model_dump(exclude_none=True)
    return await eagle_api_post("/api/item/update", payload)


@tool
async def get_item_source(data: GetItemSourceRequest):
    """
    Get the source path of the file specified.
    
    Args:
        data: Request with item ID
        
    Returns:
        dict: Source path information or error
    """
    payload = data.model_dump(exclude_none=True)

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
    
    Args:
        library: Library information from API
        item: Item information from API
        
    Returns:
        str | None: Constructed source path or None if failed
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


# List of all item tools
item_tools = [
    add_item_from_url,
    add_items_from_urls, 
    add_item_from_path,
    add_items_from_paths,
    add_bookmark,
    get_item_info,
    get_item_thumbnail,
    get_item_list,
    move_item_to_trash,
    refresh_item_palette,
    refresh_item_thumbnail,
    update_item,
    get_item_source,
]