from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any

# Crea una instancia del router
router = APIRouter()

# Variable para almacenar los datos de matches
matches_data: List[Dict[str, Any]] = []

# Actualiza los datos desde matches.py
def set_matches_data(data: List[Dict[str, Any]]):
    # A la variable global matches_data
    # Se pasa data
    # La cual trae los datos desde matches.py
    global matches_data
    matches_data = data

# Define el endpoint de get-odds
# Asíncrona para que no bloquee la app
# Sin parámetros
@router.get("/get-odds")
async def get_odds(
    amount: float,
    tournamentId: int | None = None,
    matchId: int | None = None
):
    # Si no hay datos
    if not matches_data:
        raise HTTPException(
            status_code=404,
            detail="No se encontraron datos"
        )
    
    # Retorna la respuesta de process_odds con los datos
    return process_odds(matches_data, amount)

# Estructura los datos
def process_odds(data: List[Dict[str, Any]], amount: float):
    try:
        odds_data = [{
            "oddsData": {
                "result": {
                    "tie": {
                        "name": item["STKS"][0]["NM"].get("13"),
                        "profit": item["STKS"][0]["FCR"] * amount,
                        "odds": item["STKS"][0]["FCR"],
                        "betId": item["STKS"][0]["ID"]
                    },
                    "homeTeam": {
                        "name": item["STKS"][1]["NM"].get("13"),
                        "profit": item["STKS"][1]["FCR"] * amount,
                        "odds": item["STKS"][1]["FCR"],
                        "betId": item["STKS"][1]["ID"]
                    },
                    "awayTeam": {
                        "name": item["STKS"][2]["NM"].get("13"),
                        "profit": item["STKS"][2]["FCR"] * amount,
                        "odds": item["STKS"][2]["FCR"],
                        "betId": item["STKS"][2]["ID"]
                    }
                },
                "over_under": {
                    "over": {
                        "name": "Más de 3.00",
                        "profit": 2.13,
                        "odds": 113,
                        "betId": 4638174111
                    },
                    "under": {
                        "name": "Menos de 3.00",
                        "profit": 1.71,
                        "odds": -141,
                        "betId": 4638174059
                    }
                },
                "handicap": {
                    "homeTeam": {
                        "name": str(item["STKS"][1]["NM"].get("13")) + " -1.00",
                        "profit": 1.87,
                        "odds": -115,
                        "betId": 4638174082
                    },
                    "awayTeam": {
                        "name": str(item["STKS"][2]["NM"].get("13")) + " 1.00",
                        "profit": 1.93,
                        "odds": -108,
                        "betId": 4638174108
                    },
                },
            }
        }
        for item in data.get("result", [])]

        # Retorna los datos
        return odds_data
    
    # Si ocurre un error inesperado
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno en el servidor: {str(e)}"
        )