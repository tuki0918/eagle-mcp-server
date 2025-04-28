from pydantic import BaseModel, Field
from typing import Annotated, Literal


class ConnectResponse(BaseModel):
    status: Annotated[Literal["success", "error"], Field(...)]
    message: Annotated[str, Field(...)]
