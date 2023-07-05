from typing import Any
from fastapi.responses import JSONResponse
from src.models import *


class ErrorResponse(JSONResponse):
    def __init__(self, status_code: int, message: str,) -> None:
        if status_code < 400 or status_code > 599:
            raise ValueError("Status code must an error (400 >= x <= 599).")
        super().__init__(ErrorResponseModel(msg=message).dict(),
                         status_code, None, None, None)


class DocumentCreatedResponse(JSONResponse):
    def __init__(self, id: Any, doc: dict[str, Any]) -> None:
        content: dict[str, Any] = DocumentCreatedModel(id=id, document=doc).dict()
        super().__init__(content, 201, None, None, None)
