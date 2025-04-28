from pydantic import BaseModel, Field
from typing import Annotated, Literal, Union


class SuccessResponse(BaseModel):
    status: Literal["success"] = "success"


class ErrorResponse(BaseModel):
    status: Literal["error"] = "error"
    message: Annotated[
        str,
        Field(...),
    ]


ApiResponse = Union[SuccessResponse, ErrorResponse]
