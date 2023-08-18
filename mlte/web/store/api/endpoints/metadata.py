"""
mlte/web/store/api/endpoints/metadata.py

Endpoints for artifact organization.
"""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, HTTPException

import mlte.store.error as errors
import mlte.web.store.api.codes as codes
from mlte.context.model import (
    Model,
    ModelCreate,
    Namespace,
    NamespaceCreate,
    Version,
    VersionCreate,
)
from mlte.web.store.api import dependencies

# The router exported by this submodule
router = APIRouter()


@router.post("/namespace")
def create_namespace(namespace: NamespaceCreate) -> Namespace:
    """
    Create a MLTE namespace.
    :param namespace: The namespace create model
    :return: The created namespace
    """
    with dependencies.session() as handle:
        try:
            return handle.create_namespace(namespace)
        except errors.ErrorAlreadyExists as e:
            raise HTTPException(
                status_code=codes.ALREADY_EXISTS, detail=f"{e} already exists."
            )
        except Exception:
            raise HTTPException(
                status_code=codes.INTERNAL_ERROR,
                detail="Internal server error.",
            )


@router.get("/namespace/{namespace_id}")
def read_namespace(*, namespace_id: str) -> Namespace:
    """
    Read a MLTE namespace.
    :param namespace_id: The namespace identifier
    :return: A collection of the models in the namespace
    """
    with dependencies.session() as handle:
        try:
            return handle.read_namespace(namespace_id)
        except errors.ErrorNotFound as e:
            raise HTTPException(
                status_code=codes.NOT_FOUND, detail=f"{e} not found."
            )
        except Exception:
            raise HTTPException(
                status_code=codes.INTERNAL_ERROR,
                detail="Internal server error.",
            )


@router.get("/namespace")
def list_namespaces() -> List[str]:
    """
    List MLTE namespaces.
    :return: A collection of namespace identifiers
    """
    with dependencies.session() as handle:
        try:
            return handle.list_namespaces()
        except errors.ErrorNotFound as e:
            raise HTTPException(
                status_code=codes.NOT_FOUND, detail=f"{e} not found."
            )
        except Exception:
            raise HTTPException(
                status_code=codes.INTERNAL_ERROR,
                detail="Internal server error.",
            )


@router.delete("/namespace/{namespace_id}")
def delete_namespace(*, namespace_id: str) -> Namespace:
    """
    Delete a MLTE namespace.
    :param namespace_id: The namespace identifier
    """
    with dependencies.session() as handle:
        try:
            return handle.delete_namespace(namespace_id)
        except errors.ErrorNotFound as e:
            raise HTTPException(
                status_code=codes.NOT_FOUND, detail=f"{e} not found."
            )
        except Exception:
            raise HTTPException(
                status_code=codes.INTERNAL_ERROR,
                detail="Internal server error.",
            )


@router.post("/namespace/{namespace_id}/model")
def create_model(*, namespace_id: str, model: ModelCreate) -> Model:
    """
    Create a MLTE model.
    :param namespace_id: The namespace identifier
    :param model: The model create model
    :return: The created model
    """
    with dependencies.session() as handle:
        try:
            return handle.create_model(namespace_id, model)
        except errors.ErrorNotFound as e:
            raise HTTPException(
                status_code=codes.NOT_FOUND, detail=f"{e} not found."
            )
        except errors.ErrorAlreadyExists as e:
            raise HTTPException(
                status_code=codes.ALREADY_EXISTS, detail=f"{e} already exists."
            )
        except Exception:
            raise HTTPException(
                status_code=codes.INTERNAL_ERROR,
                detail="Internal server error.",
            )


@router.get("/namespace/{namespace_id}/model/{model_id}")
def read_model(*, namespace_id: str, model_id: str) -> Model:
    """
    Read a MLTE model.
    :param namespace_id: The namespace identifier
    :param model_id: The model identifier
    :return: The read model
    """
    with dependencies.session() as handle:
        try:
            return handle.read_model(namespace_id, model_id)
        except errors.ErrorNotFound as e:
            raise HTTPException(
                status_code=codes.NOT_FOUND, detail=f"{e} not found."
            )
        except Exception:
            raise HTTPException(
                status_code=codes.INTERNAL_ERROR,
                detail="Internal server error.",
            )


@router.get("/namespace/{namespace_id}/model")
def list_models(namespace_id: str) -> List[str]:
    """
    List MLTE models in the provided namespace.
    :param namespace_id: The namespace identifier
    :return: A collection of model identifiers
    """
    with dependencies.session() as handle:
        try:
            return handle.list_models(namespace_id)
        except errors.ErrorNotFound as e:
            raise HTTPException(
                status_code=codes.NOT_FOUND, detail=f"{e} not found."
            )
        except Exception:
            raise HTTPException(
                status_code=codes.INTERNAL_ERROR,
                detail="Internal server error.",
            )


@router.delete("/namespace/{namespace_id}/model/{model_id}")
def delete_model(*, namespace_id: str, model_id: str) -> Model:
    """
    Delete a MLTE model.
    :param namespace_id: The namespace identifier
    :param model_id: The model identifier
    :return: The deleted model
    """
    with dependencies.session() as handle:
        try:
            return handle.delete_model(namespace_id, model_id)
        except errors.ErrorNotFound as e:
            raise HTTPException(
                status_code=codes.NOT_FOUND, detail=f"{e} not found."
            )
        except Exception:
            raise HTTPException(
                status_code=codes.INTERNAL_ERROR,
                detail="Internal server error.",
            )


@router.post("/namespace/{namespace_id}/model/{model_id}/version")
def create_version(
    *, namespace_id: str, model_id: str, version: VersionCreate
) -> Version:
    """
    Create a MLTE version.
    :param namespace_id: The namespace identifier
    :param model_id: The model identifier
    :param version: The version create model
    :return: The created version
    """
    with dependencies.session() as handle:
        try:
            return handle.create_version(namespace_id, model_id, version)
        except errors.ErrorNotFound as e:
            raise HTTPException(
                status_code=codes.NOT_FOUND, detail=f"{e} not found."
            )
        except errors.ErrorAlreadyExists as e:
            raise HTTPException(
                status_code=codes.ALREADY_EXISTS, detail=f"{e} already exists."
            )
        except Exception:
            raise HTTPException(
                status_code=codes.INTERNAL_ERROR,
                detail="Internal server error.",
            )


@router.get("/namespace/{namespace_id}/model/{model_id}/version/{version_id}")
def read_version(*, namespace_id: str, model_id: str, version_id) -> Version:
    """
    Read a MLTE version.
    :param namespace_id: The namespace identifier
    :param model_id: The model identifier
    :param version_id: The version identifier
    :return: The read version
    """
    with dependencies.session() as handle:
        try:
            return handle.read_version(namespace_id, model_id, version_id)
        except errors.ErrorNotFound as e:
            raise HTTPException(
                status_code=codes.NOT_FOUND, detail=f"{e} not found."
            )
        except Exception:
            raise HTTPException(
                status_code=codes.INTERNAL_ERROR,
                detail="Internal server error.",
            )


@router.get("/namespace/{namespace_id}/model/{model_id}/version")
def list_versions(namespace_id: str, model_id: str) -> List[str]:
    """
    List MLTE versions for the provided namespace and model.
    :param namespace_id: The namespace identifier
    :param model_id: The model identifier
    :return: A collection of version identifiers
    """
    with dependencies.session() as handle:
        try:
            return handle.list_versions(namespace_id, model_id)
        except errors.ErrorNotFound as e:
            raise HTTPException(
                status_code=codes.NOT_FOUND, detail=f"{e} not found."
            )
        except Exception:
            raise HTTPException(
                status_code=codes.INTERNAL_ERROR,
                detail="Internal server error.",
            )


@router.delete(
    "/namespace/{namespace_id}/model/{model_id}/version/{version_id}"
)
def delete_version(*, namespace_id: str, model_id: str, version_id) -> Version:
    """
    Delete a MLTE version.
    :param namespace_id: The namespace identifier
    :param model_id: The model identifier
    :param version_id: The version identifier
    :return: The deleted version
    """
    with dependencies.session() as handle:
        try:
            return handle.delete_version(namespace_id, model_id, version_id)
        except errors.ErrorNotFound as e:
            raise HTTPException(
                status_code=codes.NOT_FOUND, detail=f"{e} not found."
            )
        except Exception:
            raise HTTPException(
                status_code=codes.INTERNAL_ERROR,
                detail="Internal server error.",
            )
