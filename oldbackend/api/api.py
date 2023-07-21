"""
store/api/api.py

Top-level API functionality.
"""

from fastapi import APIRouter

from mlte.store.api.endpoints import health, negotiation_card

# The base API router across all endpoints
api_router = APIRouter()
api_router.include_router(health.router, prefix="/healthz", tags=["health"])
api_router.include_router(
    negotiation_card.router, prefix="/negotiation-card", tags=["artifact"]
)
