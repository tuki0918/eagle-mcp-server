from typing import Literal
import httpx
import os
import logging

logger = logging.getLogger(__name__)

EAGLE_API_BASE_URL = os.environ.get("EAGLE_API_BASE_URL", "http://localhost:41595")


async def request_to_eagle_api(
    method: Literal["GET", "POST"],
    endpoint: str,
    params: dict = None,
    payload: dict = None,
):
    url = f"{EAGLE_API_BASE_URL}{endpoint}"
    try:
        async with httpx.AsyncClient() as client:
            if method == "GET":
                response = await client.get(url, params=params)
            elif method == "POST":
                response = await client.post(url, json=payload)
            else:
                return {
                    "status": "error",
                    "message": f"Unsupported HTTP method: {method}",
                }

            response.raise_for_status()
            return response.json()
    except httpx.RequestError as exc:
        logger.error(f"Request error occurred: {exc}")
        return {"status": "error", "message": f"An error occurred: {exc}"}
    except httpx.HTTPStatusError as exc:
        logger.error(
            f"HTTP error occurred: {exc.response.status_code}, "
            f"URL: {exc.request.url}, Response: {exc.response.text}"
        )
        return {
            "status": "error",
            "message": f"HTTP error occurred: {exc.response.status_code}",
        }


async def fetch_from_eagle_api(endpoint: str, params: dict = None):
    return await request_to_eagle_api("GET", endpoint, params=params)


async def post_to_eagle_api(endpoint: str, payload: dict):
    return await request_to_eagle_api("POST", endpoint, payload=payload)
