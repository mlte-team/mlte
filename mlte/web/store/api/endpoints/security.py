"""
mlte/web/store/api/endpoints/security.py

Security setup and token endpoints.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from mlte.user.model import User
from mlte.web.store.api import codes
from mlte.web.store.api.auth import authentication
from mlte.web.store.api.auth import fake_db as db
from mlte.web.store.api.auth import token
from mlte.web.store.api.auth.http_auth_exception import HTTPAuthException

# The router exported by this submodule
router = APIRouter()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
"""Securty scheme to be used by all."""


async def get_current_user(
    current_token: Annotated[str, Depends(oauth2_scheme)]
) -> User:
    try:
        username = token.decode_user_token(
            token.Token(access_token=current_token)
        )
    except Exception:
        raise HTTPAuthException(
            detail="Could not decode token properly", error="invalid_token"
        )
    user = db.get_user(username=username)
    if user is None:
        raise HTTPAuthException(
            detail="Could not validate credentials", error="invalid_token"
        )
    if user.disabled:
        raise HTTPException(
            status_code=codes.FORBIDDEN, detail="User is inactive"
        )
    return user


@router.get("/users/me")
def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    return current_user


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> token.Token:
    # Validate user and password from db.
    is_valid_user = authentication.authenticate_user(
        form_data.username, form_data.password
    )
    if not is_valid_user:
        raise HTTPAuthException(detail="Incorrect username or password")

    # Get user data to create the token.
    user = db.get_user(form_data.username)
    if user is None:
        raise HTTPAuthException(detail="Could not load user details")

    # Create and return token using username as data.
    return token.create_user_token(user.username)
