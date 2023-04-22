"""
store/frontend/dependencies.py

This file defines common dependencies that are used by API functions.
In practice, this ensures that the backend is initialized prior to
attempting to service any incoming requests.
"""

from typing import Generator
from mlte.store.backend.engine import g_engine
from mlte.store.backend import SessionHandle


def get_handle() -> Generator[SessionHandle, None, None]:
    """
    Get a handle to backend session.
    :return: The handle
    """
    try:
        handle = g_engine.handle()
        yield handle
    finally:
        handle.close()
