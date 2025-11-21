import os
import json
from typing import Any, Dict
from schemas.pydantic.cv_model import CVSchema
from schemas.json.schema_cv import SCHEMA_CV
import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig
from pydantic import ValidationError
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s') 
logger = logging.getLogger(__name__)

PROMPT_TEMPLATE = """
Tu es un expert en extraction structurée à partir de texte libre. 
À partir du texte ci-dessous (un CV), renvoie les données extraites sous forme de JSON EXACTEMENT selon le schéma suivant (tous les champs doivent être présents, même s'ils sont vides).
 
Règles importantes :
1. Garde les **noms de champs exactement identiques** au schéma JSON (respecte la casse, les accents et les underscores).
2. Tous les champs doivent apparaître (même vides).
3. Pour les champs de type **liste** :
   - Si AUCUNE information n’est disponible pour un objet, ne mets pas l’objet vide, mais une liste vide `[]`.
   - Si au moins un champ de l’objet contient une valeur, alors conserve **toute la structure** de l’objet avec les autres champs vides.
4. Ne traduis pas les noms des champs.
5. La réponse doit être **uniquement** un JSON bien formé, sans texte supplémentaire ni commentaires.
6. **Aucune valeur ne doit contenir de saut de ligne, de retour à la ligne ou de texte sur plusieurs lignes.**
   - Toutes les valeurs doivent tenir sur une seule ligne.
   - Si le texte extrait contient des retours à la ligne, **remplace-les par un espace unique.**
7. Aucune clé ni valeur ne doit être omise ou tronquée.
8. Laisse la valeurs de "contenu" en string vide "".

SCHÉMA :
{schema}

TEXTE DU CV :
{cv_text}

Réponse attendue : uniquement un JSON valide conforme aux règles ci-dessus.
""".strip()


def _build_prompt(cv_text: str) -> str:
    return PROMPT_TEMPLATE.format(
        schema=json.dumps(SCHEMA_CV, indent=2, ensure_ascii=False),
        cv_text=cv_text.strip()
    )

def _parse_json_strict_or_braces_fallback(raw: str) -> dict:
    try:
        return json.loads(raw)
    except Exception:
        json_start = raw.find("{")
        json_end = raw.rfind("}") + 1
        if json_start == -1 or json_end <= 0:
            raise ValueError(f"Réponse non‑JSON :\n{raw}")
        return json.loads(raw[json_start:json_end])

def extract_structured_data_from_cv_gemini( 
    cv_text: str,
    model: str = "gemini-2.5-pro",
    project: str = os.getenv("GCP_PROJECT_ID"),
    location: str = "us-central1",
) -> "CVSchema":

    vertexai.init(project=project, location=location)

    prompt = _build_prompt(cv_text)

    gen_config = GenerationConfig(
        temperature=0.2,
        max_output_tokens=8000,  
        candidate_count=1,
        response_mime_type="application/json",
    )

    model_ref = GenerativeModel(model)
    try:
        resp = model_ref.generate_content(
            [
                prompt
            ],
            generation_config=gen_config,
        )
    except Exception as e:
        raise Exception(f"Gemini API error: {e}")

    raw_text = None
    try:
        raw_text = getattr(resp, "text", None)
        if not raw_text:
            parts = (
                resp.candidates[0].content.parts
                if getattr(resp, "candidates", None)
                else []
            )
            if parts and hasattr(parts[0], "text"):
                raw_text = parts[0].text
    except Exception:
        pass

    if not raw_text or not str(raw_text).strip():
        raise ValueError("Réponse vide de Gemini (aucun texte/JSON récupéré).")
    # logger.info(f"Gemini raw response: {raw_text}") 
    try:
        parsed: Dict[str, Any] = _parse_json_strict_or_braces_fallback(raw_text)
        return CVSchema(**parsed)
    except (ValueError, ValidationError) as e:
        raise ValueError(f"Parsing JSON failed: {e}\n\nText:\n{raw_text}")
