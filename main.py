from typing import Annotated
from fastapi import FastAPI, Query
from fastapi_mcp import FastApiMCP
from schemas import (
    ConnectResponse,
    CreateFolderRequest,
    RenameFolderRequest,
    UpdateFolderRequest,
    AddItemFromURLRequest,
    AddItemsFromURLsRequest,
    GetItemListRequest,
)
import httpx
import os

# Define the base URL for the Eagle API
EAGLE_API_BASE_URL = os.environ.get("EAGLE_API_BASE_URL", "http://localhost:41595")

print(f"EAGLE_API_BASE_URL env: {os.environ.get('EAGLE_API_BASE_URL')}")
print(f"EAGLE_API_BASE_URL: {EAGLE_API_BASE_URL}")

app = FastAPI(
    title="Eagle MCP API",
)


@app.get(
    "/api/connect", operation_id="connect", tags=["MCP"], response_model=ConnectResponse
)
async def connect() -> ConnectResponse:
    return ConnectResponse(message="Connected!")


async def fetch_from_eagle_api(endpoint: str, params: dict = None):
    url = f"{EAGLE_API_BASE_URL}{endpoint}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as exc:
        return {"status": "error", "message": f"An error occurred: {exc}"}
    except httpx.HTTPStatusError as exc:
        return {
            "status": "error",
            "message": f"HTTP error occurred: {exc.response.status_code}",
        }


async def post_to_eagle_api(endpoint: str, payload: dict):
    url = f"{EAGLE_API_BASE_URL}{endpoint}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as exc:
        return {"status": "error", "message": f"An error occurred: {exc}"}
    except httpx.HTTPStatusError as exc:
        return {
            "status": "error",
            "message": f"HTTP error occurred: {exc.response.status_code}",
        }


# Application


@app.get(
    "/api/application/info",
    operation_id="get_application_info",
    tags=["Application"],
    description=(
        "Get detailed information on the Eagle App currently running. In most cases, this could be used to determine whether certain functions are available on the user's device.\n\n"
        "External API: [https://api.eagle.cool/application/info](https://api.eagle.cool/application/info)"
    ),
)
async def get_application_info():
    return await fetch_from_eagle_api("/api/application/info")


# Folder


@app.post(
    "/api/folder/create",
    operation_id="create_folder",
    tags=["Folder"],
    description=(
        "Create a folder. The created folder will be put at the bottom of the folder list of the current library.\n\n"
        "External API: [https://api.eagle.cool/folder/create](https://api.eagle.cool/folder/create)"
    ),
)
async def create_folder(data: CreateFolderRequest):
    payload = {"folderName": data.folderName, "parent": data.parent}
    return await post_to_eagle_api("/api/folder/create", payload)


@app.post(
    "/api/folder/rename",
    operation_id="rename_folder",
    tags=["Folder"],
    description=(
        "Rename the specified folder.\n\n"
        "External API: [https://api.eagle.cool/folder/rename](https://api.eagle.cool/folder/rename)"
    ),
)
async def rename_folder(data: RenameFolderRequest):
    payload = {"folderId": data.folderId, "newName": data.newName}
    return await post_to_eagle_api("/api/folder/rename", payload)


@app.post(
    "/api/folder/update",
    operation_id="update_folder",
    tags=["Folder"],
    description=(
        "Update the specified folder.\n\n"
        "External API: [https://api.eagle.cool/folder/update](https://api.eagle.cool/folder/update)"
    ),
)
async def update_folder(data: UpdateFolderRequest):
    payload = {"folderId": data.folderId}
    if data.newName is not None:
        payload["newName"] = data.newName
    if data.newDescription is not None:
        payload["newDescription"] = data.newDescription
    if data.newColor is not None:
        payload["newColor"] = data.newColor.value
    return await post_to_eagle_api("/api/folder/update", payload)


@app.get(
    "/api/folder/list",
    operation_id="get_folder_list",
    tags=["Folder"],
    description=(
        "Get the list of folders of the current library.\n\n"
        "External API: [https://api.eagle.cool/folder/list](https://api.eagle.cool/folder/list)"
    ),
)
async def get_folder_list():
    return await fetch_from_eagle_api("/api/folder/list")


@app.get(
    "/api/folder/listRecent",
    operation_id="get_folder_list_recent",
    tags=["Folder"],
    description=(
        "Get the list of folders recently used by the user.\n\n"
        "External API: [https://api.eagle.cool/folder/list-recent](https://api.eagle.cool/folder/list-recent)"
    ),
)
async def get_folder_list_recent():
    return await fetch_from_eagle_api("/api/folder/listRecent")


# Item


@app.post(
    "/api/item/addFromURL",
    operation_id="add_item_from_url",
    tags=["Item"],
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


@app.post(
    "/api/item/addFromURLs",
    operation_id="add_items_from_urls",
    tags=["Item"],
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


@app.get(
    "/api/item/list",
    operation_id="get_item_list",
    tags=["Item"],
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


mcp = FastApiMCP(
    app,
    name="Eagle MCP Server",
    description="An MCP server for Eagle",
)

mcp.mount()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
