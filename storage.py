# Almacena los datos de cada unas de las APIs
stored_data = {
    "sports": [],
    "championships": [],
    "tournaments": [],
    "matches": []
}

# Actualiza cada sección de stored_data
def update_section(section: str, data: list):
    if section in stored_data:
        stored_data[section] = data
    else:
        raise ValueError(f"Sección {section} no válida")