from fastapi import APIRouter, HTTPException
from typing import Optional
from storage import stored_data

router = APIRouter()

@router.get("/get-all-data")
async def get_all_data(section: Optional[str] = None, id: Optional[int] = None):
    try:
        if section:
            section_data = stored_data.get(section)
            if not section_data:
                raise HTTPException(
                    status_code=404,
                    detail="Sección no encontrada"
                )
        if id is not None:
            section_data = [item for item in section_data if item["ID" == id]]
            if not section_data:
                raise HTTPException(
                    status_code=404,
                    detail=f"No se encontró el ID {id} en la sección {section}"
                )
        if not section and id is not None:
            raise HTTPException(
                status_code=400,
                detail="Para buscar un ID debe especificar una sección"
            )
        return stored_data
    # Si ocurre un error inesperado
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error interno en el servidor: {str(e)}"
        )