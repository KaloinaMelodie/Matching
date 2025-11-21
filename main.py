from fastapi import FastAPI
from core.database import initiate_database
from routers import include_routes, auth
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Autoriser ton frontend
origins = [
    "http://localhost:5173",
    "http://localhost:4173",
    "https://front-talentmatch.onrender.com"
        # port de Vite
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # autorise le frontend
    allow_credentials=True,
    allow_methods=["*"],     # GET, POST, PUT, DELETE…
    allow_headers=["*"],     # tous les headers
)

@app.on_event("startup")
async def start_db():
    await initiate_database()
    print("")


# importation des routes
include_routes(app) 

@app.get("/")
def read_root():
    return {"Hello": "World"}

