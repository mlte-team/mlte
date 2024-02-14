"""
mlte/store/artifact/underlying/rdbs/metadata_spec.py

Definition of the metadata (DB schema) for spec and validated spec in the artifact store,
as well as converstions between schema and internal models.
"""
from __future__ import annotations

from typing import List, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from mlte.store.artifact.underlying.rdbs.metadata import (
    DBArtifactHeader,
    DBBase,
)
from mlte.store.artifact.underlying.rdbs.metadata_value import DBValue

# -------------------------------------------------------------------------
# Spec Elements
# -------------------------------------------------------------------------


class DBSpec(DBBase):
    __tablename__ = "spec"

    id: Mapped[int] = mapped_column(primary_key=True)
    artifact_header_id: Mapped[DBArtifactHeader] = mapped_column(
        ForeignKey("artifact_header.id")
    )

    artifact_header: Mapped[DBArtifactHeader] = relationship(
        back_populates="body_spec", cascade="all"
    )
    properties: Mapped[List[DBProperty]] = relationship(
        back_populates="spec", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Spec(id={self.id!r}, artifact_header={self.artifact_header!r}, properties={self.properties!r})"


class DBProperty(DBBase):
    __tablename__ = "property"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    rationale: Mapped[str]
    module: Mapped[str]
    spec_id: Mapped[int] = mapped_column(ForeignKey("spec.id"))

    spec: Mapped[DBSpec] = relationship(back_populates="properties")
    conditions: Mapped[List[DBCondition]] = relationship(
        cascade="all, delete-orphan", back_populates="property"
    )
    results: Mapped[List[DBResult]] = relationship(back_populates="property")

    def __repr__(self) -> str:
        return f"Property(id={self.id!r}, name={self.name!r}, description={self.description!r}, rationale={self.rationale!r}, module={self.module!r})"


class DBCondition(DBBase):
    __tablename__ = "condition"

    id: Mapped[int] = mapped_column(primary_key=True)
    measurement_id: Mapped[str]
    name: Mapped[str]
    arguments: Mapped[str]  # Json string of the aray of arguments.
    callback: Mapped[str]
    value_class: Mapped[str]
    property_id: Mapped[int] = mapped_column(ForeignKey("property.id"))

    property: Mapped[DBProperty] = relationship(back_populates="conditions")

    def __repr__(self) -> str:
        return f"Condition(id={self.id!r}, name={self.name!r}, arguments={self.arguments!r}, value_class={self.value_class!r}, property={self.property!r})"


# -------------------------------------------------------------------------
# ValidatedSpec Elements
# -------------------------------------------------------------------------


class DBValidatedSpec(DBBase):
    __tablename__ = "validated_spec"

    id: Mapped[int] = mapped_column(primary_key=True)
    artifact_header_id: Mapped[DBArtifactHeader] = mapped_column(
        ForeignKey("artifact_header.id")
    )
    spec_id: Mapped[Optional[int]] = mapped_column(ForeignKey("spec.id"))

    artifact_header: Mapped[DBArtifactHeader] = relationship(
        back_populates="body_validated_spec", cascade="all"
    )
    spec: Mapped[DBSpec] = relationship()
    results: Mapped[List[DBResult]] = relationship(
        back_populates="validated_spec", cascade="all"
    )

    def __repr__(self) -> str:
        return f"ValidatedSpec(id={self.id!r}, artifact_header={self.artifact_header!r}, spec={self.spec!r})"


class DBResult(DBBase):
    __tablename__ = "result"

    id: Mapped[int] = mapped_column(primary_key=True)
    measurement_id: Mapped[str]
    type: Mapped[str]
    message: Mapped[str]
    property_id: Mapped[int] = mapped_column(ForeignKey("property.id"))
    validated_spec_id: Mapped[int] = mapped_column(
        ForeignKey("validated_spec.id")
    )

    evidence_metadata: Mapped[DBEvidenceMetadata] = relationship(
        cascade="all, delete-orphan", back_populates="result"
    )
    validated_spec: Mapped[DBValidatedSpec] = relationship(
        back_populates="results"
    )
    property: Mapped[DBProperty] = relationship(back_populates="results")

    def __repr__(self) -> str:
        return f"Result(id={self.id!r}, type={self.type!r}, message={self.message!r}, evidence_metadata={self.evidence_metadata!r})"


class DBEvidenceMetadata(DBBase):
    __tablename__ = "evidence_metadata"

    id: Mapped[int] = mapped_column(primary_key=True)
    identifier: Mapped[str]
    measurement_type: Mapped[str]
    info: Mapped[Optional[str]]
    result_id: Mapped[Optional[int]] = mapped_column(ForeignKey("result.id"))
    value_id: Mapped[Optional[int]] = mapped_column(ForeignKey("value.id"))

    result: Mapped[DBResult] = relationship(back_populates="evidence_metadata")
    value: Mapped[DBValue] = relationship(back_populates="evidence_metadata")

    def __repr__(self) -> str:
        return f"EvidenceMetadata(id={self.id!r}, identifier={self.identifier!r}, measurement_type={self.measurement_type!r}, info={self.info!r})"
