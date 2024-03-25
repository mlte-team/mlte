"""
test/backend/fixture/state.py

Set up for store fixtures in API state.
"""

from __future__ import annotations

import pytest

from mlte.backend.state import state
from mlte.store.user.store import UserStore


def set_memory_user_store_in_state(
    store_fixture_name: str, request: pytest.FixtureRequest
):
    """Sets an provided fixture user store in the backend state."""
    user_store: UserStore = request.getfixturevalue(store_fixture_name)
    state.set_user_store(user_store)


def clear_state():
    """Clears the the backend state."""
    state._artifact_store = None
    state._user_store = None
