from fastapi import HTTPException
from services import matchingService
import traceback
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def cvMatchOffres(candidat,top_n) :
    try:
        offres = await matchingService.match_offres_for_cv(candidat,top_n=top_n)
        return offres 
    except Exception as e:
            raise HTTPException(status_code=404, detail=str(e) )


async def offreMatchCandidats(offre,top_n) :
    try:
        candidats = await matchingService.match_cvs_for_offre(offre,top_n=top_n)
        return candidats 
    except Exception as e:
            print(e)
            traceback.print_exc()
            raise HTTPException(status_code=404, detail=str(e) )