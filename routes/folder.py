from fastapi import APIRouter
from schemas.folder import CreateFolderRequest, RenameFolderRequest, UpdateFolderRequest
from utils.eagle_api import eagle_api_get, eagle_api_post

router = APIRouter(tags=["Folder"])


@router.post(
    "/api/folder/create",
    operation_id="create_folder",
    description=(
        "Create a folder. The created folder will be put at the bottom of the folder list of the current library."
    ),
)
async def create_folder(data: CreateFolderRequest):
    """
    reference: https://api.eagle.cool/folder/create
    """
    payload = data.model_dump(exclude_none=True)
    return await eagle_api_post("/api/folder/create", payload)


@router.post(
    "/api/folder/rename",
    operation_id="rename_folder",
    description=("Rename the specified folder."),
)
async def rename_folder(data: RenameFolderRequest):
    """
    reference: https://api.eagle.cool/folder/rename
    """
    payload = data.model_dump(exclude_none=True)
    return await eagle_api_post("/api/folder/rename", payload)


@router.post(
    "/api/folder/update",
    operation_id="update_folder",
    description=("Update the specified folder."),
)
async def update_folder(data: UpdateFolderRequest):
    """
    reference: https://api.eagle.cool/folder/update
    """
    payload = data.model_dump(exclude_none=True)
    return await eagle_api_post("/api/folder/update", payload)


@router.get(
    "/api/folder/list",
    operation_id="get_folder_list",
    description=("Get the list of folders of the current library."),
)
async def get_folder_list():
    """
    reference: https://api.eagle.cool/folder/list
    """
    return await eagle_api_get("/api/folder/list")


@router.get(
    "/api/folder/listRecent",
    operation_id="get_folder_list_recent",
    description=("Get the list of folders recently used by the user."),
)
async def get_folder_list_recent():
    """
    reference: https://api.eagle.cool/folder/list-recent
    """
    return await eagle_api_get("/api/folder/listRecent")
