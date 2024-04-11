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
from mlte.backend.api import dependencies
from mlte.backend.api.auth.authorization import AuthorizedUser
from mlte.user.model import BasicUser, UserCreate

# The router exported by this submodule
router = APIRouter()


@router.get("/user/me")
def read_users_me(
    current_user: AuthorizedUser,
) -> BasicUser:
    return current_user


@router.post("/user")
def create_user(
    *,
    user: UserCreate,
    current_user: AuthorizedUser,
) -> BasicUser:
    """
    Create a MLTE user.
    :param user: The user to create
    :return: The created user
    """
    with dependencies.user_store_session() as user_store:
        try:
            return user_store.create_user(user)
        except errors.ErrorAlreadyExists as e:
            raise HTTPException(
                status_code=codes.ALREADY_EXISTS, detail=f"{e} already exists."
            )
        except Exception:
            raise HTTPException(
                status_code=codes.INTERNAL_ERROR,
                detail="Internal server error.",
            )


@router.put("/user")
def edit_user(
    *,
    user: Union[UserCreate, BasicUser],
    current_user: AuthorizedUser,
) -> BasicUser:
    """
    Edit a MLTE user.
    :param user: The user to edit
    :return: The edited user
    """
    with dependencies.user_store_session() as user_store:
        try:
            return user_store.edit_user(user)
        except errors.ErrorNotFound as e:
            raise HTTPException(
                status_code=codes.NOT_FOUND, detail=f"{e} not found."
            )
        except Exception:
            raise HTTPException(
                status_code=codes.INTERNAL_ERROR,
                detail="Internal server error.",
            )


@router.get("/user/{username}")
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
    with dependencies.user_store_session() as user_store:
        try:
            return user_store.read_user(username)
        except errors.ErrorNotFound as e:
            raise HTTPException(
                status_code=codes.NOT_FOUND, detail=f"{e} not found."
            )
        except Exception:
            raise HTTPException(
                status_code=codes.INTERNAL_ERROR,
                detail="Internal server error.",
            )


@router.get("/user")
def list_users(
    current_user: AuthorizedUser,
) -> List[str]:
    """
    List MLTE users.
    :return: A collection of usernames
    """
    with dependencies.user_store_session() as user_store:
        try:
            return user_store.list_users()
        except Exception:
            raise HTTPException(
                status_code=codes.INTERNAL_ERROR,
                detail="Internal server error.",
            )


@router.get("/users/details")
def list_users_details(
    current_user: AuthorizedUser,
) -> List[BasicUser]:
    """
    List MLTE users, with details for each user.
    :return: A collection of users with their details.
    """
    with dependencies.user_store_session() as user_store:
        try:
            detailed_users = []
            usernames = user_store.list_users()
            for username in usernames:
                user_details = BasicUser(
                    **user_store.read_user(username).model_dump()
                )
                detailed_users.append(user_details)
            return detailed_users
        except Exception:
            raise HTTPException(
                status_code=codes.INTERNAL_ERROR,
                detail="Internal server error.",
            )


@router.delete("/user/{username}")
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
    with dependencies.user_store_session() as user_store:
        try:
            return user_store.delete_user(username)
        except errors.ErrorNotFound as e:
            raise HTTPException(
                status_code=codes.NOT_FOUND, detail=f"{e} not found."
            )
        except Exception:
            raise HTTPException(
                status_code=codes.INTERNAL_ERROR,
                detail="Internal server error.",
            )
