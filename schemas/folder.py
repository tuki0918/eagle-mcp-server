from pydantic import BaseModel, Field
from typing import Optional
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
    folderName: str = Field(..., description="Name of the folder")
    parent: Optional[str] = Field(
        None,
        description="ID of the parent folder",
    )


class RenameFolderRequest(BaseModel):
    folderId: str = Field(..., description="The folder's ID")
    newName: str = Field(
        ...,
        description="The new name of the folder",
    )


class UpdateFolderRequest(BaseModel):
    folderId: str = Field(..., description="The folder's ID")
    newName: Optional[str] = Field(None, description="The new name of the folder")
    newDescription: Optional[str] = Field(
        None, description="The new description of the folder"
    )
    newColor: Optional[FolderColor] = Field(
        None,
        description='"red","orange","green","yellow","aqua","blue","purple","pink"',
    )
