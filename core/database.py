import os
import pkgutil
import importlib
import inspect
import certifi
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie, Document
from dotenv import load_dotenv

# Charger les variables d'environnement (.env)
if os.path.exists(".env.production"):
    load_dotenv(".env.production") 
else:
    load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("MONGO_DB_NAME")

async def initiate_database():
    # Création du client MongoDB avec certificats SSL fiables
    client = AsyncIOMotorClient(
        MONGO_URI,
        tls=True,
        tlsCAFile=certifi.where(),
        serverSelectionTimeoutMS=30000,  # timeout explicite (30s)
    )

    db = client[DB_NAME]

    # Importer tous les modèles Beanie présents dans le package "models"
    import models
    document_models = []
    package_path = models.__path__

    for _, module_name, _ in pkgutil.iter_modules(package_path):
        module = importlib.import_module(f"models.{module_name}")
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, Document) and obj is not Document:
                document_models.append(obj)

    # Initialiser Beanie avec les modèles détectés
    await init_beanie(database=db, document_models=document_models)
