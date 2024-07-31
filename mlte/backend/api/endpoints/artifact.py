"""
mlte/store/api/endpoints/artifact.py

API definition for MLTE artifacts.
"""

from __future__ import annotations

import traceback
from typing import List

from fastapi import APIRouter, HTTPException

import mlte.backend.api.codes as codes
import mlte.store.error as errors
from mlte.artifact.model import ArtifactModel
from mlte.backend.api import dependencies
from mlte.backend.api.auth.authorization import AuthorizedUser
from mlte.backend.api.model import WriteArtifactRequest, WriteArtifactResponse
from mlte.store.common.query import Query

# The router exported by this submodule
router = APIRouter()


@router.post("")
def write_artifact(
    model_id: str,
    version_id: str,
    request: WriteArtifactRequest,
    current_user: AuthorizedUser,
) -> WriteArtifactResponse:
    """
    Write an artifact.
    :param model_id: The model identifier
    :param version_id: The version identifier
    :param request: The artifact write request
    :return: The created artifact
    """
    with dependencies.artifact_store_session() as artifact_store:
        try:
            artifact = artifact_store.write_artifact_with_header(
                model_id,
                version_id,
                request.artifact,
                force=request.force,
                parents=request.parents,
                user=current_user.username,
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
    model_id: str,
    version_id: str,
    artifact_id: str,
    current_user: AuthorizedUser,
) -> ArtifactModel:
    """
    Read an artifact by identifier.
    :param model_id: The model identifier
    :param version_id: The version identifier
    :param artifact_id: The identifier for the artifact
    :return: The read artifact
    """
    with dependencies.artifact_store_session() as handle:
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
    current_user: AuthorizedUser,
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
    with dependencies.artifact_store_session() as handle:
        try:
            return handle.read_artifacts(model_id, version_id, limit, offset)
        except Exception:
            raise HTTPException(
                status_code=codes.INTERNAL_ERROR,
                detail="Internal server error.",
            )


# TODO: this uses post to take advantge of the Query model. However, this is not corret REST syntax,
# and it forces us to use write permissions to reach this endpoint. This should be fixed.
@router.post("/search")
def search_artifacts(
    model_id: str,
    version_id: str,
    query: Query,
    current_user: AuthorizedUser,
) -> List[ArtifactModel]:
    """
    Search artifacts.

    :param model_id: The model identifier
    :param version_id: The version identifier
    :param query: The artifact query
    :return: The read artifacts
    """
    with dependencies.artifact_store_session() as handle:
        try:
            return handle.search_artifacts(model_id, version_id, query)
        except Exception:
            raise HTTPException(
                status_code=codes.INTERNAL_ERROR,
                detail="Internal server error.",
            )


@router.delete("/{artifact_id}")
def delete_artifact(
    model_id: str,
    version_id: str,
    artifact_id: str,
    current_user: AuthorizedUser,
) -> ArtifactModel:
    """
    Delete an artifact by identifier.
    :param model_id: The model identifier
    :param version_id: The version identifier
    :param artifact_id: The identifier for the artifact
    :return: The deleted artifact
    """
    with dependencies.artifact_store_session() as handle:
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
