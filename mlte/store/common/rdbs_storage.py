"""
mlte/store/common/rdbs/store.py

Base RDBS store.
"""
from __future__ import annotations

from typing import Callable, Optional

import sqlalchemy
import sqlalchemy.orm
import sqlalchemy_utils
from sqlalchemy.orm import DeclarativeBase

from mlte.store.base import StoreURI
from mlte.store.common.storage import Storage


class RDBStorage(Storage):
    """Helper to setup RDB storage.."""

    def __init__(
        self,
        uri: StoreURI,
        base_class: DeclarativeBase,
        init_tables_func: Optional[Callable[[sqlalchemy.Engine], None]],
        **kwargs,
    ) -> None:
        super().__init__(uri)

        self.engine = sqlalchemy.create_engine(uri.uri, **kwargs)
        """The underlying DB engine access."""

        # Create the DB if it doesn't exist already.
        if not sqlalchemy_utils.database_exists(self.engine.url):
            sqlalchemy_utils.create_database(self.engine.url)

        # Creates the DB items if they don't exist already.
        self._create_tables(base_class)
        if init_tables_func:
            init_tables_func(self.engine)

    def _create_tables(self, base_class: DeclarativeBase):
        """Creates all items, if they don't exist already."""
        base_class.metadata.create_all(self.engine)

    def close(self):
        """Cleanup."""
        self.engine.dispose()
