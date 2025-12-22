"""TestSuite contains a collection of TestCases."""

from __future__ import annotations

import typing

from mlte._private.function_info import get_function_code
from mlte.artifact.artifact import Artifact
from mlte.artifact.model import ArtifactLevel, ArtifactModel
from mlte.artifact.type import ArtifactType
from mlte.context.context import Context
from mlte.evidence.artifact import Evidence
from mlte.measurement.process_measurement import ProcessMeasurement
from mlte.measurement.process_measurement_group import ProcessMeasurementGroup
from mlte.model.base_model import BaseModel
from mlte.negotiation.model import NegotiationCardModel
from mlte.store.artifact.store import ArtifactStore
from mlte.store.artifact.store_session import ManagedArtifactSession
from mlte.store.query import Query, TypeFilter
from mlte.suite.model import TestSuiteModel
from mlte.suite.test_case import TestCase


class TestSuite(Artifact):
    """
    The TestSuite contains a collection of TestCases to be
    measured and validated.
    """

    type = ArtifactType.TEST_SUITE
    """Class attribute indicating type."""

    def __init__(
        self,
        identifier: typing.Optional[str] = None,
        test_cases: list[TestCase] = [],
    ):
        """
        Initialize a TestSuite instance.

        :param test_cases: The collection of test cases.
        """
        super().__init__(identifier)

        self.level = ArtifactLevel.MODEL
        """Indicate that this type of artifact will exist at the model level."""

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
    ) -> dict[str, Evidence]:
        """
        Executes all configured measurements with the provided inputs.

        :param input: a dictionary of inputs for each test case, keyed by test case id, each containing a list of inputs for that case.
        :return: a dict of Evidences, keyed by test case id, generated as resuts for all the executed measurements, one per test case.
        """
        # Check for invalid input ids.
        for case_id, args in input.items():
            if case_id not in self.test_cases:
                raise RuntimeError(
                    f"Test Case id {case_id} received in input does not exist in this suite."
                )

        # Go over all cases.
        evidences: dict[str, Evidence] = {}
        groups: dict[str, list[ProcessMeasurement]] = {}
        for case_id, case in self.test_cases.items():
            # Only run cases for which we have an input definition.
            if case_id in input:
                args = input[case_id]
                if (
                    case.measurement
                    and isinstance(case.measurement, ProcessMeasurement)
                    and case.measurement.group
                ):
                    # If there is a group, store the case there to run those per group later.
                    if case.measurement.group not in groups:
                        groups[case.measurement.group] = []
                    groups[case.measurement.group].append(case.measurement)
                else:
                    # If case has no group, just run it directly.
                    evidence = case.measure(*args)
                    evidences[case_id] = evidence

        # Run measurements groups.
        group_evidences = ProcessMeasurementGroup.evaluate_groups(groups, input)
        evidences.update(group_evidences)

        return evidences

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
            negotiation_cards = store_session.artifact_mapper.search(
                Query(
                    filter=TypeFilter(item_type=ArtifactType.NEGOTIATION_CARD)
                ),
                context=(context.model, context.version),
            )
            for _, case in self.test_cases.items():
                # Check each QAS id, in each test case.
                found = False
                for qas_id in case.quality_scenarios:
                    # Check for all negotiation cards, in case there is more than one.
                    for artifact in negotiation_cards:
                        card = typing.cast(NegotiationCardModel, artifact.body)
                        scenarios = card.system_requirements

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
    # Templating.
    # -------------------------------------------------------------------------

    def template(self):
        from mlte.tests.test_case import TestCase  # noqa
        from mlte.tests.test_suite import TestSuite

        suite = TestSuite(  # noqa
            test_cases=[
                # CASES
            ]
        )

    def to_template_str(self) -> str:
        """Convert the test suite into a template string."""
        source = get_function_code(self.template)[8:]

        # Remove all extra indentation.
        source = source.replace("\n        ", "\n")

        cases = ""
        for _, test in self.test_cases.items():
            cases += test.to_template_str()

        # Substitute in cases template.
        source = source.replace("        # CASES", cases[:-1])

        return source

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

        # We compare cases directly, since they have serialized validators that have to be compared in a particular way.
        all_cases_equal = False
        if len(self.test_cases) == len(other.test_cases):
            for id, _ in self.test_cases.items():
                if (
                    id not in other.test_cases
                    or self.test_cases[id] != other.test_cases[id]
                ):
                    all_cases_equal = False
                    break
            all_cases_equal = True

        return self.identifier == other.identifier and all_cases_equal
