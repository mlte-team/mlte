"""
mlte/backend/api/auth/http_auth_exception.py

Exception used for authentication issues.
"""
from __future__ import annotations

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from mlte.backend.api import codes


def json_content_exception_handler(
    request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    """Exception handler that doesn't add the "details" key to a JSON response."""
    return JSONResponse(
        status_code=exc.status_code, headers=exc.headers, content=exc.detail
    )


class HTTPTokenException(HTTPException):
    """Exception used for issues when a token is requested."""

    def __init__(
        self,
        status_code: int = codes.BAD_REQUEST,
        error: str = "",
        error_decription: str = "",
    ):
        """Constructor, calls based class with predefined params."""
        headers = {"Content-Type": "application/json;charset=UTF-8"}
        details = {}
        if error != "":
            details = {"error": error, "error_description": error_decription}

        super().__init__(
            status_code=status_code,
            headers=headers,
            detail=details,
        )


class HTTPAuthException(HTTPException):
    """Exception used for HTTP authentication issues."""

    def __init__(
        self,
        status_code: int = codes.UNAUTHORIZED,
        error: str = "",
        error_decription: str = "",
    ):
        """Constructor, calls based class with predefined params."""
        header_value = "Bearer"
        if error != "":
            header_value += f' error="{error}"'
            header_value += f', error_description="{error_decription}"'
        headers = {"WWW-Authenticate": header_value}

        super().__init__(
            status_code=status_code,
            headers=headers,
        )
