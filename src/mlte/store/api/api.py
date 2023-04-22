"""
store/api/api.py

Top-level API functionality.
"""

from fastapi import APIRouter

from mlte.store.api.endpoints import health, metadata, result

# The base API router across all endpoints
api_router = APIRouter()
api_router.include_router(health.router, prefix="/healthz", tags=["health"])
api_router.include_router(
    metadata.router, prefix="/metadata", tags=["metadata"]
)
api_router.include_router(result.router, prefix="/result", tags=["result"])
