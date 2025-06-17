"""Definition of the metadata (DB schema) for the artifact store."""

from sqlalchemy.orm import Session

from mlte.report.model import (
    CommentDescriptor,
    QuantitiveAnalysisDescriptor,
    ReportModel,
)
from mlte.store.artifact.underlying.rdbs import (
    card_factory,
    result_factory,
    suite_factory,
)
from mlte.store.artifact.underlying.rdbs.main_metadata import DBArtifact
from mlte.store.artifact.underlying.rdbs.report_metadata import (
    DBCommentDescriptor,
    DBReport,
)

# -------------------------------------------------------------------------
# Report Factory Methods
# -------------------------------------------------------------------------


def create_report_orm(
    report: ReportModel,
    artifact: DBArtifact,
    session: Session,
) -> DBReport:
    """Creates the DB object from the corresponding internal model."""
    # Create the internal card, suite and results ORMs that will be preserved as a copy.
    # Note that they will not be stored as independent artifacts, thus the None artifac_orm param.
    card_orm = card_factory.create_card_orm(
        report.negotiation_card, artifact_orm=None, session=session
    )
    suite_orm = suite_factory.create_suite_orm(
        report.test_suite, artifact_orm=None
    )
    results_orm = result_factory.create_results_orm(
        report.test_results, artifact_orm=None
    )

    # Create the actual object.
    report_orm = DBReport(
        artifact=artifact,
        negotiation_card_identifier=report.negotiation_card_id,
        negotiation_card=card_orm,
        test_suite_identifier=report.test_suite_id,
        test_suite=suite_orm,
        test_results_identifier=report.test_results_id,
        test_results=results_orm,
        comments=[],
        quantitative_analysis_content=report.quantitative_analysis.content,
    )

    # Create list of comment objects.
    for comment in report.comments:
        comment_orm = DBCommentDescriptor(content=comment.content)
        report_orm.comments.append(comment_orm)

    return report_orm


def create_report_model(report_orm: DBReport) -> ReportModel:
    """Creates the internal model object from the corresponding DB object."""
    negotiation_card = card_factory.create_card_model(
        report_orm.negotiation_card
    )
    test_suite = suite_factory.create_suite_model(report_orm.test_suite)
    test_results = result_factory.create_results_model(report_orm.test_results)

    body = ReportModel(
        negotiation_card_id=report_orm.negotiation_card_identifier,
        negotiation_card=negotiation_card,
        test_suite_id=report_orm.test_suite_identifier,
        test_suite=test_suite,
        test_results_id=report_orm.test_results_identifier,
        test_results=test_results,
        comments=[
            CommentDescriptor(content=comment.content)
            for comment in report_orm.comments
            if comment.content is not None
        ],
        quantitative_analysis=QuantitiveAnalysisDescriptor(
            content=report_orm.quantitative_analysis_content
        ),
    )
    return body
