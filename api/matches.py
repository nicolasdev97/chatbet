from fastapi import APIRouter, HTTPException
from services.fetch_data import fetch_data

# Se crea una instancia del router
router = APIRouter()

# Se define el endpoint de get-matches
# Asíncrona para que no detenga la ejecución
# Se pasan parámetros con valores por defecto
@router.get("/get-matches")
async def get_matches(
    lIds: int = 13,
    tIds: int = 4584,
    dateFrom: str = "2025-02-13T00:00:00",
    dateTo: str = "2025-02-26T00:00:00",
    cC: str = "DEF",
    sttIds: int = 1
):
    params = {
        "lIds": lIds,
        "tIds": tIds,
        "dateFrom": dateFrom,
        "dateTo": dateTo,
        "cC": cC,
        "sttIds": sttIds
    }
    try:
        # Se llama a la función fetch_data pasando el endpoint y sus parametros
        data = await fetch_data("getMatches", params)

        # Si no hay datos
        if not data:
            raise HTTPException(
                status_code=404,
                detail="No se encontró partidos"
            )
        
        # Se crea una lista con el ID y el Name de los partidos obtenidos
        matches_filtered = [{"ID": item["ID"], "Name": item["NM"].get("13")} for item in data.get("result", [])]
        return {"matches": matches_filtered}
    # Si ocurre un error inesperado
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error interno en el servidor: {str(e)}"
        )