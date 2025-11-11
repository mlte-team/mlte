"""API definition for MLTE artifacts."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

import mlte.backend.api.codes as codes
import mlte.store.error as errors
from mlte._private import url as url_utils
from mlte.artifact.factory import ArtifactFactory
from mlte.artifact.model import ArtifactModel
from mlte.backend.api.auth.authorization import AuthorizedUser
from mlte.backend.api.error_handlers import raise_http_internal_error
from mlte.backend.api.models.artifact_model import (
    WriteArtifactRequest,
    WriteArtifactResponse,
)
from mlte.backend.core import state_stores
from mlte.backend.core.state import state
from mlte.context.context import Context
from mlte.store.query import Query

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
    model_id = url_utils.revert_valid_url_part(model_id)
    version_id = url_utils.revert_valid_url_part(version_id)

    try:
        artifact = ArtifactFactory.from_model(request.artifact)
        model = artifact.save_with(
            Context(model_id, version_id),
            state.stores.artifact_store,
            force=request.force,
            parents=request.parents,
            user=current_user.username,
        )
        return WriteArtifactResponse(artifact=model)
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
    model_id = url_utils.revert_valid_url_part(model_id)
    version_id = url_utils.revert_valid_url_part(version_id)
    artifact_id = url_utils.revert_valid_url_part(artifact_id)
    with state_stores.artifact_store_session() as artifact_store:
        try:
            return artifact_store.artifact_mapper.read(
                artifact_id, (model_id, version_id)
            )
        except errors.ErrorNotFound as e:
            raise HTTPException(
                status_code=codes.NOT_FOUND, detail=f"{e} not found."
            )
        except Exception as ex:
            raise_http_internal_error(ex)


@router.get("")
def read_artifacts(
    model_id: str,
    version_id: str,
    current_user: AuthorizedUser,
    limit: int = 100,
    offset: int = 0,
) -> list[ArtifactModel]:
    """
    Read artifacts with limit and offset.
    :param model_id: The model identifier
    :param version_id: The version identifier
    :param limit: The limit on returned artifacts
    :param offset: The offset on returned artifacts
    :return: The read artifacts
    """
    model_id = url_utils.revert_valid_url_part(model_id)
    version_id = url_utils.revert_valid_url_part(version_id)
    with state_stores.artifact_store_session() as artifact_store:
        try:
            return artifact_store.artifact_mapper.list_details(
                context=(model_id, version_id), limit=limit, offset=offset
            )
        except Exception as ex:
            raise_http_internal_error(ex)


# TODO: this uses post to take advantge of the Query model. However, this is not corret REST syntax,
# and it forces us to use write permissions to reach this endpoint. This should be fixed.
@router.post("/search")
def search_artifacts(
    model_id: str,
    version_id: str,
    query: Query,
    current_user: AuthorizedUser,
) -> list[ArtifactModel]:
    """
    Search artifacts.

    :param model_id: The model identifier
    :param version_id: The version identifier
    :param query: The artifact query
    :return: The read artifacts
    """
    model_id = url_utils.revert_valid_url_part(model_id)
    version_id = url_utils.revert_valid_url_part(version_id)
    with state_stores.artifact_store_session() as artifact_store:
        try:
            return artifact_store.artifact_mapper.search(
                query, context=(model_id, version_id)
            )
        except Exception as ex:
            raise_http_internal_error(ex)


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
    model_id = url_utils.revert_valid_url_part(model_id)
    version_id = url_utils.revert_valid_url_part(version_id)
    artifact_id = url_utils.revert_valid_url_part(artifact_id)
    with state_stores.artifact_store_session() as artifact_store:
        try:
            return artifact_store.artifact_mapper.delete(
                artifact_id, (model_id, version_id)
            )
        except errors.ErrorNotFound as e:
            raise HTTPException(
                status_code=codes.NOT_FOUND, detail=f"{e} not found."
            )
        except Exception as ex:
            raise_http_internal_error(ex)
