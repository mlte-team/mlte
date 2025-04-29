"""
TestSuite contains a collection of TestCases.
"""

from __future__ import annotations

import typing

from mlte.artifact.artifact import Artifact
from mlte.artifact.model import ArtifactModel
from mlte.artifact.type import ArtifactType
from mlte.context.context import Context
from mlte.evidence.artifact import Evidence
from mlte.model.base_model import BaseModel
from mlte.negotiation.model import NegotiationCardModel
from mlte.store.artifact.store import ArtifactStore, ManagedArtifactSession
from mlte.store.query import Query, TypeFilter
from mlte.tests.model import TestSuiteModel
from mlte.tests.test_case import TestCase

DEFAULT_TEST_SUITE_ID = "default.test_suite"


class TestSuite(Artifact):
    """
    The TestSuite contains a collection of TestCases to be
    measured and validated.
    """

    def __init__(
        self,
        identifier: str = DEFAULT_TEST_SUITE_ID,
        test_cases: list[TestCase] = [],
    ):
        """
        Initialize a TestSuite instance.

        :param test_cases: The collection of test cases.
        """
        super().__init__(identifier, ArtifactType.TEST_SUITE)

        # Check that no tests cases have the same id.
        found_ids = []
        for test_case in test_cases:
            if test_case.identifier in found_ids:
                raise RuntimeError(
                    f"Found repeated test case id: <{test_case.identifier}>, all tests cases must have unique ids."
                )
            found_ids.append(test_case.identifier)

        self.test_cases = {
            test_case.identifier: test_case for test_case in test_cases
        }
        """The collection of TestCases that compose the TestSuite."""

    def add_test_case(self, test_case: TestCase):
        """Adds a test case to its list. Will overwrite if another one with same id had been stored before."""
        self.test_cases[test_case.identifier] = test_case

    def run_measurements(
        self, input: dict[str, list[typing.Any]]
    ) -> list[Evidence]:
        """Tries to execute all configured measurements with the provided arguments."""
        evidences: list[Evidence] = []
        for case_id, args in input.items():
            if case_id not in self.test_cases:
                raise RuntimeError(
                    f"Test Case id {case_id} received in args does not exist in this suite."
                )
            evidence = self.test_cases[case_id].measure(*args)
            evidences.append(evidence)
        return evidences

    # -------------------------------------------------------------------------
    # Artifact overrides.
    # -------------------------------------------------------------------------

    @staticmethod
    def get_default_id() -> str:
        """Overriden"""
        return DEFAULT_TEST_SUITE_ID

    # -------------------------------------------------------------------------
    # Model serialization.
    # -------------------------------------------------------------------------

    def to_model(self) -> ArtifactModel:
        """Convert a TestSuite artifact to its corresponding model."""
        return ArtifactModel(
            header=self.build_artifact_header(),
            body=TestSuiteModel(
                test_cases=[
                    test_case.to_model()
                    for _, test_case in self.test_cases.items()
                ],
            ),
        )

    @classmethod
    def from_model(cls, model: BaseModel) -> TestSuite:
        """Convert a TestSuite model to its corresponding artifact."""
        assert isinstance(
            model, ArtifactModel
        ), f"Can't create object from non-ArtifactModel model: type{type(model)}."
        assert (
            model.header.type == ArtifactType.TEST_SUITE
        ), "Type should be TestSuite."
        body = typing.cast(TestSuiteModel, model.body)
        return TestSuite(
            identifier=model.header.identifier,
            test_cases=[
                TestCase.from_model(test_case_model)
                for test_case_model in body.test_cases
            ],
        )

    # Overriden.
    @classmethod
    def load(cls, identifier: typing.Optional[str] = None) -> TestSuite:
        """
        Load a TestSuite from the configured global session.
        :param identifier: The identifier for the artifact. If None,
        the default id is used.
        """
        suite = super().load(identifier)
        return typing.cast(TestSuite, suite)

    # -------------------------------------------------------------------------
    # Hooks.
    # -------------------------------------------------------------------------

    def pre_save_hook(self, context: Context, store: ArtifactStore) -> None:
        """
        A method that artifact subclasses can override to enforce pre-save invariants.
        :param context: The context in which to save the artifact
        :param store: The store in which to save the artifact
        :raises RuntimeError: On broken invariant
        """
        # Check that the QAS ids in the test cases are all valid QAS ids.
        with ManagedArtifactSession(store.session()) as store_session:
            # Load all negotiation card, to find the ids of the QAS there.
            negotiation_cards = store_session.search_artifacts(
                context.model,
                context.version,
                Query(
                    filter=TypeFilter(item_type=ArtifactType.NEGOTIATION_CARD)
                ),
            )
            for _, case in self.test_cases.items():
                # Check each QAS id, in each test case.
                found = False
                for qas_id in case.quality_scenarios:
                    # Check for all negotiation cards, in case there is more than one.
                    for artifact in negotiation_cards:
                        card = typing.cast(NegotiationCardModel, artifact.body)
                        scenarios = card.nc_data.system_requirements

                        # Look in each scenario for the negotiation card, to find the QAS id.
                        for scenario in scenarios:
                            if qas_id == scenario.identifier:
                                found = True
                                break

                        # Stop looking into other cards if we found the id.
                        if found:
                            break

                if not found and case.quality_scenarios:
                    raise RuntimeError(
                        f"Quality Attribute Scenario with id {qas_id} was not found on any NegotiationCard"
                    )

    # -------------------------------------------------------------------------
    # Builtin overloads.
    # -------------------------------------------------------------------------

    def __str__(self) -> str:
        """Return a string representation of TestCase."""
        return f"TestSuite contains {len(self.test_cases)} test cases"

    def __eq__(self, other: object) -> bool:
        """Compare TestSuite instances for equality."""
        if not isinstance(other, TestSuite):
            return False
        reference: TestSuite = other
        return self.to_model() == reference.to_model()
