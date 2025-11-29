from services.milvusService import MilvusService
from services import candidatService
from services import offreService

from threading import Thread, Event
from time import sleep
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def match_offres_for_cv(cv_candidat, top_n: int | None = None):
    raw_results = MilvusService().search(
        query=cv_candidat.contenu,
        top_n=top_n or 10,
        partitions=["offres_vector"],
    )
    if not raw_results:
        return []

    offre_ids_ordered = [r["doc_id"] for r in raw_results]

    offres = await offreService.get_offres_by_ids(offre_ids_ordered)

    offres_by_id = {str(offre.id): offre for offre in offres}

    results = []
    for r in raw_results:
        offre_id = r["doc_id"]
        offre = offres_by_id.get(offre_id)
        if not offre:
            continue
        results.append({
            "offre": offre,
            "score": r.get("score", 0.0),
        })

    if top_n is not None:
        return results[:top_n]
    return results



async def match_cvs_for_offre(offre, top_n: int | None = None):
    raw_results = MilvusService().search(
        query=offre.contenu,
        top_n=top_n or 10,
        partitions=["cvs_vector"],
    )
    if not raw_results:
        return []

    cv_ids_ordered = [r["doc_id"] for r in raw_results]

    cvs = await candidatService.get_candidats_by_ids(cv_ids_ordered)

    cvs_by_id = {str(cv.id): cv for cv in cvs}

    results = []
    for r in raw_results:
        cv_id = r["doc_id"]
        cv = cvs_by_id.get(cv_id)
        if not cv:
            continue
        results.append({
            "candidat": cv,
            "score": r.get("score", 0.0),
        })

    if top_n is not None:
        return results[:top_n]
    return results
