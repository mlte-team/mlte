"""
Definition of the metadata (DB schema) for TestSuite and TestResults in the artifact store,
as well as conversions between schema and internal models.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from mlte.store.artifact.underlying.rdbs.main_metadata import DBArtifact, DBBase
from mlte.store.artifact.underlying.rdbs.suite_metadata import DBTestSuite

# Needed to avoid circular import issues from relationships between tables classes.
if TYPE_CHECKING:
    from mlte.store.artifact.underlying.rdbs.evidence_metadata import (
        DBEvidenceMetadata,
    )
else:
    DBEvidenceMetadata = "DBEvidenceMetadata"


# -------------------------------------------------------------------------
# TestResults Elements
# -------------------------------------------------------------------------


class DBTestResults(DBBase):
    __tablename__ = "test_results"

    id: Mapped[int] = mapped_column(primary_key=True)
    artifact_id: Mapped[Optional[DBArtifact]] = mapped_column(
        ForeignKey(DBArtifact.get_id_column())
    )
    test_suite_identifier: Mapped[str] = mapped_column()
    test_suite_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(DBTestSuite.get_id_column())
    )

    artifact: Mapped[Optional[DBArtifact]] = relationship(
        back_populates="body_test_results", cascade="all"
    )
    test_suite: Mapped[DBTestSuite] = relationship()
    results: Mapped[list[DBResult]] = relationship(
        back_populates="test_results", cascade="all"
    )

    def __repr__(self) -> str:
        return f"TestResults(id={self.id!r}, artifact={self.artifact!r}, test_suite={self.test_suite!r})"


class DBResult(DBBase):
    __tablename__ = "result"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str]
    message: Mapped[str]
    test_results_id: Mapped[int] = mapped_column(ForeignKey("test_results.id"))

    evidence_metadata: Mapped[DBEvidenceMetadata] = relationship(
        cascade="all, delete-orphan", back_populates="result"
    )
    test_results: Mapped[DBTestResults] = relationship(back_populates="results")

    def __repr__(self) -> str:
        return f"Result(id={self.id!r}, type={self.type!r}, message={self.message!r}, evidence_metadata={self.evidence_metadata!r})"
