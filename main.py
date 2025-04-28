from fastapi import FastAPI
from fastapi_mcp import FastApiMCP
from routes import (
    mcp_router,
    application_router,
    folder_router,
    item_router,
    library_router,
)

app = FastAPI(
    title="Eagle MCP API",
)

# Register routers
app.include_router(mcp_router)
app.include_router(application_router)
app.include_router(folder_router)
app.include_router(item_router)
app.include_router(library_router)

mcp = FastApiMCP(
    app,
    name="Eagle MCP Server",
    description="An MCP server for Eagle",
)

mcp.mount()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
