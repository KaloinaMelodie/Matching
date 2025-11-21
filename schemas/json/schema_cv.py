SCHEMA_CV = {
    "informations_personnelles": {
        "nom": "string",
        "prenom": "string",
        "adresse": "string",
        "sexe": "string",
        "date_de_naissance": "string",  
        "email": "string",
        "numero_telephone": "string"
    },
    "experiences_professionnelles": [
        {
            "titre_du_poste": "string",
            "nom_de_l_entreprise": "string",
            "dates_de_debut_et_de_fin": "string",
            "missions_realisees": ["string", "..."]
        }
    ],
    "formation": [
        {
            "diplome": "string",
            "etablissement": "string",
            "dates_de_debut_et_de_fin": "string",
            "specialite": "string"
        }
    ],
    "langues": [
        {
            "langue_maitrisee": "string",
            "niveau_de_maitrise": "string"
        }
    ],
    "certifications": [
        {
            "titre": "string",
            "dates_d_obtention": "string"
        }
    ],
    "passe_temps": [
        {
            "nom": "string"
        }
    ],
    "competences": {
        "competences_techniques": ["string", "..."],
        "competences_comportementales_soft_skills": ["string", "..."]
    },
    "contenu":"string"
}
