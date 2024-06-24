"""
test/backend/fixture/http.py

Fixtures for artifact store HTTP unit tests.
"""

from __future__ import annotations

from typing import Callable, Optional

import pytest

from mlte.user.model import UserWithPassword
from test.backend.fixture.test_api import TestAPI

# -----------------------------------------------------------------------------
# Store Backend Fixtures
# -----------------------------------------------------------------------------


@pytest.fixture(scope="function")
def mem_store_test_api() -> Callable[[Optional[UserWithPassword]], TestAPI]:
    """Sets up memory based store for the API and gets an associated client."""

    def wrapper(api_user: Optional[UserWithPassword] = None) -> TestAPI:
        test_api = TestAPI()
        test_api.set_users(api_user)
        return test_api

    return wrapper
