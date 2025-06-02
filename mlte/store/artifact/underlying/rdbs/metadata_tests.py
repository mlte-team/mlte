"""
Definition of the metadata (DB schema) for TestSuite and TestResults in the artifact store,
as well as converstions between schema and internal models.
"""

from __future__ import annotations

from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from mlte.store.artifact.underlying.rdbs.metadata import (
    DBArtifactHeader,
    DBBase,
)
from mlte.store.artifact.underlying.rdbs.metadata_evidence import DBEvidence

# -------------------------------------------------------------------------
# TestSuite Elements
# -------------------------------------------------------------------------


class DBTestSuite(DBBase):
    __tablename__ = "test_suite"

    id: Mapped[int] = mapped_column(primary_key=True)
    artifact_header_id: Mapped[DBArtifactHeader] = mapped_column(
        ForeignKey("artifact_header.id")
    )

    artifact_header: Mapped[DBArtifactHeader] = relationship(
        back_populates="body_test_suite", cascade="all"
    )
    test_cases: Mapped[list[DBTestCase]] = relationship(
        back_populates="test_suite", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"TestSuite(id={self.id!r}, artifact_header={self.artifact_header!r}, test_cases={self.test_cases!r})"


class DBTestCase(DBBase):
    __tablename__ = "test_case"

    id: Mapped[int] = mapped_column(primary_key=True)
    identifier: Mapped[str]
    goal: Mapped[str]
    qas_list: Mapped[str]
    measurement_metadata: Mapped[Optional[str]]
    validator: Mapped[Optional[str]]
    test_suite_id: Mapped[int] = mapped_column(ForeignKey("test_suite.id"))

    test_suite: Mapped[DBTestSuite] = relationship(back_populates="test_cases")

    def __repr__(self) -> str:
        return f"TestCase(id={self.id!r}, name={self.identifier!r}, goal={self.goal!r})"


# -------------------------------------------------------------------------
# TestResults Elements
# -------------------------------------------------------------------------


class DBTestResults(DBBase):
    __tablename__ = "test_results"

    id: Mapped[int] = mapped_column(primary_key=True)
    artifact_header_id: Mapped[DBArtifactHeader] = mapped_column(
        ForeignKey("artifact_header.id")
    )
    test_suite_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("test_suite.id")
    )

    artifact_header: Mapped[DBArtifactHeader] = relationship(
        back_populates="body_test_results", cascade="all"
    )
    test_suite: Mapped[DBTestSuite] = relationship()
    results: Mapped[list[DBResult]] = relationship(
        back_populates="test_results", cascade="all"
    )

    def __repr__(self) -> str:
        return f"TestResults(id={self.id!r}, artifact_header={self.artifact_header!r}, test_suite={self.test_suite!r})"


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


# -------------------------------------------------------------------------
# Common metadata.
# -------------------------------------------------------------------------


class DBEvidenceMetadata(DBBase):
    __tablename__ = "evidence_metadata"

    id: Mapped[int] = mapped_column(primary_key=True)
    test_case_id: Mapped[str]
    measurement: Mapped[str]
    result_id: Mapped[Optional[int]] = mapped_column(ForeignKey("result.id"))
    evidence_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("evidence.id")
    )

    result: Mapped[DBResult] = relationship(back_populates="evidence_metadata")
    evidence: Mapped[DBEvidence] = relationship(
        back_populates="evidence_metadata"
    )

    def __repr__(self) -> str:
        return f"EvidenceMetadata(id={self.id!r}, identifier={self.test_case_id!r}, measurement={self.measurement!r})"
