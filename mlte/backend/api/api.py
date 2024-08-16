"""
mlte/backend/api/api.py

Top-level API functionality.
"""

from fastapi import APIRouter

from mlte.backend.api.endpoints import (
    artifact,
    catalog_entry,
    context,
    group,
    health,
    token,
    user,
)

# The common URL prefix for all artifact routes
_ARTIFACT_PREFIX = "/model/{model_id}/version/{version_id}"

# The base API router across all endpoints
api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(context.router, tags=["context"])
api_router.include_router(token.router, tags=["token"])
api_router.include_router(user.router, tags=["user"])
api_router.include_router(group.router, tags=["group"])
api_router.include_router(catalog_entry.router, tags=["catalog_entry"])
api_router.include_router(
    artifact.router,
    prefix=f"{_ARTIFACT_PREFIX}/artifact",
    tags=["artifact"],
)
