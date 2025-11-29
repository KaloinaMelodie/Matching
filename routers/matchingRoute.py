from fastapi import APIRouter
from models.offre import Offre
from schemas.offreSchema import OffreCreateSchema
from models.candidat import Candidat
from schemas.candidatSchema import CandidatCreateSchema
from utils.extract_helper import make_contenu_from_candidat,offre_to_text
from controllers import matchingController as ctrl 
from typing import Optional
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s') 
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/matching",
    tags=["matching"],
    responses={404: {"description": "Page non trouvée"}}
)

    
@router.get("/cv" )
async def createCandidat(candidat: CandidatCreateSchema,top_n: Optional[int] = 10):
    candidatModel = Candidat(**candidat.dict())
    candidatModel.contenu = make_contenu_from_candidat(candidatModel) 
    return await ctrl.cvMatchOffres(candidatModel,top_n)


@router.get("/offre" )
async def createCandidat(offre: OffreCreateSchema,top_n: Optional[int] = 10):
    offreModel = Offre(**offre.dict())
    offreModel.contenu = offre_to_text(offre.dict())["contenu"]
    return await ctrl.offreMatchCandidats(offreModel,top_n)