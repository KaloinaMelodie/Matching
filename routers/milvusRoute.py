from fastapi import APIRouter, HTTPException, Body,Query
from models import TextInput
from services.milvusService import MilvusService
from agents.embedder import  generate_embedding_gemini
from exceptions.exceptions import *
from core.responses import *
from agents import *
from typing import List, Optional
import logging 
from pathlib import Path
import os


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/generate")
async def generate(
    provider: str = Query("vertex-gemini"),
    temperature: float = Query(0.7)
): 
    try:
        if input is None:
            raise BadRequestException("Donnée manquant")
        search_results = [
            {        
      "id": "04258211665b474dbe6fd9107fba52d6_0",
      "doc_id": "04258211665b474dbe6fd9107fba52d6",
      "chunk_index": 0,
      "nom": "De SAHI Anosy-MUS formulaire ménage",
      "emplacement": [
        "https://portal.mwater.co/#/forms/04258211665b474dbe6fd9107fba52d6"
      ],
      "content": "De SAHI Anosy-MUS formulaire ménage. Contexte. Site Ménage. Sites liés. Communauté. Dans quelle communauté ce ménage fait-il partie ? Limite administrative. Région. District. Commune. Le commune n'est pas trouvé sur la liste des limites administratives. Quel est le nom du commune ? Milieu de résidence. Urbain. Rural. Fokontany. Date de l'enquête. <**REMARQUE: L'enquêteur doit lire ce texte tel qu’il est rédigé**>. Puis-je commencer maintenant ? Oui. Non. Si OUI, commencer l'entretien, Si non, arrêter l'entretien. **Note:** Le consentement ne peut être obtenu que si la personne interrogée est âgée de 18 ans ou plus. Pour les moins de 18 ans, l'assentiment de la personne interrogée et le consentement du parent ou du tuteur sont nécessaires. Si le consentement/l'assentiment n'est pas obtenu, l'entretien ne doit pas commencer. CARACTERISTIQUES SOCIODEMOGRAPHIQUES ET ECONOMIQUES DES MENAGES. Qui a répondu au questionnaire ? Chef de ménage. Le ou la Conjoint(e). Other (please specify). CARACTERISTIQUES SOCIODEMOGRAPHIQUES ET ECONOMIQUES DES INDIVIDUS. Tout d'abord, dites-moi SVP le nom de chaque personne qui vit habituellement ici, en commençant par le chef de ménage. Quel est le lien de parenté de (nom) avec (nom du chef de ménage) ? CM. Conjoint (e). Fils/Fille. Other (please specify). Est-ce que (nom) est de sexe masculin ou féminin ? Homme. Femme. Quel âge a (nom) ? Enregistrer en années révolues. Quel est le niveau d’éducation du CM ? Sans niveau. Primaire. Secondaire I. Secondaire II ou plus. Cette question est à poser pour les personnes âgées de 3 ans ou plus."
    }
        ]

        search_results = MilvusService().search(input.question,input.user)
        response = search_results
        return success_response(data=response, status_code=200)
    except HTTPException as he:
        raise he
    except Exception as e:
        import traceback
        traceback_str = traceback.format_exc()
        # logger.warning(traceback_str)
        raise Exception(str(e))

@router.get("/initmilvus")
async def init_milvus():
    try:
        MilvusService()
    except HTTPException as he:
        raise he
    except Exception as e:
        import traceback
        traceback_str = traceback.format_exc()
        raise Exception(str(e))
    
    
@router.get("/embedded_gemini")
async def embed_gemini(input: Optional[TextInput] = Body(default=None)):
    try:
        if input is None:
            raise BadRequestException("Donnée manquant") 
        data = generate_embedding_gemini(input.text)
        return success_response(data=data, status_code=200)
    except HTTPException as he:
        raise he
    except Exception as e:
        import traceback
        traceback_str = traceback.format_exc()
        # logger.warning(traceback_str)
        raise Exception(str(e))




@router.post("/clean_collection")
def read_cvs():
    try:
        MilvusService()._clean_collection() 
        MilvusService()
        return success_response(message="collection cleaned successfully",status_code=201)
    except HTTPException as he:
        raise he
    except Exception as e:
        import traceback
        traceback_str = traceback.format_exc()
        logger.warning(traceback_str)
        raise Exception(str(e))

@router.post("/clean_formation_collection")
def read_cvs():
    try:
        MilvusService()._clean_formation_collection() 
        MilvusService()
        return success_response(message="formation collection cleaned successfully",status_code=201)
    except HTTPException as he:
        raise he
    except Exception as e:
        import traceback
        traceback_str = traceback.format_exc()
        logger.warning(traceback_str)
        raise Exception(str(e))
    
@router.post("/cvs_milvus")
async def update_cvs_milvus():
    try:
        message = await MilvusService().bulk_insert_cvs_to_milvus()
        return success_response(message=message,status_code=201)
    except HTTPException as he:
        raise he
    except Exception as e:
        import traceback
        traceback_str = traceback.format_exc()
        logger.warning(traceback_str)
        raise Exception(str(e))

@router.post("/offres_milvus")
async def update_offres_milvus():
    try:
        message = await MilvusService().bulk_insert_offres_to_milvus()
        return success_response(message=message,status_code=201)
    except HTTPException as he:
        raise he
    except Exception as e:
        import traceback
        traceback_str = traceback.format_exc()
        logger.warning(traceback_str)
        raise Exception(str(e))
    

@router.get("/cvs_milvus")
def read_cvs_milvus():
    try:
        rows = MilvusService().list_cvs()   
        return success_response(data = rows,status_code=200)
    except HTTPException as he:
        raise he
    except Exception as e:
        import traceback
        traceback_str = traceback.format_exc()
        logger.warning(traceback_str)
        raise Exception(str(e))

@router.get("/offres_milvus") 
def read_offres_milvus():
    try: 
        rows = MilvusService().list_offres()   
        return success_response(data = rows,status_code=200)
    except HTTPException as he:
        raise he
    except Exception as e:
        import traceback
        traceback_str = traceback.format_exc()
        logger.warning(traceback_str)
        raise Exception(str(e))

@router.delete("/offres_partition")
def delete_offres_partition():
    try:
        message = MilvusService()._clean_offre_partition()
        return success_response(message=message,status_code=200)
    except HTTPException as he:
        raise he
    except Exception as e:
        import traceback
        traceback_str = traceback.format_exc()
        logger.warning(traceback_str)
        raise Exception(str(e))
    
@router.delete("/cvs_partition")
def delete_cvs_partition():
    try:
        message = MilvusService()._clean_cv_partition()
        return success_response(message=message,status_code=200)
    except HTTPException as he:
        raise he
    except Exception as e:
        import traceback
        traceback_str = traceback.format_exc()
        logger.warning(traceback_str)
        raise Exception(str(e))
