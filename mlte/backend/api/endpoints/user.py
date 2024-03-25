"""
mlte/backend/api/endpoints/user.py

Security setup and token endpoints.
"""

from fastapi import APIRouter, Depends
from typing_extensions import Annotated

from mlte.backend.api.auth.authorization import get_user_from_token
from mlte.user.model import BasicUser

# The router exported by this submodule
router = APIRouter()


@router.get("/users/me")
def read_users_me(
    current_user: Annotated[BasicUser, Depends(get_user_from_token)]
) -> BasicUser:
    return current_user