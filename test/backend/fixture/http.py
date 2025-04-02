"""
test/backend/fixture/http.py

Fixtures for artifact store HTTP unit tests.
"""

from __future__ import annotations

from typing import Callable, Optional

import pytest

from mlte.user.model import UserWithPassword
from test.backend.fixture.test_api import TestAPI
from test.store.catalog.fixture import TEST_CATALOG_ID

# -----------------------------------------------------------------------------
# Store Backend Fixtures
# -----------------------------------------------------------------------------


@pytest.fixture(scope="function")
def mem_store_test_api() -> Callable[[Optional[UserWithPassword]], TestAPI]:
    """Sets up a memory-based test API and returns it."""

    def wrapper(
        api_user: Optional[UserWithPassword] = None,
        default_catalog_id: str = TEST_CATALOG_ID,
    ) -> TestAPI:
        return TestAPI(user=api_user, default_catalog_id=default_catalog_id)

    return wrapper
