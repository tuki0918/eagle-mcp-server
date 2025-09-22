from typing import Optional, Annotated
from pydantic import Field
from fastmcp import FastMCP
from utils.eagle_api import eagle_api_get, eagle_api_post


def register_folder_tools(mcp: FastMCP):
    """Register folder-related tools to the MCP server."""

    @mcp.tool(
        tags={"Folder"},
        meta={"reference": "https://api.eagle.cool/folder/create"},
    )
    async def create_folder(
        folder_name: Annotated[str, Field(description="Name of the folder")],
        parent: Annotated[
            Optional[str], Field(description="ID of the parent folder")
        ] = None,
    ):
        """
        Create a folder. The created folder will be put at the bottom of the folder list of the current library.

        Args:
            folder_name: Name of the folder
            parent: ID of the parent folder (optional)

        Returns:
            dict: Result of folder creation operation
        """
        payload = {"folderName": folder_name}
        if parent is not None:
            payload["parent"] = parent
        return await eagle_api_post("/api/folder/create", payload)

    @mcp.tool(
        tags={"Folder"},
        meta={"reference": "https://api.eagle.cool/folder/rename"},
        enabled=False,
    )
    async def rename_folder(
        folder_id: Annotated[str, Field(description="The folder's ID")],
        new_name: Annotated[str, Field(description="The new name of the folder")],
    ):
        """
        Rename the specified folder.

        Args:
            folder_id: The folder's ID
            new_name: The new name of the folder

        Returns:
            dict: Result of folder rename operation
        """
        payload = {"folderId": folder_id, "newName": new_name}
        return await eagle_api_post("/api/folder/rename", payload)

    @mcp.tool(
        tags={"Folder"},
        meta={"reference": "https://api.eagle.cool/folder/update"},
    )
    async def update_folder(
        folder_id: Annotated[str, Field(description="The folder's ID")],
        new_name: Annotated[
            Optional[str], Field(description="The new name of the folder")
        ] = None,
        new_description: Annotated[
            Optional[str], Field(description="The new description of the folder")
        ] = None,
        new_color: Annotated[
            Optional[str],
            Field(
                description="The new color: red,orange,green,yellow,aqua,blue,purple,pink"
            ),
        ] = None,
    ):
        """
        Update the specified folder properties including name, description, and color.

        Args:
            folder_id: The folder's ID
            new_name: The new name of the folder (optional)
            new_description: The new description of the folder (optional)
            new_color: The new color of the folder: "red","orange","green","yellow","aqua","blue","purple","pink" (optional)

        Returns:
            dict: Result of folder update operation
        """
        payload = {"folderId": folder_id}
        if new_name is not None:
            payload["newName"] = new_name
        if new_description is not None:
            payload["newDescription"] = new_description
        if new_color is not None:
            payload["newColor"] = new_color
        return await eagle_api_post("/api/folder/update", payload)

    @mcp.tool(
        tags={"Folder"},
        meta={"reference": "https://api.eagle.cool/folder/list"},
    )
    async def get_folder_list():
        """
        Get the list of folders of the current library.

        Returns:
            dict: List of folders in the current library
        """
        return await eagle_api_get("/api/folder/list")

    @mcp.tool(
        tags={"Folder"},
        meta={"reference": "https://api.eagle.cool/folder/list-recent"},
        enabled=False,
    )
    async def get_folder_list_recent():
        """
        Get the list of folders recently used by the user.

        Returns:
            dict: List of recently used folders
        """
        return await eagle_api_get("/api/folder/listRecent")
