from beanie import Document
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import date

# --- Sous-modèles ---

class InformationsPersonnelles(BaseModel):
    nom: str
    prenom: str
    adresse: str
    sexe: str
    date_de_naissance: Optional[str]
    email: str
    numero_telephone: str

class ExperienceProfessionnelle(BaseModel):
    titre_du_poste: str
    nom_de_l_entreprise: str
    dates_de_debut_et_de_fin: str 
    missions_realisees: List[str] 
class Formation(BaseModel):
    diplome: str
    etablissement: str
    dates_de_debut_et_de_fin: str
    specialite: str

class Langue(BaseModel):
    langue_maitrisee: str
    niveau_de_maitrise: str

class Certification(BaseModel):
    titre: str
    dates_d_obtention: str

class PasseTemps(BaseModel):
    nom: str

class Competences(BaseModel):
    competences_techniques: List[str]
    competences_comportementales_soft_skills: List[str]

# --- Modèle principal ---

class Candidat(Document):
    informations_personnelles: InformationsPersonnelles
    experiences_professionnelles: List[ExperienceProfessionnelle]
    formation: List[Formation]
    langues: List[Langue]
    certifications: List[Certification]
    passe_temps: List[PasseTemps]
    competences: Competences
    contenu: str 

    class Settings:
        name = "candidats"  # nom de la collection MongoDB
