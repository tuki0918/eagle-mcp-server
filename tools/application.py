"""
Application tools for Eagle MCP Server
"""
from fastmcp import tool
from utils.eagle_api import eagle_api_get

@tool
async def get_application_info():
    """
    Get detailed information on the Eagle App currently running.
    
    In most cases, this could be used to determine whether certain functions 
    are available on the user's device.
    
    Returns:
        dict: Application information including version, platform, etc.
    """
    return await eagle_api_get("/api/application/info")

# List of all application tools
application_tools = [
    get_application_info,
]