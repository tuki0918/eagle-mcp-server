from fastapi import APIRouter
from schemas import AddItemFromURLRequest, AddItemsFromURLsRequest, GetItemListRequest
from utils.eagle_api import fetch_from_eagle_api, post_to_eagle_api

router = APIRouter(tags=["Item"])


@router.post(
    "/api/item/addFromURL",
    operation_id="add_item_from_url",
    description=(
        "Add an image from an address to Eagle App. If you intend to add multiple items in a row, we suggest you use `add_items_from_urls`.\n\n"
        "External API: [https://api.eagle.cool/item/add-from-url](https://api.eagle.cool/item/add-from-url)"
    ),
)
async def add_item_from_url(data: AddItemFromURLRequest):
    payload = {
        "url": data.url,
        "name": data.name,
    }
    if data.website is not None:
        payload["website"] = data.website
    if data.tags is not None:
        payload["tags"] = data.tags
    if data.star is not None:
        payload["star"] = data.star
    if data.annotation is not None:
        payload["annotation"] = data.annotation
    if data.modificationTime is not None:
        payload["modificationTime"] = data.modificationTime
    if data.folderId is not None:
        payload["folderId"] = data.folderId
    if data.headers is not None:
        payload["headers"] = data.headers
    return await post_to_eagle_api("/api/item/addFromURL", payload)


@router.post(
    "/api/item/addFromURLs",
    operation_id="add_items_from_urls",
    description=(
        "Add multiple images from URLs to Eagle App.\n\n"
        "External API: [https://api.eagle.cool/item/add-from-urls](https://api.eagle.cool/item/add-from-urls)"
    ),
)
async def add_items_from_urls(data: AddItemsFromURLsRequest):
    items = [item.model_dump() for item in data.items]
    payload = {"items": items}
    if data.folderId is not None:
        payload["folderId"] = data.folderId
    return await post_to_eagle_api("/api/item/addFromURLs", payload)


@router.get(
    "/api/item/list",
    operation_id="get_item_list",
    description=(
        "Get items that match the filter condition.\n\n"
        "External API: [https://api.eagle.cool/item/list](https://api.eagle.cool/item/list)"
    ),
)
async def get_item_list(data: GetItemListRequest):
    params = {
        "limit": data.limit,
        "offset": data.offset,
    }
    if data.orderBy is not None:
        params["orderBy"] = data.orderBy
    if data.keyword is not None:
        params["keyword"] = data.keyword
    if data.ext is not None:
        params["ext"] = data.ext
    if data.tags is not None:
        params["tags"] = data.tags
    if data.folders is not None:
        params["folders"] = data.folders
    return await fetch_from_eagle_api("/api/item/list", params=params)
