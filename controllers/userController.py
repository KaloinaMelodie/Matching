from fastapi import HTTPException
from fastapi.responses import JSONResponse


def helloUser():
    try:
        return "Hello World"
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Erreur lors de la création de l'utilisateur.")