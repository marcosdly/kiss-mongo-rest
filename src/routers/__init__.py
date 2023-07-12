from enum import Enum
from fastapi import FastAPI
from src.db import CLIENT
from src.routers.document import router

class Routers(Enum):
    """Enumeration/Dataclass for all the routers."""
    DOCUMENT = router

app = FastAPI(root_path="/api")

for r in Routers: app.include_router(r.value)

@app.on_event("shutdown")
def app_shutdown() -> None:
    CLIENT.close()