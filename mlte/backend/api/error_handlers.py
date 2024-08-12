"""
mlte/backend/api/error_handlers.py

Methods to handle and raise HTTP errors.
"""

import traceback as tb
import typing

from fastapi import HTTPException

import mlte.backend.api.codes as codes


def raise_http_internal_error(ex: Exception) -> typing.NoReturn:
    """Handles an error as an internal error, raising proper exception."""
    print(f"Internal server error. {ex}")
    print(tb.format_exc())
    raise HTTPException(
        status_code=codes.INTERNAL_ERROR,
        detail="Internal server error.",
    )
