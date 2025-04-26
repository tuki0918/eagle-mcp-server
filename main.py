from fastapi import FastAPI
from fastapi_mcp import FastApiMCP

app = FastAPI(
    title="Eagle MCP API",
)


@app.get("/api/connect", operation_id="connect", tags=["MCP"])
async def connect():
    return {"message": "Connected!"}


mcp = FastApiMCP(
    app,
    name="Eagle MCP",
    description="An MCP server for Eagle",
)

mcp.mount()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
