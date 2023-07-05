from fastapi import FastAPI
from src.routers import API
from hypercorn.config import Config
from hypercorn.asyncio import serve
from src.io_utils import ConfigFiles
import asyncio


if __name__ == "__main__":
    app = FastAPI()
    app.include_router(API)
    asgi_config: Config = Config().from_toml(ConfigFiles.HYPERCORN)
    # FastAPI doesn't use Hypercorn's specific types, but works regardless.
    asyncio.run(serve(app, asgi_config))  # type: ignore
