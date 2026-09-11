"""
test/backend/fixture/http.py

Fixtures for artifact store HTTP unit tests.
"""

from __future__ import annotations

from collections.abc import Callable

import pytest

from mlte.user.model import UserWithPassword
from test.backend.fixture.test_api import TestAPI

# -----------------------------------------------------------------------------
# Store Backend Fixtures
# -----------------------------------------------------------------------------


@pytest.fixture(scope="function")
def mem_store_test_api() -> Callable[[UserWithPassword | None], TestAPI]:
    """Sets up a memory-based test API and returns it."""

    def wrapper(
        api_user: UserWithPassword | None = None,
    ) -> TestAPI:
        return TestAPI(user=api_user)

    return wrapper
