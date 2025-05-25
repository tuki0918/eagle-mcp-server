from fastmcp import Resource, Tool
from schemas.library import SwitchLibraryRequest, GetLibraryIconRequest
from utils.eagle_api import eagle_api_get, eagle_api_post

class LibraryResource(Resource):
    name = "library"
    description = "Eagle library operations"

    @Tool()
    async def get_library_info(self):
        """Get detailed information of the library currently running."""
        return await eagle_api_get("/api/library/info")

    @Tool()
    async def get_library_history(self):
        """Get the history of the library."""
        return await eagle_api_get("/api/library/history")

    @Tool()
    async def switch_library(self, data: SwitchLibraryRequest):
        """Switch the current library to a different one."""
        payload = data.model_dump(exclude_none=True)
        return await eagle_api_post("/api/library/switch", payload)

    @Tool()
    async def get_library_icon(self, data: GetLibraryIconRequest):
        """Get the icon of the library."""
        payload = data.model_dump(exclude_none=True)
        result = await eagle_api_get("/api/library/icon", payload, is_binary=True)
        if isinstance(result, dict) and result.get("status") == "error":
            return result
        content, content_type = result
        # fastmcpではバイナリ返却は要検討。ここではパススルーで返す例。
        return {"content": content, "content_type": content_type}
