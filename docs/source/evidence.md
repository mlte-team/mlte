# Collect Evidence

## Import/Explore Measurements
When using MLTE, model developers determine how the model performs against the previously set [requirements](requirements.md) by collecting results that attest to the satisfaction of particular properties. They do so by defining and executing measurements — functions that assess phenomena related to the property of interest.
Here we demonstrate importing a MLTE-defined measurement, which is then invoked to produce a Result. This Result can then be inspected and automatically saved to the artifact store.

```Python
from mlte.measurement.storage import LocalObjectSize
from mlte.measurement.result import Integer

# Create a measurement
measurement = LocalObjectSize("model size")
# Execute the measurement
size: Integer = measurement.evaluate(MODELS_DIR / "model.pkl")

# Inspec results
print(size)
```

## Invoke/Execute Measurements
Executing a measurement depends on the type of measurement it is; below are two examples, CPU utilization statistics for a local training job and local object storage size.

### Measurement of CPU Utilization
```Python
from mlte.measurement.cpu import LocalProcessCPUUtilization, CPUStatistics

# Create a measurement
measurement = LocalProcessCPUUtilization("training cpu")
# Execute the measurement
cpu_stats: CPUStatistics = measurement.evaluate(spawn_training_job())

# Inspect results
print(cpu_stats)
```

### Measurement of Local Object Size
```Python
from mlte.measurement.storage import LocalObjectSize
from mlte.measurement.result import Integer

# Create a measurement
measurement = LocalObjectSize("model size")
# Execute the measurement
size: Integer = measurement.evaluate(MODELS_DIR / "model.pkl")
```

## Persist Results
Persisting results with MLTE is simple. See the following example, which uses the Local Object Size from above.

```Python
from mlte.measurement.storage import LocalObjectSize
from mlte.measurement.result import Integer

# Create a measurement
measurement = LocalObjectSize("model size")
# Execute the measurement
size: Integer = measurement.evaluate(MODELS_DIR / "model.pkl")

# Inspec results
print(size)

# Save to artifact store
size.save()
```

## Ingest External Functionality
Users can wrap the output of external measurements in a suitable Result type to integrate them into MLTE. In the following example, we wrap the output from the accuracy score function from [scikit learn](https://scikit-learn.org/stable/modules/model_evaluation.html#accuracy-score) with a built in MLTE type (Real) to integrate it with our collection of evidence, by using ExternalMeasurement. The Real Result instance is then persisted to the MLTE artifact store.

```Python
from sklearn.metrics import accuracy_score

from mlte.measurement.result import Real
from mlte.measurement import ExternalMeasurement

# Evaluate performance
accuracy_measurement = ExternalMeasurement("accuracy", Real)
accuracy = accuracy_measurement.evaluate(accuracy_score(y_test, y_pred))

# Inspect result
print(accuracy)

# Save to artifact store
accuracy.save()
```

## Define Custom Results
Here, we define a custom Result type to cope with the output of a third-party library that is not built into MLTE. This is similar to the use-case above, except we create a custom Result type instead of using one that is already built in MLTE.

```Python
from sklearn.metrics import confusion_matrix
from confusion_matrix import ConfusionMatrix
from mlte.measurement import ExternalMeasurement

# Generate result
matrix_measurement = ExternalMeasurement("confusion matrix", ConfusionMatrix)
matrix = matrix_measurement.evaluate(confusion_matrix(y_test, y_pred))

# Inspect
print(matrix)

# Save to artifact store
matrix.save()
```

## Define Custom Measurements
MLTE supports the definition of custom measurements. See [Extending MLTE](extending_mlte.md) for more details, and see below for an example of how to write a custom measurement.

```Python
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
# add a validator for the minimum acceptable accuracy, and bind to spec property
measure_accuracy = bind(
    ClassificationAccuracy().with_validator_accuracy_not_less_than(threshold=0.65),
    spec.get_property("Accuracy")
)
```