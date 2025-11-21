from beanie import Document
from typing import List, Optional

class Offre(Document):
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

    class Settings:
        name = "offres"
