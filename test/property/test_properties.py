"""
test/property/test_properties.py

Unit tests for model properties.
"""

from mlte.property.base import Property
from mlte.property.costs.predicting_compute_cost import PredictingComputeCost
from mlte.property.costs.predicting_memory_cost import PredictingMemoryCost
from mlte.property.costs.storage_cost import StorageCost
from mlte.property.costs.training_compute_cost import TrainingComputeCost
from mlte.property.costs.training_memory_cost import TrainingMemoryCost
from mlte.property.fairness.fairness import Fairness
from mlte.property.functionality.task_efficacy import TaskEfficacy
from mlte.property.interpretability.interpretability import Interpretability
from mlte.property.robustness.robustness import Robustness


def assert_property(prop: Property, name: str, rationale: str, module: str):
    assert prop.name == name
    assert len(prop.description) > 0
    assert prop.rationale == rationale
    assert prop.module == module


def test_storage_cost():
    p = StorageCost("test")
    assert_property(
        p, "StorageCost", "test", "mlte.property.costs.storage_cost"
    )


def test_training_compute_cost():
    p = TrainingComputeCost("test")
    assert_property(
        p,
        "TrainingComputeCost",
        "test",
        "mlte.property.costs.training_compute_cost",
    )


def test_training_memory_cost():
    p = TrainingMemoryCost("test")
    assert_property(
        p,
        "TrainingMemoryCost",
        "test",
        "mlte.property.costs.training_memory_cost",
    )


def test_task_efficacy():
    p = TaskEfficacy("test")
    assert_property(
        p, "TaskEfficacy", "test", "mlte.property.functionality.task_efficacy"
    )


def test_predicting_compute_cost():
    p = PredictingComputeCost("test")
    assert_property(
        p,
        "PredictingComputeCost",
        "test",
        "mlte.property.costs.predicting_compute_cost",
    )


def test_predicting_memory_cost():
    p = PredictingMemoryCost("test")
    assert_property(
        p,
        "PredictingMemoryCost",
        "test",
        "mlte.property.costs.predicting_memory_cost",
    )


def test_fairness():
    p = Fairness("test")
    assert_property(p, "Fairness", "test", "mlte.property.fairness.fairness")


def test_robustness():
    p = Robustness("test")
    assert_property(
        p, "Robustness", "test", "mlte.property.robustness.robustness"
    )


def test_interpretability():
    p = Interpretability("test")
    assert_property(
        p,
        "Interpretability",
        "test",
        "mlte.property.interpretability.interpretability",
    )
