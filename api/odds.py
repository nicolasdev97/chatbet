from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any

# Crea una instancia del router
router = APIRouter()

# Variable para almacenar los datos de matches
matches_data: List[Dict[str, Any]] = []
# Variable para almacenar el mercado que se consulta en matches
sttIds_data: int = 0

# Actualiza los datos desde matches.py
def set_matches_data(data: List[Dict[str, Any]], sttIds: int):
    # Actualiza los datos de matches y el mercado de matches
    global matches_data, sttIds_data
    matches_data = data
    sttIds_data = sttIds

# Define el endpoint de get-odds
# Asíncrona para que no bloquee la app
# Se pasan parámetros opcionales
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
    return process_odds(matches_data, amount, sttIds_data)

# Estructuración de datos
def process_odds(
        data: List[Dict[str, Any]],
        amount: float, sttIds_data: int
):
    try:
        # Se crea la variable donde irá la estructura
        odds_data = []

        # Itera sobre los resultados
        for item in data.get("result"):
            # Si el mercado es 1 genera una estructura results
            if sttIds_data == 1:
                result_market = {
                    "tie": format_odds(item["STKS"][0], amount),
                    "homeTeam": format_odds(item["STKS"][1], amount),
                    "awayTeam": format_odds(item["STKS"][2], amount)
                }
            
            # Si el mercado es 2 calcula el mercado y genera una estructura handicap
            elif sttIds_data == 2:
                result_market = {
                    "handicap": calculate_main_market_for_segment(item["STKS"], amount, sttIds_data)
                }
            
            # Si el mercado es 3 calcula el mercado y genera una estructura over_under
            elif sttIds_data == 3:
                result_market = {
                    "over_under": calculate_main_market_for_segment(item["STKS"], amount, sttIds_data)
                }
            
            # Si no es ninguno de los 3 mercados
            else:
                raise HTTPException(
                    status_code=404,
                    detail="No se encontraron datos"
                )
            
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
    
# Retorna un diccionario con una estructura base
def format_odds(stake: Dict[str, Any], amount: float):
    return {
        "name": stake["NM"].get("13"),
        "profit": stake["FCR"] * amount,
        "odds": stake["FCR"],
        "betId": stake["ID"]
    }

# Calcula el tipo de mercado
def calculate_main_market_for_segment(stakes: List[Dict[str, Any]], amount: float, sttIds_data: int | None):
    # Menor diferencia
    min_diff = float("inf")
    
    # Mejor combinación
    best_pair = None
    
    # Total de apuestas
    n = len(stakes)

    # Por cada apuesta itera en todas las apuestas
    for i in range(n):
        for j in range(i + 1, n):
            # Guarda el ARG de las dos apuestas
            arg1 = float(stakes[i].get("ARG"))
            arg2 = float(stakes[j].get("ARG"))

            # Verifica que los ARG no estén vacíos
            if arg1 is None or arg2 is None:
                continue

            # Convierte los ARG en float
            arg1 = float(arg1)
            arg2 = float(arg2)

            # Cuando encuentra dos ARG iguales
            if arg1 == arg2:
                # Calcula la diferencia con sus respectivos FCR
                diff = abs(stakes[i]["FCR"] - stakes[j]["FCR"])
                
                # Se asegura de guardar la menor diferencia y sus respectivos stakes
                if diff < min_diff:
                    min_diff = diff
                    best_pair = (stakes[i], stakes[j])
    
    # Si best_pair no está vacío
    if best_pair:
        # Si el mercado es 2 retorna la estructura de handicap
        if sttIds_data == 2:
            return {
            "homeTeam": format_odds(best_pair[0], amount),
            "awayTeam": format_odds(best_pair[1], amount)
        }
        
        # Si el mercado es 3 retorna la estructura de over_under
        if sttIds_data == 3:
            return {
            "over": format_odds(best_pair[0], amount),
            "under": format_odds(best_pair[1], amount)
        }
    
    # Si el best_pair está vacío
    else:
        raise HTTPException(
            status_code=404,
            detail="No se encontraron datos"
        )