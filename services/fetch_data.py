from fastapi import HTTPException
import httpx

# Se define la URL donde se harán las peticiones
API_URL = "https://vjq8qplo2h.execute-api.us-east-1.amazonaws.com/test"

async def fetch_data(endpoint: str, params: dict):
    url = f"{API_URL}/{endpoint}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response. raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail="Error al obtener los datos de la API"
            )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno en el servidor: {str(e)}"
        )