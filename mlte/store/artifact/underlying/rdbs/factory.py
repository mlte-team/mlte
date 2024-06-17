"""
mlte/store/artifact/underlying/rdbs/factory.py

Creation of metadata objects from pydantic models.
"""

import typing

from sqlalchemy.orm import Session

from mlte.artifact.model import ArtifactHeaderModel, ArtifactModel
from mlte.artifact.type import ArtifactType
from mlte.negotiation.model import NegotiationCardModel
from mlte.report.model import ReportModel
from mlte.spec.model import SpecModel
from mlte.store.artifact.underlying.rdbs.factory_nc import (
    create_negotiation_db_from_model,
    create_negotiation_model_from_db,
    create_report_db_from_model,
    create_report_model_from_db,
)
from mlte.store.artifact.underlying.rdbs.factory_spec import (
    create_spec_db_from_model,
    create_spec_model_from_db,
    create_v_spec_db_from_model,
    create_v_spec_model_from_db,
)
from mlte.store.artifact.underlying.rdbs.factory_value import (
    create_value_db_from_model,
    create_value_model_from_db,
)
from mlte.store.artifact.underlying.rdbs.metadata import (
    DBArtifactHeader,
    DBArtifactType,
)
from mlte.store.artifact.underlying.rdbs.metadata_nc import (
    DBNegotiationCard,
    DBReport,
)
from mlte.store.artifact.underlying.rdbs.metadata_spec import (
    DBSpec,
    DBValidatedSpec,
)
from mlte.store.artifact.underlying.rdbs.metadata_value import DBValue
from mlte.validation.model import ValidatedSpecModel
from mlte.value.model import ValueModel

# -------------------------------------------------------------------------
# DB artifact factory.
# -------------------------------------------------------------------------


def create_db_artifact(
    artifact: ArtifactModel,
    artifact_type_obj: DBArtifactType,
    version_id: int,
    session: Session,
) -> typing.Union[
    DBSpec, DBValidatedSpec, DBNegotiationCard, DBReport, DBValue
]:
    """Converts an internal model to its corresponding DB object for artifacts."""
    artifact_header = DBArtifactHeader(
        identifier=artifact.header.identifier,
        type=artifact_type_obj,
        timestamp=artifact.header.timestamp,
        username=artifact.header.creator,
        version_id=version_id,
    )

    if artifact.header.type == ArtifactType.SPEC:
        # Create a DBSpec and its internal lists: properties, and inside them, conditions.
        spec = typing.cast(SpecModel, artifact.body)
        return create_spec_db_from_model(spec, artifact_header)
    elif artifact.header.type == ArtifactType.VALIDATED_SPEC:
        # Create a DBValidatedSpec db object.
        validated_spec = typing.cast(ValidatedSpecModel, artifact.body)
        return create_v_spec_db_from_model(
            validated_spec, artifact_header, session
        )
    elif artifact.header.type == ArtifactType.NEGOTIATION_CARD:
        # Create a DBNegotiationCard object and all its subpieces.
        negotiation_card = typing.cast(NegotiationCardModel, artifact.body)
        return create_negotiation_db_from_model(
            negotiation_card, artifact_header, session
        )
    elif artifact.header.type == ArtifactType.REPORT:
        # Create a DBReport object and all its subpieces.
        report = typing.cast(ReportModel, artifact.body)
        return create_report_db_from_model(report, artifact_header, session)
    elif artifact.header.type == ArtifactType.VALUE:
        # Create a DBValue object and all its subpieces.
        value = typing.cast(ValueModel, artifact.body)
        return create_value_db_from_model(value, artifact_header)
    else:
        raise Exception(
            f"Unsupported artifact type for conversion: {artifact.header.type}"
        )


# -------------------------------------------------------------------------
# Artifact model factory.
# -------------------------------------------------------------------------


def create_artifact_from_db(
    artifact_header_obj: DBArtifactHeader, session: Session
) -> ArtifactModel:
    """
    Creates an Artifact model from the corresponding DB object and DB header.

    :param artifact_header_obj: A DBArtifactHeader object from the DB with header info.
    :param session: The DB session to use.
    :return: the DB data converted into an ArtifactModel.
    """
    artifact_header = ArtifactHeaderModel(
        identifier=artifact_header_obj.identifier,
        type=ArtifactType(artifact_header_obj.type.name),
        timestamp=artifact_header_obj.timestamp,
        creator=artifact_header_obj.username,
    )

    body: typing.Union[
        SpecModel,
        ValidatedSpecModel,
        NegotiationCardModel,
        ReportModel,
        ValueModel,
    ]
    if artifact_header.type == ArtifactType.SPEC:
        # Creating a Spec from DB data.
        spec_obj = typing.cast(DBSpec, artifact_header_obj.body_spec)
        body = create_spec_model_from_db(spec_obj)
    elif artifact_header.type == ArtifactType.VALIDATED_SPEC:
        # Creating a ValidatedSpec from DB data.
        validated_obj = typing.cast(
            DBValidatedSpec, artifact_header_obj.body_validated_spec
        )
        body = create_v_spec_model_from_db(validated_obj)
    elif artifact_header.type == ArtifactType.NEGOTIATION_CARD:
        # Creating a NegotiationCard from DB data.
        negotiation_obj = typing.cast(
            DBNegotiationCard, artifact_header_obj.body_negotiation_card
        )
        body = create_negotiation_model_from_db(negotiation_obj)
    elif artifact_header.type == ArtifactType.REPORT:
        # Creating a Report from DB data.
        report_obj = typing.cast(DBReport, artifact_header_obj.body_report)
        body = create_report_model_from_db(report_obj)
    elif artifact_header.type == ArtifactType.VALUE:
        # Creating a Value from DB data.
        value_obj = typing.cast(DBValue, artifact_header_obj.body_value)
        body = create_value_model_from_db(value_obj)

    else:
        raise Exception(
            f"Unsupported artifact type for conversion: {artifact_header.type}"
        )

    return ArtifactModel(header=artifact_header, body=body)
