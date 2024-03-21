"""
mlte/web/store/api/endpoints/token.py

Token endpoint.
"""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from typing_extensions import Annotated

from mlte.model.base_model import BaseModel
from mlte.web.store.api import codes
from mlte.web.store.api.auth import authentication
from mlte.web.store.api.auth import fake_db as db
from mlte.web.store.api.auth import jwt
from mlte.web.store.api.auth.http_auth_exception import HTTPAuthException

GRANT_TYPE_PASSWORD = "password"
"""Grant type name used in token requests."""

BEARER_TOKEN_TYPE = "bearer"
"""Bearer token type."""

TOKEN_ENDPOINT_URL = "token"
"""The relative URL of the endpoint."""

# The router exported by this submodule
router = APIRouter()


class TokenResponse(BaseModel):
    """Model for the token response to return."""

    access_token: str
    """The actual encoded token."""

    token_type: str
    """The token type."""

    expires_in: int
    """Lifetime in seconds of the token."""


def create_token_response(access_token: jwt.Token) -> TokenResponse:
    """Creates a Bearer Token response with the given access token."""
    return TokenResponse(
        access_token=access_token.encoded_token,
        token_type=BEARER_TOKEN_TYPE,
        expires_in=access_token.expires_in,
    )


# TODO: Add support for other grant types.
@router.post(f"/{TOKEN_ENDPOINT_URL}")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> TokenResponse:
    """
    OAuth 2 Access Server Token Endpoint. Assumes use of JWT Bearer tokens, with username being the embedded information.
    Currently only supports RO Credentials ("password") grant type.
    """
    user = None
    if form_data.grant_type == GRANT_TYPE_PASSWORD:
        # Validate user and password from db.
        is_valid_user = authentication.authenticate_user(
            form_data.username, form_data.password
        )
        if not is_valid_user:
            raise HTTPAuthException(detail="Incorrect username or password")
        user = db.get_user(form_data.username)
    else:
        raise HTTPException(
            codes.INTERNAL_ERROR,
            detail=f"Unsupported grant type: {form_data.grant_type}",
        )

    # Check if we were able to get a user's info properly.
    if user is None:
        raise HTTPAuthException(detail="Could not load user details")

    # Create and return token using username as data.
    access_token = jwt.create_user_token(user.username)
    return create_token_response(access_token)
