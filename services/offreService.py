from models.offre import Offre
from core.exceptions import NotFoundError

async def createOffre(offre: Offre) -> Offre:
    return await offre.insert()

async def getAllOffres():
    return await Offre.find_all().to_list()

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
