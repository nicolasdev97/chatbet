from fastapi import APIRouter, HTTPException
from services.fetch_data import fetch_data
from storage import update_section

# Crea una instancia del router
router = APIRouter()

# Define el endpoint de get-championships
# Asíncrona para que no bloquee la app
# Se pasan parámetros con valores por defecto
@router.get("/get-championships")
async def get_championships(
    lIds: int = 13,
    spIds: int = 1,
    forLive: bool = False,
    uT: int = 2,
    cC: str = "DEF"
):
    params = {
        "lIds": lIds,
        "spIds": spIds,
        "forLive": forLive,
        "uT": uT,
        "cC": cC
    }
    try:
        # Llama a la función fetch_data pasando el endpoint y sus parametros
        data = await fetch_data("getChampionships", params)

        # Si no hay datos
        if not data:
            raise HTTPException(
                status_code=404,
                detail="No se encontraron campeonatos"
            )
        
        # Crea una lista con el id y el nombre de los campeonatos obtenidos
        championships_filtered = [{"championshipId": item["ID"], "championshipName": item["NM"].get("13")} for item in data.get("result", [])]

        # Guarda la lista en stored_data
        update_section("championships", championships_filtered)

        # Retorna la lista
        return {"championships": championships_filtered}
    
    # Si ocurre un error inesperado
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error interno en el servidor: {str(e)}"
        )