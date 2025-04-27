from fastapi import APIRouter
from schemas import CreateFolderRequest, RenameFolderRequest, UpdateFolderRequest
from utils.eagle_api import fetch_from_eagle_api, post_to_eagle_api

router = APIRouter(tags=["Folder"])


@router.post(
    "/api/folder/create",
    operation_id="create_folder",
    description=(
        "Create a folder. The created folder will be put at the bottom of the folder list of the current library.\n\n"
        "External API: [https://api.eagle.cool/folder/create](https://api.eagle.cool/folder/create)"
    ),
)
async def create_folder(data: CreateFolderRequest):
    payload = {"folderName": data.folderName}
    if data.parent is not None:
        payload["parent"] = data.parent
    return await post_to_eagle_api("/api/folder/create", payload)


@router.post(
    "/api/folder/rename",
    operation_id="rename_folder",
    description=(
        "Rename the specified folder.\n\n"
        "External API: [https://api.eagle.cool/folder/rename](https://api.eagle.cool/folder/rename)"
    ),
)
async def rename_folder(data: RenameFolderRequest):
    payload = {"folderId": data.folderId, "newName": data.newName}
    return await post_to_eagle_api("/api/folder/rename", payload)


@router.post(
    "/api/folder/update",
    operation_id="update_folder",
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


@router.get(
    "/api/folder/list",
    operation_id="get_folder_list",
    description=(
        "Get the list of folders of the current library.\n\n"
        "External API: [https://api.eagle.cool/folder/list](https://api.eagle.cool/folder/list)"
    ),
)
async def get_folder_list():
    return await fetch_from_eagle_api("/api/folder/list")


@router.get(
    "/api/folder/listRecent",
    operation_id="get_folder_list_recent",
    description=(
        "Get the list of folders recently used by the user.\n\n"
        "External API: [https://api.eagle.cool/folder/list-recent](https://api.eagle.cool/folder/list-recent)"
    ),
)
async def get_folder_list_recent():
    return await fetch_from_eagle_api("/api/folder/listRecent")
