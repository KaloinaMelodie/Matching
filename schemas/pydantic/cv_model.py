from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import date


class InformationsPersonnelles(BaseModel):
    nom: Optional[str]
    prenom: Optional[str]
    adresse: Optional[str]
    sexe: Optional[str]
    date_de_naissance: Optional[str]
    email: Optional[str]
    numero_telephone: Optional[str]

class ExperienceProfessionnelle(BaseModel):
    titre_du_poste: Optional[str]
    nom_de_l_entreprise: Optional[str]
    dates_de_debut_et_de_fin: Optional[str ]
    missions_realisees: Optional[List[str] ]
class Formation(BaseModel):
    diplome: Optional[str]
    etablissement: Optional[str]
    dates_de_debut_et_de_fin: Optional[str]
    specialite: Optional[str]

class Langue(BaseModel):
    langue_maitrisee: Optional[str]
    niveau_de_maitrise: Optional[str]

class Certification(BaseModel):
    titre: Optional[str]
    dates_d_obtention: Optional[str]

class PasseTemps(BaseModel):
    nom: Optional[str]

class Competences(BaseModel):
    competences_techniques: Optional[List[str]]
    competences_comportementales_soft_skills: Optional[List[str]]


class CVSchema(BaseModel):
    informations_personnelles: Optional[InformationsPersonnelles]
    experiences_professionnelles: Optional[List[ExperienceProfessionnelle]]
    formation: Optional[List[Formation]]
    langues: Optional[List[Langue]]
    certifications: Optional[List[Certification]]
    passe_temps: Optional[List[PasseTemps]]
    competences: Optional[Competences]
    contenu: Optional[str]

