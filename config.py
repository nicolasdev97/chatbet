import os
from dotenv import load_dotenv

# Carga las variables del .env
load_dotenv()

# Obtiene la url de la API desde .env
API_URL = os.getenv("ENV_API_URL")