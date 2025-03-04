from fastapi import APIRouter, HTTPException
from services.fetch_data import fetch_data
from storage import update_section
from api.odds import set_matches_data

# Crea una instancia del router
router = APIRouter()

# Define el endpoint de get-matches
# Asíncrona para que no bloquee la app
# Se pasan parámetros con valores por defecto
@router.get("/get-matches")
async def get_matches(
    lIds: int = 13,
    tIds: int = 998,
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
        # Llama a la función fetch_data pasando el endpoint y sus parametros
        data = await fetch_data("getMatches", params)

        # Si no hay datos
        if not data:
            raise HTTPException(
                status_code=404,
                detail="No se encontraron partidos"
            )
        
        # Crea una lista con el id y el nombre de los partidos obtenidos
        matches_filtered = [{
            "tournamentID": item["TIID"],
            "matchId": item["ID"],
            "homeTeamName": item["HNM"].get("13"),
            "homeTeamID": item["HCIDS"][0],
            "awayTeamName": item["ANM"].get("13"),
            "awayTeamID": item["ACIDS"][0],
            "startDate": item["StartDate"]}
            for item in data.get("result", [])]

        # Guarda los datos de la lista en stored_data
        update_section("matches", matches_filtered)

        # Pasa los datos de la lista a odds.py
        set_matches_data(data, sttIds)

        # Retorna los datos
        return {"matches": matches_filtered}
    
    # Si ocurre un error inesperado
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error interno en el servidor: {str(e)}"
        )