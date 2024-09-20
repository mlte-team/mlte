"""
mlte/backend/api/endpoints/context.py

Endpoints for artifact organization context.
"""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, HTTPException

import mlte.backend.api.codes as codes
import mlte.store.error as errors
from mlte.backend.api.auth.authorization import AuthorizedUser
from mlte.backend.api.error_handlers import raise_http_internal_error
from mlte.backend.core import state_stores
from mlte.context.model import Model, ModelCreate, Version, VersionCreate
from mlte.store.user.policy import Policy
from mlte.user.model import ResourceType

# The router exported by this submodule
router = APIRouter()


@router.post("")
def create_model(
    *,
    model: ModelCreate,
    current_user: AuthorizedUser,
) -> Model:
    """
    Create a MLTE model.
    :param model: The model create model
    :return: The created model
    """
    # First create model.
    created_model: Model
    with state_stores.artifact_store_session() as handle:
        try:
            created_model = handle.create_model(model)
        except errors.ErrorNotFound as e:
            raise HTTPException(
                status_code=codes.NOT_FOUND, detail=f"{e} not found."
            )
        except errors.ErrorAlreadyExists as e:
            raise HTTPException(
                status_code=codes.ALREADY_EXISTS, detail=f"{e} already exists."
            )
        except Exception as ex:
            raise_http_internal_error(ex)

    with state_stores.user_store_session() as handle:
        # Now create permissions and groups associated to it.
        try:
            Policy.create(
                ResourceType.MODEL,
                created_model.identifier,
                handle,
                current_user,
            )
        except Exception as ex:
            raise_http_internal_error(ex)

    return created_model


@router.get("/{model_id}")
def read_model(
    *,
    model_id: str,
    current_user: AuthorizedUser,
) -> Model:
    """
    Read a MLTE model.
    :param model_id: The model identifier
    :return: The read model
    """
    try:
        with state_stores.artifact_store_session() as handle:
            model = handle.read_model(model_id)

        return model
    except errors.ErrorNotFound as e:
        raise HTTPException(
            status_code=codes.NOT_FOUND, detail=f"{e} not found."
        )
    except Exception as ex:
        raise_http_internal_error(ex)


@router.get("")
def list_models(
    current_user: AuthorizedUser,
) -> List[str]:
    """
    List MLTE models.
    :return: A collection of model identifiers
    """
    with state_stores.artifact_store_session() as handle:
        try:
            return handle.list_models()
        except errors.ErrorNotFound as e:
            raise HTTPException(
                status_code=codes.NOT_FOUND, detail=f"{e} not found."
            )
        except Exception as ex:
            raise_http_internal_error(ex)


@router.delete("/{model_id}")
def delete_model(
    *,
    model_id: str,
    current_user: AuthorizedUser,
) -> Model:
    """
    Delete a MLTE model.
    :param model_id: The model identifier
    :return: The deleted model
    """
    deleted_model: Model
    with state_stores.artifact_store_session() as handle:
        try:
            deleted_model = handle.delete_model(model_id)
        except errors.ErrorNotFound as e:
            raise HTTPException(
                status_code=codes.NOT_FOUND, detail=f"{e} not found."
            )
        except Exception:
            raise HTTPException(
                status_code=codes.INTERNAL_ERROR,
                detail="Internal server error.",
            )

    with state_stores.user_store_session() as handle:
        # Now delete related permissions and groups.
        try:
            Policy.remove(ResourceType.MODEL, model_id, handle)
        except Exception as ex:
            raise_http_internal_error(ex)

    return deleted_model


@router.post("/{model_id}/version")
def create_version(
    *,
    model_id: str,
    version: VersionCreate,
    current_user: AuthorizedUser,
) -> Version:
    """
    Create a MLTE version.
    :param model_id: The model identifier
    :param version: The version create model
    :return: The created version
    """
    with state_stores.artifact_store_session() as handle:
        try:
            return handle.create_version(model_id, version)
        except errors.ErrorNotFound as e:
            raise HTTPException(
                status_code=codes.NOT_FOUND, detail=f"{e} not found."
            )
        except errors.ErrorAlreadyExists as e:
            raise HTTPException(
                status_code=codes.ALREADY_EXISTS, detail=f"{e} already exists."
            )
        except Exception as ex:
            raise_http_internal_error(ex)


@router.get("/{model_id}/version/{version_id}")
def read_version(
    *,
    model_id: str,
    version_id,
    current_user: AuthorizedUser,
) -> Version:
    """
    Read a MLTE version.
    :param model_id: The model identifier
    :param version_id: The version identifier
    :return: The read version
    """
    with state_stores.artifact_store_session() as handle:
        try:
            return handle.read_version(model_id, version_id)
        except errors.ErrorNotFound as e:
            raise HTTPException(
                status_code=codes.NOT_FOUND, detail=f"{e} not found."
            )
        except Exception as ex:
            raise_http_internal_error(ex)


@router.get("/{model_id}/version")
def list_versions(
    model_id: str,
    current_user: AuthorizedUser,
) -> List[str]:
    """
    List MLTE versions for the provided model.
    :param model_id: The model identifier
    :return: A collection of version identifiers
    """
    with state_stores.artifact_store_session() as handle:
        try:
            return handle.list_versions(model_id)
        except errors.ErrorNotFound as e:
            raise HTTPException(
                status_code=codes.NOT_FOUND, detail=f"{e} not found."
            )
        except Exception as ex:
            raise_http_internal_error(ex)


@router.delete("/{model_id}/version/{version_id}")
def delete_version(
    *,
    model_id: str,
    version_id,
    current_user: AuthorizedUser,
) -> Version:
    """
    Delete a MLTE version.
    :param model_id: The model identifier
    :param version_id: The version identifier
    :return: The deleted version
    """
    with state_stores.artifact_store_session() as handle:
        try:
            return handle.delete_version(model_id, version_id)
        except errors.ErrorNotFound as e:
            raise HTTPException(
                status_code=codes.NOT_FOUND, detail=f"{e} not found."
            )
        except Exception as ex:
            raise_http_internal_error(ex)
