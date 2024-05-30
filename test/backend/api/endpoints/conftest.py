"""
test/backend/api/endpoints/conftest.py

Loading common fixtures used in tests in this and child folders.
"""

from test.backend.fixture.http import (  # noqa
    mem_store_and_test_http_client as test_client_fix,
)
