from typing import Literal, Union
import httpx
import os
import logging
import json

logger = logging.getLogger(__name__)

EAGLE_API_BASE_URL = os.environ.get("EAGLE_API_BASE_URL", "http://localhost:41595")


async def request_to_eagle_api(
    method: Literal["GET", "POST"],
    endpoint: str,
    params: dict = None,
    payload: dict = None,
    is_binary: bool = False,
) -> Union[dict, tuple[bytes, str]]:
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

            if is_binary:
                content_type = response.headers.get("Content-Type", "image/png")
                return response.content, content_type

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
    except json.JSONDecodeError as exc:
        logger.error(f"JSON decode error occurred: {exc}, Response: {response.text}")
        response_text = response.text
        if len(response_text) > 100:
            response_text = f"{response_text[:100]}..."
        return {
            "status": "error",
            "message": f"Invalid JSON response: {response_text}",
        }
    except Exception as exc:
        logger.error(f"Unexpected error occurred: {exc}")
        return {
            "status": "error",
            "message": "An unexpected error occurred",
        }


async def eagle_api_get(endpoint: str, params: dict = None, is_binary: bool = False):
    return await request_to_eagle_api(
        "GET", endpoint, params=params, is_binary=is_binary
    )


async def eagle_api_post(endpoint: str, payload: dict, is_binary: bool = False):
    return await request_to_eagle_api(
        "POST", endpoint, payload=payload, is_binary=is_binary
    )
