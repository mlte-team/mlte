"""
store/api/endpoints/metadata.py

Metadata endpoints.
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from mlte.store.api import dependencies
from mlte.store.backend import SessionHandle
from mlte.store.models import Result

# The router exported by this submodule
router = APIRouter()


# -----------------------------------------------------------------------------
# Routes: Read Results
# -----------------------------------------------------------------------------


@router.get(
    "/{model_identifier}/{model_version}/{result_identifier}/{result_version}"
)
async def get_result_version(
    *,
    handle: SessionHandle = Depends(dependencies.get_handle),
    model_identifier: str,
    model_version: str,
    result_identifier: str,
    result_version: int,
):
    """
    Get an individual result version.
    :param handle: The backend session handle
    :type handle: SessionHandle
    :param model_identifier: The identifier for the model of interest
    :type model_identifier: str
    :param model_version: The version string for the model of interest
    :type model_version: str
    :param result_identifier: The identifier for the result of interest
    :type result_identifier: str
    :param result_version: The version identifier for the result of interest
    :type result_version: int
    """
    try:
        # Read the result from the store
        document = handle.read_result(
            model_identifier, model_version, result_identifier, result_version
        )
    except RuntimeError as e:
        raise HTTPException(status_code=404, detail=f"{e}")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error.")
    return document


@router.get("/{model_identifier}/{model_version}/{result_identifier}")
async def get_result(
    *,
    handle: SessionHandle = Depends(dependencies.get_handle),
    model_identifier: str,
    model_version: str,
    result_identifier: str,
):
    """
    Get an individual result.
    :param handle: The backend session handle
    :type handle: SessionHandle
    :param model_identifier: The identifier for the model of interest
    :type model_identifier: str
    :param model_version: The version string for the model of interest
    :type model_version: str
    :param result_identifier: The identifier for the result of interest
    :type result_identifier: str
    """
    try:
        # Result the result from the store
        document = handle.read_result(
            model_identifier, model_version, result_identifier
        )
    except RuntimeError as e:
        raise HTTPException(status_code=404, detail=f"{e}")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error.")
    return document


@router.get("/{model_identifier}/{model_version}")
async def get_results(
    *,
    handle: SessionHandle = Depends(dependencies.get_handle),
    model_identifier: str,
    model_version: str,
    result_tag: Optional[str] = None,
):
    """
    Get a result or a collection of results.
    :param handle: The backend session handle
    :type handle: SessionHandle
    :param model_identifier: The identifier for the model of interest
    :type model_identifier: str
    :param model_version: The version string for the model of interest
    :type model_version: str
    :param result_tag: The tag for the result of interest
    :type result_tag: Optional[str]
    """
    try:
        document = handle.read_results(
            model_identifier, model_version, result_tag
        )
    except RuntimeError as e:
        raise HTTPException(status_code=404, detail=f"{e}")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error.")
    return document


# -----------------------------------------------------------------------------
# Routes: Write Results
# -----------------------------------------------------------------------------


@router.post("/{model_identifier}/{model_version}")
async def post_result(
    *,
    handle: SessionHandle = Depends(dependencies.get_handle),
    model_identifier: str,
    model_version: str,
    result: Result,
):
    """
    Post a result or collection of results.
    :param handle: The backend session handle
    :type handle: SessionHandle
    :param result: The result to write
    :type result: RequestModelResult
    """
    if len(result.versions) != 1:
        raise HTTPException(status_code=500, detail="Update this code.")

    try:
        # Write the result to the backend
        document = handle.write_result(
            model_identifier,
            model_version,
            result.identifier,
            result.versions[0].data,
            result.tag,
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error.")

    return document


# -----------------------------------------------------------------------------
# Routes: Delete Results
# -----------------------------------------------------------------------------


@router.delete(
    "/{model_identifier}/{model_version}/{result_identifier}/{result_version}"
)
async def delete_result_version(
    *,
    handle: SessionHandle = Depends(dependencies.get_handle),
    model_identifier: str,
    model_version: str,
    result_identifier: str,
    result_version: int,
):
    """
    Delete an individual result version.
    :param handle: The backend session handle
    :type handle: SessionHandle
    :param model_identifier: The identifier for the model of interest
    :type model_identifier: str
    :param model_version: The version string for the model of interest
    :type model_version: str
    :param result_identifier: The identifier for the result of interest
    :type result_identifier: str
    :param result_version: The version identifier for the result
    :type result_version: int
    """
    try:
        document = handle.delete_result_version(
            model_identifier, model_version, result_identifier, result_version
        )
    except RuntimeError as e:
        raise HTTPException(status_code=404, detail=f"{e}")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error.")

    return document


@router.delete("/{model_identifier}/{model_version}/{result_identifier}")
async def delete_result(
    *,
    handle: SessionHandle = Depends(dependencies.get_handle),
    model_identifier: str,
    model_version: str,
    result_identifier: str,
):
    """
    Delete an individual result.
    :param handle: The backend session handle
    :type handle: SessionHandle
    :param model_identifier: The identifier for the model of interest
    :type model_identifier: str
    :param model_version: The version string for the model of interest
    :type model_version: str
    :param result_identifier: The identifier for the result of interest
    :type result_identifier: str
    """
    try:
        document = handle.delete_result(
            model_identifier, model_version, result_identifier
        )
    except RuntimeError as e:
        raise HTTPException(status_code=404, detail=f"{e}")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error.")

    return document


@router.delete("/{model_identifier}/{model_version}")
async def delete_results(
    *,
    handle: SessionHandle = Depends(dependencies.get_handle),
    model_identifier: str,
    model_version: str,
    result_tag: Optional[str] = None,
):
    """
    Delete a collection of results.
    :param handle: The backend session handle
    :type handle: SessionHandle
    :param model_identifier: The identifier for the model of interest
    :type model_identifier: str
    :param model_version: The version string for the model of interest
    :type model_version: str
    :param result_tag: The (optional) tag that identifies results of interest
    :type result_tag: Optional[str]
    """
    try:
        document = handle.delete_results(
            model_identifier, model_version, result_tag
        )
    except RuntimeError as e:
        raise HTTPException(status_code=404, detail=f"{e}")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error.")

    return document
