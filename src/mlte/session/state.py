"""
mlte/session/state.py

Session state management for the MLTE library.
"""

from mlte.context import Context


class SessionState:
    """
    The SessionState data structure encapsulates package-wide state.

    The primary function of the SessionState data structure is to provide
    convenient access to the MLTE context for application developers.
    """

    _instance = None

    def __new__(self):
        if self._instance is None:
            self._instance = super(SessionState, self).__new__(self)
        return self._instance

    def __init__(self):
        self.context = Context()
        """The MLTE context for the session."""

    def assert_populated(self):
        """
        Determine if the global MLTE context is initialized. Raise if not.
        :raises RuntimeError: If the global MLTE context instance is not initialized
        """
        self.context.assert_populated()


# Singleton session state
g_state = SessionState()


def session_state() -> SessionState:
    """Return the package global state."""
    return g_state


def set_namespace(namespace_identifier: str):
    """
    Set the global MLTE context namespace.
    :param namespace_identifier: The namespace identifier
    """
    g_state.context.namespace = namespace_identifier


def set_model(model_identifier: str):
    """
    Set the global MLTE context model identifier.
    :param model_identifier: The model identifier
    """
    g_state.context.model = model_identifier


def set_version(version_identifier: str):
    """
    Set the global MLTE context model version identifier.
    :param version_identifier: The model version identifier
    """
    g_state.context.version = version_identifier


def set_uri(artifact_store_uri: str):
    """
    Set the global MLTE context artifact store URI.
    :param artifact_store_uri: The artifact store URI string
    """
    g_state.context.uri = artifact_store_uri
