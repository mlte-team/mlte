"""
mlte/store/api/endpoints/artifact.py

API definition for MLTE artifacts.
"""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, HTTPException

import mlte.store.error as errors
import mlte.web.store.api.codes as codes
from mlte.artifact.model import ArtifactModel
from mlte.store.query import Query
from mlte.web.store.api import dependencies

# The router exported by this submodule
router = APIRouter()


@router.post("")
def write_artifact(
    namespace_id: str,
    model_id: str,
    version_id: str,
    artifact: ArtifactModel,
) -> ArtifactModel:
    """
    Write an artifact.
    :param namespace_id: The namespace identifier
    :param model_id: The model identifier
    :param version_id: The version identifier
    :param model: The artifact model
    :return: The created artifact
    """
    with dependencies.session() as handle:
        try:
            return handle.write_artifact(
                namespace_id, model_id, version_id, artifact
            )
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


@router.get("/{artifact_id}")
def read_artifact(
    namespace_id: str, model_id: str, version_id: str, artifact_id: str
) -> ArtifactModel:
    """
    Read an artifact by identifier.
    :param namespace_id: The namespace identifier
    :param model_id: The model identifier
    :param version_id: The version identifier
    :param artifact_id: The identifier for the artifact
    :return: The read artifact
    """
    with dependencies.session() as handle:
        try:
            return handle.read_artifact(
                namespace_id, model_id, version_id, artifact_id
            )
        except errors.ErrorNotFound as e:
            raise HTTPException(
                status_code=codes.NOT_FOUND, detail=f"{e} not found."
            )
        except Exception:
            raise HTTPException(
                status_code=codes.INTERNAL_ERROR,
                detail="Internal server error.",
            )


@router.get("")
def read_artifacts(
    namespace_id: str,
    model_id: str,
    version_id: str,
    limit: int = 100,
    offset: int = 0,
) -> List[ArtifactModel]:
    """
    Read artifacts with limit and offset.
    :param namespace_id: The namespace identifier
    :param model_id: The model identifier
    :param version_id: The version identifier
    :param limit: The limit on returned artifacts
    :param offset: The offset on returned artifacts
    :return: The read artifacts
    """
    with dependencies.session() as handle:
        try:
            return handle.read_artifacts(
                namespace_id, model_id, version_id, limit, offset
            )
        except Exception:
            raise HTTPException(
                status_code=codes.INTERNAL_ERROR,
                detail="Internal server error.",
            )


@router.post("/search")
def search_artifacts(
    namespace_id: str, model_id: str, version_id: str, query: Query
) -> List[ArtifactModel]:
    """
    Search artifacts.
    :param namespace_id: The namespace identifier
    :param model_id: The model identifier
    :param version_id: The version identifier
    :param query: The artifact query
    :return: The read artifacts
    """
    with dependencies.session() as handle:
        try:
            return handle.search_artifacts(
                namespace_id, model_id, version_id, query
            )
        except Exception:
            raise HTTPException(
                status_code=codes.INTERNAL_ERROR,
                detail="Internal server error.",
            )


@router.delete("/{artifact_id}")
def delete_artifact(
    namespace_id: str, model_id: str, version_id: str, artifact_id: str
) -> ArtifactModel:
    """
    Delete an artifact by identifier.
    :param namespace_id: The namespace identifier
    :param model_id: The model identifier
    :param version_id: The version identifier
    :param artifact_id: The identifier for the artifact
    :return: The deleted artifact
    """
    with dependencies.session() as handle:
        try:
            return handle.delete_artifact(
                namespace_id, model_id, version_id, artifact_id
            )
        except errors.ErrorNotFound as e:
            raise HTTPException(
                status_code=codes.NOT_FOUND, detail=f"{e} not found."
            )
        except Exception:
            raise HTTPException(
                status_code=codes.INTERNAL_ERROR,
                detail="Internal server error.",
            )
