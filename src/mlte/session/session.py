"""
mlte/session/session.py

Session state management for the MLTE library.
"""

from mlte.context import Context


class Session:
    """
    The Session data structure encapsulates package-wide state.

    The primary function of the Session data structure is to provide
    convenient access to the MLTE context for application developers.
    """

    _instance = None

    def __new__(self):
        if self._instance is None:
            self._instance = super(Session, self).__new__(self)
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
g_session = Session()


def session() -> Session:
    """Return the package global state."""
    return g_session


def set_namespace(namespace_identifier: str):
    """
    Set the global MLTE context namespace.
    :param namespace_identifier: The namespace identifier
    """
    g_session.context.namespace = namespace_identifier


def set_model(model_identifier: str):
    """
    Set the global MLTE context model identifier.
    :param model_identifier: The model identifier
    """
    g_session.context.model = model_identifier


def set_version(version_identifier: str):
    """
    Set the global MLTE context model version identifier.
    :param version_identifier: The model version identifier
    """
    g_session.context.version = version_identifier


def set_uri(artifact_store_uri: str):
    """
    Set the global MLTE context artifact store URI.
    :param artifact_store_uri: The artifact store URI string
    """
    g_session.context.uri = artifact_store_uri
