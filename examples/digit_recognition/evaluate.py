"""
An example demonstrating model evaluation with MLTE.
"""

import os
import sys
import time
import argparse
import threading
import subprocess
from typing import Tuple, List, Dict, Any

import mlflow
from mlflow import log_param

# Silence warnings from Tensorflow
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import tensorflow as tf

from mlte.report import Report, Dataset, User, UseCase, Limitation, render

from mlte.suite import Suite
from mlte.property.costs import (
    StorageCost,
    TrainingComputeCost,
    TrainingMemoryCost,
)
from mlte.property.functionality import TaskEfficacy

from mlte.measurement import Measurement, bind
from mlte.measurement.storage import LocalObjectSize
from mlte.measurement.cpu import LocalProcessCPUUtilization
from mlte.measurement.memory import LocalProcessMemoryConsumption
from mlte.measurement.validation import (
    ValidationResult,
    Validator,
    Success,
    Failure,
)
from mlte.measurement.utility import flatten, concurrently


# Script exit codes
EXIT_SUCCESS = 0
EXIT_FAILURE = 1

# The path to which the trained model is saved
MODEL_PATH = "model.tf"

# -----------------------------------------------------------------------------
# Model Preliminaries
# -----------------------------------------------------------------------------


def load_data():
    """Load the MNIST image dataset."""
    (X_train, y_train), (X_test, y_test) = tf.keras.datasets.mnist.load_data()

    X_train = tf.pad(X_train, [[0, 0], [2, 2], [2, 2]]) / 255
    X_test = tf.pad(X_test, [[0, 0], [2, 2], [2, 2]]) / 255
    X_train = tf.expand_dims(X_train, axis=3, name=None)
    X_test = tf.expand_dims(X_test, axis=3, name=None)
    X_train = tf.repeat(X_train, 3, axis=3)
    X_test = tf.repeat(X_test, 3, axis=3)

    X_val = X_train[-2000:, :, :, :]
    y_val = y_train[-2000:]

    X_train = X_train[:-2000, :, :, :]
    y_train = y_train[:-2000]

    return (X_train, y_train), (X_test, y_test), (X_val, y_val)


def load_model(path: str):
    """Load a model from the specified path."""
    return tf.keras.models.load_model(path)


# -----------------------------------------------------------------------------
# Build a Report
# -----------------------------------------------------------------------------


def build_report() -> Report:
    """
    Build a MLTE model evaluation report.

    This function demonstrates the construction of a
    model evaluation report with MLTE. All of the
    content for the report appears in the body of
    this function, apart from the associated Suite.
    """

    # Begin a report
    report = Report()

    # Populate report metadata
    report.metadata.project_name = "Digit Recognition"
    report.metadata.authors = ["Kyle Dotterrer", "Kate Maffey", "Jenny Niemann"]
    report.metadata.source_url = "https://github.com/mlte-team/mlte"
    report.metadata.artifacts_url = "https://mlte-team-data.s3.amazonaws.com"
    report.metadata.timestamp = f"{int(time.time())}"

    # Populate report model details
    report.model_details.name = "DigitRecognizer1.0"
    report.model_details.overview = """
    This model recognizes handwritten digits.
    Input images are classified as one of the digits 0-9.
    """
    report.model_details.documentation = """
    This model is a modification of the ResNet152 residual DNN.
    """

    # Populate report model specifications
    report.model_specification.domain = "Image Classification"
    report.model_details.architecture = "ResNet152 with output heads appended."
    report.model_specification.input = "Input images in array or tensor format."
    report.model_specification.output = (
        "Probability distribution over 10 classes."
    )
    report.model_specification.data = [
        Dataset(
            "ILSVRC2012",
            "https://image-net.org/challenges/LSVRC/2012/",
            "ImageNet Large Scale Visual Recognition Challenge 2012",
        )
    ]

    # Add intended users
    report.considerations.users = [User("Human resources staff.")]

    # Add intended use cases
    report.considerations.use_cases = [
        UseCase("Optical character recognition.")
    ]

    # Add limitations
    report.considerations.limitations = [
        Limitation("Classification results are sensitive to image rotation.")
    ]

    # Return the populated report
    return report


# -----------------------------------------------------------------------------
# Build a Suite
# -----------------------------------------------------------------------------


def build_suite() -> Suite:
    """
    Build a MLTE evaluation suite.

    This function demonstrates the construction of a
    model evaluation suite with MLTE. We begin by
    instantiating a Suite instance, and attaching
    several Property instances to this Suite.
    """

    # Instantiate a suite for our model evaluation
    suite = Suite("DigitRecognizer1.0")

    # Add properties of interest
    suite.add_property(TaskEfficacy())
    suite.add_property(StorageCost())
    suite.add_property(TrainingComputeCost())
    suite.add_property(TrainingMemoryCost())

    # Return the completed suite
    return suite


# -----------------------------------------------------------------------------
# Select Measurements
# -----------------------------------------------------------------------------


KB = 2**10
MB = 2**20
GB = 2**30


def select_measurements(
    suite: Suite,
) -> Tuple[
    LocalObjectSize, LocalProcessCPUUtilization, LocalProcessMemoryConsumption
]:
    """
    Select measurements and associate them with properties.

    This function demonstrates the process of selecting
    measurements for quantitative model evaluation with MLTE.

    For each of the measurements we select, we perform the
    following three steps to integrate it into our evaluation:

        1. Instantiate the measurement
        2. Attach a validator that verifies the measurement result
        3. Bind the measurement to a property in the suite
    """

    # Create a measurement for the size of the trained model;
    # attach a validator for the size, and bind to suite property
    measure_size = bind(
        LocalObjectSize().with_validator_size_not_greater_than(
            threshold=1 * GB
        ),
        suite.get_property("StorageCost"),
    )

    # Create a measurement for the CPU utilization of the training process;
    # bind the measurement to the `TrainingComputeCost` property;
    # add a validator to the measurement as a distinct step
    measure_cpu = bind(
        LocalProcessCPUUtilization(), suite.get_property("TrainingComputeCost")
    )
    measure_cpu.with_validator_max_utilization_not_greater_than(threshold=0.9)

    # Create a measurement for memory consumption of the training process;
    # bind the measurement to the `TrainingMemoryCost` property;
    # add a validator to the measurement as a distinct step
    measure_mem = bind(
        LocalProcessMemoryConsumption(),
        suite.get_property("TrainingMemoryCost"),
    )
    measure_mem.with_validator_max_consumption_not_greater_than(
        threshold=1 * GB // KB
    )

    # Return the prepared measurements
    return measure_size, measure_cpu, measure_mem


# -----------------------------------------------------------------------------
# Define a Custom Measurement
# -----------------------------------------------------------------------------


class ClassificationAccuracy(Measurement):
    """Measure the accuracy of an image classifier."""

    def __init__(self):
        """Initialize a ClassificationAccuracy instance."""
        super().__init__("ClassificationAccuracy")

    def __call__(self, model, features, labels) -> Dict[str, Any]:
        """
        Compute classification accuracy for the given model.

        :param model: The trained model
        :param features The input features (array or tensor)
        :param labels The input labels (array or tensor)

        :return Classification accuracy on the given dataset
        """
        metrics = model.evaluate(features, labels, return_dict=True)
        return {"accuracy": metrics["accuracy"]}

    def with_validator_accuracy_not_less_than(
        self, threshold: float
    ) -> Measurement:
        """
        Add a validator for the classification accuracy

        :param threshold The minimum acceptable accuracy

        :return The measurement instance (`self`)
        """
        return self.with_validator(
            Validator(
                "MinimumAccuracy",
                lambda result: Success(
                    (
                        f"Accuracy {result.data['accuracy']:.2f}"
                        f" above threshold {threshold}."
                    )
                )
                if result.data["accuracy"] >= threshold
                else Failure(
                    (
                        f"Accuracy {result.data['accuracy']:.2f}"
                        f" below threshold {threshold}."
                    )
                ),
            )
        )


# -----------------------------------------------------------------------------
# Collect Measurements + Integrate with External Tools
# -----------------------------------------------------------------------------


def _spawn_training_process():
    """Spawn the training process."""
    prog = subprocess.Popen(["python", "train.py", "model.tf"])
    thread = threading.Thread(target=lambda: prog.wait())
    thread.start()
    return prog


def collect_measurements(
    measure_size: LocalObjectSize,
    measure_cpu: LocalProcessCPUUtilization,
    measure_mem: LocalProcessMemoryConsumption,
    measure_accuracy: ClassificationAccuracy,
) -> List[ValidationResult]:
    # Load the test dataset
    (_, _), (X_test, y_test), (_, _) = load_data()

    # Validate model accuracy
    test_accuracy = measure_accuracy.validate(
        load_model(MODEL_PATH), X_test, y_test
    )
    print(f"[+] {test_accuracy[0].message}")
    log_param("test_accuracy", test_accuracy[0].data["accuracy"])

    # Validate model size
    model_size = measure_size.validate(MODEL_PATH)
    print(f"[+] {model_size[0].message}")
    log_param("model_size", model_size[0].data.value)

    program = _spawn_training_process()
    cost_results = concurrently(
        lambda: measure_cpu.validate(program.pid),
        lambda: measure_mem.validate(program.pid),
    )

    print(f"[+] {cost_results[0][0].message}")
    print(f"[+] {cost_results[1][0].message}")

    log_param("avg_cpu_utilization", cost_results[0][0].data.avg)
    log_param("avg_memory_consumption", cost_results[0][1].data.avg)

    return flatten(test_accuracy, model_size, cost_results)


# -----------------------------------------------------------------------------
# Generate a Report
# -----------------------------------------------------------------------------


def parse_arguments() -> str:
    """Parse commandline arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("tracking_uri", type=str, help="MLflow tracking URI.")
    args = parser.parse_args()
    return args.tracking_uri


def main() -> int:
    """
    Generate a MLTE model evaluation report.
    """
    assert os.path.exists(
        MODEL_PATH
    ), "Trained model should be present before evaluation."
    tracking_uri = parse_arguments()

    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment("digit-recognizer")

    # Build the initial report
    report = build_report()

    # Build the evaluation suite
    suite = build_suite()

    # Bind pre-defined measurements to suite
    measure_size, measure_cpu, measure_mem = select_measurements(suite)

    # Bind custom measurement to suite
    measure_accuracy = bind(
        ClassificationAccuracy().with_validator_accuracy_not_less_than(
            threshold=0.65
        ),
        suite.get_property("TaskEfficacy"),
    )

    # Collect measurements
    evidence = collect_measurements(
        measure_size, measure_cpu, measure_mem, measure_accuracy
    )

    # Attach measurements to suite
    report.suite = suite.collect(*evidence)

    # Render the final report
    render(report)

    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
