from models.offre import Offre
from core.exceptions import NotFoundError
import typing
from typing import List
from beanie import PydanticObjectId
from beanie.operators import NotIn

async def createOffre(offre: Offre) -> Offre:
    return await offre.insert()

async def getAllOffres():
    return await Offre.find_all().to_list()


async def get_offres_chunk_not_in_ids(
        existing_ids: typing.Set[str],
        limit: int = 100
    ) -> List["Offre"]:
        if not existing_ids:
            return await Offre.find_all().limit(limit).to_list()

        ids_to_exclude = [PydanticObjectId(_id) for _id in existing_ids]

        return await Offre.find(
            NotIn(Offre.id, ids_to_exclude)
        ).limit(limit).to_list()

async def getOffreById(offreId: str) -> Offre:
    offre = await Offre.get(offreId)
    if not offre:
        raise NotFoundError("Offre non trouvée.")
    return offre

async def updateOffre(offreId: str, updateData: Offre) -> Offre:
    existing = await getOffreById(offreId)
    updateDict = updateData.dict(exclude_unset=True)

    for field, value in updateDict.items():
        setattr(existing, field, value)

    await existing.save()
    return existing

async def deleteOffre(offreId: str):
    offre = await getOffreById(offreId)
    await offre.delete()
    return {"message": "Offre supprimée avec succès"}
