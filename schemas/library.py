from pydantic import BaseModel, Field
from typing import Annotated


class SwitchLibraryRequest(BaseModel):
    libraryPath: Annotated[str, Field(..., description="The path of the library")]


class GetLibraryIconRequest(BaseModel):
    libraryPath: Annotated[str, Field(..., description="The path of the library")]
