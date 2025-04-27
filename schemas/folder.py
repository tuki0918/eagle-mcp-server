from pydantic import BaseModel, Field
from typing import Annotated, Optional
from enum import Enum


class FolderColor(str, Enum):
    RED = "red"
    ORANGE = "orange"
    GREEN = "green"
    YELLOW = "yellow"
    AQUA = "aqua"
    BLUE = "blue"
    PURPLE = "purple"
    PINK = "pink"


class CreateFolderRequest(BaseModel):
    folderName: Annotated[str, Field(..., description="Name of the folder")]
    parent: Annotated[
        Optional[str],
        Field(
            None,
            description="ID of the parent folder",
        ),
    ]


class RenameFolderRequest(BaseModel):
    folderId: Annotated[str, Field(..., description="The folder's ID")]
    newName: Annotated[
        str,
        Field(
            ...,
            description="The new name of the folder",
        ),
    ]


class UpdateFolderRequest(BaseModel):
    folderId: Annotated[str, Field(..., description="The folder's ID")]
    newName: Annotated[
        Optional[str], Field(None, description="The new name of the folder")
    ]
    newDescription: Annotated[
        Optional[str], Field(None, description="The new description of the folder")
    ]
    newColor: Annotated[
        Optional[FolderColor],
        Field(
            None,
            description='"red","orange","green","yellow","aqua","blue","purple","pink"',
        ),
    ]
