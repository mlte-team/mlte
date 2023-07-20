# Extending MLTE
If the current MLTE measurement offerings are not sufficient for your project, there are a number of ways to expand or customize MLTE to work for you.

## 1. Using MLTE Value Types
If you are looking to use your own functions or those from another library (such as [Scikit Learn](https://scikit-learn.org/stable/)), but you are content to wrap the output of those functions in one of the existing MLTE Value types, this option is for you. See below for a demonstration of how to wrap your function output in the proper MLTE Value type and persist it to the MLTE artifact store.

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

## 2. Writing MLTE Value Types
If you want to use your own functions (or those from another library), and you do not want to use one of the existing MLTE Value types, then you can write your own Value type but you **must implement Value**.  
There are two paths to writing MLTE Value types:
1. You can write a MLTE type that implements Value and keep it internal to your use of MLTE.
2. You can write a MLTE type that implements Value and contribute it back to MLTE by opening a pull request.  

See below for an example of how to write a MLTE value type, regardless of whether you are maintaining it internally or submitting it as a contribution to MLTE.

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

## 3. Writing Custom Measurements
If you would like to create everything on your own, you can write your own custom MLTE measurement.
Similar to writing a MLTE Value type, you can pursue one of two paths when you write your custom measurement:
1. You can write a measurement and keep it internal to your use of MLTE.
2. You can write a measurement and contribute it back to MLTE by opening a pull request.  

See below for an example of how to write a custom measurement, regardless of whether you are maintaining it internally or submitting it as a contribution to MLTE.

```Python
from typing import Any

from mlte.measurement import Measurement
from mlte.value.types import Real

# Define a custom measurement

class ClassificationAccuracy(Measurement):
    """Measure the accuracy of an image classifier."""
    def __init__(self):
        """Initialize a ClassificationAccuracy instance."""
        super().__init__("ClassificationAccuracy")

    def __call__(self, model, features, labels) -> Real:
        """
        Compute classification accuracy for the given model.
        
        :param model: The trained model
        :param features The input features (array or tensor)
        :param labels The input labels (array or tensor)

        :return Classification accuracy on the given dataset
        """
        metrics = model.evaluate(features, labels, return_dict=True)
        return Real(self.metadata, metrics["accuracy"])

```

## Contact
If you have further questions about MLTE that were not answered here in the [documentation](https://mlte.readthedocs.io/en/latest/index.html) or in the [framework](https://github.com/mlte-team/mlte-framework), you can reach out to the MLTE Team using our email: mlte dot team dot info at gmail dot com.