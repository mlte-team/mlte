"""
mlte/store/api/endpoints/artifact.py

API definition for MLTE artifacts.
"""

from typing import Optional

from fastapi import APIRouter, HTTPException

import mlte.store.error as errors
import mlte.store.query as query
import mlte.web.store.api.codes as codes
from mlte.artifact.model import ArtifactModel, ArtifactType
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
    Read a negotiation card.
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
    artifact_id: Optional[str] = None,
    artifact_type: Optional[ArtifactType] = None,
) -> list[ArtifactModel]:
    """
    Read a negotiation card.
    :param namespace_id: The namespace identifier
    :param model_id: The model identifier
    :param version_id: The version identifier
    :param artifact_id: The identifier for the artifact
    :param artifact_type: The type identifier for the artifact
    :return: The read artifacts
    """
    filter = _construct_filter(artifact_id, artifact_type)
    with dependencies.session() as handle:
        try:
            return handle.read_artifacts(
                namespace_id, model_id, version_id, filter
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


@router.delete("/{artifact_id}")
def delete_artifact(
    namespace_id: str, model_id: str, version_id: str, artifact_id: str
) -> ArtifactModel:
    """
    Delete a negotiation card.
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


def _construct_filter(
    artifact_id: Optional[str] = None,
    artifact_type: Optional[ArtifactType] = None,
) -> query.ArtifactFilter:
    """
    Construct a store filter for the given query parameters.
    :param artifact_id: The artifact identifier
    :param artifact_type: The artifact type
    :return: The filter
    """
    if artifact_id is None and artifact_type is None:
        return query.AllFilter()

    filter: query.ArtifactFilter = query.AllFilter()
    if artifact_id is not None:
        filter = query.AndFilter(
            filter, query.ArtifactIdentifierFilter(artifact_id=artifact_id)
        )
    if artifact_type is not None:
        filter = query.AndFilter(
            filter, query.ArtifactTypeFilter(artifact_type=artifact_type)
        )
    return filter
