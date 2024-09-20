"""
mlte/backend/api/auth/authorization.py

Setup of OAuth based authorization checks.
"""

from json import JSONDecodeError

from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from typing_extensions import Annotated

from mlte.backend.api import codes
from mlte.backend.api.auth import jwt
from mlte.backend.api.auth.http_auth_exception import HTTPAuthException
from mlte.backend.api.endpoints.token import TOKEN_ENDPOINT_URL
from mlte.backend.api.models.artifact_model import USER_ME_ID
from mlte.backend.core import state_stores
from mlte.backend.core.config import settings
from mlte.backend.core.state import state
from mlte.store.user.store import UserStore
from mlte.user.model import (
    BasicUser,
    MethodType,
    Permission,
    ResourceType,
    RoleType,
)

# -----------------------------------------------------------------------------
# Helper functions.
# -----------------------------------------------------------------------------


async def get_current_resource(request: Request) -> Permission:
    """Gets a resource permission description for the current resource, method and model."""
    # Parse URL for resource type.
    url = request.url.path
    resource_url = url.replace(settings.API_PREFIX, "")
    resource_type = ResourceType.get_type_from_url(resource_url)
    if resource_type is None:
        raise RuntimeError(
            f"Could not parse resource type from URL: {resource_url}"
        )

    # Parse URL and body for resource id, if any.
    resource_id = None
    if resource_type is not None:
        url_parts = resource_url.split("/")
        if len(url_parts) > 2:
            resource_id = url_parts[2]
        else:
            try:
                # If the URL didn't have an id, try to get it from a JSON body.
                data = await request.json()
                id_key = UserStore.ID_MAP[resource_type]
                if id_key in data:
                    resource_id = data[id_key]
            except JSONDecodeError:
                # This request had no JSON body, thus no id.
                pass

    # Get method.
    method = MethodType[request.method]

    # NOTE: if this is a search, treat it as if it was a GET method.
    # This is used so that read permissions will be applied to searches, while allowing
    # it to send complex queries through its body.
    if url.endswith("/search"):
        method = MethodType.GET

    # Build and return the resource permission description
    resource = Permission(
        resource_type=resource_type, resource_id=resource_id, method=method
    )
    # print(f"Resource: {resource}")
    return resource


def get_username_from_token(token: str, key: str) -> str:
    """Obtains a user from an encoded token, if the token is valid."""
    # Decode token, checking for format and expiration.
    decoded_token = jwt.decode_user_token(token, key)
    return decoded_token.username


def is_authorized(current_user: BasicUser, resource: Permission) -> bool:
    """Checks if the current user is authorized to access the current resource."""
    # print(
    #    f"Checking authorization for user {current_user.username} to resource {resource}"
    # )

    if current_user.role == RoleType.ADMIN:
        # If having admin role, always get access.
        # print("User is admin")
        return True
    else:
        # Handle special resource cases.
        if (
            resource.resource_type == ResourceType.USER
            and resource.resource_id == USER_ME_ID
        ):
            resource.resource_id = current_user.username

        # Check to find if the current user has permissions through any of its groups.
        # print(current_user.groups)
        print(f"Resource: {resource}")
        for group in current_user.groups:
            # print(group)
            for permission in group.permissions:
                if permission.grants_access(resource):
                    # print("Permission for this model found")
                    return True

    # If none of the above are true, deny access.
    # print("Permission not granted.")
    return False


# -----------------------------------------------------------------------------
# Dep injection to get current authorized user.
# -----------------------------------------------------------------------------


# TODO: Add support for more than password grant type.
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_PREFIX}{TOKEN_ENDPOINT_URL}"
)
"""Securty scheme to be used."""


async def get_authorized_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    resource: Annotated[Permission, Depends(get_current_resource)],
) -> BasicUser:
    """
    Given a token, gets the authenticated user and checks if it has access to resources.

    :param token: A JWT bearer access token with user information.
    :param resource: A ResourceAction object indicating the resource and actions we are checking for.
    :return: A User data structure, with a User that has access to the resources.
    """
    # Validate token and get username.
    # print(f"Get authorized user token {token}, resource {resource}")
    try:
        username = get_username_from_token(token, state.token_key)
    except Exception as ex:
        raise HTTPAuthException(
            error="invalid_token",
            error_decription=f"Could not decode token: {ex}",
        )

    # Check if user in token exists.
    user = None
    with state_stores.user_store_session() as user_store:
        user = user_store.user_mapper.read(username)
    if user is None:
        raise HTTPAuthException(
            error="invalid_token",
            error_decription="Username in token was not found.",
        )

    # Check if user is enabled to be used.
    if user.disabled:
        raise HTTPException(
            status_code=codes.FORBIDDEN, detail="User is inactive"
        )

    # Check proper authorizations.
    if not is_authorized(user, resource):
        raise HTTPException(
            status_code=codes.FORBIDDEN,
            detail="User is not authorized to access this resource.",
        )

    # Convert to simple user version to avoid including hashed password.
    basic_user = BasicUser(**user.model_dump())
    return basic_user


AuthorizedUser = Annotated[BasicUser, Depends(get_authorized_user)]
"""Type alias to simplify use of get user."""
