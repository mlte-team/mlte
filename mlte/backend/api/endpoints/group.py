"""
mlte/backend/api/endpoints/group.py

Group CRUD endpoint.
"""
from __future__ import annotations

import traceback as tb
from typing import List

from fastapi import APIRouter, HTTPException

import mlte.backend.api.codes as codes
import mlte.store.error as errors
from mlte.backend.api import dependencies
from mlte.backend.api.auth.authorization import AuthorizedUser
from mlte.user.model import Group, Permission

# The router exported by this submodule
router = APIRouter()


@router.post("/group")
def create_group(
    *,
    group: Group,
    current_user: AuthorizedUser,
) -> Group:
    """
    Create a MLTE group.
    :param group: The group to create
    :return: The created group
    """
    with dependencies.user_store_session() as user_store:
        try:
            return user_store.group_mapper.create(group)
        except errors.ErrorAlreadyExists as e:
            raise HTTPException(
                status_code=codes.ALREADY_EXISTS, detail=f"{e} already exists."
            )
        except Exception as e:
            print(f"Internal server error. {e}")
            print(tb.format_exc())
            raise HTTPException(
                status_code=codes.INTERNAL_ERROR,
                detail="Internal server error.",
            )


@router.put("/group")
def edit_group(
    *,
    group: Group,
    current_user: AuthorizedUser,
) -> Group:
    """
    Edit a MLTE group.
    :param group: The group to edit
    :return: The edited group
    """
    with dependencies.user_store_session() as user_store:
        try:
            return user_store.group_mapper.edit(group)
        except errors.ErrorNotFound as e:
            raise HTTPException(
                status_code=codes.NOT_FOUND, detail=f"{e} not found."
            )
        except Exception as e:
            print(f"Internal server error. {e}")
            print(tb.format_exc())
            raise HTTPException(
                status_code=codes.INTERNAL_ERROR,
                detail="Internal server error.",
            )


@router.get("/group/{group_name}")
def read_group(
    *,
    group_name: str,
    current_user: AuthorizedUser,
) -> Group:
    """
    Read a MLTE group.
    :param group group_name: The group name
    :return: The read group
    """
    with dependencies.user_store_session() as user_store:
        try:
            return user_store.group_mapper.read(group_name)
        except errors.ErrorNotFound as e:
            raise HTTPException(
                status_code=codes.NOT_FOUND, detail=f"{e} not found."
            )
        except Exception as e:
            print(f"Internal server error. {e}")
            print(tb.format_exc())
            raise HTTPException(
                status_code=codes.INTERNAL_ERROR,
                detail="Internal server error.",
            )


@router.get("/group")
def list_groups(
    current_user: AuthorizedUser,
) -> List[str]:
    """
    List MLTE group.
    :return: A collection of group names
    """
    with dependencies.user_store_session() as user_store:
        try:
            return user_store.group_mapper.list()
        except Exception as e:
            print(f"Internal server error. {e}")
            print(tb.format_exc())
            raise HTTPException(
                status_code=codes.INTERNAL_ERROR,
                detail="Internal server error.",
            )


@router.get("/groups/details")
def list_group_details(
    current_user: AuthorizedUser,
) -> List[Group]:
    """
    List MLTE group, with details for each group.
    :return: A collection of groups with their details.
    """
    with dependencies.user_store_session() as user_store:
        try:
            return user_store.group_mapper.list_details()
        except Exception as e:
            print(f"Internal server error. {e}")
            print(tb.format_exc())
            raise HTTPException(
                status_code=codes.INTERNAL_ERROR,
                detail="Internal server error.",
            )


@router.delete("/group/{group_name}")
def delete_user(
    *,
    group_name: str,
    current_user: AuthorizedUser,
) -> Group:
    """
    Delete a MLTE group.
    :param group_name: The group name
    :return: The deleted group
    """
    with dependencies.user_store_session() as user_store:
        try:
            return user_store.group_mapper.delete(group_name)
        except errors.ErrorNotFound as e:
            raise HTTPException(
                status_code=codes.NOT_FOUND, detail=f"{e} not found."
            )
        except Exception as e:
            print(f"Internal server error. {e}")
            print(tb.format_exc())
            raise HTTPException(
                status_code=codes.INTERNAL_ERROR,
                detail="Internal server error.",
            )


@router.get("/groups/permissions")
def list_permissions(
    current_user: AuthorizedUser,
) -> List[str]:
    """
    List MLTE permissions.
    :return: A collection of permissions
    """
    with dependencies.user_store_session() as user_store:
        try:
            return user_store.permission_mapper.list()
        except Exception as e:
            print(f"Internal server error. {e}")
            print(tb.format_exc())
            raise HTTPException(
                status_code=codes.INTERNAL_ERROR,
                detail="Internal server error.",
            )


@router.get("/groups/permissions/details")
def list_permission_details(
    current_user: AuthorizedUser,
) -> List[Permission]:
    """
    List MLTE permissions, with details.
    :return: A collection of permissions, with details.
    """
    with dependencies.user_store_session() as user_store:
        try:
            return user_store.permission_mapper.list_details()
        except Exception as e:
            print(f"Internal server error. {e}")
            print(tb.format_exc())
            raise HTTPException(
                status_code=codes.INTERNAL_ERROR,
                detail="Internal server error.",
            )
