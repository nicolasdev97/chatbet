from fastapi import APIRouter, HTTPException
from services.fetch_data import fetch_data
from storage import update_section

# Crea una instancia del router
router = APIRouter()

# Define el endpoint de get-tournaments
# Asíncrona para que no bloquee la app
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
        # Llama a la función fetch_data pasando el endpoint y sus parametros
        data = await fetch_data("getTournaments", params)

        # Si no hay datos
        if not data:
            raise HTTPException(
                status_code=404,
                detail="No se encontraron torneos"
            )
        
        # Crea una lista con el id y el nombre de los torneos obtenidos
        tournaments_filtered = [{
            "championshipID": item["CHIID"],
            "tournamentId": item["ID"],
            "tournamentName": item["NM"].get("2")}
            for item in data.get("result", [])]

        # Guarda los datos de la lista en stored_data
        update_section("tournaments", tournaments_filtered)

        # Retorna los datos
        return {"tournaments": tournaments_filtered}
    
    # Si ocurre un error inesperado
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error interno en el servidor: {str(e)}"
        )