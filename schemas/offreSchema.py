from pydantic import BaseModel
from typing import List, Optional
from models.offre import Offre

# -------- CREATE --------
class OffreCreateSchema(BaseModel):
    titre: str
    entreprise: str
    contrat: str
    description: List[str]
    date_limite: str
    avantages_entreprise: Optional[str] = None
    mission: List[str]
    profil: List[str]
    reference: str
    lien_offre: str
    lien_description: str
    contenu: str

# -------- UPDATE --------
class OffreUpdateSchema(BaseModel):
    titre: Optional[str] = None
    entreprise: Optional[str] = None
    contrat: Optional[str] = None
    description: Optional[List[str]] = None
    date_limite: Optional[str] = None
    avantages_entreprise: Optional[str] = None
    mission: Optional[List[str]] = None
    profil: Optional[List[str]] = None
    reference: Optional[str] = None
    lien_offre: Optional[str] = None
    lien_description: Optional[str] = None

# -------- RESPONSE --------
class OffreResponseSchema(OffreCreateSchema):
    id: str

# -------- HELPER --------
def toOffreResponse(offre: Offre) -> OffreResponseSchema:
    d = offre.dict()
    d["id"] = str(offre.id)
    return OffreResponseSchema(**d)
