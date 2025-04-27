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


@app.post(
    "/api/item/addFromURL",
    operation_id="add_item_from_url",
    tags=["Item"],
    description=(
        "Add an image from an address to Eagle App. If you intend to add multiple items in a row, we suggest you use `add_items_from_urls`.\n\n"
        "External API: [https://api.eagle.cool/item/add-from-url](https://api.eagle.cool/item/add-from-url)"
    ),
)
async def add_item_from_url(
    url: Annotated[
        str,
        Query(
            description="Required, the URL of the image to be added. Supports http, https, base64"
        ),
    ],
    name: Annotated[
        str, Query(description="Required, the name of the image to be added.")
    ],
    website: Annotated[
        str | None, Query(description="The Address of the source of the image")
    ] = None,
    tags: Annotated[list[str] | None, Query(description="Tags for the image.")] = None,
    star: Annotated[
        int | None, Query(description="The rating for the image.", ge=0, le=5)
    ] = None,
    annotation: Annotated[
        str | None, Query(description="The annotation for the image.")
    ] = None,
    modificationTime: Annotated[
        int | None,
        Query(
            description="The creation date (ms) of the image. The parameter can be used to alter the image's sorting order in Eagle."
        ),
    ] = None,
    folderId: Annotated[
        str | None,
        Query(
            description="If this parameter is defined, the image will be added to the corresponding folder."
        ),
    ] = None,
    # TODO: fastapi err
    # headers: Annotated[
    #     dict[str, str] | None,
    #     Query(
    #         description="Optional, customize the HTTP headers properties, this could be used to circumvent the security of certain websites."
    #     ),
    # ] = None,
):
    payload = {
        "url": url,
        "name": name,
    }
    if website is not None:
        payload["website"] = website
    if tags is not None:
        payload["tags"] = tags
    if star is not None:
        payload["star"] = star
    if annotation is not None:
        payload["annotation"] = annotation
    if modificationTime is not None:
        payload["modificationTime"] = modificationTime
    if folderId is not None:
        payload["folderId"] = folderId
    # if headers is not None:
    #     payload["headers"] = headers
    return await post_to_eagle_api("/api/item/addFromURL", payload)


@app.get(
    "/api/item/list",
    operation_id="get_item_list",
    tags=["Item"],
    description=(
        "Get items that match the filter condition.\n\n"
        "External API: [https://api.eagle.cool/item/list](https://api.eagle.cool/item/list)"
    ),
)
async def get_item_list(
    limit: Annotated[
        int | None,
        Query(
            description="The number of items to be displayed. the default number is `200`",
            ge=1,
        ),
    ] = 200,
    offset: Annotated[
        int | None,
        Query(
            description="Offset a collection of results from the api. Start with `0`",
            ge=0,
        ),
    ] = 0,
    orderBy: Annotated[
        str | None,
        Query(
            description="The sorting order. `CREATEDATE`, `FILESIZE`, `NAME`, `RESOLUTION`, add a minus sign for descending order: `-FILESIZE`"
        ),
    ] = None,
    keyword: Annotated[str | None, Query(description="Filter by the keyword")] = None,
    ext: Annotated[
        str | None,
        Query(description="Filter by the extension type, e.g.: `jpg`, `png`"),
    ] = None,
    tags: Annotated[
        str | None,
        Query(
            description="Filter by tags. Use `,` to divide different tags. E.g.: `Design`, `Poster`"
        ),
    ] = None,
    folders: Annotated[
        str | None,
        Query(
            description="Filter by Folders. Use `,` to divide folder IDs. E.g.: `KAY6NTU6UYI5Q,KBJ8Z60O88VMG`"
        ),
    ] = None,
):
    params = {
        "limit": limit,
        "offset": offset,
    }
    if orderBy is not None:
        params["orderBy"] = orderBy
    if keyword is not None:
        params["keyword"] = keyword
    if ext is not None:
        params["ext"] = ext
    if tags is not None:
        params["tags"] = tags
    if folders is not None:
        params["folders"] = folders
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
