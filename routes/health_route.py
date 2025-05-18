# ------------------------------------------------------------------------------
# Route
# ------------------------------------------------------------------------------

from fastapi import APIRouter


api_router = APIRouter()

@api_router.get("/health", tags=["Health"])
async def health_check():
    """
    Simple health check endpoint. Returns a JSON response with a single key "status" and value "ok".
    """
    return {"status": "ok"}
