"""
store/api/api.py

Top-level API functionality.
"""

from fastapi import APIRouter

from mlte.web.store.api.endpoints import artifact, health, metadata

# The common URL prefix for all artifact routes
_ARTIFACT_PREFIX = (
    "/namespace/{namespace_id}/model/{model_id}/version/{version_id}"
)

# The base API router across all endpoints
api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(metadata.router, tags=["metadata"])
api_router.include_router(
    artifact.router,
    prefix=f"{_ARTIFACT_PREFIX}/artifact",
    tags=["artifact"],
)
