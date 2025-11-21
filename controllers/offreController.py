from fastapi import HTTPException
from services import offreService
from core.exceptions import NotFoundError
from schemas.offreSchema import (
    OffreCreateSchema,
    OffreUpdateSchema,
    OffreResponseSchema,
)
from core.responseUtils import toResponse, toListResponse
from models.offre import Offre

async def createOffre(offreData: OffreCreateSchema) -> OffreResponseSchema:
    offreModel = Offre(**offreData.dict())
    created = await offreService.createOffre(offreModel)
    return toResponse(created,OffreResponseSchema)

async def getAllOffres() -> list[OffreResponseSchema]:
    offres = await offreService.getAllOffres()
    return toListResponse(offres,OffreResponseSchema)

async def getOffreById(offreId: str) -> OffreResponseSchema:
    try:
        offre = await offreService.getOffreById(offreId)
        return toResponse(offre,OffreResponseSchema)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

async def updateOffre(offreId: str, updateData: OffreUpdateSchema) -> OffreResponseSchema:
    try:
        existing = await offreService.getOffreById(offreId)
        updateDict = updateData.dict(exclude_unset=True)
        for field, value in updateDict.items():
            setattr(existing, field, value)
        updated = await offreService.updateOffre(offreId, existing)
        return toResponse(updated,OffreResponseSchema)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

async def deleteOffre(offreId: str):
    try:
        return await offreService.deleteOffre(offreId)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
