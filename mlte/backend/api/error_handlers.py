"""
mlte/backend/api/error_handlers.py

Methods to handle and raise HTTP errors.
"""

import logging
import traceback as tb
import typing

from fastapi import HTTPException

import mlte.backend.api.codes as codes


def raise_http_internal_error(ex: Exception) -> typing.NoReturn:
    """Handles an error as an internal error, raising proper exception."""
    logging.error(f"Internal server error. {ex}")
    logging.error(tb.format_exc())
    raise HTTPException(
        status_code=codes.INTERNAL_ERROR,
        detail="Internal server error.",
    )
