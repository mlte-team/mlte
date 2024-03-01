"""
mlte/store/api/endpoints/artifact.py

API definition for MLTE artifacts.
"""

from __future__ import annotations

import traceback
from typing import List

from fastapi import APIRouter, HTTPException

import mlte.store.error as errors
import mlte.web.store.api.codes as codes
from mlte.artifact.model import ArtifactModel
from mlte.store.artifact.query import Query
from mlte.web.store.api import dependencies
from mlte.web.store.api.model import WriteArtifactRequest, WriteArtifactResponse

# The router exported by this submodule
router = APIRouter()


@router.post("")
def write_artifact(
    model_id: str,
    version_id: str,
    request: WriteArtifactRequest,
) -> WriteArtifactResponse:
    """
    Write an artifact.
    :param model_id: The model identifier
    :param version_id: The version identifier
    :param request: The artifact write request
    :return: The created artifact
    """
    with dependencies.session() as handle:
        try:
            artifact = handle.write_artifact_with_timestamp(
                model_id,
                version_id,
                request.artifact,
                force=request.force,
                parents=request.parents,
            )
            return WriteArtifactResponse(artifact=artifact)
        except errors.ErrorNotFound as e:
            raise HTTPException(
                status_code=codes.NOT_FOUND, detail=f"{e} not found."
            )
        except errors.ErrorAlreadyExists as e:
            raise HTTPException(
                status_code=codes.ALREADY_EXISTS, detail=f"{e} already exists."
            )
        except Exception:
            print(traceback.format_exc())
            raise HTTPException(
                status_code=codes.INTERNAL_ERROR,
                detail="Internal server error.",
            )


@router.get("/{artifact_id}")
def read_artifact(
    model_id: str, version_id: str, artifact_id: str
) -> ArtifactModel:
    """
    Read an artifact by identifier.
    :param model_id: The model identifier
    :param version_id: The version identifier
    :param artifact_id: The identifier for the artifact
    :return: The read artifact
    """
    with dependencies.session() as handle:
        try:
            return handle.read_artifact(model_id, version_id, artifact_id)
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
    model_id: str,
    version_id: str,
    limit: int = 100,
    offset: int = 0,
) -> List[ArtifactModel]:
    """
    Read artifacts with limit and offset.
    :param model_id: The model identifier
    :param version_id: The version identifier
    :param limit: The limit on returned artifacts
    :param offset: The offset on returned artifacts
    :return: The read artifacts
    """
    with dependencies.session() as handle:
        try:
            return handle.read_artifacts(model_id, version_id, limit, offset)
        except Exception:
            raise HTTPException(
                status_code=codes.INTERNAL_ERROR,
                detail="Internal server error.",
            )


@router.post("/search")
def search_artifacts(
    model_id: str, version_id: str, query: Query
) -> List[ArtifactModel]:
    """
    Search artifacts.

    :param model_id: The model identifier
    :param version_id: The version identifier
    :param query: The artifact query
    :return: The read artifacts
    """
    with dependencies.session() as handle:
        try:
            return handle.search_artifacts(model_id, version_id, query)
        except Exception:
            raise HTTPException(
                status_code=codes.INTERNAL_ERROR,
                detail="Internal server error.",
            )


@router.delete("/{artifact_id}")
def delete_artifact(
    model_id: str, version_id: str, artifact_id: str
) -> ArtifactModel:
    """
    Delete an artifact by identifier.
    :param model_id: The model identifier
    :param version_id: The version identifier
    :param artifact_id: The identifier for the artifact
    :return: The deleted artifact
    """
    with dependencies.session() as handle:
        try:
            return handle.delete_artifact(model_id, version_id, artifact_id)
        except errors.ErrorNotFound as e:
            raise HTTPException(
                status_code=codes.NOT_FOUND, detail=f"{e} not found."
            )
        except Exception:
            raise HTTPException(
                status_code=codes.INTERNAL_ERROR,
                detail="Internal server error.",
            )
