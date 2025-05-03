from fastapi import APIRouter
from schemas.mcp import ConnectResponse, ConnectSuccessResponse

router = APIRouter(tags=["MCP"])


@router.get(
    "/api/connect",
    operation_id="connect",
    response_model=ConnectResponse,
    tags=["Disabled"],
)
async def connect() -> ConnectResponse:
    return ConnectSuccessResponse(message="Connected!")
