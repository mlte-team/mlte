"""
mlte/backend/core/state_stores.py

Managed store sessions obtained from the global state context.
"""

from contextlib import contextmanager
from typing import Generator

from mlte.backend.core.state import state
from mlte.store.artifact.store import ArtifactStoreSession
from mlte.store.catalog.catalog_group import CatalogStoreGroupSession
from mlte.store.user.store_session import UserStoreSession


@contextmanager
def artifact_store_session() -> Generator[ArtifactStoreSession, None, None]:
    """
    Get a handle to underlying store session.
    :return: The session handle
    """
    session: ArtifactStoreSession = state.artifact_store.session()
    try:
        yield session
    finally:
        session.close()


@contextmanager
def user_store_session() -> Generator[UserStoreSession, None, None]:
    """
    Get a handle to underlying store session.
    :return: The session handle
    """
    session: UserStoreSession = state.user_store.session()
    try:
        yield session
    finally:
        session.close()


@contextmanager
def catalog_stores_session() -> Generator[CatalogStoreGroupSession, None, None]:
    """
    Get a handle to underlying store session.
    :return: The session handle
    """
    session: CatalogStoreGroupSession = state.catalog_stores.session()
    try:
        yield session
    finally:
        session.close()
