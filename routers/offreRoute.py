from fastapi import APIRouter
from typing import List
from controllers import offreController
from schemas.offreSchema import (
    OffreCreateSchema,
    OffreUpdateSchema,
    OffreResponseSchema
)

router = APIRouter(
    prefix="/offres",
    tags=["offres"],
    responses={404: {"description": "Offre non trouvée"}}
)

@router.post("", response_model=OffreResponseSchema)
async def createOffre(offre: OffreCreateSchema):
    return await offreController.createOffre(offre)

@router.get("/", response_model=List[OffreResponseSchema])
async def getAllOffres():
    return await offreController.getAllOffres()

@router.get("/{offreId}", response_model=OffreResponseSchema)
async def getOffreById(offreId: str):
    return await offreController.getOffreById(offreId)

@router.put("/{offreId}", response_model=OffreResponseSchema)
async def updateOffre(offreId: str, offre: OffreUpdateSchema):
    return await offreController.updateOffre(offreId, offre)

@router.delete("/{offreId}")
async def deleteOffre(offreId: str):
    return await offreController.deleteOffre(offreId)
