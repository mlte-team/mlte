"""
mlte/backend/api/auth/authorization.py

Setup of OAuth based authorization checks.
"""

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from typing_extensions import Annotated

from mlte.backend.api import codes, dependencies
from mlte.backend.api.auth import jwt
from mlte.backend.api.auth.http_auth_exception import HTTPAuthException
from mlte.backend.api.endpoints.token import TOKEN_ENDPOINT_URL
from mlte.user.model import BasicUser

# TODO: Add support for more than password grant type.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=TOKEN_ENDPOINT_URL)
"""Securty scheme to be used."""


async def get_user_from_token(
    token: Annotated[str, Depends(oauth2_scheme)]
) -> BasicUser:
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
    user = None
    with dependencies.user_store_session() as handle:
        user = handle.read_user(username)
    if user is None:
        raise HTTPAuthException(
            detail="Could not validate credentials", error="invalid_token"
        )
    if user.disabled:
        raise HTTPException(
            status_code=codes.FORBIDDEN, detail="User is inactive"
        )

    # Convert to simple user version to avoid including hashed password.
    basic_user = BasicUser(
        username=user.username, email=user.email, disabled=user.disabled
    )
    return basic_user
