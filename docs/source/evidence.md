# Collect Evidence

## Import/Explore Measurements
When using MLTE, model developers determine how the model performs against the previously set [requirements](requirements.md) by collecting values that attest to the satisfaction of particular properties. They do so by defining and executing measurements — functions that assess phenomena related to the property of interest.
Here we demonstrate importing a MLTE-defined measurement, which is then invoked to produce a Value. This Value can then be inspected and automatically saved to the artifact store.

```Python
from mlte.measurement.storage import LocalObjectSize
from mlte.value.types import Integer

# Create a measurement
measurement = LocalObjectSize("model size")
# Execute the measurement
size: Integer = measurement.evaluate(MODELS_DIR / "model.pkl")

# Inspec values
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

# Inspect values
print(cpu_stats)
```

### Measurement of Local Object Size
```Python
from mlte.measurement.storage import LocalObjectSize
from mlte.value.types import Integer

# Create a measurement
measurement = LocalObjectSize("model size")
# Execute the measurement
size: Integer = measurement.evaluate(MODELS_DIR / "model.pkl")
```

## Persist Values
Persisting values with MLTE is simple. See the following example, which uses the Local Object Size from above.

```Python
from mlte.measurement.storage import LocalObjectSize
from mlte.values.type import Integer

# Create a measurement
measurement = LocalObjectSize("model size")
# Execute the measurement
size: Integer = measurement.evaluate(MODELS_DIR / "model.pkl")

# Inspec values
print(size)

# Save to artifact store
size.save()
```

## Ingest External Functionality
Users can wrap the output of external measurements in a suitable Value type to integrate them into MLTE. In the following example, we wrap the output from the accuracy score function from [scikit learn](https://scikit-learn.org/stable/modules/model_evaluation.html#accuracy-score) with a built in MLTE type (Real) to integrate it with our collection of evidence, by using ExternalMeasurement. The Real Value instance is then persisted to the MLTE artifact store.

```Python
from sklearn.metrics import accuracy_score

from mlte.value.types import Real
from mlte.measurement import ExternalMeasurement

# Evaluate performance
accuracy_measurement = ExternalMeasurement("accuracy", Real, accuracy_score)
accuracy = accuracy_measurement.evaluate(y_test, y_pred)

# Inspect value
print(accuracy)

# Save to artifact store
accuracy.save()
```

## Define Custom Values
Here, we define a custom Value type to cope with the output of a third-party library that is not built into MLTE. This is similar to the use-case above, except we create a custom Value type instead of using one that is already built in MLTE.

```Python
from sklearn.metrics import confusion_matrix
from confusion_matrix import ConfusionMatrix
from mlte.measurement import ExternalMeasurement

# Generate value
matrix_measurement = ExternalMeasurement("confusion matrix", ConfusionMatrix, confusion_matrix)
matrix = matrix_measurement.evaluate(y_test, y_pred)

# Inspect
print(matrix)

# Save to artifact store
matrix.save()
```

## Define Custom Measurements
MLTE supports the definition of custom measurements. See [Extending MLTE](extending_mlte.md) for more details.
