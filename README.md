# Chatbet

## Introducción

API desarrollada con FastAPI que consume apuestas deportivas desde una API externa, estructura sus datos y los expone mediante diversos endpoints.

## Instalación

### Clonar el repositorio

```
git clone chatbet
```
```
cd chatbet
```

### Crear y activar el entorno virtual

```
python -m venv venv # Crea el entorno
```
```
source venv/bin/activate # En macOs/Linux
```
```
venv/Scripts/activate # En Windows
```

### Instalar dependencias

```
pip install -r requirements.txt
```

### Configurar variables de entorno

```
ENV_API_URL = "https://vjq8qplo2h.execute-api.us-east-1.amazonaws.com/test"
```

### Ejecutar la aplicación

```
uvicorn main:app --reload
```
La API estará disponible en http://127.0.0.1:8000/docs#/

## Desplegar con Docker

### Construir la imagen con Docker

```
docker build -t fastapi-app .
```

### Ejecutar el contenedor

```
docker run -p 8000:8000 fastapi-app
```
La API estará disponible en http://127.0.0.1:8000/docs#/

## Endpoints

### Get /get-sports

Obtiene los deportes disponibles de la API externa.  

Parámetros:  
```lIds``` (int) -> Identificador de lenguaje  
```mT``` (int) -> Tipo de partido: prepartido=0, en vivo=1, ambos=2  
```forLive``` (bool) -> True si es en vivo, False si es prepartido  
```uT``` (int) -> Tipo de usuario: betshop=1, internet=2, terminal=5  
```cC``` (str) -> Código del país  

Ejemplo:
```
http://127.0.0.1:8000/docs#/default/get_sports_get_sports_get
```

### Get /get-championships

Obtiene los campeonatos disponibles de la API externa.  

Parámetros:  
```lIds``` (int) -> Identificador de lenguaje  
```spIds``` (int) -> Lista de identificadores de los deportes  
```forLive``` (bool) -> True si es en vivo, False si es prepartido  
```uT``` (int) -> Tipo de usuario: betshop=1, internet=2, terminal=5  
```cC``` (str) -> Código del país  

Ejemplo:
```
http://127.0.0.1:8000/docs#/default/get_championships_get_championships_get
```

### Get /get-tournaments

Obtiene los torneos disponibles de la API externa.  

Parámetros:  
```lIds``` (int) -> Identificador de lenguaje  
```chIds``` (int) -> Lista de identificadores de los campeonatos  
```forLive``` (bool) -> True si es en vivo, False si es prepartido  
```cC``` (str) -> Código del país  

Ejemplo:
```
http://127.0.0.1:8000/docs#/default/get_tournaments_get_tournaments_get
```

### Get /get-matches

Obtiene los partidos disponibles de la API externa.  

Parámetros:  
```lIds``` (int) -> Identificador de lenguaje  
```tIds``` (int) -> Lista de identificadores de los torneos  
```dateFrom``` (str) -> Partidos con fechas de inicio posteriores  
```dateFrom``` (str) -> Partidos con fechas de inicio anteriores  
```cC``` (str) -> Código del país  
```sttIds``` (int) -> Tipos de mercados  

Ejemplo:
```
http://127.0.0.1:8000/docs#/default/get_matches_get_matches_get
```

### Get /get-all-data

Obtiene los datos de todos los endpoints de la API externa.  

Parámetros:  
```section``` (str | None) -> Trae datos de una sección: sports, championships, tournaments, matches  
```id``` (int | None) -> Busca en la sección consultada el id (Es obligatorio añadir una sección si se quiere buscar por id)  

Nota:  
Inicialmente estará vacío, cada vez que llame un endpoint, ej: get-sports la próxima vez que llame get-all-data obtendrá los datos de get-sports.  

Ejemplo:
```
http://127.0.0.1:8000/docs#/default/get_matches_get_matches_get
```

### Get /get-odds

Obtiene los datos de los mercados 1, 2 y 3 de la API externa.  

Parámetros:  
```amount``` (float) -> Cantidad que pone el usuario  
```tournamentId``` (int | None) -> Id de algún torneo  
```matchId``` (str | None) -> Id de algún partido  

Nota:  
Dependiendo del mercado que consulte en get-matches (sttIds), será el mercado que aparezca, ej: si sttIds=2, apaecerá el mercado 2. Por eso antes de ejecutar get-odds, es necesario ejecutar get-matches con el sttIds que se quiera buscar en get-odds.  

Ejemplo:
```
http://127.0.0.1:8000/docs#/default/get_matches_get_matches_get
```