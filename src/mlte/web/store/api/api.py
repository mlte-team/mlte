"""
store/api/api.py

Top-level API functionality.
"""

from fastapi import APIRouter

from mlte.web.store.api.endpoints import health, metadata, negotiation_card

# The base API router across all endpoints
api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(metadata.router, tags=["metadata"])
api_router.include_router(
    negotiation_card.router, prefix="/negotiation-card", tags=["artifact"]
)
