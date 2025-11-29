import typing
from models.candidat import Candidat
from core.exceptions import NotFoundError, ConflictError
from beanie.operators import Set
from typing import List
from beanie import PydanticObjectId
from beanie.operators import NotIn
from beanie.operators import In

from utils.extract_helper import make_contenu_from_candidat

async def createCandidat(candidat: Candidat) -> Candidat:
    email = candidat.informations_personnelles.email
    existing = await Candidat.find_one({"informations_personnelles.email": email})
    if existing:
        raise ConflictError("Un candidat avec cet email existe déjà.")
    candidat.contenu = make_contenu_from_candidat(candidat) 
    return await candidat.insert()

async def getAllCandidats():
    return await Candidat.find_all().to_list()

async def get_candidates_chunk_not_in_ids(
        existing_ids: typing.Set[str],
        limit: int = 100
    ) -> List["Candidat"]:
        if not existing_ids:
            return await Candidat.find_all().limit(limit).to_list()

        ids_to_exclude = [PydanticObjectId(_id) for _id in existing_ids]

        return await Candidat.find(
            NotIn(Candidat.id, ids_to_exclude)
        ).limit(limit).to_list()

async def get_candidats_by_ids(ids: List[str]) -> List["Candidat"]:
        object_ids = [PydanticObjectId(_id) for _id in ids]
        return await Candidat.find(In(Candidat.id, object_ids)).to_list()

async def getCandidatById(candidat_id: str) -> Candidat:
    candidat = await Candidat.get(candidat_id)
    if not candidat:
        raise NotFoundError("Candidat non trouvé.")
    return candidat

async def updateCandidat(candidatId: str, updateData: Candidat) -> Candidat:
    existing = await getCandidatById(candidatId)  
    updateDict = updateData.dict(exclude_unset=True)

    for field, value in updateDict.items():
        setattr(existing, field, value)

    await existing.save()
    return existing

async def deleteCandidat(candidat_id: str):
    candidat = await getCandidatById(candidat_id)
    await candidat.delete()
    return {"message": "Candidat supprimé avec succès"}
