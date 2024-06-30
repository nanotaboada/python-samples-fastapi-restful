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

app = FastAPI(lifespan=lifespan)
app.include_router(player_route.api_router)
