# Define Requirements

## Write a Specification
Teams construct a specification by selecting the characteristics the model must exhibit to be considered acceptable, which we call properties. Properties may be any attribute of the trained model, the procedure used to train it (including training data), or its ability to perform inference. See below for an example.

### Preliminaries
To begin, we set up depdencies for running the package locally.
```python
# Prerequisites for loading the package locally
import os
import sys

def package_root() -> str:
    """Resolve the path to the project root."""
    return os.path.abspath(os.path.join(os.getcwd(), "..", "src/"))

sys.path.append(package_root())
```

### Initialize MLTE Context
MLTE contains a global context that manages the currently active session. Initializing the context tells MLTE how to store all of the artifacts that it produces and should be done each time you use MLTE.

```python
import mlte

store_path = os.path.join(os.getcwd(), "store")

mlte.set_model("IrisClassifier", "0.0.1")
mlte.set_artifact_store_uri(f"local://{store_path}")
```

### Write the Specification
```python
from mlte.spec import Spec, Condition

from mlte.property.costs import (
    StorageCost,
    TrainingComputeCost,
    TrainingMemoryCost
)
from mlte.property.functionality import TaskEfficacy

from mlte.measurement.storage import LocalObjectSize
from mlte.measurement.cpu import LocalProcessCPUUtilization
from mlte.measurement.memory import LocalProcessMemoryConsumption
from mlte.measurement import ExternalMeasurement

spec = Spec({
    TaskEfficacy("Important to understand if the model is useful for this case"): 
                    [Condition("accuracy", ExternalMeasurement.__name__, "greater_or_equal_to", 0.9),
                     Condition("confusion matrix", ExternalMeasurement.__name__, "misclassification_count_less_than", 2),
                     Condition("classes", ExternalMeasurement.__name__, "ignore", "Inspect the image.")],
    StorageCost("Critical since model will be in an embedded decice"): 
                    [Condition("size", LocalObjectSize.__name__, "less_than", 3000)],
    TrainingMemoryCost("Useful to evaluate resources needed"): 
                    [Condition("mem", LocalProcessMemoryConsumption.__name__, "greater_or_equal_to", 0.9)],
    TrainingComputeCost("Useful to evaluate resources needed"): 
                    [Condition("cpu", LocalProcessCPUUtilization.__name__, "max_utilization_less_than", 5.0)]
    })
spec.save()
```

## Explore Properties
A list of the properties offered by MLTE can be found in the [framework](https://github.com/mlte-team/mlte-framework). Note that MLTE is in a protoype state and the list will be updated and extended as development continues.