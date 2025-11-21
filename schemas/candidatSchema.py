from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import date
from models.candidat import Candidat 


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


class CandidatCreateSchema(BaseModel):
    informations_personnelles: InformationsPersonnelles
    experiences_professionnelles: List[ExperienceProfessionnelle]
    formation: List[Formation]
    langues: List[Langue]
    certifications: List[Certification]
    passe_temps: List[PasseTemps]
    competences: Competences
    contenu: str 


class CandidatUpdateSchema(BaseModel):
    informations_personnelles: Optional[InformationsPersonnelles] = None
    experiences_professionnelles: Optional[List[ExperienceProfessionnelle]] = None
    formation: Optional[List[Formation]] = None
    langues: Optional[List[Langue]] = None
    certifications: Optional[List[Certification]] = None
    passe_temps: Optional[List[PasseTemps]] = None
    competences: Optional[Competences] = None


class CandidatResponseSchema(CandidatCreateSchema):
    id: str 

