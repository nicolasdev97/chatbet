from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any

# Crea una instancia del router
router = APIRouter()

# Variable para almacenar los datos de matches
matches_data: List[Dict[str, Any]] = []

# Actualiza los datos desde matches.py
def set_matches_data(data: List[Dict[str, Any]], sttIds: int):
    # A la variable global matches_data
    # Se pasa data
    # La cual trae los datos desde matches.py
    global matches_data, sttIds_data
    matches_data = data
    sttIds_data = sttIds

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
    
    # filtered_data = [
    #     match for match in matches_data
    #     if (tournamentId is None or match["tournamentId"] == tournamentId)
    #     and (matchId is None or match["matchId"] == matchId)
    # ]
    
    # Retorna la respuesta de process_odds con los datos
    return process_odds(matches_data, amount, sttIds_data)

# Estructura los datos
def process_odds(data: List[Dict[str, Any]], amount: float, sttIds_data: int):
    try:
        odds_data = []

        for item in data.get("result"):
            if sttIds_data == 1:
                result_market = {
                    "tie": format_odds(item["STKS"][0], amount),
                    "homeTeam": format_odds(item["STKS"][1], amount),
                    "awayTeam": format_odds(item["STKS"][2], amount)
                }
            elif sttIds_data == 2:
                result_market = {
                    "handicap": calculate_main_market_for_segment(item["STKS"], amount, sttIds_data)
                }
            elif sttIds_data == 3:
                result_market = {
                    "over_under": calculate_main_market_for_segment(item["STKS"], amount, sttIds_data)
                }
            else:
                result_market = {
                    "Paila": "Paila"
                }
            odds_data.append({
                "oddsData": {
                    "result": result_market
                }
            })
        # Retorna los datos
        return odds_data
    
    # Si ocurre un error inesperado
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno en el servidor: {str(e)}"
        )
    
def format_odds(stake: Dict[str, Any], amount: float):
    return {
        "name": stake["NM"].get("13"),
        "profit": stake["FCR"] * amount,
        "odds": stake["FCR"],
        "betId": stake["ID"]
    }

def calculate_main_market_for_segment(stakes: List[Dict[str, Any]], amount: float, sttIds_data: int | None):
    min_diff = float("inf")
    best_pair = None
    n = len(stakes)

    for i in range(n):
        for j in range(i + 1, n):
            arg1 = float(stakes[i].get("ARG"))
            arg2 = float(stakes[j].get("ARG"))

            if arg1 is None or arg2 is None:
                continue

            arg1 = float(arg1)
            arg2 = float(arg2)
            if arg1 == arg2:
                diff = abs(stakes[i]["FCR"] - stakes[j]["FCR"])
                if diff < min_diff:
                    min_diff = diff
                    best_pair = (stakes[i], stakes[j])
    
    if best_pair:
        if sttIds_data == 2:
            return {
            "homeTeam": format_odds(best_pair[0], amount),
            "awayTeam": format_odds(best_pair[1], amount)
        }
        if sttIds_data == 3:
            return {
            "over": format_odds(best_pair[0], amount),
            "under": format_odds(best_pair[1], amount)
        }
    else:
        return "nou"