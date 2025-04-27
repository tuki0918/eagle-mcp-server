from typing import Annotated
from fastapi import FastAPI, Query
from fastapi_mcp import FastApiMCP
from schemas import ConnectResponse
import httpx
import os

# Define the base URL for the Eagle API
EAGLE_API_BASE_URL = os.environ.get("EAGLE_API_BASE_URL", "http://localhost:41595")

app = FastAPI(
    title="Eagle MCP API",
)


@app.get(
    "/api/connect", operation_id="connect", tags=["MCP"], response_model=ConnectResponse
)
async def connect() -> ConnectResponse:
    return ConnectResponse(message="Connected!")


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
async def create_folder(
    folderName: Annotated[str, Query(description="The name of the Folder")],
    parent: Annotated[str, Query(description="ID of the parent folder")],
):
    payload = {"folderName": folderName, "parent": parent}
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
async def rename_folder(
    folderId: Annotated[str, Query(description="The folder's ID")],
    newName: Annotated[str, Query(description="The new name of the folder")],
):
    payload = {"folderId": folderId, "newName": newName}
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
async def update_folder(
    folderId: Annotated[str, Query(description="The folder's ID")],
    newName: Annotated[
        str | None, Query(description="The new name of the folder")
    ] = None,
    newDescription: Annotated[
        str | None,
        Query(description="The new description of the folder"),
    ] = None,
    newColor: Annotated[
        str | None,
        Query(
            description='"red","orange","green","yellow","aqua","blue","purple","pink"'
        ),
    ] = None,
):
    payload = {"folderId": folderId}
    if newName is not None:
        payload["newName"] = newName
    if newDescription is not None:
        payload["newDescription"] = newDescription
    if newColor is not None:
        payload["newColor"] = newColor.value
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
# ...


mcp = FastApiMCP(
    app,
    name="Eagle MCP Server",
    description="An MCP server for Eagle",
)

mcp.mount()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
