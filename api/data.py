from fastapi import APIRouter, HTTPException
from storage import stored_data

router = APIRouter()

# Define el endpoint de get-all-data
# Asíncrona para que no bloquee la app
# Se pasan parámetros opcionales
@router.get("/get-all-data")
async def get_all_data(section: str | None = None, id: int | None = None):
    try:
        # Si la sección no está vacía
        if section:
            # Trae los datos de dicha sección
            section_data = stored_data.get(section)
            
            # Si no encuentra dicha sección
            if not section_data:
                raise HTTPException(
                    status_code=404,
                    detail=f"No se encontró la sección {section}"
                )
            
            # Si el id no está vacío
            if id is not None:
                # Trae los datos de dicha sección que coincidan con el id
                section_data = [item for item in section_data if item["sectionID" == id]]
                
                # Si no encuentra ningun dato que coincida con el id en dicha sección
                if not section_data:
                    raise HTTPException(
                        status_code=404,
                        detail=f"No se encontró el id {id} en la sección {section}"
                    )
        
        # Si la sección está vacía y el id no está vacío
        if not section and id is not None:
            raise HTTPException(
                status_code=400,
                detail="Para buscar un id debe especificar una sección"
            )
        
        # Retorna la lista
        return stored_data
    
    # Si ocurre un error inesperado
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error interno en el servidor: {str(e)}"
        )