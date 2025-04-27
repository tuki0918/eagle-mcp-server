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
    payload = data.model_dump(exclude_none=True)
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
    payload = data.model_dump(exclude_none=True)
    payload["items"] = [item.model_dump(exclude_none=True) for item in data.items]
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
    params = data.model_dump(exclude_none=True)
    return await fetch_from_eagle_api("/api/item/list", params=params)
