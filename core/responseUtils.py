# utils/responseUtils.py

from typing import Type, TypeVar, List
from beanie import Document
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)

def toResponse(model: Document, schema: Type[T]) -> T:
    base = model.dict()
    
    # On supprime le champ 'id' s'il existe (car ObjectId)
    base.pop("id", None)
    
    # On force l'insertion de l'id converti en str au début
    ordered = {"id": str(model.id)}
    ordered.update(base)
    
    return schema(**ordered)


def toListResponse(models: List[Document], schema: Type[T]) -> List[T]:
    return [toResponse(model, schema) for model in models]
