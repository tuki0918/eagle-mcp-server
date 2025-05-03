from fastapi import APIRouter
from schemas.library import SwitchLibraryRequest
from utils.eagle_api import eagle_api_get, eagle_api_post

router = APIRouter(tags=["Library"])


@router.get(
    "/api/library/info",
    operation_id="get_library_info",
    description=(
        "Get detailed information of the library currently running. The function can be used to obtain details such as `All Folders`, `All Smart Folders`, `All Tag Groups`, `Quick Access` and etc."
    ),
)
async def get_library_info():
    """
    reference: https://api.eagle.cool/library/info
    """
    return await eagle_api_get("/api/library/info")


@router.get(
    "/api/library/history",
    operation_id="get_library_history",
    description=("Get the list of libraries recently opened by the Application."),
)
async def get_library_history():
    """
    reference: https://api.eagle.cool/library/history
    """
    return await eagle_api_get("/api/library/history")


@router.post(
    "/api/library/switch",
    operation_id="switch_library",
    description=("Switch the library currently opened by Eagle."),
)
async def switch_library(data: SwitchLibraryRequest):
    """
    reference: https://api.eagle.cool/library/switch
    """
    payload = data.model_dump(exclude_none=True)
    return await eagle_api_post("/api/library/switch", payload)
