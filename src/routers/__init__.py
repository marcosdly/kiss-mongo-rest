from enum import Enum
from fastapi import APIRouter

class Routers(Enum):
    """Enumeration/Dataclass for all the routers."""
    DOCUMENT = __import__(".document").router

API = APIRouter(prefix="/api", routes=[r.value for r in Routers])