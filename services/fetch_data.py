from fastapi import HTTPException
import httpx
from config import API_URL

# Define la función
# El parámetro ep representa el endpoint que va a consultar
# El parámetro params representa los querys que se enviarán a la solicitud
async def fetch_data(ep: str, params: dict):
    # Define la URL a la que se va a realizar la consulta
    url = f"{API_URL}/{ep}"
    
    try:
        # Crea un cliente HTTP asíncrono
        # El cliente se cierra después de usarse
        # Para evitar problemas de conexión
        async with httpx.AsyncClient() as client:
            # Se realiza la solcitud get a la URL previamente definida pasando los querys
            response = await client.get(url, params=params)
            
            # Verifica si hay un código de error
            response. raise_for_status()

            # Retorna la respuesta
            return response.json()
        
    # Si ocurre un error inesperado
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error interno en el servidor: {str(e)}"
        )