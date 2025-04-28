from fastapi import APIRouter
from schemas import (
    ErrorResponse,
    AddItemFromURLRequest,
    AddItemsFromURLsRequest,
    AddItemFromPathRequest,
    AddItemsFromPathsRequest,
    GetItemInfoRequest,
    GetItemThumbnailRequest,
    GetItemListRequest,
    GetItemSourcePathRequest,
    UpdateItemRequest,
    GetItemSourcePathResponse,
    GetItemSourcePathSuccessResponse,
)
from utils.eagle_api import eagle_api_get, eagle_api_post

router = APIRouter(tags=["Item"])


@router.post(
    "/api/item/addFromURL",
    operation_id="add_item_from_url",
    description=(
        "Add an image from an address to Eagle App. If you intend to add multiple items in a row, we suggest you use `add_items_from_urls`.\n\n"
        "More details: [https://api.eagle.cool/item/add-from-url](https://api.eagle.cool/item/add-from-url)"
    ),
)
async def add_item_from_url(data: AddItemFromURLRequest):
    payload = data.model_dump(exclude_none=True)
    return await eagle_api_post("/api/item/addFromURL", payload)


@router.post(
    "/api/item/addFromURLs",
    operation_id="add_items_from_urls",
    description=(
        "Add multiple images from URLs to Eagle App.\n\n"
        "More details: [https://api.eagle.cool/item/add-from-urls](https://api.eagle.cool/item/add-from-urls)"
    ),
)
async def add_items_from_urls(data: AddItemsFromURLsRequest):
    payload = data.model_dump(exclude_none=True)
    payload["items"] = [item.model_dump(exclude_none=True) for item in data.items]
    return await eagle_api_post("/api/item/addFromURLs", payload)


@router.post(
    "/api/item/addFromPath",
    operation_id="add_item_from_path",
    description=(
        "Add a local file to Eagle App. If you intend to add multiple items in a row, we suggest you use `add_items_from_paths`.\n\n"
        "More details: [https://api.eagle.cool/item/add-from-path](https://api.eagle.cool/item/add-from-path)"
    ),
)
async def add_item_from_path(data: AddItemFromPathRequest):
    payload = data.model_dump(exclude_none=True)
    return await eagle_api_post("/api/item/addFromPath", payload)


@router.post(
    "/api/item/addFromPaths",
    operation_id="add_items_from_paths",
    description=(
        "Add multiple local files to Eagle App.\n\n"
        "More details: [https://api.eagle.cool/item/add-from-paths](https://api.eagle.cool/item/add-from-paths)"
    ),
)
async def add_items_from_paths(data: AddItemsFromPathsRequest):
    payload = data.model_dump(exclude_none=True)
    payload["items"] = [item.model_dump(exclude_none=True) for item in data.items]
    return await eagle_api_post("/api/item/addFromPaths", payload)


@router.post(
    "/api/item/info",
    operation_id="get_item_info",
    description=(
        "Get Properties of the specified file, including the file name, tags, categorizations, folders, dimensions, etc.\n\n"
        "More details: [https://api.eagle.cool/item/info](https://api.eagle.cool/item/info)"
    ),
)
async def get_item_info(data: GetItemInfoRequest):
    payload = data.model_dump(exclude_none=True)
    return await eagle_api_get("/api/item/info", payload)


@router.post(
    "/api/item/thumbnail",
    operation_id="get_item_thumbnail",
    description=(
        "Get the path of the thumbnail of the file specified. If you would like to get a batch of thumbnail paths, the combination of Library path + Object IDis recommended.\n\n"
        "More details: [https://api.eagle.cool/item/thumbnail](https://api.eagle.cool/item/thumbnail)"
    ),
)
async def get_item_thumbnail(data: GetItemThumbnailRequest):
    payload = data.model_dump(exclude_none=True)
    return await eagle_api_get("/api/item/thumbnail", payload)


@router.post(
    "/api/item/list",
    operation_id="get_item_list",
    description=(
        "Get items that match the filter condition.\n\n"
        "More details: [https://api.eagle.cool/item/list](https://api.eagle.cool/item/list)"
    ),
)
async def get_item_list(data: GetItemListRequest):
    payload = data.model_dump(exclude_none=True)
    return await eagle_api_get("/api/item/list", payload)


@router.post(
    "/api/item/update",
    operation_id="update_item",
    description=(
        "Modify data of specified fields of the item.\n\n"
        "More details: [https://api.eagle.cool/item/update](https://api.eagle.cool/item/update)"
    ),
)
async def update_item(data: UpdateItemRequest):
    payload = data.model_dump(exclude_none=True)
    return await eagle_api_post("/api/item/update", payload)


@router.post(
    "/api/item/source",
    operation_id="get_item_source_path",
    response_model=GetItemSourcePathResponse,
    description=("Get the source path of the file specified."),
)
async def get_item_source_path(
    data: GetItemSourcePathRequest,
) -> GetItemSourcePathResponse:
    payload = data.model_dump(exclude_none=True)

    library = await eagle_api_get("/api/library/info")
    if library.get("status") != "success":
        return ErrorResponse(message="Failed to fetch eagle info")

    item = await eagle_api_get("/api/item/info", payload)
    if item.get("status") != "success":
        return ErrorResponse(message="Failed to fetch item info")

    source_path = construct_source_path(library, item)
    if source_path is None:
        return ErrorResponse(message="Failed to fetch source path")

    return GetItemSourcePathSuccessResponse(data={"source": source_path})


def construct_source_path(library: dict, item: dict) -> str | None:
    try:
        library_path = library["data"]["library"]["path"]
        item_id = item["data"]["id"]
        item_name = item["data"]["name"]
        item_ext = item["data"]["ext"]

        return f"{library_path}/images/{item_id}.info/{item_name}.{item_ext}"
    except KeyError:
        return None
