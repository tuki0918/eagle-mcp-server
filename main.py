from fastapi import FastAPI
from fastapi_mcp import FastApiMCP

app = FastAPI()

@app.get("/api/connect", operation_id="connect")
async def connect():
    return {"message": "Connected!"}

mcp = FastApiMCP(
    app,
    name="My API MCP",
    description="Very cool MCP server",
)

mcp.mount()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
