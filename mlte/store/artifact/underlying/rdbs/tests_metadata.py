"""
Definition of the metadata (DB schema) for TestSuite and TestResults in the artifact store,
as well as conversions between schema and internal models.
"""

from __future__ import annotations

from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from mlte.store.artifact.underlying.rdbs.main_metadata import DBArtifact, DBBase

# -------------------------------------------------------------------------
# TestSuite Elements
# -------------------------------------------------------------------------


class DBTestSuite(DBBase):
    __tablename__ = "test_suite"

    id: Mapped[int] = mapped_column(primary_key=True)
    artifact_id: Mapped[Optional[DBArtifact]] = mapped_column(
        ForeignKey(DBArtifact.get_id_column())
    )

    artifact: Mapped[Optional[DBArtifact]] = relationship(
        back_populates="body_test_suite", cascade="all"
    )
    test_cases: Mapped[list[DBTestCase]] = relationship(
        back_populates="test_suite", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"TestSuite(id={self.id!r}, artifact={self.artifact!r}, test_cases={self.test_cases!r})"


class DBTestCase(DBBase):
    __tablename__ = "test_case"

    id: Mapped[int] = mapped_column(primary_key=True)
    identifier: Mapped[str]
    goal: Mapped[str]
    qas_list: Mapped[str]
    measurement_metadata: Mapped[Optional[str]]
    validator: Mapped[Optional[str]]
    test_suite_id: Mapped[int] = mapped_column(
        ForeignKey(DBTestSuite.get_id_column())
    )

    test_suite: Mapped[DBTestSuite] = relationship(back_populates="test_cases")

    def __repr__(self) -> str:
        return f"TestCase(id={self.id!r}, name={self.identifier!r}, goal={self.goal!r})"
