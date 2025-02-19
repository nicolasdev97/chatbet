from fastapi import APIRouter, HTTPException
from services.fetch_data import fetch_data
from storage import update_section

# Crea una instancia del router
router = APIRouter()

# Define el endpoint de get-sports
# Asíncrona para que no bloquee la app
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
        # Llama a la función fetch_data pasando el endpoint y sus parametros
        data = await fetch_data("getSports", params)

        # Si no hay datos
        if not data:
            raise HTTPException(
                status_code=404,
                detail="No se encontraron deportes"
            )
        
        # Crea una lista con el id y el nombre de los deportes obtenidos
        sports_filtered = [{
            "sportId": item["ID"],
            "sportName": item["NM"].get("2")}
            for item in data.get("result", [])]

        # Guarda los datos de la lista en stored_data
        update_section("sports", sports_filtered)

        # Retorna los datos
        return {"sports": sports_filtered}
    
    # Si ocurre un error inesperado
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error interno en el servidor: {str(e)}"
        )