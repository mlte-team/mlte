"""
mlte/backend/api/endpoints/token.py

Token endpoint.
"""

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing_extensions import Annotated

from mlte.backend.api.auth import authentication, jwt
from mlte.backend.api.auth.http_auth_exception import HTTPTokenException
from mlte.backend.core import state_stores
from mlte.backend.core.state import state
from mlte.model.base_model import BaseModel
from mlte.store.user import policy

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


def create_token_response(access_token: jwt.EncodedToken) -> TokenResponse:
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
        with state_stores.user_store_session() as user_store_session:
            is_valid_user = authentication.authenticate_user(
                form_data.username, form_data.password, user_store_session
            )
            if not is_valid_user:
                raise HTTPTokenException(
                    error="invalid_grant",
                    error_decription="Incorrect username or password.",
                )
            user = user_store_session.user_mapper.read(form_data.username)
    else:
        raise HTTPTokenException(
            error="unsupported_grant_type",
            error_decription=f"Grant type {form_data.grant_type} is not supported.",
        )

    # Check if we were able to get a user's info properly.
    if user is None:
        raise HTTPTokenException(
            error="invalid_request",
            error_decription="Could not load user details.",
        )

    # Check if user is enabled to get tokens and access system.
    if user.disabled:
        raise HTTPTokenException(
            error="invalid_request",
            error_decription="User is inactive.",
        )

    # Create policies for models if needed.
    # TODO: this is terribly not efficient. This is checked every time anybody logins.
    with state_stores.artifact_store_session() as artifact_store:
        with state_stores.user_store_session() as user_store:
            policy.create_model_policies_if_needed(artifact_store, user_store)

    # Create and return token using username as data.
    access_token = jwt.create_user_token(user.username, state.token_key)
    return create_token_response(access_token)
