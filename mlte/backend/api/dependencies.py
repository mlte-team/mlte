"""
mlte/backend/api/dependencies.py

This file defines common dependencies that are used by API functions.
In practice, this ensures that the backend is initialized prior to
attempting to service any incoming requests.

Originally, I used FastAPI dependency injection to manage dependencies,
but it became so much harder to manage the fact that initialization was
occurring at import time rather than at invocation time that I removed
this in favor of slightly more brittle but eminently more workable
solution that involves manual context management with a global state object.
"""

from contextlib import contextmanager
from typing import Generator

from mlte.backend.state import state
from mlte.store.artifact.store import ArtifactStoreSession
from mlte.store.catalog.group import CatalogStoreGroupSession
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
