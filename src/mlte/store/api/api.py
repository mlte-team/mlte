"""
mlte/store/api/api.py

Top-level API functionality.
"""

from fastapi import APIRouter

from mlte.store.api.endpoints import health, metadata, value

# The base API router across all endpoints
api_router = APIRouter()
api_router.include_router(health.router, prefix="/healthz", tags=["health"])
api_router.include_router(
    metadata.router, prefix="/metadata", tags=["metadata"]
)
api_router.include_router(value.router, prefix="/value", tags=["value"])
