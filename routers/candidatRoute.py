from fastapi import APIRouter
from typing import List
from controllers import candidatController
from schemas.candidatSchema import (
    CandidatCreateSchema,
    CandidatUpdateSchema,
    CandidatResponseSchema
)

router = APIRouter(
    prefix="/candidats",
    tags=["candidats"],
    responses={404: {"description": "Candidat non trouvé"}}
)

@router.post("", response_model=CandidatResponseSchema)
async def createCandidat(candidat: CandidatCreateSchema):
    return await candidatController.createCandidat(candidat)

@router.get("", response_model=List[CandidatResponseSchema])
async def getAllCandidats():
    return await candidatController.getAllCandidats()

@router.get("/{candidat_id}", response_model=CandidatResponseSchema)
async def getCandidatById(candidat_id: str):
    return await candidatController.getCandidatById(candidat_id)

@router.put("/{candidat_id}", response_model=CandidatResponseSchema)
async def updateCandidat(candidat_id: str, candidat: CandidatUpdateSchema):
    return await candidatController.updateCandidat(candidat_id, candidat)

@router.delete("/{candidat_id}")
async def deleteCandidat(candidat_id: str):
    return await candidatController.deleteCandidat(candidat_id)
