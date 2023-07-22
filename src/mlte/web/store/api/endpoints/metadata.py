"""
mlte/web/store/api/endpoints/metadata.py

Endpoints for artifact organization.
"""

from fastapi import APIRouter, HTTPException

import mlte.store.error as errors
from mlte.context.model import Model, Namespace, Version
from mlte.web.store.api import dependencies

# The router exported by this submodule
router = APIRouter()

# "Not found"
CODE_NOT_FOUND = 404

# "Conflict"
CODE_ALREADY_EXISTS = 409


@router.post("/namespace")
def create_namespace(namespace: Namespace) -> None:
    """
    Create a MLTE namespace.
    """
    with dependencies.session() as handle:
        try:
            handle.create_namespace(namespace)
        except errors.ErrorAlreadyExists as e:
            raise HTTPException(
                status_code=CODE_ALREADY_EXISTS, detail=f"{e} already exists."
            )
        except Exception:
            raise HTTPException(
                status_code=500, detail="Internal server error."
            )


@router.get("/namespace/{id}")
def read_namespace(*, id: str) -> list[Model]:
    """
    Read a MLTE namespace.
    :param id: The namespace identifier
    :return: A collection of the models in the namespace
    """
    with dependencies.session() as handle:
        try:
            models = handle.read_namespace(id)
        except errors.ErrorNotFound as e:
            raise HTTPException(
                status_code=CODE_NOT_FOUND, detail=f"{e} not found."
            )
        except Exception:
            raise HTTPException(
                status_code=500, detail="Internal server error."
            )

    return models


@router.get("/namespace")
def list_namespaces() -> list[str]:
    """
    List MLTE namespaces.
    :return: A collection of namespace identifiers
    """
    with dependencies.session() as handle:
        try:
            ids = handle.list_namespaces()
        except errors.ErrorAlreadyExists as e:
            raise HTTPException(
                status_code=CODE_ALREADY_EXISTS, detail=f"{e} already exists."
            )
        except Exception:
            raise HTTPException(
                status_code=500, detail="Internal server error."
            )
    return ids


@router.delete("/namespace/{id}")
def delete_namespace(*, id: str) -> None:
    """
    Delete a MLTE namespace.
    :param id: The namespace identifier
    """
    with dependencies.session() as handle:
        try:
            handle.delete_namespace(id)
        except errors.ErrorNotFound as e:
            raise HTTPException(
                status_code=CODE_NOT_FOUND, detail=f"{e} not found."
            )
        except Exception:
            raise HTTPException(
                status_code=500, detail="Internal server error."
            )
