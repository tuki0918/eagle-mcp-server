from pydantic import Field
from typing import Annotated, Union
from schemas.api import SuccessResponse, ErrorResponse


class ConnectSuccessResponse(SuccessResponse):
    message: Annotated[str, Field(...)]


ConnectResponse = Union[ConnectSuccessResponse, ErrorResponse]
