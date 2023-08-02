"""
mlte/store/api/endpoints/health.py

Generic health check endpoint.
"""

from fastapi import APIRouter

# The router exported by this submodule
router = APIRouter()


@router.get("/healthz")
def healthcheck():
    """Perform a health check on artifact store server."""
    return {"status": "healthy"}
