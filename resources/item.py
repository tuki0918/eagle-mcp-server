from fastmcp import Resource, Tool
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

class ItemResource(Resource):
    name = "item"
    description = "Eagle item operations"

    @Tool()
    async def get_item_info(self, data: GetItemInfoRequest):
        """Get Properties of the specified file, including the file name, tags, categorizations, folders, dimensions, etc."""
        payload = data.model_dump(exclude_none=True)
        return await eagle_api_get("/api/item/info", payload)

    @Tool()
    async def add_item_from_url(self, data: AddItemFromURLRequest):
        payload = data.model_dump(exclude_none=True)
        return await eagle_api_post("/api/item/addFromURL", payload)

    @Tool()
    async def add_items_from_urls(self, data: AddItemsFromURLsRequest):
        payload = data.model_dump(exclude_none=True)
        payload["items"] = [item.model_dump(exclude_none=True) for item in data.items]
        return await eagle_api_post("/api/item/addFromURLs", payload)

    @Tool()
    async def add_item_from_path(self, data: AddItemFromPathRequest):
        payload = data.model_dump(exclude_none=True)
        return await eagle_api_post("/api/item/addFromPath", payload)

    @Tool()
    async def add_items_from_paths(self, data: AddItemsFromPathsRequest):
        payload = data.model_dump(exclude_none=True)
        payload["items"] = [item.model_dump(exclude_none=True) for item in data.items]
        return await eagle_api_post("/api/item/addFromPaths", payload)

    @Tool()
    async def add_bookmark(self, data: AddBookmarkRequest):
        payload = data.model_dump(exclude_none=True)
        return await eagle_api_post("/api/item/addBookmark", payload)

    @Tool()
    async def get_item_thumbnail(self, data: GetItemThumbnailRequest):
        payload = data.model_dump(exclude_none=True)
        return await eagle_api_get("/api/item/thumbnail", payload)

    @Tool()
    async def get_item_list(self, data: GetItemListRequest):
        payload = data.model_dump(exclude_none=True)
        return await eagle_api_get("/api/item/list", payload)

    @Tool()
    async def move_item_to_trash(self, data: MoveItemToTrashRequest):
        payload = data.model_dump(exclude_none=True)
        return await eagle_api_post("/api/item/moveToTrash", payload)

    @Tool()
    async def refresh_item_palette(self, data: RefreshItemPaletteRequest):
        payload = data.model_dump(exclude_none=True)
        return await eagle_api_post("/api/item/refreshPalette", payload)

    @Tool()
    async def refresh_item_thumbnail(self, data: RefreshItemThumbnailRequest):
        payload = data.model_dump(exclude_none=True)
        return await eagle_api_post("/api/item/refreshThumbnail", payload)

    @Tool()
    async def update_item(self, data: UpdateItemRequest):
        payload = data.model_dump(exclude_none=True)
        return await eagle_api_post("/api/item/update", payload)

    @Tool()
    async def get_item_source(self, data: GetItemSourceRequest) -> GetItemSourceResponse:
        payload = data.model_dump(exclude_none=True)
        library = await eagle_api_get("/api/library/info")
        if library.get("status") != "success":
            return {"status": "error", "message": "Failed to fetch eagle info"}
        item = await eagle_api_get("/api/item/info", payload)
        if item.get("status") != "success":
            return {"status": "error", "message": "Failed to fetch item info"}
        source_path = self.construct_source_path(library, item)
        if source_path is None:
            return {"status": "error", "message": "Failed to fetch source path"}
        return GetItemSourceSuccessResponse(data={"source": source_path})

    def construct_source_path(self, library: dict, item: dict) -> str | None:
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

    # ...existing code...
