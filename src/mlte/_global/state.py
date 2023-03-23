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
        self.model_identifier: str = ""
        # The version string for the model in global context
        self.model_version: str = ""
        # The URI for the artifact store in global context
        self.artifact_store_uri: str = ""

    def has_model(self) -> bool:
        return self.model_identifier != "" and self.model_version != ""

    def has_artifact_store_uri(self) -> bool:
        return self.artifact_store_uri != ""

    def set_model(self, model_identifier: str, model_version: str):
        if model_identifier == "":
            raise RuntimeError("Model identifier cannot be empty.")
        if model_version == "":
            raise RuntimeError("Model version cannot be empty.")
        self.model_identifier = model_identifier
        self.model_version = model_version

    def set_artifact_store_uri(self, artifact_store_uri: str):
        if artifact_store_uri == "":
            raise RuntimeError("Artifact store URI cannot be empty.")
        self.artifact_store_uri = artifact_store_uri

    def get_model(self) -> Tuple[str, str]:
        assert self.has_model(), "Broken precondition."
        return self.model_identifier, self.model_version

    def get_artifact_store_uri(self) -> str:
        assert self.has_artifact_store_uri(), "Broken precondition."
        return self.artifact_store_uri

    def check(self):
        """
        Ensure that the global state contains
        information necessary to save/load artifacts.
        """
        if not self.has_model():
            raise RuntimeError(
                "Set model context prior to saving or loading artifacts."
            )
        if not self.has_artifact_store_uri():
            raise RuntimeError(
                "Set artifact store URI prior to saving or loading artifacts."
            )


# Singleton global state
g_state = GlobalState()


def global_state() -> GlobalState:
    """Return the package global state."""
    return g_state
