"""
Global state management.
"""

from typing import Tuple


class GlobalState:
    """Encapsulates package-wide global state."""

    _instance = None

    def __new__(self):
        if self._instance is None:
            self._instance = super(GlobalState, self).__new__(self)
        return self._instance

    def __init__(self):
        # The identifier for the model in global context
        self.model_identifier: str = None
        # The version string for the model in global context
        self.model_version: str = None
        # The URI for the artifact store in global context
        self.artifact_store_uri: str = None

    def has_model(self) -> bool:
        return (
            self.model_identifier is not None and self.model_version is not None
        )

    def has_artifact_store_uri(self) -> bool:
        return self.artifact_store_uri is not None

    def set_model(self, model_identifier: str, model_version: str):
        self.model_identifier = model_identifier
        self.model_version = model_version

    def set_artifact_store_uri(self, artifact_store_uri: str):
        self.artifact_store_uri = artifact_store_uri

    def get_model(self) -> Tuple[str, str]:
        assert self.has_model(), "Broken precondition."
        return self.model_identifier, self.model_version

    def get_artifact_store_uri(self) -> str:
        assert self.has_artifact_store_uri(), "Broken precondition."
        return self.artifact_store_uri


# Singleton global state
g_state = GlobalState()


def global_state() -> GlobalState:
    """Return the package global state."""
    return g_state
