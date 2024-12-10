"""
test/qa_category/test_qa_categories.py

Unit tests for model QA categories.
"""

from mlte.qa_category.base import QACategory
from mlte.qa_category.costs.predicting_compute_cost import (
    PredictingComputeCost,
)
from mlte.qa_category.costs.predicting_memory_cost import (
    PredictingMemoryCost,
)
from mlte.qa_category.costs.storage_cost import StorageCost
from mlte.qa_category.costs.training_compute_cost import (
    TrainingComputeCost,
)
from mlte.qa_category.costs.training_memory_cost import (
    TrainingMemoryCost,
)
from mlte.qa_category.fairness.fairness import Fairness
from mlte.qa_category.functionality.task_efficacy import (
    TaskEfficacy,
)
from mlte.qa_category.interpretability.interpretability import (
    Interpretability,
)
from mlte.qa_category.robustness.robustness import Robustness


def assert_qa_category(
    prop: QACategory, name: str, rationale: str, module: str
):
    assert prop.name == name
    assert len(prop.description) > 0
    assert prop.rationale == rationale
    assert prop.module == module


def test_storage_cost():
    p = StorageCost("test")
    assert_qa_category(
        p, "StorageCost", "test", "mlte.qa_category.costs.storage_cost"
    )


def test_training_compute_cost():
    p = TrainingComputeCost("test")
    assert_qa_category(
        p,
        "TrainingComputeCost",
        "test",
        "mlte.qa_category.costs.training_compute_cost",
    )


def test_training_memory_cost():
    p = TrainingMemoryCost("test")
    assert_qa_category(
        p,
        "TrainingMemoryCost",
        "test",
        "mlte.qa_category.costs.training_memory_cost",
    )


def test_task_efficacy():
    p = TaskEfficacy("test")
    assert_qa_category(
        p, "TaskEfficacy", "test", "mlte.qa_category.functionality.task_efficacy"
    )


def test_predicting_compute_cost():
    p = PredictingComputeCost("test")
    assert_qa_category(
        p,
        "PredictingComputeCost",
        "test",
        "mlte.qa_category.costs.predicting_compute_cost",
    )


def test_predicting_memory_cost():
    p = PredictingMemoryCost("test")
    assert_qa_category(
        p,
        "PredictingMemoryCost",
        "test",
        "mlte.qa_category.costs.predicting_memory_cost",
    )


def test_fairness():
    p = Fairness("test")
    assert_qa_category(p, "Fairness", "test", "mlte.qa_category.fairness.fairness")


def test_robustness():
    p = Robustness("test")
    assert_qa_category(
        p, "Robustness", "test", "mlte.qa_category.robustness.robustness"
    )


def test_interpretability():
    p = Interpretability("test")
    assert_qa_category(
        p,
        "Interpretability",
        "test",
        "mlte.qa_category.interpretability.interpretability",
    )
