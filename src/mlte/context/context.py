"""
Global package context.
"""

from mlte._global import global_state


def set_namespace(namespace_identifier: str):
    """
    Set the global namespace identifier.

    :param namespace_identifier: The identifier for the namespace
    :type namespace_identifier: str
    """
    state = global_state()
    state.set_namespace(namespace_identifier)


def set_model(model_identifier: str, model_version: str):
    """
    Set the global model identifier and version.

    :param model_identifier: The identifier for the model
    :type model_identifier: str
    :param model_version: The version string for the model
    :type model_version: str
    """
    state = global_state()
    state.set_model(model_identifier, model_version)


def set_artifact_store_uri(artifact_store_uri: str):
    """
    Set the global artifact store URI.

    :param artifact_store_uri: The URI for the artifact store
    :type artifact_store_uri: str
    """
    state = global_state()
    state.set_artifact_store_uri(artifact_store_uri)
