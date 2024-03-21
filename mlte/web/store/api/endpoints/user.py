"""
mlte/web/store/api/endpoints/user.py

Security setup and token endpoints.
"""

from typing import Annotated

from fastapi import APIRouter, Depends

from mlte.user.model import User
from mlte.web.store.api.auth.authorization import get_user_from_token

# The router exported by this submodule
router = APIRouter()


@router.get("/users/me")
def read_users_me(
    current_user: Annotated[User, Depends(get_user_from_token)]
) -> User:
    return current_user
