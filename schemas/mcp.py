from pydantic import BaseModel, Field
from typing import Annotated


class ConnectResponse(BaseModel):
    message: Annotated[str, Field(...)]
