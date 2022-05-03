# Examples
Below is a basic example of the workflow and conventions for using *MLTE*. Displayed are the necessary commands to import and utilize *MLTE* for a trivial model that utilizes and predicts on the MNIST dataset. 

## Installation
If *MLTE* is not already installed in your work environemnt, you will need to install it. To get the most up to date version run

```python
%pip install mlte-python
```

## Model Setup
Below is a code snippet to load a the common example MNIST dataset and pretrained tensorflow model. This model will be used to demonstrate the functionality of *MLTE*.

```python
import tensorflow as tf

def load_data():
    """Load the MNIST image dataset."""
    (X_train, y_train), (X_test, y_test) = tf.keras.datasets.mnist.load_data()
    
    X_train = tf.pad(X_train, [[0, 0], [2,2], [2,2]]) / 255
    X_test = tf.pad(X_test, [[0, 0], [2,2], [2,2]]) / 255
    X_train = tf.expand_dims(X_train, axis=3, name=None)
    X_test = tf.expand_dims(X_test, axis=3, name=None)
    X_train = tf.repeat(X_train, 3, axis=3)
    X_test = tf.repeat(X_test, 3, axis=3)
    
    X_val = X_train[-2000:,:,:,:]
    y_val = y_train[-2000:]
    
    X_train = X_train[:-2000,:,:,:]
    y_train = y_train[:-2000]

    return (X_train, y_train), (X_test, y_test), (X_val, y_val)

def load_model(path: str):
    """Load a model from the specified path."""
    return tf.keras.models.load_model(path)    
```

## Select Measurements
Currently there are several measurements already implemented in *MLTE* measurement pacakage. As development continues, more measurements will be added. Below we demonstrate the process of binding measurements and their associated validators to the respective properties in a suite collection. 

```python
from mlte.measurement import bind
from mlte.measurement.storage import LocalObjectSize
from mlte.measurement.cpu import LocalProcessCPUUtilization 
from mlte.measurement.memory import LocalProcessMemoryConsumption

KB = 2**10
MB = 2**20
GB = 2**30

# Create a measurement for the size of the trained model;
# attach a validator for the size, and bind to suite property
measure_size = bind(
    LocalObjectSize().with_validator_size_not_greater_than(threshold=64*MB),
    suite.get_property("StorageCost")
)

# Create a measurement for the CPU utilization of the training process;
# attach a validator for the maximum utilization, and bind to suite property
measure_cpu = bind(
    LocalProcessCPUUtilization().with_validator_max_utilization_not_greater_than(threshold=0.9),
    suite.get_property("TrainingComputeCost")
)

# Create a measurement for memory consumption of the training process;
# attach a validator for the maximum consumption, and bind to suite property
measure_mem = bind(
    LocalProcessMemoryConsumption().with_validator_max_consumption_not_greater_than(threshold=1*GB/KB),
    suite.get_property("TrainingMemoryCost")
)
```

## Define a Custom Measurement
*MLTE* allows users to easly implement their own custom measurements. This is an important feature becuase many models may require unique or novel measurements for different properties. Below is a demostration of creating a novel "classification accuracy" metric in *MLTE*. 

```python
from typing import Dict, Any

from mlte.measurement import Measurement
from mlte.measurement.evaluation import Opaque
from mlte.measurement.validation import Validator, Success, Failure

# Define a custom measurement

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
                lambda result: Success(f"Accuracy {result.data['accuracy']:.2f} above threshold {threshold}.")
                if result.data["accuracy"] >= threshold 
                else Failure(f"Accuracy {result.data['accuracy']:.2f} below thresold {threshold}.")
            )
        )

# Create a measurement for classification accuracy;
# add a validator for the minimum acceptable accuracy, and bind to suite property
measure_accuracy = bind(
    ClassificationAccuracy().with_validator_accuracy_not_less_than(threshold=0.65),
    suite.get_property("Accuracy")
)
```

## Collect and Validate Measurements
Measurements have an associated validator that must be validated. Below we demonstrate the validation process

```python
import threading
import subprocess

from mlte.measurement.utility import concurrently

def spawn_training_process():
    """Spawn the training process."""
    prog = subprocess.Popen(["python", "train.py", "model.tf"])
    thread = threading.Thread(target=lambda: prog.wait())
    thread.start()
    return prog

# Load the test dataset
(_, _), (X_test, y_test), (_, _) = load_data()

# Validate model accuracy
test_accuracy = measure_accuracy.validate(
    load_model(MODEL_PATH),
    X_test,
    y_test)

print(test_accuracy[0].message)

# Validate model size
model_size = measure_size.validate(MODEL_PATH)

print(model_size[0].message)

program = spawn_training_process()
cost_results = concurrently(
    lambda: measure_cpu.validate(program.pid),
    lambda: measure_mem.validate(program.pid)
)

print(cost_results[0][0].message)
print(cost_results[1][0].message)
```

## Build a Suite
Suites are collections of properties that developers have prioritized for evaluating the model. Below we show the creation of a suite that contains four properties, accuracy, storage costs, training compute cost, and training memory cost. The Suite is named "DigitRecognizer1.0"

```python
from mlte.suites import Suite
from mlte.properties.costs import (
    StorageCost,
    TrainingComputeCost,
    TrainingMemoryCost
)
from mlte.properties.functionality import Accuracy

# Construct a suite with the selected properties
suite = Suite("DigitRecognizer1.0")
suite.add_property(Accuracy())
suite.add_property(StorageCost())
suite.add_property(TrainingComputeCost())
suite.add_property(TrainingMemoryCost())
```

## Build a Report
Automatically generated reports are an important function of *MLTE*. The report format was heavily influenced by [ModelCards](https://ai.googleblog.com/2020/07/introducing-model-card-toolkit-for.html)

```python
import time
from mlte.report import (
    Report,
    Dataset,
    User,
    UseCase,
    Limitation
)

# Begin a report
report = Report()

# Populate report metadata
report.metadata.project_name = "Digit Recognition"
report.metadata.authors = ["Kyle Dotterrer", "Kate Maffey", "Jenny Niemann"]
report.metadata.source_url = "https://github.com/mlte-team/source"
report.metadata.artifact_url = "https://mlte-team-data.s3.amazonaws.com"
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
report.model_specification.output = "Probability distribution over 10 classes."
report.model_specification.data = [
    Dataset(
        "ILSVRC2012",
        "https://image-net.org/challenges/LSVRC/2012/",
        "ImageNet Large Scale Visual Recognition Challenge 2012")
]

# Populate report considerations
report.considerations.users = [
    User("Human resources staff.")
]

report.considerations.use_cases = [
    UseCase("Optical character recognition.")
]

report.considerations.limitations = [
    Limitation("Classification results are sensitive to image rotation.")
]
```

## Generate a Report
After a report is created, it must be generated to create and display the html output

```python
import time
from mlte.report import (
    Report,
    Dataset,
    User,
    UseCase,
    Limitation
)

# Begin a report
report = Report()

# Populate report metadata
report.metadata.project_name = "Digit Recognition"
report.metadata.authors = ["Kyle Dotterrer", "Kate Maffey", "Jenny Niemann"]
report.metadata.source_url = "https://github.com/mlte-team/source"
report.metadata.artifact_url = "https://mlte-team-data.s3.amazonaws.com"
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
report.model_specification.output = "Probability distribution over 10 classes."
report.model_specification.data = [
    Dataset(
        "ILSVRC2012",
        "https://image-net.org/challenges/LSVRC/2012/",
        "ImageNet Large Scale Visual Recognition Challenge 2012")
]

# Populate report considerations
report.considerations.users = [
    User("Human resources staff.")
]

report.considerations.use_cases = [
    UseCase("Optical character recognition.")
]

report.considerations.limitations = [
    Limitation("Classification results are sensitive to image rotation.")
]
```

