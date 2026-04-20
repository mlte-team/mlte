"""Functions for bundling and unbundling remote catalog ids into the standard CatalogEntry entity."""

from typing import Optional

from mlte.catalog.model import CatalogEntry

COMPOSITE_ID_SEPARATOR = "--"


def split_ids(composite_id: str) -> tuple[Optional[str], str]:
    """Split a composite id, returning the first part, and the rest."""
    # We'll split it into two parts. If less, we just return the whole thing as the entry id.
    catalog_id = None
    entry_id = composite_id
    parts = composite_id.split(COMPOSITE_ID_SEPARATOR, maxsplit=1)
    if len(parts) == 2:
        catalog_id = parts[0]
        entry_id = parts[1]

    return catalog_id, entry_id


def generate_composite_id(id1: Optional[str], id2: str) -> str:
    """Creates a composite id given two ids."""
    if id1:
        return f"{id1}{COMPOSITE_ID_SEPARATOR}{id2}"
    else:
        return id2


def remove_remote_catalog_id(entry: CatalogEntry) -> CatalogEntry:
    """
    Creates a new entry from the given one, removing the remote catalog id from its identifier.

    :param entry: An entry with its entry_id being a combination of the remote catalog id the entry is in and the real entry id.
    :return: An entry with its expected entry id, as well as its catalog_id being the final remote catalog id where it is stored remotely.
    """
    new_entry = entry.model_copy()
    new_entry.header = entry.header.model_copy()

    remote_catalog_id, entry_id = split_ids(entry.header.identifier)
    new_entry.header.identifier = entry_id
    new_entry.header.catalog_id = remote_catalog_id

    return new_entry
