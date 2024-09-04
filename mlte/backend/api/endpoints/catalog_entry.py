"""
mlte/backend/api/endpoints/catalog.py

Test Catalog Entry CRUD endpoint.
"""
from __future__ import annotations

from typing import List

from fastapi import APIRouter, HTTPException

import mlte.backend.api.codes as codes
import mlte.store.error as errors
from mlte.backend.api import dependencies
from mlte.backend.api.auth.authorization import AuthorizedUser
from mlte.backend.api.error_handlers import raise_http_internal_error
from mlte.catalog.model import CatalogEntry
from mlte.store.query import Query

# The router exported by this submodule
router = APIRouter()


@router.post("/{catalog_id}/entry")
def create_catalog_entry(
    *,
    catalog_id: str,
    entry: CatalogEntry,
    current_user: AuthorizedUser,
) -> CatalogEntry:
    """
    Create a MLTE catalog entry.
    :param entry: The catalog entry to create
    :return: The created catalog entry
    """
    with dependencies.catalog_stores_session() as catalog_stores:
        try:
            entry.header.catalog_id = catalog_id
            return catalog_stores.get_session(catalog_id).entry_mapper.create(
                entry
            )
        except errors.ErrorNotFound as e:
            raise HTTPException(
                status_code=codes.NOT_FOUND, detail=f"{e} not found."
            )
        except errors.ErrorAlreadyExists as e:
            raise HTTPException(
                status_code=codes.ALREADY_EXISTS, detail=f"{e} already exists."
            )
        except Exception as e:
            raise_http_internal_error(e)


@router.put("/{catalog_id}/entry")
def edit_catalog_entry(
    *,
    catalog_id: str,
    entry: CatalogEntry,
    current_user: AuthorizedUser,
) -> CatalogEntry:
    """
    Edit a MLTE entry.
    :param entry: The entry to edit
    :return: The edited entry
    """
    with dependencies.catalog_stores_session() as catalog_stores:
        try:
            entry.header.catalog_id = catalog_id
            return catalog_stores.get_session(catalog_id).entry_mapper.edit(
                entry
            )
        except errors.ErrorNotFound as e:
            raise HTTPException(
                status_code=codes.NOT_FOUND, detail=f"{e} not found."
            )
        except Exception as e:
            raise_http_internal_error(e)


@router.get("/{catalog_id}/entry/{catalog_entry_id}")
def read_catalog_entry(
    *,
    catalog_id: str,
    catalog_entry_id: str,
    current_user: AuthorizedUser,
) -> CatalogEntry:
    """
    Read a MLTE entry.
    :param catalog_entry_id: The entry name
    :return: The read entry
    """
    with dependencies.catalog_stores_session() as catalog_stores:
        try:
            return catalog_stores.get_session(catalog_id).entry_mapper.read(
                catalog_entry_id
            )
        except errors.ErrorNotFound as e:
            raise HTTPException(
                status_code=codes.NOT_FOUND, detail=f"{e} not found."
            )
        except Exception as e:
            raise_http_internal_error(e)


@router.delete("/{catalog_id}/entry/{catalog_entry_id}")
def delete_catalog_entry(
    *,
    catalog_id: str,
    catalog_entry_id: str,
    current_user: AuthorizedUser,
) -> CatalogEntry:
    """
    Delete a MLTE catalog entry.
    :param catalog_entry_id: The entry id
    :return: The deleted entry
    """
    with dependencies.catalog_stores_session() as catalog_stores:
        try:
            return catalog_stores.get_session(catalog_id).entry_mapper.delete(
                catalog_entry_id
            )
        except errors.ErrorNotFound as e:
            raise HTTPException(
                status_code=codes.NOT_FOUND, detail=f"{e} not found."
            )
        except Exception as e:
            raise_http_internal_error(e)


@router.get("/{catalog_id}/entry/")
def list_catalog_entries(
    *,
    catalog_id: str,
    current_user: AuthorizedUser,
) -> List[CatalogEntry]:
    """
    List MLTE catalog entries, with details for each entry.
    :return: A collection of entries with their details.
    """
    with dependencies.catalog_stores_session() as catalog_stores:
        try:
            return catalog_stores.get_session(
                catalog_id
            ).entry_mapper.list_details()
        except errors.ErrorNotFound as e:
            raise HTTPException(
                status_code=codes.NOT_FOUND, detail=f"{e} not found."
            )
        except Exception as e:
            raise_http_internal_error(e)


@router.get("s/entry")
def list_catalog_entries_all_catalogs(
    *,
    current_user: AuthorizedUser,
) -> List[CatalogEntry]:
    """
    List MLTE catalog entries, with details for each entry.
    :return: A collection of entries with their details.
    """
    with dependencies.catalog_stores_session() as catalog_stores:
        try:
            return catalog_stores.list_details()
        except Exception as e:
            raise_http_internal_error(e)


@router.post("s/entry/search")
def search(
    *,
    query: Query,
    current_user: AuthorizedUser,
) -> List[CatalogEntry]:
    """
    Search MLTE catalog entries, with details for each entry.
    :param query: The search query.
    :return: A collection of entries with their details for the provided query.
    """
    with dependencies.catalog_stores_session() as catalog_stores:
        try:
            return catalog_stores.search(query=query)
        except Exception as e:
            raise_http_internal_error(e)


# TODO:
# 1. Implement HTTP Catalog Store
# 2. Review default groups for test catalog
# 3. Add unit tests for catalog endpoints
