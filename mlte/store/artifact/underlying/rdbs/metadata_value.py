"""
mlte/store/artifact/underlying/rdbs/metadata_value.py

Definition of the metadata (DB schema) for Values in the artifact store.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, select
from sqlalchemy.orm import Mapped, Session, mapped_column, relationship

from mlte.store.artifact.underlying.rdbs.metadata import (
    DBArtifactHeader,
    DBBase,
)
from mlte.value.model import ValueType

# Needed to avoid circular import issues from relationships between tables classes.
if TYPE_CHECKING:
    from mlte.store.artifact.underlying.rdbs.metadata_spec import (
        DBEvidenceMetadata,
    )
else:
    DBEvidenceMetadata = "DBEvidenceMetadata"


# -------------------------------------------------------------------------
# Value Elements
# -------------------------------------------------------------------------


class DBValueType(DBBase):
    __tablename__ = "value_type"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    def __repr__(self) -> str:
        return f"ValueType(id={self.id!r}, name={self.name!r})"


class DBValue(DBBase):
    __tablename__ = "value"

    id: Mapped[int] = mapped_column(primary_key=True)
    artifact_header_id: Mapped[DBArtifactHeader] = mapped_column(
        ForeignKey("artifact_header.id")
    )
    value_class: Mapped[str]
    value_type: Mapped[str]
    data_json: Mapped[str]

    artifact_header: Mapped[DBArtifactHeader] = relationship(
        back_populates="body_value", cascade="all"
    )
    evidence_metadata: Mapped[DBEvidenceMetadata] = relationship(
        back_populates="value", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Value(id={self.id!r}, artifact_header={self.artifact_header!r}, value_class={self.value_class!r}, data_json={self.data_json!r})"


# -------------------------------------------------------------------------
# Pre-filled table functions.
# -------------------------------------------------------------------------


def init_value_types(session: Session):
    """Initializes the table with the configured value types."""
    if session.scalars(select(DBValueType)).first() is None:
        types = [e.value for e in ValueType]
        for type in types:
            type_obj = DBValueType(name=type)
            session.add(type_obj)
        session.commit()
