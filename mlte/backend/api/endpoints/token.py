"""
mlte/backend/api/endpoints/token.py

Token endpoint.
"""

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing_extensions import Annotated

from mlte.backend.api import dependencies
from mlte.backend.api.auth import authentication, jwt
from mlte.backend.api.auth.http_auth_exception import HTTPTokenException
from mlte.backend.core.config import settings
from mlte.model.base_model import BaseModel

GRANT_TYPE_PASSWORD = "password"
"""Grant type name used in token requests."""

BEARER_TOKEN_TYPE = "bearer"
"""Bearer token type."""

TOKEN_ENDPOINT_URL = "/token"
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


@router.post(f"{TOKEN_ENDPOINT_URL}")
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
        with dependencies.user_store_session() as user_store_session:
            is_valid_user = authentication.authenticate_user(
                form_data.username, form_data.password, user_store_session
            )
            if not is_valid_user:
                raise HTTPTokenException(
                    error="invalid_grant",
                    error_decription="Incorrect username or password",
                )
            user = user_store_session.read_user(form_data.username)
    else:
        raise HTTPTokenException(
            error="unsupported_grant_type",
            error_decription=f"Grant type {form_data.grant_type} is not supported",
        )

    # Check if we were able to get a user's info properly.
    if user is None:
        raise HTTPTokenException(
            error="invalid_request",
            error_decription="Could not load user details",
        )

    # Create and return token using username as data.
    access_token = jwt.create_user_token(user.username, settings.JWT_SECRET_KEY)
    return create_token_response(access_token)
