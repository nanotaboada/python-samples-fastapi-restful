# ------------------------------------------------------------------------------
# Main
# ------------------------------------------------------------------------------

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from routes import player_route


@asynccontextmanager
async def lifespan(app: FastAPI):
    FastAPICache.init(InMemoryBackend())
    yield

app = FastAPI(lifespan=lifespan,
              title="python-samples-fastapi-restful",
              description="🧪 Proof of Concept for a RESTful API made with Python 3 and FastAPI",
              version="1.0.0",)

app.include_router(player_route.api_router)
