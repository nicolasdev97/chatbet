from fastapi import APIRouter, HTTPException
from services.fetch_data import fetch_data

# Se crea una instancia del router
router = APIRouter()

# Se define el endpoint de get-sports
# Asíncrona para que no detenga la ejecución
# Se pasan parámetros con valores por defecto
@router.get("/get-sports")
async def get_sports(
    lIds: int = 2,
    mT: int = 2,
    forLive: bool = False,
    uT: int = 2,
    cC: str = "DEF"
):
    params = {
        "lIds": lIds,
        "mT": mT,
        "forLive": forLive,
        "uT": uT,
        "cC": cC
    }
    try:
        # Se llama a la función fetch_data pasando el endpoint y sus parametros
        data = await fetch_data("getSports", params)

        # Si no hay datos
        if not data:
            raise HTTPException(
                status_code=404,
                detail="No se encontró deportes"
            )
        
        # Se crea una lista con el ID y el Name de los deportes obtenidos
        sports_filtered = [{"ID": item["ID"], "Name": item["NM"].get("2")} for item in data.get("result", [])]
        return {"sports": sports_filtered}
    # Si ocurre un error inesperado
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error interno en el servidor: {str(e)}"
        )