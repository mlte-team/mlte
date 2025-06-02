"""Definition of the metadata (DB schema) for the artifact store."""

from sqlalchemy.orm import Session

from mlte.report.model import (
    CommentDescriptor,
    QuantitiveAnalysisDescriptor,
    ReportModel,
)
from mlte.store.artifact.underlying.rdbs.card_factory import (
    create_negotiation_db_from_model,
    create_negotiation_model_from_db,
)
from mlte.store.artifact.underlying.rdbs.main_metadata import DBArtifact
from mlte.store.artifact.underlying.rdbs.report_metadata import (
    DBCommentDescriptor,
    DBReport,
)
from mlte.store.artifact.underlying.rdbs.result_factory import (
    create_test_results_db_from_model,
    create_test_results_model_from_db,
)
from mlte.store.artifact.underlying.rdbs.tests_factory import (
    create_test_suite_db_from_model,
    create_test_suite_model_from_db,
)

# -------------------------------------------------------------------------
# Report Factory Methods
# -------------------------------------------------------------------------


def create_report_db_from_model(
    report: ReportModel,
    artifact: DBArtifact,
    session: Session,
) -> DBReport:
    """Creates the DB object from the corresponding internal model."""
    negotiation_card_data_obj = create_negotiation_db_from_model(
        report.negotiation_card, artifact, session
    )
    test_suite_obj = create_test_suite_db_from_model(
        report.test_suite, artifact
    )
    test_results_obj = create_test_results_db_from_model(
        report.test_results, artifact, session
    )

    # Create the actual object.
    report_obj = DBReport(
        artifact=artifact,
        negotiation_card=negotiation_card_data_obj,
        test_suite=test_suite_obj,
        test_results=test_results_obj,
        comments=[],
        quantitative_analysis_content=report.quantitative_analysis.content,
    )

    # Create list of comment objects.
    for comment in report.comments:
        comment_obj = DBCommentDescriptor(content=comment.content)
        report_obj.comments.append(comment_obj)

    return report_obj


def create_report_model_from_db(report_obj: DBReport) -> ReportModel:
    """Creates the internal model object from the corresponding DB object."""
    negotiation_card = create_negotiation_model_from_db(
        report_obj.negotiation_card
    )
    test_suite = create_test_suite_model_from_db(report_obj.test_suite)
    test_results = create_test_results_model_from_db(report_obj.test_results)

    body = ReportModel(
        negotiation_card_id=report_obj.negotiation_card_identifier,
        negotiation_card=negotiation_card,
        test_suite_id=report_obj.test_suite_identifier,
        test_suite=test_suite,
        test_results_id=report_obj.test_results_identifier,
        test_results=test_results,
        comments=[
            CommentDescriptor(content=comment.content)
            for comment in report_obj.comments
            if comment.content is not None
        ],
        quantitative_analysis=QuantitiveAnalysisDescriptor(
            content=report_obj.quantitative_analysis_content
        ),
    )
    return body
