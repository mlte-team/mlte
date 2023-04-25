"""
store/api/endpoints/metadata.py

Metadata endpoints.
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from mlte.store.api import dependencies
from mlte.store.backend import SessionHandle
from mlte.store.models import Value

# The router exported by this submodule
router = APIRouter()


# -----------------------------------------------------------------------------
# Routes: Read Values
# -----------------------------------------------------------------------------


@router.get(
    "/{model_identifier}/{model_version}/{value_identifier}/{value_version}"
)
async def get_value_version(
    *,
    model_identifier: str,
    model_version: str,
    value_identifier: str,
    value_version: int,
):
    """
    Get an individual value version.
    :param model_identifier: The identifier for the model of interest
    :type model_identifier: str
    :param model_version: The version string for the model of interest
    :type model_version: str
    :param value_identifier: The identifier for the value of interest
    :type value_identifier: str
    :param value_version: The version identifier for the value of interest
    :type value_version: int
    """
    with dependencies.get_handle() as handle:
        try:
            # Read the value from the store
            document = handle.read_value(
                model_identifier,
                model_version,
                value_identifier,
                value_version,
            )
        except RuntimeError as e:
            raise HTTPException(status_code=404, detail=f"{e}")
        except Exception:
            raise HTTPException(
                status_code=500, detail="Internal server error."
            )
        return document


@router.get("/{model_identifier}/{model_version}/{value_identifier}")
async def get_value(
    *,
    model_identifier: str,
    model_version: str,
    value_identifier: str,
):
    """
    Get an individual value.
    :param model_identifier: The identifier for the model of interest
    :type model_identifier: str
    :param model_version: The version string for the model of interest
    :type model_version: str
    :param value_identifier: The identifier for the value of interest
    :type value_identifier: str
    """
    with dependencies.get_handle() as handle:
        try:
            # Value the value from the store
            document = handle.read_value(
                model_identifier, model_version, value_identifier
            )
        except RuntimeError as e:
            raise HTTPException(status_code=404, detail=f"{e}")
        except Exception:
            raise HTTPException(
                status_code=500, detail="Internal server error."
            )
        return document


@router.get("/{model_identifier}/{model_version}")
async def get_values(
    *,
    model_identifier: str,
    model_version: str,
    value_tag: Optional[str] = None,
):
    """
    Get a value or a collection of values.
    :param model_identifier: The identifier for the model of interest
    :type model_identifier: str
    :param model_version: The version string for the model of interest
    :type model_version: str
    :param value_tag: The tag for the value of interest
    :type value_tag: Optional[str]
    """
    with dependencies.get_handle() as handle:
        try:
            document = handle.read_values(
                model_identifier, model_version, value_tag
            )
        except RuntimeError as e:
            raise HTTPException(status_code=404, detail=f"{e}")
        except Exception:
            raise HTTPException(
                status_code=500, detail="Internal server error."
            )
        return document


# -----------------------------------------------------------------------------
# Routes: Write Values
# -----------------------------------------------------------------------------


@router.post("/{model_identifier}/{model_version}")
async def post_value(
    *,
    model_identifier: str,
    model_version: str,
    value: Value,
):
    """
    Post a value or collection of values.
    :param handle: The backend session handle
    :type handle: SessionHandle
    :param value: The value to write
    :type value: Value
    """
    if len(value.versions) != 1:
        raise HTTPException(status_code=500, detail="Update this code.")

    with dependencies.get_handle() as handle:
        try:
            # Write the value to the backend
            document = handle.write_value(
                model_identifier,
                model_version,
                value.identifier,
                value.versions[0].data,
                value.tag,
            )
        except Exception:
            raise HTTPException(
                status_code=500, detail="Internal server error."
            )

        return document


# -----------------------------------------------------------------------------
# Routes: Delete Values
# -----------------------------------------------------------------------------


@router.delete(
    "/{model_identifier}/{model_version}/{value_identifier}/{value_version}"
)
async def delete_value_version(
    *,
    handle: SessionHandle = Depends(dependencies.get_handle),
    model_identifier: str,
    model_version: str,
    value_identifier: str,
    value_version: int,
):
    """
    Delete an individual value version.
    :param model_identifier: The identifier for the model of interest
    :type model_identifier: str
    :param model_version: The version string for the model of interest
    :type model_version: str
    :param value_identifier: The identifier for the value of interest
    :type value_identifier: str
    :param value_version: The version identifier for the value
    :type value_version: int
    """
    with dependencies.get_handle() as handle:
        try:
            document = handle.delete_value_version(
                model_identifier,
                model_version,
                value_identifier,
                value_version,
            )
        except RuntimeError as e:
            raise HTTPException(status_code=404, detail=f"{e}")
        except Exception:
            raise HTTPException(
                status_code=500, detail="Internal server error."
            )

        return document


@router.delete("/{model_identifier}/{model_version}/{value_identifier}")
async def delete_value(
    *,
    model_identifier: str,
    model_version: str,
    value_identifier: str,
):
    """
    Delete an individual value.
    :param model_identifier: The identifier for the model of interest
    :type model_identifier: str
    :param model_version: The version string for the model of interest
    :type model_version: str
    :param value_identifier: The identifier for the value of interest
    :type value_identifier: str
    """
    with dependencies.get_handle() as handle:
        try:
            document = handle.delete_value(
                model_identifier, model_version, value_identifier
            )
        except RuntimeError as e:
            raise HTTPException(status_code=404, detail=f"{e}")
        except Exception:
            raise HTTPException(
                status_code=500, detail="Internal server error."
            )

        return document


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
