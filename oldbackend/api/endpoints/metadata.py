"""
store/api/endpoints/metadata.py

Metadata endpoints.
"""

from fastapi import APIRouter, HTTPException
from mlte.store.api import dependencies

# The router exported by this submodule
router = APIRouter()


@router.get("/model")
async def get_models():
    """
    Get metadata for all existing models.
    :param handle: The backend session handle
    :type handle: SessionHandle
    """
    with dependencies.get_handle() as handle:
        try:
            document = handle.read_model_metadata()
        except RuntimeError as e:
            raise HTTPException(status_code=404, detail=f"{e}")
        except Exception:
            raise HTTPException(
                status_code=500, detail="Internal server error."
            )
        return document


@router.get("/model/{model_identifier}")
async def get_model(
    *,
    model_identifier: str,
):
    """
    Get metadata for a single model.
    :param handle: The backend session handle
    :type handle: SessionHandle
    :param model_identifier: The identifier for the model of interest
    :type model_identifier: str
    """
    with dependencies.get_handle() as handle:
        try:
            document = handle.read_model_metadata(model_identifier)
        except RuntimeError as e:
            raise HTTPException(status_code=404, detail=f"{e}")
        except Exception:
            raise HTTPException(
                status_code=500, detail="Internal server error."
            )
        return document
