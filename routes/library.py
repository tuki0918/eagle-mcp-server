from fastapi import APIRouter
from utils.eagle_api import eagle_api_get

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
