"""
mlte/store/artifact/underlying/rdbs/metadata.py

Definition of the metadata (DB schema) for the artifact store.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import ForeignKey, UniqueConstraint, select
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    relationship,
)

from mlte.artifact.type import ArtifactType

# Needed to avoid circular import issues from relationships between tables classes.
if TYPE_CHECKING:
    from mlte.store.artifact.underlying.rdbs.metadata_nc import (
        DBNegotiationCard,
    )
    from mlte.store.artifact.underlying.rdbs.metadata_spec import (
        DBSpec,
        DBValidatedSpec,
    )
else:
    DBNegotiationCard = "DBNegotiationCard"
    DBSpec = "DBSpec"
    DBValidatedSpec = "DBValidatedSpec"


class DBBase(DeclarativeBase):
    """Base class for DB table classes."""

    pass


# -------------------------------------------------------------------------
# Structural Elements
# -------------------------------------------------------------------------


class DBNamespace(DBBase):
    __tablename__ = "namespace"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    models: Mapped[List[DBModel]] = relationship(back_populates="namespace")

    __table_args__ = (UniqueConstraint("name", name="_namespace_identifier"),)

    def __repr__(self) -> str:
        return f"Namespace(id={self.id!r}, name={self.name!r})"


class DBModel(DBBase):
    __tablename__ = "model"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    namespace_id = mapped_column(ForeignKey("namespace.id"))

    namespace: Mapped[DBNamespace] = relationship(back_populates="models")
    versions: Mapped[List[DBVersion]] = relationship(back_populates="model")

    __table_args__ = (UniqueConstraint("name", name="_model_identifier"),)

    def __repr__(self) -> str:
        return f"Version(id={self.id!r}, name={self.name!r})"


class DBVersion(DBBase):
    __tablename__ = "version"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    model_id = mapped_column(ForeignKey("model.id"))

    model: Mapped[DBModel] = relationship(back_populates="versions")

    __table_args__ = (UniqueConstraint("name", name="_version_identifier"),)

    def __repr__(self) -> str:
        return f"Version(id={self.id!r}, name={self.name!r})"


# -------------------------------------------------------------------------
# General Artifact Elements
# -------------------------------------------------------------------------


class DBArtifactType(DBBase):
    __tablename__ = "artifact_type"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    def __repr__(self) -> str:
        return f"ArtifactType(id={self.id!r}, name={self.name!r})"


class DBArtifactHeader(DBBase):
    __tablename__ = "artifact_header"

    id: Mapped[int] = mapped_column(primary_key=True)
    identifier: Mapped[str]
    timestamp: Mapped[int]
    type_id: Mapped[int] = mapped_column(ForeignKey("artifact_type.id"))
    version_id: Mapped[int] = mapped_column(ForeignKey("version.id"))

    type: Mapped[DBArtifactType] = relationship()
    version: Mapped[DBVersion] = relationship()
    body_spec: Mapped[Optional[DBSpec]] = relationship(
        back_populates="artifact_header"
    )
    body_validated_spec: Mapped[Optional[DBValidatedSpec]] = relationship(
        back_populates="artifact_header"
    )
    body_negotiation_card: Mapped[Optional[DBNegotiationCard]] = relationship(
        back_populates="artifact_header"
    )

    def __repr__(self) -> str:
        return f"ArtifactHeader(id={self.id!r}, identifier={self.identifier!r}, timestamp={self.timestamp!r}, type={self.type!r})"


# -------------------------------------------------------------------------
# Pre-filled table functions.
# -------------------------------------------------------------------------


def init_artifact_types(session: Session):
    """Initializes the table with the configured artifact types."""
    if session.scalars(select(DBArtifactType)).first() is None:
        types = [e.value for e in ArtifactType]
        for type in types:
            type_obj = DBArtifactType(name=type)
            session.add(type_obj)
        session.commit()
