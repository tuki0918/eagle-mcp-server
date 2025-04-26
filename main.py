from fastapi import FastAPI
from fastapi_mcp import FastApiMCP
import httpx

app = FastAPI(
    title="Eagle MCP API",
)

# Define the base URL for the Eagle API
EAGLE_API_BASE_URL = "http://localhost:41595"


@app.get("/api/connect", operation_id="connect", tags=["MCP"])
async def connect():
    return {"message": "Connected!"}


@app.get(
    "/api/application/info", operation_id="get_application_info", tags=["Application"]
)
async def get_application_info():
    url = f"{EAGLE_API_BASE_URL}/api/application/info"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as exc:
        return {"status": "error", "message": f"An error occurred: {exc}"}
    except httpx.HTTPStatusError as exc:
        return {
            "status": "error",
            "message": f"HTTP error occurred: {exc.response.status_code}",
        }


@app.get("/api/folder/list", operation_id="get_folder_list", tags=["Folder"])
async def get_folder_list():
    url = f"{EAGLE_API_BASE_URL}/api/folder/list"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as exc:
        return {"status": "error", "message": f"An error occurred: {exc}"}
    except httpx.HTTPStatusError as exc:
        return {
            "status": "error",
            "message": f"HTTP error occurred: {exc.response.status_code}",
        }


mcp = FastApiMCP(
    app,
    name="Eagle MCP",
    description="An MCP server for Eagle",
)

mcp.mount()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
