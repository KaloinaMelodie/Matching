from fastapi import APIRouter, HTTPException,UploadFile, File
from pydantic import BaseModel
from services.structure_extractionService import extract_structured_data_from_cv_gemini
from fastapi.responses import JSONResponse
import os, tempfile
from pathlib import Path
from typing import Dict, Any

from utils.extract_helper import (
    extract_text_pdf,         
    extract_text_docx,         
    clean_text,
    make_contenu_from_candidat,               
    sha256_of_text
)

import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s') 
logger = logging.getLogger(__name__)

router = APIRouter()

MAX_FILE_MB = 20
ALLOWED_MIME_TO_SUFFIX = {
    "application/pdf": ".pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
    "application/msword": ".docx",
    "application/octet-stream": None,
}

def _guess_suffix(filename: str) -> str | None:
    ext = Path(filename).suffix.lower()
    if ext in [".pdf", ".docx"]:
        return ext
    return None
    
@router.post("/extract-text")
async def extract_text_endpoint(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=422, detail="Missing filename.")

    suffix = ALLOWED_MIME_TO_SUFFIX.get(file.content_type)
    if suffix is None:
        suffix = _guess_suffix(file.filename)

    if suffix not in [".pdf", ".docx"]:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported file type. Only PDF or DOCX are accepted (got content_type={file.content_type}).",
        )

    contents = await file.read()
    if not contents or not contents.strip():
        raise HTTPException(status_code=422, detail="Uploaded file is empty.")

    if len(contents) > MAX_FILE_MB * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Max allowed is {MAX_FILE_MB} MB.",
        )

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    try:
        tmp.write(contents)
        tmp.flush()
        tmp.close()

        if suffix == ".pdf":
            raw_text = extract_text_pdf(tmp.name)
            mime = "application/pdf"
        else:
            raw_text = extract_text_docx(tmp.name)
            mime = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

        cleaned = clean_text(raw_text, config=None)

        payload: Dict[str, Any] = {
            "filename": file.filename,
            "mime": mime,
            "size_bytes": len(contents),
            "text": cleaned,
            "char_count": len(cleaned),
            "sha256": sha256_of_text(cleaned),
        }

        return JSONResponse(payload)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Extraction failed: {e}")
    finally:
        try:
            os.unlink(tmp.name)
        except Exception:
            pass

class CVTextRequest(BaseModel):
    text: str

@router.post("/extract-structured")
async def extract_structured_data(req: CVTextRequest):
    try:
        if not req.text or not req.text.strip():
            raise HTTPException(status_code=422, detail="CV text is required and cannot be empty.")
        structured_data = extract_structured_data_from_cv_gemini(req.text)
        return structured_data.dict()
    except HTTPException:    
        raise   
    except Exception as e:
        import traceback
        traceback_str = traceback.format_exc()
        logger.warning(traceback_str)
        raise HTTPException(status_code=500, detail=str(e))
