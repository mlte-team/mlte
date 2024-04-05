"""
mlte/store/artifact/util.py

Common utilities for store implementations.
"""

import mlte.store.error as errors
from mlte.context.model import ModelCreate, VersionCreate
from mlte.store.artifact.store import ArtifactStoreSession


def create_parents(
    session: ArtifactStoreSession,
    model_id: str,
    version_id: str,
) -> None:
    """
    Create organizational elements within a store. If they exist, this operation is a noop.
    :param session: The store instance in which elements are created
    :param model_id: The model identifier
    :param version_id: The version identifier
    """
    try:
        session.create_model(ModelCreate(identifier=model_id))
    except errors.ErrorAlreadyExists:
        pass

    try:
        session.create_version(model_id, VersionCreate(identifier=version_id))
    except errors.ErrorAlreadyExists:
        pass
