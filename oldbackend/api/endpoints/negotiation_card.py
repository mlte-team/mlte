"""
mlte/store/api/endpoints/negotiation_card.py

API definition for negotiation card artifacts.
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from mlte.store.api import dependencies
from mlte.store.backend import SessionHandle

from mlte.negotiation.model import NegotiationCardModel

# The router exported by this submodule
router = APIRouter()


@router.get("/")
async def read_negotiation_card(id: str) -> NegotiationCardModel:
    """
    Read a negotiation card.
    :param id: The identifier for the negotiation card
    """
    pass


@router.post("/")
async def write_negotiation_card(model: NegotiationCardModel) -> None:
    """
    Write a negotiation card.
    :param model: The negotiation card model
    """
    pass


@router.delete("/{model_identifier}/{model_version}")
async def delete_values(
    *,
    model_identifier: str,
    model_version: str,
    value_tag: Optional[str] = None,
):
    """
    Delete a collection of values.
    :param model_identifier: The identifier for the model of interest
    :type model_identifier: str
    :param model_version: The version string for the model of interest
    :type model_version: str
    :param value_tag: The (optional) tag that identifies values of interest
    :type value_tag: Optional[str]
    """
    with dependencies.get_handle() as handle:
        try:
            document = handle.delete_values(
                model_identifier, model_version, value_tag
            )
        except RuntimeError as e:
            raise HTTPException(status_code=404, detail=f"{e}")
        except Exception:
            raise HTTPException(
                status_code=500, detail="Internal server error."
            )

        return document
