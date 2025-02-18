from fastapi import HTTPException
import httpx
from config import API_URL

async def fetch_data(endpoint: str, params: dict):
    url = f"{API_URL}/{endpoint}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response. raise_for_status()
            return response.json()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno en el servidor: {str(e)}"
        )