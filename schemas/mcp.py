from pydantic import BaseModel


class ConnectResponse(BaseModel):
    message: str
