"""Definition of the metadata (DB schema) for the artifact store."""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

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
    from mlte.store.artifact.underlying.rdbs.card_metadata import (
        DBNegotiationCard,
    )
    from mlte.store.artifact.underlying.rdbs.evidence_metadata import DBEvidence
    from mlte.store.artifact.underlying.rdbs.report_metadata import DBReport
    from mlte.store.artifact.underlying.rdbs.result_metadata import (
        DBTestResults,
    )
    from mlte.store.artifact.underlying.rdbs.suite_metadata import DBTestSuite
else:
    DBNegotiationCard = "DBNegotiationCard"
    DBTestSuite = "DBTestSuite"
    DBTestResults = "DBTestResults"
    DBReport = "DBReport"
    DBEvidence = "DBEvidence"


class DBBase(DeclarativeBase):
    """Base class for DB table classes."""

    @classmethod
    def get_id_column(cls):
        """Method to simplify access to id column, useful for ForeignKeys."""
        return cls.__table__.c.id


# -------------------------------------------------------------------------
# Structural Elements
# -------------------------------------------------------------------------


class DBModel(DBBase):
    __tablename__ = "model"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    versions: Mapped[list[DBVersion]] = relationship(
        back_populates="model", cascade="all, delete-orphan"
    )

    __table_args__ = (UniqueConstraint("name", name="_model_identifier_uc"),)

    def __repr__(self) -> str:
        return f"Model(id={self.id!r}, name={self.name!r}, versions={self.versions})"


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


class DBArtifact(DBBase):
    __tablename__ = "artifact"

    id: Mapped[int] = mapped_column(primary_key=True)
    identifier: Mapped[str]
    timestamp: Mapped[int] = mapped_column(BigInteger)
    username: Mapped[Optional[str]]

    type_id: Mapped[int] = mapped_column(
        ForeignKey(DBArtifactType.get_id_column())
    )
    version_id: Mapped[int] = mapped_column(
        ForeignKey(DBVersion.get_id_column())
    )

    type: Mapped[DBArtifactType] = relationship()
    version: Mapped[DBVersion] = relationship()

    body_negotiation_card: Mapped[Optional[DBNegotiationCard]] = relationship(
        back_populates="artifact", cascade="all, delete-orphan"
    )
    body_test_suite: Mapped[Optional[DBTestSuite]] = relationship(
        back_populates="artifact", cascade="all, delete-orphan"
    )
    body_evidence: Mapped[Optional[DBEvidence]] = relationship(
        back_populates="artifact", cascade="all, delete-orphan"
    )
    body_test_results: Mapped[Optional[DBTestResults]] = relationship(
        back_populates="artifact", cascade="all, delete-orphan"
    )
    body_report: Mapped[Optional[DBReport]] = relationship(
        back_populates="artifact", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Artifact(id={self.id!r}, identifier={self.identifier!r}, timestamp={self.timestamp!r}, type={self.type!r})"


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
