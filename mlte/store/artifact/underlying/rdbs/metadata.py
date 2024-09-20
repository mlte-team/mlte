"""
mlte/store/artifact/underlying/rdbs/metadata.py

Definition of the metadata (DB schema) for the artifact store.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import BigInteger, ForeignKey, UniqueConstraint, select
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
        DBReport,
    )
    from mlte.store.artifact.underlying.rdbs.metadata_spec import (
        DBSpec,
        DBValidatedSpec,
    )
    from mlte.store.artifact.underlying.rdbs.metadata_value import DBValue
else:
    DBNegotiationCard = "DBNegotiationCard"
    DBSpec = "DBSpec"
    DBValidatedSpec = "DBValidatedSpec"
    DBReport = "DBReport"
    DBValue = "DBValue"


class DBBase(DeclarativeBase):
    """Base class for DB table classes."""

    pass


# -------------------------------------------------------------------------
# Structural Elements
# -------------------------------------------------------------------------


class DBModel(DBBase):
    __tablename__ = "model"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    versions: Mapped[List[DBVersion]] = relationship(
        back_populates="model", cascade="all, delete-orphan"
    )

    __table_args__ = (UniqueConstraint("name", name="_model_identifier"),)

    def __repr__(self) -> str:
        return f"Version(id={self.id!r}, name={self.name!r})"


class DBVersion(DBBase):
    __tablename__ = "version"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    model_id = mapped_column(ForeignKey("model.id"))

    model: Mapped[DBModel] = relationship(back_populates="versions")

    __table_args__ = (
        UniqueConstraint("name", "model_id", name="_version_model_ids_uc"),
    )

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
    timestamp: Mapped[int] = mapped_column(BigInteger)
    username: Mapped[Optional[str]]

    type_id: Mapped[int] = mapped_column(ForeignKey("artifact_type.id"))
    version_id: Mapped[int] = mapped_column(ForeignKey("version.id"))

    type: Mapped[DBArtifactType] = relationship()
    version: Mapped[DBVersion] = relationship()
    body_spec: Mapped[Optional[DBSpec]] = relationship(
        back_populates="artifact_header", cascade="all, delete-orphan"
    )
    body_validated_spec: Mapped[Optional[DBValidatedSpec]] = relationship(
        back_populates="artifact_header", cascade="all, delete-orphan"
    )
    body_negotiation_card: Mapped[Optional[DBNegotiationCard]] = relationship(
        back_populates="artifact_header", cascade="all, delete-orphan"
    )
    body_report: Mapped[Optional[DBReport]] = relationship(
        back_populates="artifact_header", cascade="all, delete-orphan"
    )
    body_value: Mapped[Optional[DBValue]] = relationship(
        back_populates="artifact_header", cascade="all, delete-orphan"
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
