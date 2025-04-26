from fastapi import FastAPI
from fastapi_mcp import FastApiMCP
import httpx

app = FastAPI(
    title="Eagle MCP API",
)

# Define the base URL for the Eagle API
EAGLE_API_BASE_URL = "http://localhost:41595"


@app.get("/api/connect", operation_id="connect", tags=["MCP"])
async def connect():
    return {"message": "Connected!"}


async def fetch_from_eagle_api(endpoint: str):
    url = f"{EAGLE_API_BASE_URL}{endpoint}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
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
    description="Get detailed information on the Eagle App currently running. In most cases, this could be used to determine whether certain functions are available on the user's device.",
)
async def get_application_info():
    return await fetch_from_eagle_api("/api/application/info")


# Folder


@app.post(
    "/api/folder/create",
    operation_id="create_folder",
    tags=["Folder"],
    description="Create a folder. The created folder will be put at the bottom of the folder list of the current library.",
)
async def create_folder(folderName: str, parentId: str = None):
    payload = {"folderName": folderName, "parent": parentId}
    return await post_to_eagle_api("/api/folder/create", payload)


@app.post(
    "/api/folder/rename",
    operation_id="rename_folder",
    tags=["Folder"],
    description="Rename the specified folder.",
)
async def rename_folder(id: str, name: str):
    payload = {"folderId": id, "newName": name}
    return await post_to_eagle_api("/api/folder/rename", payload)


@app.get("/api/folder/list", operation_id="get_folder_list", tags=["Folder"])
async def get_folder_list():
    return await fetch_from_eagle_api("/api/folder/list")


@app.get(
    "/api/folder/listRecent", operation_id="get_folder_list_recent", tags=["Folder"]
)
async def get_folder_list_recent():
    return await fetch_from_eagle_api("/api/folder/listRecent")


@app.post("/api/folder/update", operation_id="update_folder", tags=["Folder"])
async def update_folder(
    id: str, name: str = None, description: str = None, parentId: str = None
):
    payload = {"id": id}
    if name is not None:
        payload["name"] = name
    if description is not None:
        payload["description"] = description
    if parentId is not None:
        payload["parentId"] = parentId
    return await post_to_eagle_api("/api/folder/update", payload)


@app.post("/api/item/addFromURLs", operation_id="add_items_from_urls", tags=["Item"])
async def add_items_from_urls(
    urls: list[str], folderId: str = None, tags: list[str] = None
):
    payload = {"urls": urls}
    if folderId is not None:
        payload["folderId"] = folderId
    if tags is not None:
        payload["tags"] = tags
    return await post_to_eagle_api("/api/item/addFromURLs", payload)


@app.post("/api/item/addFromPath", operation_id="add_item_from_path", tags=["Item"])
async def add_item_from_path(path: str, folderId: str = None, tags: list[str] = None):
    payload = {"path": path}
    if folderId is not None:
        payload["folderId"] = folderId
    if tags is not None:
        payload["tags"] = tags
    return await post_to_eagle_api("/api/item/addFromPath", payload)


@app.post("/api/item/addFromURL", operation_id="add_item_from_url", tags=["Item"])
async def add_item_from_url(url: str, folderId: str = None, tags: list[str] = None):
    payload = {"url": url}
    if folderId is not None:
        payload["folderId"] = folderId
    if tags is not None:
        payload["tags"] = tags
    return await post_to_eagle_api("/api/item/addFromURL", payload)


mcp = FastApiMCP(
    app,
    name="Eagle MCP",
    description="An MCP server for Eagle",
)

mcp.mount()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
