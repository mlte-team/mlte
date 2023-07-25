"""
mlte/store/api/endpoints/negotiation_card.py

API definition for negotiation card artifacts.
"""
from fastapi import APIRouter, HTTPException

import mlte.store.error as errors
from mlte.negotiation.model import NegotiationCardModel
from mlte.web.store.api import dependencies

# "Not found"
CODE_NOT_FOUND = 404

# "Conflict"
CODE_ALREADY_EXISTS = 409

# The router exported by this submodule
router = APIRouter()


@router.post("")
def write_negotiation_card(
    namespace_id: str,
    model_id: str,
    version_id: str,
    artifact: NegotiationCardModel,
) -> NegotiationCardModel:
    """
    Write a negotiation card.
    :param namespace_id: The namespace identifier
    :param model_id: The model identifier
    :param version_id: The version identifier
    :param model: The artifact model
    :return: The created artifact
    """
    with dependencies.session() as handle:
        try:
            return handle.create_negotiation_card(
                namespace_id, model_id, version_id, artifact
            )
        except errors.ErrorNotFound as e:
            raise HTTPException(
                status_code=CODE_NOT_FOUND, detail=f"{e} not found."
            )
        except errors.ErrorAlreadyExists as e:
            raise HTTPException(
                status_code=CODE_ALREADY_EXISTS, detail=f"{e} already exists."
            )
        except Exception:
            raise HTTPException(
                status_code=500, detail="Internal server error."
            )


@router.get("/{artifact_id}")
def read_negotiation_card(
    namespace_id: str, model_id: str, version_id: str, artifact_id: str
) -> NegotiationCardModel:
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
            return handle.read_negotiation_card(
                namespace_id, model_id, version_id, artifact_id
            )
        except errors.ErrorNotFound as e:
            raise HTTPException(
                status_code=CODE_NOT_FOUND, detail=f"{e} not found."
            )
        except Exception:
            raise HTTPException(
                status_code=500, detail="Internal server error."
            )


@router.delete("/{arfiact_id}")
def delete_negotation_card(
    namespace_id: str, model_id: str, version_id: str, artifact_id: str
) -> NegotiationCardModel:
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
            return handle.delete_negotiation_card(
                namespace_id, model_id, version_id, artifact_id
            )
        except errors.ErrorNotFound as e:
            raise HTTPException(
                status_code=CODE_NOT_FOUND, detail=f"{e} not found."
            )
        except Exception:
            raise HTTPException(
                status_code=500, detail="Internal server error."
            )