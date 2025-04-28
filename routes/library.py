from fastapi import APIRouter
from utils.eagle_api import fetch_from_eagle_api

router = APIRouter(tags=["Library"])


@router.get(
    "/api/library/info",
    operation_id="get_library_info",
    description=(
        "Get detailed information of the library currently running. The function can be used to obtain details such as `All Folders`, `All Smart Folders`, `All Tag Groups`, `Quick Access` and etc.\n\n"
        "More details: [https://api.eagle.cool/library/info](https://api.eagle.cool/library/info)"
    ),
)
async def get_library_info():
    return await fetch_from_eagle_api("/api/library/info")
