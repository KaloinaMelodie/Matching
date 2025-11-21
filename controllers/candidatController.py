from fastapi import HTTPException
from services import candidatService
from core.exceptions import NotFoundError, ConflictError
from schemas.candidatSchema import (
    CandidatCreateSchema,
    CandidatUpdateSchema,
    CandidatResponseSchema,
)
from models.candidat import Candidat
from core.responseUtils import toResponse, toListResponse


async def createCandidat(candidatData: CandidatCreateSchema) -> CandidatResponseSchema:
    try:
        candidatModel = Candidat(**candidatData.dict())
        created = await candidatService.createCandidat(candidatModel)
        return toResponse(created,CandidatResponseSchema)
    except ConflictError as e:
        raise HTTPException(status_code=409, detail=str(e))


async def getAllCandidats() -> list[CandidatResponseSchema]:
    candidats = await candidatService.getAllCandidats()
    return toListResponse(candidats,CandidatResponseSchema)


async def getCandidatById(candidatId: str) -> CandidatResponseSchema:
    try:
        candidat = await candidatService.getCandidatById(candidatId)
        return toResponse(candidat,CandidatResponseSchema)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


async def updateCandidat(candidatId: str, updateData: CandidatUpdateSchema) -> CandidatResponseSchema:
    try:
        existing = await candidatService.getCandidatById(candidatId)
        updateDict = updateData.dict(exclude_unset=True)

        for field, value in updateDict.items():
            setattr(existing, field, value)

        updated = await candidatService.updateCandidat(candidatId, existing)
        return toResponse(updated,CandidatResponseSchema)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


async def deleteCandidat(candidatId: str):
    try:
        return await candidatService.deleteCandidat(candidatId)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
