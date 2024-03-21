"""
mlte/web/store/api/auth/authorization.py

Setup of OAuth based authorization checks.
"""

from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from mlte.user.model import User
from mlte.web.store.api import codes
from mlte.web.store.api.auth import fake_db as db
from mlte.web.store.api.auth import jwt
from mlte.web.store.api.auth.http_auth_exception import HTTPAuthException
from mlte.web.store.api.endpoints.token import TOKEN_ENDPOINT_URL

# TODO: Add support for more than password grant type.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=TOKEN_ENDPOINT_URL)
"""Securty scheme to be used."""


async def get_user_from_token(
    token: Annotated[str, Depends(oauth2_scheme)]
) -> User:
    """
    Given a token, gets the authenticated user and checks if it has access to resources.

    :param token: A JWT bearer access token with user information.
    :return: A User data structure, with a User that has access to the resources.
    """
    try:
        username = jwt.decode_user_token(token)
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
