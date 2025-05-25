from fastmcp import Resource, Tool
from schemas.folder import CreateFolderRequest, RenameFolderRequest, UpdateFolderRequest
from utils.eagle_api import eagle_api_get, eagle_api_post

class FolderResource(Resource):
    name = "folder"
    description = "Eagle folder operations"

    @Tool()
    async def create_folder(self, data: CreateFolderRequest):
        """Create a folder. The created folder will be put at the bottom of the folder list of the current library."""
        payload = data.model_dump(exclude_none=True)
        return await eagle_api_post("/api/folder/create", payload)

    @Tool()
    async def rename_folder(self, data: RenameFolderRequest):
        """Rename a folder."""
        payload = data.model_dump(exclude_none=True)
        return await eagle_api_post("/api/folder/rename", payload)

    @Tool()
    async def update_folder(self, data: UpdateFolderRequest):
        """Update folder attributes."""
        payload = data.model_dump(exclude_none=True)
        return await eagle_api_post("/api/folder/update", payload)

    @Tool()
    async def get_folder_list(self):
        """Get the list of folders in the current library."""
        return await eagle_api_get("/api/folder/list")

    @Tool()
    async def get_folder_list_recent(self):
        """Get the list of recently used folders."""
        return await eagle_api_get("/api/folder/listRecent")

    # 他のAPIも順次移植予定
