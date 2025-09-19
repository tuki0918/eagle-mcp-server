import asyncio
from fastmcp import FastMCP

mcp = FastMCP("Test Server")

@mcp.tool
def test_tool():
    """A test tool"""
    return "Hello from test tool"

async def main():
    print("FastMCP setup successful")
    tools = await mcp.get_tools()
    print("Tools:", list(tools.keys()))

if __name__ == "__main__":
    asyncio.run(main())
