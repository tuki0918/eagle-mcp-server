from fastapi import APIRouter
from utils.eagle_api import eagle_api_get

router = APIRouter(tags=["Application"])


@router.get(
    "/api/application/info",
    operation_id="get_application_info",
    description=(
        "Get detailed information on the Eagle App currently running. In most cases, this could be used to determine whether certain functions are available on the user's device."
    ),
)
async def get_application_info():
    """
    reference: https://api.eagle.cool/application/info
    """
    return await eagle_api_get("/api/application/info")
