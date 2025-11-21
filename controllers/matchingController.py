from fastapi import HTTPException
from services import matchingService
import traceback

async def cvMatchOffres(id,top_n) :
    try:
        offres = await matchingService.match_offres_for_cv(id,top_n=top_n)
        return offres 
    except Exception as e:
            raise HTTPException(status_code=404, detail=str(e) )


async def offreMatchCandidats(id,top_n) :
    try:
        candidats = await matchingService.match_cvs_for_offre(id,top_n=top_n)
        return candidats 
    except Exception as e:
            print(e)
            traceback.print_exc()
            raise HTTPException(status_code=404, detail=str(e) )