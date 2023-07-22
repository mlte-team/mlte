"""
mlte/store/api/endpoints/negotiation_card.py

API definition for negotiation card artifacts.
"""

from typing import Optional

from fastapi import APIRouter, HTTPException

from mlte.negotiation.model import NegotiationCardModel
from mlte.store.store import StoreSession
from mlte.web.store.api import dependencies

# The router exported by this submodule
router = APIRouter()


@router.get("/")
def read_negotiation_card(id: str) -> NegotiationCardModel:
    """
    Read a negotiation card.
    :param id: The identifier for the negotiation card
    """
    pass


@router.post("/")
def write_negotiation_card(model: NegotiationCardModel) -> None:
    """
    Write a negotiation card.
    :param model: The negotiation card model
    """
    pass
