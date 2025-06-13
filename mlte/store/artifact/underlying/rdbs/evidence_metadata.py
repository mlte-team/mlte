"""Definition of the metadata (DB schema) for Values in the artifact store."""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, select
from sqlalchemy.orm import Mapped, Session, mapped_column, relationship

from mlte.evidence.model import EvidenceType
from mlte.store.artifact.underlying.rdbs.main_metadata import DBArtifact, DBBase

# Needed to avoid circular import issues from relationships between tables classes.
if TYPE_CHECKING:
    from mlte.store.artifact.underlying.rdbs.result_metadata import DBResult
else:
    DBResult = "DBResult"


# -------------------------------------------------------------------------
# Evidence Elements
# -------------------------------------------------------------------------


class DBEvidenceType(DBBase):
    __tablename__ = "evidence_type"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    def __repr__(self) -> str:
        return f"EvidenceType(id={self.id!r}, name={self.name!r})"


class DBEvidence(DBBase):
    __tablename__ = "evidence"

    id: Mapped[int] = mapped_column(primary_key=True)
    artifact_id: Mapped[DBArtifact] = mapped_column(
        ForeignKey(DBArtifact.get_id_column())
    )
    evidence_class: Mapped[str]
    evidence_type: Mapped[str]
    data_json: Mapped[str]

    artifact: Mapped[DBArtifact] = relationship(
        back_populates="body_evidence", cascade="all"
    )
    evidence_metadata: Mapped[DBEvidenceMetadata] = relationship(
        back_populates="evidence", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Evidence(id={self.id!r}, artifact={self.artifact!r}, evidence_class={self.evidence_class!r}, data_json={self.data_json!r})"


class DBEvidenceMetadata(DBBase):
    __tablename__ = "evidence_metadata"

    id: Mapped[int] = mapped_column(primary_key=True)
    test_case_id: Mapped[str]
    measurement: Mapped[str]
    result_id: Mapped[Optional[int]] = mapped_column(ForeignKey("result.id"))
    evidence_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(DBEvidence.get_id_column())
    )

    result: Mapped[DBResult] = relationship(back_populates="evidence_metadata")
    evidence: Mapped[DBEvidence] = relationship(
        back_populates="evidence_metadata"
    )

    def __repr__(self) -> str:
        return f"EvidenceMetadata(id={self.id!r}, identifier={self.test_case_id!r}, measurement={self.measurement!r})"


# -------------------------------------------------------------------------
# Pre-filled table functions.
# -------------------------------------------------------------------------


def init_evidence_types(session: Session):
    """Initializes the table with the configured evidence types."""
    if session.scalars(select(DBEvidenceType)).first() is None:
        types = [e.value for e in EvidenceType]
        for type in types:
            type_obj = DBEvidenceType(name=type)
            session.add(type_obj)
        session.commit()
