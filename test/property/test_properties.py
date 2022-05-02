"""
Unit tests for model properties.
"""

from mlte.property.costs import (
    StorageCost,
    TrainingComputeCost,
    TrainingMemoryCost,
)
from mlte.property.functionality import TaskEfficacy


def test_storage_cost():
    p = StorageCost()
    assert p.name == "StorageCost"
    assert len(p.description) > 0


def test_training_compute_cost():
    p = TrainingComputeCost()
    assert p.name == "TrainingComputeCost"
    assert len(p.description) > 0


def test_training_memory_cost():
    p = TrainingMemoryCost()
    assert p.name == "TrainingMemoryCost"
    assert len(p.description) > 0


def test_task_efficiacy():
    p = TaskEfficacy()
    assert p.name == "TaskEfficacy"
    assert len(p.description) > 0
