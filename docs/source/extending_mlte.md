# Extending MLTE
If the current MLTE measurement offerings are not sufficient for your project, there are a number of ways to expand or customize MLTE to work for you.

## 1. Using MLTE Result Types
If you are looking to use your own functions or those from another library (such as [Scikit Learn](https://scikit-learn.org/stable/)), but you are content to wrap the output of those functions in one of the existing MLTE Result types, this option is for you. See below for a demonstration of how to wrap your function output in the proper MLTE Result type and persist it to the MLTE artifact store.

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

## 2. Writing MLTE Result Types
If you want to use your own functions (or those from another library), and you do not want to use one of the existing MLTE Result types, then you can write your own Result type but you **must implement Result**.  
There are two paths to writing MLTE result types:
1. You can write a MLTE type that implements Result and keep it internal to your use of MLTE.
2. You can write a MLTE type that implements Result and contribute it back to MLTE by opening a pull request.  

See below for an example of how to write a MLTE result type, regardless of whether you are maintaining it internally or submitting it as a contribution to MLTE.

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

## 3. Writing Custom Measurements
If you would like to create everything on your own, you can write your own custom MLTE measurement.
Similar to writing a MLTE Result type, you can pursue one of two paths when you write your custom measurement:
1. You can write a measurement and keep it internal to your use of MLTE.
2. You can write a measurement and contribute it back to MLTE by opening a pull request.  

See below for an example of how to write a custom measurement, regardless of whether you are maintaining it internally or submitting it as a contribution to MLTE.

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

## Contact
If you have further questions about MLTE that were not answered here in the [documentation](https://mlte.readthedocs.io/en/latest/index.html) or in the [framework](https://github.com/mlte-team/mlte-framework), you can reach out to the MLTE Team using our email: mlte dot team dot info at gmail dot com.