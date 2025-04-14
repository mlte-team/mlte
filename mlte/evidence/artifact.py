"""
Artifact implementation for MLTE Evidence.
"""

from __future__ import annotations

import typing
from abc import ABC, abstractmethod
from typing import Optional, TypeVar

from mlte._private import meta
from mlte._private.reflection import load_class_or_function
from mlte.artifact.artifact import Artifact
from mlte.artifact.model import ArtifactModel
from mlte.artifact.type import ArtifactType
from mlte.context.context import Context
from mlte.evidence.metadata import EvidenceMetadata
from mlte.evidence.model import EvidenceModel
from mlte.model.base_model import BaseModel
from mlte.store.artifact.store import ArtifactStore

DEFAULT_EVIDENCE_ID = "default.evidence"
"""This is supposed to be a temporary id, not for permanent use."""

T = TypeVar("T", bound="Evidence")
"""Needed for generic return of type."""


class Evidence(Artifact, ABC):
    """
    The Evidence class serves as the base class of all
    semantically-enriched measurement evaluation evidence.
    The Evidence provides a common interface for inspecting
    the results of measurement evaluation, and also
    encapsulates the functionality required to uniquely
    associate evaluation results with the originating measurement.
    """

    def __init__(self):
        """Initialize a Evidence instance"""
        """We use the default id for now, it will be updated later with the metadata."""
        super().__init__(self.get_default_id(), ArtifactType.EVIDENCE)

        self.typename: str = meta.get_qualified_name(self.__class__)
        """The class type of the evidence itself."""

        self.metadata: Optional[EvidenceMetadata] = None
        """Metadata has not been initialized yet."""

    def with_metadata(self: T, evidence_metadata: EvidenceMetadata) -> T:
        """Sets the evidence metadata, returns updated object."""
        self.metadata = evidence_metadata

        # Also set an identifier associated to the metadata.
        self.identifier = f"{evidence_metadata.test_case_id}.evidence"

        return self

    @staticmethod
    def get_default_id() -> str:
        """Default evidence id."""
        return DEFAULT_EVIDENCE_ID

    def __str__(self) -> str:
        """Return a string representation."""
        return self.to_model().to_json_string()

    # -------------------------------------------------------------------------
    # Model handling.
    # -------------------------------------------------------------------------

    def _to_artifact_model(self, value_model: BaseModel) -> ArtifactModel:
        """
        Convert a evidence artifact to its corresponding artifact model.
        :param value_model: The specific evidence/value model data.
        """
        if not self.metadata:
            raise RuntimeError(
                "Can't convert Evidence to model, it is missing its metadata."
            )

        model = ArtifactModel(
            header=self.build_artifact_header(),
            body=EvidenceModel(
                metadata=self.metadata,
                evidence_class=meta.get_qualified_name(self.__class__),
                value=value_model,  # type: ignore
            ),
        )
        return model

    @abstractmethod
    def to_model(self) -> ArtifactModel:
        """
        Convert a evidence artifact to its corresponding model.
        NOTE: To cope with polymorphism, the Evidence artifact type
        does not define this required method itself; instead, it
        is delegated to subclasses that implement concrete types
        """
        raise NotImplementedError("Evidence.to_model()")

    @classmethod
    @abstractmethod
    def from_model(cls, _: BaseModel) -> Evidence:
        """
        Convert a evidence model to its corresponding artifact.
        NOTE: To cope with polymorphism, the Evidence artifact type
        does not define this required method itself; instead, it
        is delegated to subclasses that implement concrete types
        """
        raise NotImplementedError("Evidence.from_model()")

    # -------------------------------------------------------------------------
    # Class loading methods.
    # -------------------------------------------------------------------------

    @staticmethod
    def load_all() -> list[Evidence]:
        """Loads all Evidences stored for the current session's context and store."""
        evidence_models = Evidence.load_models_for_session(
            ArtifactType.EVIDENCE
        )
        return Evidence._load_from_models(evidence_models)

    @staticmethod
    def load_all_with(context: Context, store: ArtifactStore) -> list[Evidence]:
        """Loads all Evidences stored for the given context and store."""
        evidence_models = Evidence.load_models(
            ArtifactType.EVIDENCE, context, store
        )
        return Evidence._load_from_models(evidence_models)

    @staticmethod
    def _load_from_models(
        evidence_models: list[ArtifactModel],
    ) -> list[Evidence]:
        """Converts a list of evidence models (as Artifact Models) into evidence artifacts."""
        evidences: list[Evidence] = []
        for artifact_model in evidence_models:
            model: EvidenceModel = typing.cast(
                EvidenceModel, artifact_model.body
            )
            evidence_class: Evidence = typing.cast(
                Evidence, load_class_or_function(model.evidence_class)
            )
            evidence = evidence_class.from_model(artifact_model)
            evidences.append(evidence)
        return evidences

    # Overriden.
    @classmethod
    def load(cls, identifier: typing.Optional[str] = None) -> Evidence:
        """
        Load a Evidence from the configured global session.
        :param identifier: The identifier for the artifact. If None,
        the default id is used.
        """
        evidence = super().load(identifier)
        return typing.cast(Evidence, evidence)
