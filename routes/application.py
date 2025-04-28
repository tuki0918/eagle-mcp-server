from fastapi import APIRouter
from utils.eagle_api import fetch_from_eagle_api

router = APIRouter(tags=["Application"])


@router.get(
    "/api/application/info",
    operation_id="get_application_info",
    description=(
        "Get detailed information on the Eagle App currently running. In most cases, this could be used to determine whether certain functions are available on the user's device.\n\n"
        "More details: [https://api.eagle.cool/application/info](https://api.eagle.cool/application/info)"
    ),
)
async def get_application_info():
    return await fetch_from_eagle_api("/api/application/info")
