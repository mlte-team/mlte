# Using MLTE

Now that you've [set up `MLTE`](getting_started.md), you're ready to use it. We at the `MLTE` Team believe that effective evaluation starts at the inception of a project, so that's where `MLTE` starts. 

## 1. Negotiate Model Quality Requirements

Step 1 is a negotiation - a discussion about requirements - amongst stakeholders, software engineers, data scientists, and anyone else involved in the project. 

- Determine who is facilitating the negotiation and ensure they have reviewed the instructions and content for the negotiation card, which can be found in the `MLTE` user interface. (If they have not yet set up `MLTE`, send them to our [Getting Started](getting_started.md) page.)
    - The most important portion of the negotiation is determining the system goals and their corresponding performance metrics and baseline. This ensures you will be able to evaluate if your model is adding value. 
- The negotiation is meant to be a collaborative discussion where all involved parties can agree on project requirements and can discuss some of the technical details that are important.
- Once the negotiation is complete and the negotiation card is filled in, development can begin. The negotiation card gives the team a reference for project goals and allows them to plan out their development cycles appropriately.

## 2. Internal Model Testing (IMT)

Step 2 ensues after initial model development has been completed and the team has a model that is ready for a first round of testing. In IMT, the development team evaluates how the model performs against its baseline on the chosen performance metrics for each system goal. Evaluation in `MLTE` follows this process:

- Initialize the `MLTE` context.
- Define a preliminary specification.
- Collect evidence.
- Validate results.
- Examine findings.

### IMT: Initialize the MLTE Context

`MLTE` contains a global context that manages the currently active session. Initializing the context tells `MLTE` how to store all of the artifacts that it produces.

```python
import os
from mlte.session import set_context, set_store

store_path = os.path.join(os.getcwd(), "store")
os.makedirs(store_path, exist_ok=True)   # Ensure we are creating the folder if it is not there.

set_context("ns", "IrisClassifier", "0.0.1")
set_store(f"local://{store_path}")
```

### IMT: Define a Preliminary `Specification`

A `Specification` (or `Spec`) represents the requirements the completed model must meet in order to be acceptable for use in the system into which it will be integrated. Full `Spec` definition will be completed in [SDMT](#4-system-dependent-model-testing-sdmt); in IMT, we use it in a preliminary fashion so the development team can do an initial round of model testing. Here we define a `Spec` using accuracy as a performance metric. We also add in further initial testing capacity by including a confusion matrix and class distribution.

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

After building the `Spec`, `MLTE` allows you to collect evidence to attest to whether or not the model realizes the desired properties. Here we collect evidence by wrapping the output from scikit-learn's <a href="https://scikit-learn.org/stable/modules/model_evaluation.html#accuracy-score" target="_blank">accuracy_score</a> with a builtin `MLTE` type (Real). Note that this example does not include data and model training code, but those can be found in the full `MLTE` <a href="https://github.com/mlte-team/mlte/tree/500a80c9dd15310e1f37b127a289472533200c24/demo" target="_blank">demo notebooks</a>.

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

To communicate results and examine findings, `MLTE` produces a report. While IMT is intended to be an initial and preliminary evaluation, the report is an artifact that will aid in the second [negotiation point](#3-negotiate-model-requirements-beyond-task-efficacy). You can import content from your negotiation card using the `MLTE` UI, and the fields can be customized as needed.

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

Once the descriptive portions of the report are defined, you can render the report to examine your findings.

```python
from mlte.report import render

# Build the base report
report = build_report()
# Attach the validated specification
report.spec = validated_spec

# Save the report as an HTML document
report.to_html(REPORTS_DIR / "report.html", local=True)
```

IMT is an iterative process - the development team will likely repeat it several times given the exploratory nature of many machine learning projects.

## 3. Negotiate Model Requirements Beyond Task Efficacy

After completing IMT, development teams should have a sense of how their model performs on the core project performance metric against the chosen baseline. Step 3 is another negotiation amongst everyone involved in the project: stakeholders, software engineers, data scientists, and anyone else involved such as a project manager.

- The emphasis of this negotiation is to review the discussion in [step 1](#1-negotiate-model-quality-requirements) and update it based on the intial evaluation that was performed in [step 2](#2-internal-model-testing-imt).
- It is also important to ensure that the development team has all the information they need to build out a `Specification` (`Spec`) after this negotiation.
- To conduct the negotiation, ensure the facilitator has the negotiation card for the project and that they are comfortable with the `MLTE` user interface.

Once the negotiation is complete and the contents of the negotiation card have been updated, the development team will conduct a comprehensive round of testing as part of System Dependent Model Testing, step 4.

## 4. System Dependent Model Testing (SDMT)

SDMT ensures that a model will function as intended when it is part of a larger system. Using the updated negotiation card, development teams must define a `Specification` (`Spec`) that evaluates all relevant dimensions for the overall system to function. To do so, `MLTE` uses the following process:

- Initialize the `MLTE` context.
- Define a preliminary specification.
- Collect evidence.
- Validate results.
- Examine findings.

### SDMT: Initialize the MLTE Context

Similar to IMT, you begin by initializing the context to tell `MLTE` how to store all of the artifacts it produces.

```python
import os
from mlte.session import set_context, set_store

store_path = os.path.join(os.getcwd(), "store")
os.makedirs(store_path, exist_ok=True)   # Ensure we are creating the folder if it is not there.

set_context("ns", "IrisClassifier", "0.0.1")
set_store(f"local://{store_path}")
```

### SDMT: Define a `Specification`

A `Spec` represents the requirements and corresponding thresholds (or validators) the completed model must meet in order to be acceptable for use in the system into which it will be integrated.

- Teams design a specification by selecting and prioritizing the model requirements that are important to their project from the list of `MLTE` [*properties*](properties.md). 
- To validate that a requirement for a property is met by an ML model and system, `MLTE` uses *measurements*, which correspond to properties. Selecting measurements that correspond to properties is part of `Spec` definition.

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

After building the `Spec`, teams must collect evidence to attest to whether or not the model realizes the desired properties. Here we demonstrate a few different ways to collect evidence. Note that this example does not include data and model training code, but those can be found in the full `MLTE` <a href="https://github.com/mlte-team/mlte/tree/master/demo" target="_blank">demo notebooks</a>.

#### Evidence: MLTE Measurements

The simplest use-case is to import a MLTE-defined `Measurement`, which is then invoked to produce a `Value`. This value can then be inspected and automatically saved to the artifact store. Following are two examples of this type of evidence collection.

```python
from mlte.measurement.storage import LocalObjectSize
from mlte.value.types.integer import Integer

# Create a measurement
store_measurement = LocalObjectSize("model size")
# Execute the measurement
size: Integer = store_measurement.evaluate(MODELS_DIR / "model_demo.pkl")

# Inspec values
print(size)

# Save to artifact store
size.save()
```

```python
script = Path.cwd() / "train.py"
args = [
    "--dataset-dir", str(DATASETS_DIR.absolute()),
    "--models-dir", str(MODELS_DIR.absolute())
]

from mlte.measurement import ProcessMeasurement
from mlte.measurement.cpu import LocalProcessCPUUtilization, CPUStatistics

# Create a measurement
cpu_measurement = LocalProcessCPUUtilization("training cpu")
# Execute the measurement
cpu_stats: CPUStatistics = cpu_measurement.evaluate(ProcessMeasurement.start_script(script, args))

# Inspect values
print(cpu_stats)

# Save to artifact store
cpu_stats.save()
```

#### Evidence: External Measurements

Given the existence of many libraries that offer easy evaluation of machine learning models, `MLTE` is built to be able to integrate results from any external library. In this example, we simply wrap the output from accuracy_score with a builtin `MLTE` type (Real) to integrate it with our collection of evidence.
 
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

#### Evidence: Custom Types for External Measurements

`MLTE` also allows users to define custom types to cope with the output of a third-party library that is not supported by a `MLTE` builtin.

```python
from sklearn.metrics import confusion_matrix
from confusion_matrix import ConfusionMatrix
from mlte.measurement import ExternalMeasurement

# Generate value
matrix_measurement = ExternalMeasurement("confusion matrix", ConfusionMatrix, confusion_matrix)
matrix = matrix_measurement.evaluate(y_test, y_pred)

# Inspect
print(matrix)

# Save to artifact store
matrix.save(parents=True)
```

#### Evidence: Alternative Media in Measurements

In addition to typical evaluation outputs, `MLTE` also allows for integration of other forms of media in the evidence collection process.

```python
import matplotlib.pyplot as plt

from mlte.measurement import ExternalMeasurement
from mlte.value.types.image import Image

x = ["Setosa", "Versicolour", "Virginica"]
y = [sum(1 for value in y_pred if value == target) for target in [0, 1, 2]]

plt.bar(x, y)
plt.title("Distribution of Predicted Classes")
plt.xlabel("Class Label")
plt.xticks([0, 1, 2])
plt.ylabel("Occurrences")
plt.savefig(MEDIA_DIR / "classes.png")

img_collector = ExternalMeasurement("class distribution", Image)
img = img_collector.ingest(MEDIA_DIR / "classes.png")

img.save()
```

### SDMT: Validate Results

After collecting evidence, `MLTE` requires the validation of that evidence. To do so, we create a `SpecValidator` and add all the `Value`s we have collected. That allows us to validate our `Spec` and generate a `ValidatedSpec` which has the validation results.

```python
from mlte.spec import Spec, SpecValidator
from mlte.value.types.integer import Integer
from mlte.value.types.real import Real
from mlte.value.types.image import Image
from mlte.measurement.cpu import CPUStatistics
from mlte.measurement.memory import MemoryStatistics
from confusion_matrix import ConfusionMatrix

# Load the specification
spec = Spec.load()

# Add all values to the validator.
spec_validator = SpecValidator(spec)
spec_validator.add_value(Integer.load("model size"))
spec_validator.add_value(CPUStatistics.load("training cpu"))
spec_validator.add_value(MemoryStatistics.load("training memory"))
spec_validator.add_value(Real.load("accuracy"))
spec_validator.add_value(ConfusionMatrix.load("confusion matrix"))
spec_validator.add_value(Image.load("class distribution"))
```

```python
# Validate requirements and get validated details.
validated_spec = spec_validator.validate()

# ValidatedSpec also supports persistence
validated_spec.save()
```

After validating results, development teams need to communicate the results of their evaluation with the rest of the project team. 

## 5. Communicate ML Evaluation Results

To communicate results and examine findings, `MLTE` produces a report that encapsulates all knowledge gained about the model and the system as a consequence of the evaluation process. Teams can import content from the negotiation card using the `MLTE` UI, and the fields can be customized as needed. Similar to the process during IMT, we start by defining the descriptive portions of the report.

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

Once the descriptive portions of the report are defined, you can render the report to examine your findings and communicate them to the rest of the team.

```python
from mlte.report import render

# Build the base report
report = build_report()
# Attach the validated specification
report.spec = validated_spec

# Save the report as an HTML document
report.to_html(REPORTS_DIR / "report.html", local=True)
```

If the model performs as desired, teams can consider the evaluation complete. However, it is very common that teams will need to iterate through [IMT](#2-internal-model-testing-imt) and [SDMT](#4-system-dependent-model-testing-sdmt) several times before they are satisfied with the results and ready to communicate with stakeholders.

## More Information

If this guide makes you want to learn more about `MLTE`, check out our <a href="https://arxiv.org/abs/2303.01998" target="_blank">paper</a>!