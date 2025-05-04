from fastapi import APIRouter
from schemas.api import ErrorResponse
from schemas.item import (
    AddItemFromURLRequest,
    AddItemsFromURLsRequest,
    AddItemFromPathRequest,
    AddItemsFromPathsRequest,
    AddBookmarkRequest,
    GetItemInfoRequest,
    GetItemThumbnailRequest,
    GetItemListRequest,
    GetItemSourceRequest,
    MoveItemToTrashRequest,
    RefreshItemPaletteRequest,
    RefreshItemThumbnailRequest,
    UpdateItemRequest,
    GetItemSourceResponse,
    GetItemSourceSuccessResponse,
)
from utils.eagle_api import eagle_api_get, eagle_api_post
import os

router = APIRouter(tags=["Item"])


@router.post(
    "/api/item/addFromURL",
    operation_id="add_item_from_url",
    description=(
        "Add an image from a URL to Eagle App. If you intend to add multiple items in a row, we suggest you use `add_items_from_urls`."
    ),
    tags=["Disabled"],
)
async def add_item_from_url(data: AddItemFromURLRequest):
    """
    reference: https://api.eagle.cool/item/add-from-url
    """
    payload = data.model_dump(exclude_none=True)
    return await eagle_api_post("/api/item/addFromURL", payload)


@router.post(
    "/api/item/addFromURLs",
    operation_id="add_items_from_urls",
    description=("Add multiple images from URLs to Eagle App."),
    tags=["Disabled"],
)
async def add_items_from_urls(data: AddItemsFromURLsRequest):
    """
    reference: https://api.eagle.cool/item/add-from-urls
    """
    payload = data.model_dump(exclude_none=True)
    payload["items"] = [item.model_dump(exclude_none=True) for item in data.items]
    return await eagle_api_post("/api/item/addFromURLs", payload)


@router.post(
    "/api/item/addFromPath",
    operation_id="add_item_from_path",
    description=(
        "Add a local file to Eagle App. If you intend to add multiple items in a row, we suggest you use `add_items_from_paths`."
    ),
)
async def add_item_from_path(data: AddItemFromPathRequest):
    """
    reference: https://api.eagle.cool/item/add-from-path
    """
    payload = data.model_dump(exclude_none=True)
    return await eagle_api_post("/api/item/addFromPath", payload)


@router.post(
    "/api/item/addFromPaths",
    operation_id="add_items_from_paths",
    description=("Add multiple local files to Eagle App."),
    tags=["Disabled"],
)
async def add_items_from_paths(data: AddItemsFromPathsRequest):
    """
    reference: https://api.eagle.cool/item/add-from-paths
    """
    payload = data.model_dump(exclude_none=True)
    payload["items"] = [item.model_dump(exclude_none=True) for item in data.items]
    return await eagle_api_post("/api/item/addFromPaths", payload)


@router.post(
    "/api/item/addBookmark",
    operation_id="add_bookmark",
    description=("Save the link in the URL form to Eagle App."),
    tags=["Disabled"],
)
async def add_bookmark(data: AddBookmarkRequest):
    """
    reference: https://api.eagle.cool/item/add-bookmark
    """
    payload = data.model_dump(exclude_none=True)
    return await eagle_api_post("/api/item/addBookmark", payload)


@router.post(
    "/api/item/info",
    operation_id="get_item_info",
    description=(
        "Get Properties of the specified file, including the file name, tags, categorizations, folders, dimensions, etc."
    ),
)
async def get_item_info(data: GetItemInfoRequest):
    """
    reference: https://api.eagle.cool/item/info
    """
    payload = data.model_dump(exclude_none=True)
    return await eagle_api_get("/api/item/info", payload)


@router.post(
    "/api/item/thumbnail",
    operation_id="get_item_thumbnail",
    description=(
        "Get the path of the thumbnail of the file specified. If you would like to get a batch of thumbnail paths, the combination of Library path + Object IDis recommended."
    ),
    tags=["Disabled"],
)
async def get_item_thumbnail(data: GetItemThumbnailRequest):
    """
    reference: https://api.eagle.cool/item/thumbnail
    """
    payload = data.model_dump(exclude_none=True)
    return await eagle_api_get("/api/item/thumbnail", payload)


@router.post(
    "/api/item/list",
    operation_id="get_item_list",
    description=("Get items that match the filter condition."),
)
async def get_item_list(data: GetItemListRequest):
    """
    reference: https://api.eagle.cool/item/list
    """
    payload = data.model_dump(exclude_none=True)
    return await eagle_api_get("/api/item/list", payload)


@router.post(
    "/api/item/moveToTrash",
    operation_id="move_item_to_trash",
    description=("Move items to trash."),
)
async def move_item_to_trash(data: MoveItemToTrashRequest):
    """
    reference: https://api.eagle.cool/item/api-item-movetotrash
    """
    payload = data.model_dump(exclude_none=True)
    return await eagle_api_post("/api/item/moveToTrash", payload)


@router.post(
    "/api/item/refreshPalette",
    operation_id="refresh_item_palette",
    description=(
        "Re-analysis the color of the file. When changes to the original file were made, you can call this function to refresh the Color Analysis."
    ),
    tags=["Disabled"],
)
async def refresh_item_palette(data: RefreshItemPaletteRequest):
    """
    reference: https://api.eagle.cool/item/refresh-palette
    """
    payload = data.model_dump(exclude_none=True)
    return await eagle_api_post("/api/item/refreshPalette", payload)


@router.post(
    "/api/item/refreshThumbnail",
    operation_id="refresh_item_thumbnail",
    description=(
        "Re-generate the thumbnail of the file used to display in the List.  When changes to the original file were made, you can call this function to re-generate the thumbnail, the color analysis will also be made."
    ),
    tags=["Disabled"],
)
async def refresh_item_thumbnail(data: RefreshItemThumbnailRequest):
    """
    reference: https://api.eagle.cool/item/refresh-thumbnail
    """
    payload = data.model_dump(exclude_none=True)
    return await eagle_api_post("/api/item/refreshThumbnail", payload)


@router.post(
    "/api/item/update",
    operation_id="update_item",
    description=("Modify data of specified fields of the item."),
)
async def update_item(data: UpdateItemRequest):
    """
    reference: https://api.eagle.cool/item/update
    """
    payload = data.model_dump(exclude_none=True)
    return await eagle_api_post("/api/item/update", payload)


@router.post(
    "/api/item/source",
    operation_id="get_item_source",
    response_model=GetItemSourceResponse,
    description=("Get the source path of the file specified."),
)
async def get_item_source(
    data: GetItemSourceRequest,
) -> GetItemSourceResponse:
    payload = data.model_dump(exclude_none=True)

    # `/api/item/info` APIのレスポンスに ファイルパス が含まれるように機能リクエスト済: 2025/04/29
    library = await eagle_api_get("/api/library/info")
    if library.get("status") != "success":
        return ErrorResponse(message="Failed to fetch eagle info")

    item = await eagle_api_get("/api/item/info", payload)
    if item.get("status") != "success":
        return ErrorResponse(message="Failed to fetch item info")

    source_path = construct_source_path(library, item)
    if source_path is None:
        return ErrorResponse(message="Failed to fetch source path")

    return GetItemSourceSuccessResponse(data={"source": source_path})


def construct_source_path(library: dict, item: dict) -> str | None:
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
