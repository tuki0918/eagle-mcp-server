"""
Folder tools for Eagle MCP Server
"""
from fastmcp import tool
from pydantic import BaseModel, Field
from typing import Annotated, Optional
from enum import Enum
from utils.eagle_api import eagle_api_get, eagle_api_post


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


@tool
async def create_folder(data: CreateFolderRequest):
    """
    Create a folder. The created folder will be put at the bottom of the folder list of the current library.
    
    Args:
        data: Folder creation parameters including name and optional parent folder ID
        
    Returns:
        dict: Result of folder creation operation
    """
    payload = data.model_dump(exclude_none=True)
    return await eagle_api_post("/api/folder/create", payload)


@tool  
async def rename_folder(data: RenameFolderRequest):
    """
    Rename the specified folder.
    
    Args:
        data: Folder rename parameters including folder ID and new name
        
    Returns:
        dict: Result of folder rename operation
    """
    payload = data.model_dump(exclude_none=True)
    return await eagle_api_post("/api/folder/rename", payload)


@tool
async def update_folder(data: UpdateFolderRequest):
    """
    Update the specified folder properties including name, description, and color.
    
    Args:
        data: Folder update parameters
        
    Returns:
        dict: Result of folder update operation
    """
    payload = data.model_dump(exclude_none=True)
    return await eagle_api_post("/api/folder/update", payload)


@tool
async def get_folder_list():
    """
    Get the list of folders of the current library.
    
    Returns:
        dict: List of folders in the current library
    """
    return await eagle_api_get("/api/folder/list")


@tool
async def get_folder_list_recent():
    """
    Get the list of folders recently used by the user.
    
    Returns:
        dict: List of recently used folders
    """
    return await eagle_api_get("/api/folder/listRecent")


# List of all folder tools  
folder_tools = [
    create_folder,
    rename_folder,
    update_folder,
    get_folder_list,
    get_folder_list_recent,
]