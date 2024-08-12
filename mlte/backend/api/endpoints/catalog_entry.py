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

# The router exported by this submodule
router = APIRouter()


@router.post("/catalog/{catalog_id}/entry")
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
            return catalog_stores.get_session(catalog_id).entry_mapper.create(
                entry
            )
        except errors.ErrorAlreadyExists as e:
            raise HTTPException(
                status_code=codes.ALREADY_EXISTS, detail=f"{e} already exists."
            )
        except Exception as e:
            raise_http_internal_error(e)


@router.put("/catalog/{catalog_id}/entry")
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
            return catalog_stores.get_session(catalog_id).entry_mapper.edit(
                entry
            )
        except errors.ErrorNotFound as e:
            raise HTTPException(
                status_code=codes.NOT_FOUND, detail=f"{e} not found."
            )
        except Exception as e:
            raise_http_internal_error(e)


@router.put("/catalog/{catalog_id}/entry/{catalog_entry_id}")
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


@router.get("/catalog/{catalog_id}/catalog_entry")
def list_catalog_entries(
    *,
    catalog_id: str,
    current_user: AuthorizedUser,
) -> List[str]:
    """
    List MLTE catalog entries.
    :return: A collection of catalog entry ids.
    """
    with dependencies.catalog_stores_session() as catalog_stores:
        try:
            return catalog_stores.get_session(catalog_id).entry_mapper.list()
        except Exception as e:
            raise_http_internal_error(e)


@router.get("/catalog/{catalog_id}/catalog_entries/details")
def list_catalog_entries_details(
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
        except Exception as e:
            raise_http_internal_error(e)


#NOTE: do we also need a separate endpoint with a list of only the ids of all catalog entries? Doubtful.
@router.get("/catalog_entries/details")
def list_catalog_entry_details_all_catalogs(
    *,
    current_user: AuthorizedUser,
) -> List[CatalogEntry]:
    """
    List MLTE catalog entries, with details for each entry.
    :return: A collection of entries with their details.
    """
    with dependencies.catalog_stores_session() as catalog_stores:
        try:
            return catalog_stores.list_entries()
        except Exception as e:
            raise_http_internal_error(e)


@router.put("/catalog/{catalog_id}/entry/{catalog_entry_id}")
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


# TODO: add endpoint for search functionality.
