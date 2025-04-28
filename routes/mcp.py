from fastapi import APIRouter
from schemas import ConnectResponse, ConnectSuccessResponse

router = APIRouter(tags=["MCP"])


@router.get("/api/connect", operation_id="connect", response_model=ConnectResponse)
async def connect() -> ConnectResponse:
    return ConnectSuccessResponse(message="Connected!")
