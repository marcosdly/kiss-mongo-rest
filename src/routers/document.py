from typing import Any
from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from src.messages import ErrorResponse, DocumentCreatedResponse
from src.db import CLIENT, APIDatabaseOperations

router = APIRouter(prefix="/DOCUMENT")


@router.post("/")
async def create_document(db: str, col: str, doc: dict[str, Any] = Body()) -> JSONResponse:
    # TODO return object ID when added or updated
    if err_response := APIDatabaseOperations.test_connection(CLIENT):
        return err_response
    
    collection = APIDatabaseOperations.get_collection(CLIENT, db, col)
    if isinstance(collection, ErrorResponse):
        return collection

    result = collection.insert_one(doc.copy())
    return DocumentCreatedResponse(str(result.inserted_id), doc)


@router.get("/")
async def query_collection(db: str, col: str, query: dict[str, Any] = Body()) -> dict[str, Any]:
    pass


@router.put("/")
async def update_document(db: str, col: str, doc: dict[str, Any] = Body()) -> JSONResponse:
    pass


@router.delete("/")
async def delete_document(db: str, col: str, query: dict[str, Any] = Body()) -> JSONResponse:
    pass
