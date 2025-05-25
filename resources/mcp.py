from fastmcp import Resource, Tool
from schemas.mcp import ConnectSuccessResponse

class MCPResource(Resource):
    name = "mcp"
    description = "MCP connect endpoint"

    @Tool()
    async def connect(self):
        return ConnectSuccessResponse(message="Connected!")
