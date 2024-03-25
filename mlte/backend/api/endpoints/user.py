"""
mlte/backend/api/endpoints/user.py

Security setup and token endpoints.
"""

from fastapi import APIRouter

from mlte.backend.api.auth.authorization import AuthorizedUser
from mlte.user.model import BasicUser

# The router exported by this submodule
router = APIRouter()


@router.get("/users/me")
def read_users_me(
    current_user: AuthorizedUser,
) -> BasicUser:
    return current_user
