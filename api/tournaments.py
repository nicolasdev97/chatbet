from fastapi import APIRouter, HTTPException
from services.fetch_data import fetch_data
from storage import update_section

# Se crea una instancia del router
router = APIRouter()

# Se define el endpoint de get-tournaments
# Asíncrona para que no detenga la ejecución
# Se pasan parámetros con valores por defecto
@router.get("/get-tournaments")
async def get_tournaments(
    lIds: int = 2,
    chIds: int = 709,
    forLive: bool = False,
    cC: str = "DEF"
):
    params = {
        "lIds": lIds,
        "chIds": chIds,
        "forLive": forLive,
        "cC": cC
    }
    try:
        # Se llama a la función fetch_data pasando el endpoint y sus parametros
        data = await fetch_data("getTournaments", params)

        # Si no hay datos
        if not data:
            raise HTTPException(
                status_code=404,
                detail="No se encontraron torneos"
            )
        
        # Se crea una lista con el id y el nombre de los torneos obtenidos
        tournaments_filtered = [{"tournamentId": item["ID"], "tournamentName": item["NM"].get("2")} for item in data.get("result", [])]

        # Guarda la lista en stored_data
        update_section("tournaments", tournaments_filtered)

        # Retorna la lista
        return {"tournaments": tournaments_filtered}
    
    # Si ocurre un error inesperado
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error interno en el servidor: {str(e)}"
        )