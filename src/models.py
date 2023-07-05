from typing import Any
from pydantic import BaseModel


class ErrorResponseModel(BaseModel):
    msg: str


class DocumentCreatedModel(BaseModel):
    id: Any
    document: dict[str, Any]
