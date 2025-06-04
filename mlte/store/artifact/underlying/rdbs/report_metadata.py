"""Definition of the metadata (DB schema) forcreport elements in the artifact store."""

from __future__ import annotations

from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from mlte.store.artifact.underlying.rdbs.card_metadata import DBNegotiationCard
from mlte.store.artifact.underlying.rdbs.main_metadata import DBArtifact, DBBase
from mlte.store.artifact.underlying.rdbs.result_metadata import DBTestResults
from mlte.store.artifact.underlying.rdbs.suite_metadata import DBTestSuite


class DBReport(DBBase):
    __tablename__ = "report"

    # General
    id: Mapped[int] = mapped_column(primary_key=True)
    artifact_id: Mapped[DBArtifact] = mapped_column(
        ForeignKey(DBArtifact.get_id_column())
    )
    artifact: Mapped[DBArtifact] = relationship(
        back_populates="body_report",
        cascade="all",
    )

    # Negotiation Card.
    negotiation_card_identifier: Mapped[str] = mapped_column()
    negotiation_card_id: Mapped[int] = mapped_column(
        ForeignKey(DBNegotiationCard.get_id_column())
    )
    negotiation_card: Mapped[DBNegotiationCard] = relationship()

    # Test Suite.
    test_suite_identifier: Mapped[str] = mapped_column()
    test_suite_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey(DBTestSuite.get_id_column(), ondelete="SET NULL")
    )
    test_suite: Mapped[DBTestSuite] = relationship()

    # Results.
    test_results_identifier: Mapped[str] = mapped_column()
    test_results_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey(DBTestResults.get_id_column(), ondelete="SET NULL")
    )
    test_results: Mapped[DBTestResults] = relationship()

    # Comments
    comments: Mapped[list[DBCommentDescriptor]] = relationship(
        back_populates="report", cascade="all, delete-orphan"
    )

    # Analysis.
    quantitative_analysis_content: Mapped[Optional[str]]

    def __repr__(self) -> str:
        return f"Report(id={self.id!r}, artifact={self.artifact!r})"


class DBCommentDescriptor(DBBase):
    __tablename__ = "report_comment"

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[Optional[str]]
    report_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(DBReport.get_id_column())
    )

    report: Mapped[DBReport] = relationship(back_populates="comments")

    def __repr__(self) -> str:
        return f"Comment(id={self.id!r}, content={self.content!r})"
