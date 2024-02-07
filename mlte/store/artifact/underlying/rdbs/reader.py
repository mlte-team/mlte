"""
mlte/store/artifact/underlying/rdbs/reader.py

DB utils for getting artifact related data from the DB.
"""
from __future__ import annotations

from typing import List, Tuple, Union

from sqlalchemy import ScalarResult, select
from sqlalchemy.orm import Session

import mlte.store.error as errors
from mlte.artifact.model import ArtifactModel
from mlte.artifact.type import ArtifactType
from mlte.context.model.model import Model, Namespace, Version
from mlte.store.artifact.underlying.rdbs import factory
from mlte.store.artifact.underlying.rdbs.metadata import (
    DBArtifactHeader,
    DBArtifactType,
    DBModel,
    DBNamespace,
    DBSpec,
    DBValidatedSpec,
    DBVersion,
)


class DBReader:
    """Class encapsulating functions to read artifact related data from the DB."""

    # Artifact Type - DB Object mapping.
    SUPPORTED_ARTIFACT_DB_CLASSES: dict[
        ArtifactType, Union[type[DBSpec], type[DBValidatedSpec]]
    ] = {
        ArtifactType.SPEC: DBSpec,
        ArtifactType.VALIDATED_SPEC: DBValidatedSpec,
    }

    @staticmethod
    def get_namespace(
        namespace_id: str, session: Session
    ) -> Tuple[Namespace, DBNamespace]:
        """Reads the namespace with the given identifier using the provided session, and returns a Namespace and DBNamespace object."""
        namespace_obj = session.scalar(
            select(DBNamespace).where(DBNamespace.name == namespace_id)
        )
        if namespace_obj is None:
            raise errors.ErrorNotFound(
                f"Namespace with identifier {namespace_id} was not found in the artifact store."
            )
        else:
            return (
                Namespace(
                    identifier=namespace_obj.name,
                    models=[
                        Model(
                            identifier=model_obj.name,
                            versions=[
                                Version(identifier=version_obj.name)
                                for version_obj in model_obj.versions
                            ],
                        )
                        for model_obj in namespace_obj.models
                    ],
                ),
                namespace_obj,
            )

    @staticmethod
    def get_model(
        namespace_id: str, model_id: str, session: Session
    ) -> Tuple[Model, DBModel]:
        """Reads the model with the given identifier using the provided session, and returns a Model and DBModel object."""
        model_obj = session.scalar(
            select(DBModel)
            .where(DBModel.name == model_id)
            .where(DBModel.namespace_id == DBNamespace.id)
            .where(DBNamespace.name == namespace_id)
        )

        if model_obj is None:
            raise errors.ErrorNotFound(
                f"Model with identifier {model_id} and associated to namespace {namespace_id} was not found in the artifact store."
            )
        else:
            return (
                Model(
                    identifier=model_obj.name,
                    versions=[
                        Version(identifier=version_obj.name)
                        for version_obj in model_obj.versions
                    ],
                ),
                model_obj,
            )

    @staticmethod
    def get_version(
        namespace_id: str,
        model_id: str,
        version_id: str,
        session: Session,
    ) -> Tuple[Version, DBVersion]:
        """Reads the version with the given identifier using the provided session, and returns a Version and DBVersion object. Raises ErrorNotFound if not found."""
        version_obj = session.scalar(
            select(DBVersion)
            .where(DBVersion.name == version_id)
            .where(DBVersion.model_id == DBModel.id)
            .where(DBModel.namespace_id == DBNamespace.id)
            .where(DBModel.name == model_id)
            .where(DBNamespace.name == namespace_id)
        )

        if version_obj is None:
            raise errors.ErrorNotFound(
                f"Version with identifier {version_id}  and associated to model {model_id} and namespace {namespace_id} was not found in the artifact store."
            )
        else:
            return (Version(identifier=version_obj.name)), version_obj

    @staticmethod
    def get_artifact_type(
        type: ArtifactType, session: Session
    ) -> DBArtifactType:
        """Gets the artifact type DB object corresponding to the given internal type."""
        artifact_type_obj = session.scalar(
            select(DBArtifactType).where(DBArtifactType.name == type)
        )

        if artifact_type_obj is None:
            raise Exception(f"Unknown artifact type requested: {type}")
        return artifact_type_obj

    @staticmethod
    def get_artifact(
        namespace_id: str,
        model_id: str,
        version_id: str,
        artifact_id: str,
        session: Session,
    ) -> Tuple[ArtifactModel, Union[DBSpec, DBValidatedSpec]]:
        """Reads the artifact with the given identifier using the provided session, and returns an internal object."""
        # First get the class of the artifact we are trying to read, so we can use the ORM by passing the DB object type.
        artifact_header_obj = DBReader.get_artifact_header(artifact_id, session)
        artifact_type = ArtifactType(artifact_header_obj.type.name)

        # Get artifact.
        artifact_class = DBReader.get_artifact_class(artifact_type)
        artifact_obj: Union[DBSpec, DBValidatedSpec] = session.scalar(
            select(artifact_class)
            .where(DBVersion.model_id == DBModel.id)
            .where(DBModel.namespace_id == DBNamespace.id)
            .where(DBVersion.name == version_id)
            .where(DBModel.name == model_id)
            .where(DBNamespace.name == namespace_id)
            .where(DBArtifactHeader.id == artifact_class.artifact_header_id)
            .where(DBArtifactHeader.identifier == artifact_id)
            .where(DBArtifactHeader.version_id == DBVersion.id)
        )

        if artifact_obj is None:
            raise errors.ErrorNotFound(
                f"Artifact with identifier {artifact_id}  and associated to namespace {namespace_id}, model {model_id}, and version {version_id} was not found in the artifact store."
            )
        else:
            return (
                factory.create_artifact_from_db(artifact_header_obj),
                artifact_obj,
            )

    @staticmethod
    def get_artifacts_for_type(
        namespace_id: str,
        model_id: str,
        version_id: str,
        artifact_type: ArtifactType,
        session: Session,
    ) -> List[ArtifactModel]:
        """Loads and returns a list with all the artifacts of the given type, for the given namespace/model/version."""
        artifact_class = DBReader.get_artifact_class(artifact_type)
        artifact_objs: ScalarResult[
            Union[DBSpec, DBValidatedSpec]
        ] = session.scalars(
            (
                select(artifact_class)
                .where(DBVersion.model_id == DBModel.id)
                .where(DBModel.namespace_id == DBNamespace.id)
                .where(DBVersion.name == version_id)
                .where(DBModel.name == model_id)
                .where(DBNamespace.name == namespace_id)
                .where(DBArtifactHeader.id == artifact_class.artifact_header_id)
                .where(DBArtifactHeader.version_id == DBVersion.id)
            )
        )
        artifacts = []
        for artifact_obj in artifact_objs:
            artifact = factory.create_artifact_from_db(
                artifact_obj.artifact_header
            )
            artifacts.append(artifact)
        return artifacts

    @staticmethod
    def get_artifact_header(
        artifact_id: str, session: Session
    ) -> DBArtifactHeader:
        """Gets the artifact header object of the artifact identifier provided."""
        artifact_header_obj = session.scalar(
            select(DBArtifactHeader).where(
                DBArtifactHeader.identifier == artifact_id
            )
        )
        if artifact_header_obj is None:
            raise errors.ErrorNotFound(
                f"Artifact with identifier {artifact_id} was not found in the artifact store."
            )
        else:
            return artifact_header_obj

    @staticmethod
    def get_artifact_class(
        artifact_type: ArtifactType,
    ) -> Union[type[DBSpec], type[DBValidatedSpec]]:
        """Gets the DB class of the artifact header provided."""
        if artifact_type in DBReader.SUPPORTED_ARTIFACT_DB_CLASSES:
            return DBReader.SUPPORTED_ARTIFACT_DB_CLASSES[
                ArtifactType(artifact_type)
            ]
        else:
            raise Exception(f"Unsupported artifact type: {artifact_type.value}")
