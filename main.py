from fastapi import FastAPI
from api import sports, championships, tournaments, matches

# Se crea la API
app = FastAPI()

# Se incluyen las rutas para consumir las APIs externas
app.include_router(sports.router)
app.include_router(championships.router)
app.include_router(tournaments.router)
app.include_router(matches.router)