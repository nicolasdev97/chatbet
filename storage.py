# Almacena los datos de cada unas de las APIs
stored_data = {
    "sports": [],
    "championships": [],
    "tournaments": [],
    "matches": []
}

# Actualiza cada sección de stored_data
def update_section(section: str, data: list):
    # Si la sección se encuentra en stored_data
    if section in stored_data:
        stored_data[section] = data
    # Si la sección no se encuentra en stored_data
    else:
        raise ValueError(
            f"No se encontró la sección {section}"
        )