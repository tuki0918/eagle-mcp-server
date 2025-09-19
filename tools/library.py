"""
Library tools for Eagle MCP Server
"""
from fastmcp import tool
from pydantic import BaseModel, Field
from typing import Annotated
from utils.eagle_api import eagle_api_get, eagle_api_post


class SwitchLibraryRequest(BaseModel):
    libraryPath: Annotated[str, Field(..., description="The path of the library")]


class GetLibraryIconRequest(BaseModel):
    libraryPath: Annotated[str, Field(..., description="The path of the library")]


@tool
async def get_library_info():
    """
    Get detailed information of the library currently running.
    
    The function can be used to obtain details such as `All Folders`, 
    `All Smart Folders`, `All Tag Groups`, `Quick Access` and etc.
    
    Returns:
        dict: Library information including folders, tags, etc.
    """
    return await eagle_api_get("/api/library/info")


@tool
async def get_library_history():
    """
    Get the list of libraries recently opened by the Application.
    
    Returns:
        dict: List of recently opened libraries
    """
    return await eagle_api_get("/api/library/history")


@tool
async def switch_library(data: SwitchLibraryRequest):
    """
    Switch the library currently opened by Eagle.
    
    Args:
        data: Library switch parameters including library path
        
    Returns:
        dict: Result of library switch operation
    """
    payload = data.model_dump(exclude_none=True)
    return await eagle_api_post("/api/library/switch", payload)


@tool
async def get_library_icon(data: GetLibraryIconRequest):
    """
    Obtain the icon of the specified Library.
    
    Note: This function is deprecated and returns binary data.
    
    Args:
        data: Library icon request parameters including library path
        
    Returns:
        dict: Binary content or error response
    """
    payload = data.model_dump(exclude_none=True)
    result = await eagle_api_get("/api/library/icon", payload, is_binary=True)
    
    if isinstance(result, dict) and result.get("status") == "error":
        return result
    
    content, content_type = result
    # For MCP, we'll return the content type and a note about binary data
    return {
        "content_type": content_type,
        "data_size": len(content),
        "note": "Binary icon data available but not displayed in text format"
    }


# List of all library tools
library_tools = [
    get_library_info,
    get_library_history,
    switch_library,
    get_library_icon,
]