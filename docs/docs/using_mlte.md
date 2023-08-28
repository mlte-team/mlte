# Using MLTE

Now that you've [set up MLTE](getting_started.md), you're ready to use it. We at the MLTE Team believe that effective evaluation starts at the inception of a project, so that's where MLTE starts. Step 1 is a negotiation (a discussion about requirements) amongst stakeholders, software engineers, data scientists, and anyone else involved in the project. 

## 1. Negotiate Model Quality Requirements

- Determine who is facilitating the negotiation and ensure they have reviewed the instructions and content for the negotiation card, which can be found in the MLTE user interface. (If they have not yet set up MLTE, send them to our [Getting Started](getting_started.md) page.)
    - The most important portion of the negotiation is determining the system goals and their corresponding performance metrics and baseline. This ensures you will be able to tell if your model is adding value. 
- Once the negotiation card is complete, development can begin. The negotiation card should give the team a strong sense of the project goals and allow them to plan out their development cycles appropriately before beginning.

The next MLTE step ensues after initial model development has been completed and the team has a model that is ready for a first round of testing.

## 2. Internal Model Testing (IMT)

In IMT, you and your team evaluate how your model performs against the baseline on the performance metrics for each system goal. 
- Initialize the MLTE context.
- Define a preliminary specification.
- Collect evidence.
- Validate results.
- Examine findings.

### IMT: Initialize the MLTE Context

MLTE contains a global context that manages the currently active session. Initializing the context tells MLTE how to store all of the artifacts that it produces.

```python
import os
from mlte.session import set_context, set_store

store_path = os.path.join(os.getcwd(), "store")
os.makedirs(store_path, exist_ok=True)   # Ensure we are creating the folder if it is not there.

set_context("ns", "IrisClassifier", "0.0.1")
set_store(f"local://{store_path}")
```

### IMT: Define a Preliminary `Specification`

A `Specification` (or `Spec`) represents the requirements the completed model must meet in order to be acceptable for use in the system into which it will be integrated. Full `Spec` definition will be completed in SDMT; in IMT, we use it in a preliminary fashion so the development team can do an internal round of model testing. Here we define a `Spec` using accuracy as a performance metric. We also add in further initial testing capacity by including a confusion matrix and class distribution.

```python
from mlte.spec.spec import Spec

from mlte.property.functionality import TaskEfficacy

spec = Spec(properties={
    TaskEfficacy("Important to understand if the model is useful for this case"): 
                    {"accuracy": Real.greater_or_equal_to(0.98),
                     "confusion matrix": ConfusionMatrix.misclassification_count_less_than(2),
                     "class distribution": Image.ignore("Inspect the image.")}
    })
spec.save(parents=True, force=True)
```

### IMT: Collect Evidence

After building the `Spec`, MLTE allows you to collect evidence to attest to whether or not the model realizes the desired properties. Here we collect evidence by wrapping the output from scikit-learn's [accuracy_score](https://scikit-learn.org/stable/modules/model_evaluation.html#accuracy-score) with a builtin MLTE type (Real). Note that this example does not include data and model training code, but those can be found in the full MLTE [demo notebooks](https://github.com/mlte-team/mlte/tree/500a80c9dd15310e1f37b127a289472533200c24/demo).

```python
from sklearn.metrics import accuracy_score

from mlte.value.types.real import Real
from mlte.measurement import ExternalMeasurement

# Evaluate performance
accuracy_measurement = ExternalMeasurement("accuracy", Real, accuracy_score)
accuracy = accuracy_measurement.evaluate(y_test, y_pred)

# Inspect value
print(accuracy)

# Save to artifact store
accuracy.save(parents=True)
```

### IMT: Validate Results
Now that we have evidence and a `Spec`, we can create a `SpecValidator` and add all the `Value`s we have. With that we can generate a `ValidatedSpec` which contains validated results or *findings*.

```python
from mlte.spec import Spec, SpecValidator
from mlte.value.types.real import Real
from confusion_matrix import ConfusionMatrix
from mlte.value.types.image import Image

# Load the specification
spec = Spec.load()

# Add values to the validator.
spec_validator = SpecValidator(spec)
spec_validator.add_value(Real.load("accuracy"))
spec_validator.add_value(ConfusionMatrix.load("confusion matrix"))
spec_validator.add_value(Image.load("class distribution"))

# Validate requirements and get validated details.
validated_spec = spec_validator.validate()

# ValidatedSpec also supports persistence
validated_spec.save()
```

### IMT: Examine Findings

To communicate results, MLTE produces a report. You can import content from your negotiation card using the MLTE UI, and the fields can be customized as needed.

```python
import time
from mlte.report import Report, Dataset, User, UseCase, Limitation

def unix_timestamp() -> str:
    return f"{int(time.time())}"

def build_report() -> Report:
    report = Report()
    report.metadata.project_name = "Your Project"
    report.metadata.authors = ["Jane Doe", "Joe Smith"]
    report.metadata.source_url = "https://github.com/mlte-team"
    report.metadata.artifact_url = "https://github.com/mlte-team"
    report.metadata.timestamp = unix_timestamp()

    report.model_details.name = "IrisClassifier"
    report.model_details.overview = "A model that distinguishes among three (3) types of irises."
    report.model_details.documentation = "This is a simple model that can distinguish between the setosa, versicolour, and virginica species of Iris based on physical characteristics."

    report.model_specification.domain = "Classification"
    report.model_specification.architecture = "Decision Tree"
    report.model_specification.input = "Vector[4]"
    report.model_specification.output = "Binary"
    report.model_specification.data = [
        Dataset("Dataset0", "https://github.com/mlte-team", "This is one training dataset."),
        Dataset("Dataset1", "https://github.com/mlte-team", "This is the other one we used."),
    ]

    report.considerations.users = [
        User("Botanist", "A professional botanist."),
        User("Explorer", "A weekend-warrior outdoor explorer."),
    ]
    report.considerations.use_cases = [
        UseCase("Personal Edification", "Quench your curiosity: what species of iris IS that? Wonder no longer.")
    ]
    report.considerations.limitations = [
        Limitation(
            "Low Training Data Volume",
            """
            This model was trained on a low volume of training data.
            """,
        ),
    ]
    return report
```

Once everything is specified, you can examine your findings by rendering a report.

```python
from mlte.report import render

# Build the base report
report = build_report()
# Attach the validated specification
report.spec = validated_spec

# Save the report as an HTML document
report.to_html(REPORTS_DIR / "report.html", local=True)
```

## 3. Negotiate Model Requirements Beyond Task Efficacy

TODO: write the SDMT negotiation section

## 4. System Dependent Model Testing (SDMT)

In SDMT, you and your team evaluate how your model performs against the baseline on the performance metrics for each system goal. 
- Initialize the MLTE context.
- Define a preliminary specification.
- Collect evidence.
- Validate results.
- Examine findings.
FINISH THIS

### SDMT: Initialize the MLTE Context

Similar to IMT, you begin by initializing the context to tell MLTE how to store all of the artifacts it produces.

```python
import os
from mlte.session import set_context, set_store

store_path = os.path.join(os.getcwd(), "store")
os.makedirs(store_path, exist_ok=True)   # Ensure we are creating the folder if it is not there.

set_context("ns", "IrisClassifier", "0.0.1")
set_store(f"local://{store_path}")
```

### SDMT: Define a `Specification`

A `Specification` (or `Spec`) represents the requirements and corresponding thresholds (or validators) the completed model must meet in order to be acceptable for use in the system into which it will be integrated. 

```python
from mlte.spec.spec import Spec

from mlte.property.costs import (
    StorageCost,
    TrainingComputeCost,
    TrainingMemoryCost
)
from mlte.property.functionality import TaskEfficacy


from mlte.measurement.storage import LocalObjectSize
from mlte.measurement.cpu import LocalProcessCPUUtilization
from mlte.measurement.memory import LocalProcessMemoryConsumption
from confusion_matrix import ConfusionMatrix
from mlte.value.types.real import Real
from mlte.value.types.image import Image

spec = Spec(properties={
    TaskEfficacy("Important to understand if the model is useful for this case"): 
                    {"accuracy": Real.greater_or_equal_to(0.98),
                     "confusion matrix": ConfusionMatrix.misclassification_count_less_than(2),
                     "class distribution": Image.ignore("Inspect the image.")},
    StorageCost("Critical since model will be in an embedded decice"): 
                    {"model size": LocalObjectSize.value().less_than(3000)},
    TrainingMemoryCost("Useful to evaluate resources needed"): 
                    {"training memory": LocalProcessMemoryConsumption.value().average_consumption_less_than(0.9)},
    TrainingComputeCost("Useful to evaluate resources needed"): 
                    {"training cpu": LocalProcessCPUUtilization.value().max_utilization_less_than(5.0)}
    })
spec.save(parents=True, force=True)
```

### SDMT: Collect Evidence

After building the `Spec`, MLTE allows you to collect evidence to attest to whether or not the model realizes the desired properties. Here we demonstrate a few different ways to collect evidence.
TODO: finish writing SDMT

## 5. Communicate ML Evaluation Results