"""Globally-accessible application state for the backend."""

from __future__ import annotations

from mlte.session.unified_store import UnifiedStore


class State:
    """Global state object."""

    def __init__(self):
        self.reset()

    def reset(self):
        """Resets all internal state to defaults."""

        self.stores = UnifiedStore()
        """All stores in this session."""

        self._jwt_secret_key: str = ""
        """Secret key used to sign authentication tokens."""

    def set_token_key(self, token_key: str):
        """Sets the globally used token secret key."""
        self._jwt_secret_key = token_key

    @property
    def token_key(self) -> str:
        """Get the globally-configured token secret key."""
        if self._jwt_secret_key == "":
            raise RuntimeError("Token key has not been configured.")
        return self._jwt_secret_key


# Globally-accessible application state
state = State()
