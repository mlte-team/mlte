"""
mlte/store/util.py

Common utilities for store implementations.
"""

import mlte.store.error as errors
from mlte.store.base import StoreSession
from mlte.context.model import NamespaceCreate, ModelCreate, VersionCreate


def create_parents(
    session: StoreSession, namespace_id: str, model_id: str, version_id: str
) -> None:
    """
    Create organizational elements within a store. If they exist, this operation is a noop.
    :param store: The store instance in which elements are created
    :param namespace_id: The namespace identifier
    :param model_id: The model identifier
    :param version_id: The version identifier
    """
    try:
        session.create_namespace(NamespaceCreate(identifier=namespace_id))
    except errors.ErrorAlreadyExists:
        pass

    try:
        session.create_model(namespace_id, ModelCreate(identifier=model_id))
    except errors.ErrorAlreadyExists:
        pass

    try:
        session.create_version(
            namespace_id, model_id, VersionCreate(identifier=version_id)
        )
    except errors.ErrorAlreadyExists:
        pass
