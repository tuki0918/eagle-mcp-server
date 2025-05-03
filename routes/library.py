from fastapi import APIRouter, Response
from schemas.library import SwitchLibraryRequest, GetLibraryIconRequest
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
    tags=["Disabled"],
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
    tags=["Disabled"],
)
async def switch_library(data: SwitchLibraryRequest):
    """
    reference: https://api.eagle.cool/library/switch
    """
    payload = data.model_dump(exclude_none=True)
    return await eagle_api_post("/api/library/switch", payload)


@router.post(
    "/api/library/icon",
    operation_id="get_library_icon",
    description=("Obtain the icon of the specified Library."),
    tags=["Disabled"],
    deprecated=True,
)
async def get_library_icon(data: GetLibraryIconRequest):
    """
    reference: https://api.eagle.cool/library/icon
    """
    payload = data.model_dump(exclude_none=True)
    result = await eagle_api_get("/api/library/icon", payload, is_binary=True)

    if isinstance(result, dict) and result.get("status") == "error":
        return result

    content, content_type = result
    return Response(content=content, media_type=content_type)
