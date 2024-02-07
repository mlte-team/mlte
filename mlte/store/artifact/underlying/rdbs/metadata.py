"""
mlte/store/artifact/underlying/rdbs/metadata.py

Definition of the metadata (DB schema) for the artifact store.
"""
from __future__ import annotations

from typing import List, Optional

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


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

    def __repr__(self) -> str:
        return f"ArtifactHeader(id={self.id!r}, identifier={self.identifier!r}, timestamp={self.timestamp!r}, type={self.type!r})"


# -------------------------------------------------------------------------
# Spec and Validated Spec Elements
# -------------------------------------------------------------------------


class DBSpec(DBBase):
    __tablename__ = "spec"

    id: Mapped[int] = mapped_column(primary_key=True)
    artifact_header_id: Mapped[DBArtifactHeader] = mapped_column(
        ForeignKey("artifact_header.id")
    )

    artifact_header: Mapped[DBArtifactHeader] = relationship(
        back_populates="body_spec"
    )
    properties: Mapped[List[DBProperty]] = relationship(back_populates="spec")

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
        back_populates="property"
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
        return f"Property(id={self.id!r}, name={self.name!r}, arguments={self.arguments!r}, value_class={self.value_class!r}, property={self.property!r})"


class DBValidatedSpec(DBBase):
    __tablename__ = "validated_spec"

    id: Mapped[int] = mapped_column(primary_key=True)
    artifact_header_id: Mapped[DBArtifactHeader] = mapped_column(
        ForeignKey("artifact_header.id")
    )
    spec_id: Mapped[Optional[int]] = mapped_column(ForeignKey("spec.id"))

    artifact_header: Mapped[DBArtifactHeader] = relationship(
        back_populates="body_validated_spec"
    )
    spec: Mapped[DBSpec] = relationship()
    results: Mapped[List[DBResult]] = relationship(
        back_populates="validated_spec"
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
        back_populates="result"
    )
    validated_spec: Mapped[DBValidatedSpec] = relationship(
        back_populates="results"
    )
    property: Mapped[DBProperty] = relationship(back_populates="results")

    def __repr__(self) -> str:
        return f"Property(id={self.id!r}, type={self.type!r}, message={self.message!r}, evidence_metadata={self.evidence_metadata!r})"


class DBEvidenceMetadata(DBBase):
    __tablename__ = "evidence_metadata"

    id: Mapped[int] = mapped_column(primary_key=True)
    identifier: Mapped[str]
    measurement_type: Mapped[str]
    info: Mapped[str]
    result_id: Mapped[int] = mapped_column(ForeignKey("result.id"))

    result: Mapped[DBResult] = relationship(back_populates="evidence_metadata")

    def __repr__(self) -> str:
        return f"Property(id={self.id!r}, identifier={self.identifier!r}, measurement_type={self.measurement_type!r}, info={self.info!r})"
