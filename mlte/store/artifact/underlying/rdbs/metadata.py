"""
mlte/store/artifact/underlying/rdbs/metadata.py

Definition of the metadata (DB schema) for the artifact store.
"""

from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for store metadata."""

    pass


# -------------------------------------------------------------------------
# Structural Elements
# -------------------------------------------------------------------------


class DBNamespace(Base):
    __tablename__ = "namespace"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    models: Mapped[List["DBModel"]] = relationship(back_populates="namespace")

    def __repr__(self) -> str:
        return f"Namespace(id={self.id!r}, name={self.name!r})"


class DBModel(Base):
    __tablename__ = "model"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    namespace_id = mapped_column(ForeignKey("namespace.id"))

    namespace: Mapped[DBNamespace] = relationship(back_populates="models")
    versions: Mapped[List["DBVersion"]] = relationship(back_populates="model")

    def __repr__(self) -> str:
        return f"Version(id={self.id!r}, name={self.name!r})"


class DBVersion(Base):
    __tablename__ = "version"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    model_id = mapped_column(ForeignKey("model.id"))

    model: Mapped[DBModel] = relationship(back_populates="versions")

    def __repr__(self) -> str:
        return f"Version(id={self.id!r}, name={self.name!r})"


# -------------------------------------------------------------------------
# General Artifact Elements
# -------------------------------------------------------------------------


class DBArtifactType(Base):
    __tablename__ = "artifact_type"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    def __repr__(self) -> str:
        return f"ArtifactType(id={self.id!r}, name={self.name!r})"


class DBArtifactHeader(Base):
    __tablename__ = "artifact_header"

    id: Mapped[int] = mapped_column(primary_key=True)
    identifier: Mapped[str]
    timestamp: Mapped[int]
    type_id: Mapped[int] = mapped_column(ForeignKey("artifact_type.id"))

    type: Mapped[DBArtifactType] = relationship()

    def __repr__(self) -> str:
        return f"ArtifactHeader(id={self.id!r}, identifier={self.identifier!r}, timestamp={self.timestamp!r}, type={self.type!r})"


# -------------------------------------------------------------------------
# Spec and Validated Spec Elements
# -------------------------------------------------------------------------


class DBSpec(Base):
    __tablename__ = "spec"

    id: Mapped[int] = mapped_column(primary_key=True)
    artifact_header_id: Mapped[DBArtifactHeader] = mapped_column(
        ForeignKey("artifact_header.id")
    )

    artifact_header: Mapped[DBArtifactHeader] = relationship()
    properties: Mapped[List["DBProperty"]] = relationship(back_populates="spec")

    def __repr__(self) -> str:
        return f"Spec(id={self.id!r}, artifact_header={self.artifact_header!r}, properties={self.properties!r})"


class DBProperty(Base):
    __tablename__ = "property"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    rationale: Mapped[str]
    module: Mapped[str]
    spec_id: Mapped[int] = mapped_column(ForeignKey("spec.id"))

    spec: Mapped[DBSpec] = relationship(back_populates="properties")
    conditions: Mapped[List["DBCondition"]] = relationship(
        back_populates="property"
    )
    results: Mapped[List["DBResult"]] = relationship(back_populates="property")

    def __repr__(self) -> str:
        return f"Property(id={self.id!r}, name={self.name!r}, description={self.description!r}, rationale={self.rationale!r}, module={self.module!r})"


class DBCondition(Base):
    __tablename__ = "condition"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    arguments: Mapped[str]  # Json string of the aray of arguments.
    callback: Mapped[str]
    value_class: Mapped[str]
    property_id: Mapped[int] = mapped_column(ForeignKey("property.id"))

    property: Mapped[DBProperty] = relationship(back_populates="conditions")

    def __repr__(self) -> str:
        return f"Property(id={self.id!r}, name={self.name!r}, arguments={self.arguments!r}, value_class={self.value_class!r}, property={self.property!r})"


class DBResult(Base):
    __tablename__ = "result"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str]
    message: Mapped[str]
    property_id: Mapped[int] = mapped_column(ForeignKey("property.id"))

    evidence_metadata: Mapped["DBEvidenceMetadata"] = relationship(
        back_populates="result"
    )
    property: Mapped[DBProperty] = relationship(back_populates="results")

    def __repr__(self) -> str:
        return f"Property(id={self.id!r}, type={self.type!r}, message={self.message!r}, evidence_metadata={self.evidence_metadata!r})"


class DBEvidenceMetadata(Base):
    __tablename__ = "result"

    id: Mapped[int] = mapped_column(primary_key=True)
    identifier: Mapped[str]
    measurement_type: Mapped[str]
    info: Mapped[str]
    result_id: Mapped[int] = mapped_column(ForeignKey("result.id"))

    result: Mapped[DBResult] = relationship(back_populates="evidence_metadata")

    def __repr__(self) -> str:
        return f"Property(id={self.id!r}, identifier={self.identifier!r}, measurement_type={self.measurement_type!r}, info={self.info!r})"


class DBValidatedSpec(Base):
    __tablename__ = "validated_spec"

    id: Mapped[int] = mapped_column(primary_key=True)
    artifact_header_id: Mapped[DBArtifactHeader] = mapped_column(
        ForeignKey("artifact_header.id")
    )
    spec_id: Mapped[int] = mapped_column(ForeignKey("spec.id"))

    artifact_header: Mapped[DBArtifactHeader] = relationship()
    spec: Mapped[DBSpec] = relationship()

    def __repr__(self) -> str:
        return f"ValidatedSpec(id={self.id!r}, artifact_header={self.artifact_header!r}, spec={self.spec!r})"
