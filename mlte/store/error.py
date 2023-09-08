"""
mlte/store/error.py

Error definitions for artifact store implementations.
"""


class ErrorAlreadyExists(RuntimeError):
    """An error raised when a new entity is requested but it already exists."""

    pass


class ErrorNotFound(RuntimeError):
    """An error raised when the requested entity is not found."""

    pass


class InternalError(RuntimeError):
    """A logic error in our implementation."""

    pass
