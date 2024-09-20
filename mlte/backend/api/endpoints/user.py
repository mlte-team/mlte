"""
mlte/backend/api/endpoints/user.py

User CRUD endpoint. Note that all endpoints return a BasicUser instead of a User,
which automatically removes the hashed password from the model returned.
"""
from __future__ import annotations

from typing import List, Union

from fastapi import APIRouter, HTTPException

import mlte.backend.api.codes as codes
import mlte.store.error as errors
from mlte.backend.api.auth import authorization
from mlte.backend.api.auth.authorization import AuthorizedUser
from mlte.backend.api.error_handlers import raise_http_internal_error
from mlte.backend.api.models.artifact_model import USER_ME_ID
from mlte.backend.core import state_stores
from mlte.store.user.policy import Policy
from mlte.user.model import (
    BasicUser,
    MethodType,
    Permission,
    ResourceType,
    RoleType,
    UserWithPassword,
)

# The router exported by this submodule
router = APIRouter()


# -----------------------------------------------------------------------------
# User/me endopoints
# -----------------------------------------------------------------------------


@router.get("/me")
def read_user_me(
    current_user: AuthorizedUser,
) -> BasicUser:
    """
    Returns the currently logged in user.
    :return: The user info
    """
    parameters = locals().copy()
    parameters["username"] = USER_ME_ID
    return read_user(**parameters)


@router.get("/me/models")
def list_user_models_me(
    *,
    current_user: AuthorizedUser,
) -> List[str]:
    """
    Gets a list of models the currently logged-in user is authorized to read.
    :return: The list of model ids
    """
    parameters = locals().copy()
    parameters["username"] = USER_ME_ID
    return list_user_models(**parameters)


# -----------------------------------------------------------------------------
# User endopoints
# -----------------------------------------------------------------------------


@router.post("")
def create_user(
    *,
    user: UserWithPassword,
    current_user: AuthorizedUser,
) -> BasicUser:
    """
    Create a MLTE user.
    :param user: The user to create
    :return: The created user
    """
    if user.username == USER_ME_ID:
        raise HTTPException(
            status_code=codes.BAD_REQUEST,
            detail="'me' is reserved and can't be used as a username.",
        )

    new_user: BasicUser
    with state_stores.user_store_session() as user_store:
        try:
            # Give every new user permissions to create models.
            # Check first if the group was not manually added in the received user data.
            create_model_group = Policy.build_groups(
                ResourceType.MODEL,
                resource_id=None,
                build_edit_group=False,
                build_read_group=False,
            )[0]
            user_has_create_group = False
            for group in user.groups:
                if create_model_group.name == group.name:
                    user_has_create_group = True
                    break

            if not user_has_create_group:
                user.groups.append(create_model_group)

            # Store the user.
            new_user = user_store.user_mapper.create(user)

            # Now create permissions and groups associated to it.
            Policy.create(
                ResourceType.USER,
                new_user.username,
                user_store,
                BasicUser(**new_user.model_dump()),
            )

            stored_user = user_store.user_mapper.read(new_user.username)
            return stored_user
        except errors.ErrorAlreadyExists as e:
            raise HTTPException(
                status_code=codes.ALREADY_EXISTS, detail=f"{e} already exists."
            )
        except Exception as e:
            raise_http_internal_error(e)


@router.put("")
def edit_user(
    *,
    user: Union[UserWithPassword, BasicUser],
    current_user: AuthorizedUser,
) -> BasicUser:
    """
    Edit a MLTE user.
    :param user: The user to edit
    :return: The edited user
    """
    if user.username == USER_ME_ID:
        user.username = current_user.username

    with state_stores.user_store_session() as user_store:
        try:
            # We only want to allow admins to edit a user's groups.
            if current_user.role != RoleType.ADMIN:
                # If not admin, keep current groups and ignore the new ones, if any.
                current_groups = user_store.user_mapper.read(
                    user.username
                ).groups
                user.groups = current_groups

            # Edit the user.
            return user_store.user_mapper.edit(user)
        except errors.ErrorNotFound as e:
            raise HTTPException(
                status_code=codes.NOT_FOUND, detail=f"{e} not found."
            )
        except Exception as e:
            raise_http_internal_error(e)


@router.get("/{username}")
def read_user(
    *,
    username: str,
    current_user: AuthorizedUser,
) -> BasicUser:
    """
    Read a MLTE user.
    :param username: The username
    :return: The read user
    """
    if username == USER_ME_ID:
        return current_user

    with state_stores.user_store_session() as user_store:
        try:
            return user_store.user_mapper.read(username)
        except errors.ErrorNotFound as e:
            raise HTTPException(
                status_code=codes.NOT_FOUND, detail=f"{e} not found."
            )
        except Exception as e:
            raise_http_internal_error(e)


@router.get("")
def list_users(
    current_user: AuthorizedUser,
) -> List[str]:
    """
    List MLTE users.
    :return: A collection of usernames
    """
    with state_stores.user_store_session() as user_store:
        try:
            return user_store.user_mapper.list()
        except Exception as e:
            raise_http_internal_error(e)


@router.get("s/details")
def list_users_details(
    current_user: AuthorizedUser,
) -> List[BasicUser]:
    """
    List MLTE users, with details for each user.
    :return: A collection of users with their details.
    """
    with state_stores.user_store_session() as user_store:
        try:
            detailed_users = []
            usernames = user_store.user_mapper.list()
            for username in usernames:
                user_details = BasicUser(
                    **user_store.user_mapper.read(username).model_dump()
                )
                detailed_users.append(user_details)
            return detailed_users
        except Exception as e:
            raise_http_internal_error(e)


@router.delete("/{username}")
def delete_user(
    *,
    username: str,
    current_user: AuthorizedUser,
) -> BasicUser:
    """
    Delete a MLTE user.
    :param username: The username
    :return: The deleted user
    """
    with state_stores.user_store_session() as user_store:
        try:
            deleted_user = user_store.user_mapper.delete(username)

            # Now delete related permissions and groups.
            Policy.remove(ResourceType.USER, username, user_store)

            return deleted_user
        except errors.ErrorNotFound as e:
            raise HTTPException(
                status_code=codes.NOT_FOUND, detail=f"{e} not found."
            )
        except Exception as e:
            raise_http_internal_error(e)


@router.get("/{username}/models")
def list_user_models(
    *,
    username: str,
    current_user: AuthorizedUser,
) -> List[str]:
    """
    Gets a list of models a user is authorized to read.
    :param username: The username
    :return: The list of model ids
    """
    if username == USER_ME_ID:
        username = current_user.username

    with state_stores.artifact_store_session() as artifact_store:
        with state_stores.user_store_session() as user_store:
            try:
                # Get all models, and filter out only the ones the user has read permissions for.
                user_models: List[str] = []
                user = BasicUser(
                    **user_store.user_mapper.read(username).model_dump()
                )
                all_models = artifact_store.list_models()
                for model_id in all_models:
                    permission = Permission(
                        resource_type=ResourceType.MODEL,
                        resource_id=model_id,
                        method=MethodType.GET,
                    )
                    if authorization.is_authorized(user, permission):
                        user_models.append(model_id)
                return user_models

            except errors.ErrorNotFound as e:
                raise HTTPException(
                    status_code=codes.NOT_FOUND, detail=f"{e} not found."
                )
            except Exception as e:
                raise_http_internal_error(e)
