from fastapi import APIRouter
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


@router.get("/cv/{candidat_id}" )
async def cv_get_offres(candidat_id: str,top_n: Optional[int] = 10):
    logger.info(candidat_id+" Tonga ato "+ str(top_n))
    return await ctrl.cvMatchOffres(candidat_id,top_n)


@router.get("/offre/{offre_id}")
async def offres_get_candidats(offre_id: str,top_n: Optional[int] = 10):
    logger.info(offre_id+" Tonga ato")
    return await ctrl.offreMatchCandidats(offre_id,top_n)