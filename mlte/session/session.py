"""Manages session info: context (model and version) and stores."""

from __future__ import annotations

import os
from typing import Optional

import mlte.store.artifact.util as storeutil
from mlte.context.context import Context
from mlte.custom_list.custom_list_names import CustomListName
from mlte.session.session_stores import SessionStores, setup_stores


class Session:
    """
    The Session data structure encapsulates package-wide state.

    The primary function of the Session data structure is to provide
    convenient access to the MLTE context for application developers.
    """

    ENV_CONTEXT_MODEL_VAR = "MLTE_CONTEXT_MODEL"
    ENV_CONTEXT_VERSION_VAR = "MLTE_CONTEXT_VERSION"
    ENV_STORE_URI_VAR = "MLTE_STORE_URI"
    """Environment variables to get model, version and store_uri from, if needed."""

    def __init__(self):
        """Constructors, just resets all vars."""
        self.reset()

    def reset(self):
        """Resets all internal state to defaults."""
        self._context: Optional[Context] = None
        """The MLTE context for the session."""

        self._stores: Optional[SessionStores] = None
        """All stores in this session."""

    @property
    def context(self) -> Context:
        if self._context is None:
            # If the context has not been manually set, get it from environment.
            model_context = self._get_env_var(self.ENV_CONTEXT_MODEL_VAR)
            version_context = self._get_env_var(self.ENV_CONTEXT_VERSION_VAR)
            if model_context and version_context:
                self._context = Context(
                    model=model_context, version=version_context
                )
            else:
                raise RuntimeError(
                    "Must initialize MLTE context for session, either manually or through environment variables."
                )

        return self._context

    @property
    def stores(self) -> SessionStores:
        if self._stores is None:
            # If the stores have not been manually set, get URI from environment.
            stores_uri = self._get_env_var(self.ENV_STORE_URI_VAR)
            if stores_uri:
                self._stores = setup_stores(stores_uri)
            else:
                raise RuntimeError(
                    "Must initialize store URI, either manually or through environment variables."
                )

        return self._stores

    def _set_context(self, context: Context) -> None:
        """Set the session context."""
        self._context = context

    def _set_stores(self, stores: SessionStores) -> None:
        """Set the session stores."""
        self._stores = stores

    def _get_env_var(self, env_var: str) -> Optional[str]:
        """Get env var or return none if does not exist."""
        return os.environ.get(env_var, None)

    def create_context(self):
        """Creates the currently configured context in the currently configured session. Fails if either is not set. Does nothing if already created."""
        artifact_store = self.stores.artifact_store
        context = self.context
        storeutil.create_parents(
            artifact_store.session(), context.model, context.version
        )


# Globally-accessible application state
g_session = Session()


def reset_session() -> None:
    """Used to reset session if needed."""
    g_session.reset()


def session() -> Session:
    """Return the package global session."""
    return g_session


def set_context(model_id: str, version_id: str, lazy: bool = True):
    """
    Set the global MLTE context.
    :param model_id: The model identifier
    :param version_id: The version identifier
    :param lazy: Whether to wait to create the context until an artifact is written (True), or to eagerly create it immediately (False).
    """
    g_session._set_context(Context(model_id, version_id))
    if not lazy:
        g_session.create_context()


def set_store(store_uri: str):
    """
    Set the global MLTE context store URI.
    :param store_uri: The store URI string
    """
    g_session._set_stores(setup_stores(store_uri))


def add_catalog_store(catalog_store_uri: str, id: str):
    """
    Adds a global MLTE catalog store URI.
    :param catalog_store_uri: The catalog store URI string
    """
    g_session.stores.add_catalog_store_from_uri(catalog_store_uri, id)


def print_custom_list_entries(list_name: CustomListName) -> None:
    """Prints custom list entries in a user-friendly way."""
    entry_list = g_session.stores.custom_list_store.session().custom_list_entry_mapper.list_details(
        list_name
    )
    for entry in entry_list:
        print(str(entry))
