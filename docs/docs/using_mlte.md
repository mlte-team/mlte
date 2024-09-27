# Using MLTE

After [setting up `MLTE`](setting_up_mlte.md), the process begins at the inception of a project with requirements definition. 

If your team has an existing project and you would like to test it using  `MLTE`, navigate to the [Internal Model Testing](#internal-model-testing-imt) section for a description of testing a model with `MLTE`. However, if stakeholders have not been activley involved in the process, it is recommended to start with the Negotiation Card to make sure that both system and model requirements have been elicited and defined.

## Negotiate Model Quality Requirements

To begin the `MLTE` process, teams hold a negotiation a discussion about requirements with stakeholders that should include system/product owners, software engineers, data scientists, and anyone else involved in the project. 

- The negotiation facilitator should review the instructions and content of the Negotiation Card, which can be found in the `MLTE` user interface. To set up `MLTE`, see the [Setting Up `MLTE`](setting_up_mlte.md) page, and to view the content in the Negotiation Card, see this [page](negotiation_card.md).
- The negotiation is a collaborative discussion where all involved parties aim to agree on project requirements and discuss technical details.
- Once the negotiation is complete and the Negotiation Card is filled in as much as possible (it does not have to all be filled out at once), development can begin. The Negotiation Card gives the team a reference for project goals and allows them to plan out their development cycles appropriately.

## Internal Model Testing (IMT)

After initial model development has been completed, the team should have a model that is ready for preliminary testing. In IMT, the development team evaluates how the model performs against the baselines for the defined performance metrics for each system goal. Evaluation in `MLTE` follows this process:

1. Initialize the `MLTE` context.
2. Define a specification.
3. Collect evidence.
4. Validate results.
5. Examine findings.

### 1. Initialize the MLTE Context

`MLTE` contains a global context that manages the currently active session. Initializing the context tells `MLTE` how to store all of the artifacts that it produces. 

```python
set_context("OxfordFlower", "0.0.1")
set_store(f"local://{store_path}")
```
*Note that this code is demonstrative and does not include all imports and context; for a comprehensive example of `MLTE` code, see the <a href="https://github.com/mlte-team/mlte/tree/master/demo" target="_blank">demo notebooks</a>.*

### 2. Define a `Specification`

A `Specification` (or `Spec`) represents the requirements the model must meet in order to be acceptable for use in the system into which it will be integrated. Full `Spec` definition will be completed in [SDMT](#system-dependent-model-testing-sdmt); in IMT, we use it in a preliminary fashion so the development team can do an initial round of model testing. However, the process is the same for both stages. Here we define a `Spec` using accuracy as a performance metric. We also add in further initial testing capacity by including a confusion matrix and class distribution.

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

### 3. Collect Evidence

After building the `Spec`, `MLTE` allows you to collect evidence to attest to whether or not the model realizes the desired properties. Here we collect evidence by wrapping the output from scikit-learn's <a href="https://scikit-learn.org/stable/modules/model_evaluation.html#accuracy-score" target="_blank">accuracy_score</a> with a builtin `MLTE` type (Real). 

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

*Note that this example does not include data and model training code, but those can be found in the full `MLTE` <a href="https://github.com/mlte-team/mlte/tree/master/demo" target="_blank">demo notebooks</a>.*

### 4. Validate Results

Now that we have evidence and a `Spec`, we can create a `SpecValidator` and add all the `Value`s we have. With that we can generate a `ValidatedSpec` which contains validated results or *findings*.

```python
from mlte.spec import Spec, SpecValidator
from mlte.value.types.real import Real

# Load the specification
spec = Spec.load()

# Add values to the validator.
spec_validator = SpecValidator(spec)
spec_validator.add_value(Real.load("accuracy"))


# Validate requirements and get validated details.
validated_spec = spec_validator.validate()

# ValidatedSpec also supports persistence
validated_spec.save()
```

### 5. Examine Findings

To communicate results and examine findings, `MLTE` produces a report. While IMT is intended to be an initial and preliminary evaluation, the report is an artifact that will aid in the second [negotiation point](#negotiate-model-requirements-beyond-task-efficacy). You can import content from your negotiation card using the `MLTE` UI, and the fields can be customized as needed. The report is most easily generated using the UI, but can also be produced via code as demonstrated below.

```python
import time
from mlte.report import Report, Dataset, User, UseCase, Limitation

def unix_timestamp() -> str:
    return f"{int(time.time())}"

def build_report() -> Report:
    report = Report()
    report.metadata.project_name = "Your Project"
    report.metadata.authors = ["Jane Doe", "Joe Smith"]
    report.metadata.timestamp = unix_timestamp()

    report.model_details.name = "IrisClassifier"

    report.model_specification.domain = "Classification"
    report.model_specification.data = [
        Dataset("Dataset0", "https://github.com/mlte-team", "This is one training dataset."),
        Dataset("Dataset1", "https://github.com/mlte-team", "This is the other one we used."),
    ]

    report.considerations.users = [
        User("Botanist", "A professional botanist."),
        User("Explorer", "A weekend-warrior outdoor explorer."),
    ]
    return report
```
*Note that this example only includes a few of the report fields; a full `MLTE` report in code can be found in the <a href="https://github.com/mlte-team/mlte/tree/master/demo" target="_blank">demo notebooks</a>.*

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

## Negotiate Model Requirements Beyond Task Efficacy

After completing IMT, development teams should have a sense of how their model performs on the core project performance metric against the chosen baseline. After they have this additional information, the team conducts another negotiation amongst everyone involved in the project: stakeholders, software engineers, data scientists, and anyone else involved such as a project manager ot system/product owner.

- The emphasis of this negotiation is to review the discussion from [requirements negotiation](#negotiate-model-quality-requirements) and update it based on the intial evaluation that was performed in [IMT](#internal-model-testing-imt).
- It is also important to ensure that the development team has all the information they need to build a `Specification` (`Spec`) after this negotiation.
- It is likely that the first negotiation only resulted in some sections of the Negotiation Card being filled out, and a goal of this second negotiation should be to complete more of the sections and have a better picture of what project success will be.

Once the negotiation is complete and the contents of the Negotiation Card have been updated, the development team will conduct a comprehensive round of testing as part of System Dependent Model Testing.

## System Dependent Model Testing (SDMT)

SDMT ensures that a model will function as intended when it is part of a larger system. Using the updated Negotiation Card, development teams must define a `Specification` (`Spec`) that evaluates all relevant dimensions for the overall system to function. This follows the same process described in [IMT](#internal-model-testing-imt), with more emphasis on building out the specification. As such, this section will focus on the specification and will offer more detail on collecting different types of evidence.

Teams can search the Test Catalog to find examples of how different quality attributes were tested by other teams. Note that MLTE comes with a sample test catalog simply for reference. The goal is for organizations to create and populate their own Test catalogs over time.

### Define a System-Oriented `Specification`

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

### Collecting Evidence

After building the `Spec`, teams must collect evidence to attest to whether or not the model realizes the desired properties. Here we demonstrate a few different ways to collect evidence. Note that these examples do not include data and model training code, but those can be found in the full `MLTE` <a href="https://github.com/mlte-team/mlte/tree/master/demo" target="_blank">demo notebooks</a>.

#### Evidence: MLTE Measurements

The simplest use case is to import a MLTE-defined `Measurement`, which is then invoked to produce a `Value`. This value can then be inspected and automatically saved to the artifact store. Following are two examples of this type of evidence collection.

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

## Communicate ML Evaluation Results

To communicate results and examine findings, `MLTE` produces a report that encapsulates all knowledge gained about the model and the system as a consequence of the evaluation process. Teams can import content from the Negotiation Card using the `MLTE` UI, and the fields can be customized as needed. The report is most easily generated using the UI, but can also be defined via code as demonstrated below.

```python
import time
from mlte.report import Report, Dataset, User, UseCase, Limitation

def unix_timestamp() -> str:
    return f"{int(time.time())}"

def build_report() -> Report:
    report = Report()
    report.metadata.project_name = "Your Project"
    report.metadata.authors = ["Jane Doe", "Joe Smith"]
    report.metadata.timestamp = unix_timestamp()

    report.model_details.name = "IrisClassifier"

    report.model_specification.domain = "Classification"
    report.model_specification.data = [
        Dataset("Dataset0", "https://github.com/mlte-team", "This is one training dataset."),
        Dataset("Dataset1", "https://github.com/mlte-team", "This is the other one we used."),
    ]

    report.considerations.users = [
        User("Botanist", "A professional botanist."),
        User("Explorer", "A weekend-warrior outdoor explorer."),
    ]
    return report
```
*Note that this example only includes a few of the report fields; a full `MLTE` report in code can be found in the <a href="https://github.com/mlte-team/mlte/tree/master/demo" target="_blank">demo notebooks</a>.*

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

If the model performs as desired, teams can consider the evaluation complete. However, it is very common that teams will need to iterate through [IMT](#internal-model-testing-imt) and [SDMT](#system-dependent-model-testing-sdmt) several times before they are satisfied with the results and ready to communicate with stakeholders.

## More Information

If this guide makes you want to learn more about `MLTE`, check out our <a href="https://arxiv.org/abs/2303.01998" target="_blank">paper</a>!