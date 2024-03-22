"""
mlte/backend/api/auth/http_auth_exception.py

Exception used for authentication issues.
"""

from fastapi import HTTPException

from mlte.backend.api import codes


class HTTPAuthException(HTTPException):
    """Exception used for HTTP authentication issues."""

    def __init__(
        self,
        detail: str,
        status_code: int = codes.UNAUTHORIZED,
        error: str = "",
    ):
        """Constructor, calls based class with predefined params."""
        header_value = "Bearer"
        if error != "":
            header_value += f', error="{error}"'
            header_value += f', error_description="{detail}"'

        super().__init__(
            status_code=status_code,
            detail=detail,
            headers={"WWW-Authenticate": header_value},
        )
