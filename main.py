from fastapi import FastAPI
from api import sports, championships, tournaments, matches, data, odds

# Crea la API
app = FastAPI()

# Incluye las rutas para consumir las APIs externas
app.include_router(sports.router)
app.include_router(championships.router)
app.include_router(tournaments.router)
app.include_router(matches.router)
app.include_router(data.router)
app.include_router(odds.router)