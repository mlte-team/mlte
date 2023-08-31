# Testing a Model with MLTE

In this tutorial, you will conduct a preliminary test of an example model using a `MLTE` process called Internal Model Testing. After doing this evaluation, you will use the interface to look at the artifacts you've created.

## MLTE Overview

`MLTE` (pronounced 'melt') is a process and Python package that enables teams to more effectively negotiate, evaluate, and document machine learning (ML) model and system qualities. `MLTE` gives organizations a process from start to finish that leverages existing state-of-the-art research on testing ML system capabilities as well as interfaces for tracking experiments. This tutorial addresses one portion of that process called Internal Model Testing, or IMT.

## Internal Model Testing (IMT)

This step of the [`MLTE` process](mlte_framework.md) ensues after initial model development has been completed and a model is ready for a first round of testing against the chosen baseline using a chosen performance metric. For this tutorial, we will use a basic image classifier to demonstrate how this process works in `MLTE`, and use a basic accuracy measurement and threshold (rather than expect you to go through the requirements definition process). The steps of IMT are as follows:

- Initialize the `MLTE` context.
- Define a preliminary specification.
- Collect evidence.
- Validate results.
- Examine findings.

To get started, you'll need a Jupyter Notebook running, and you'll need to have `MLTE` installed. To do so, see the [Getting Started](getting_started.md) section of this documentation.

## Initialize the MLTE Context

Before starting the test, we have to set up the `MLTE` context. `MLTE` contains a global context that manages the currently active session, and intializing it tells `MLTE` how to store all of the artifacts that it produces. This is important because the artifacts are a key way that `MLTE` verifies an evaluation has been completed properly.

```python
import os
from mlte.session import set_context, set_store

store_path = os.path.join(os.getcwd(), "store")
os.makedirs(store_path, exist_ok=True)   # Ensure we are creating the folder if it is not there.

set_context("ns", "IrisClassifier", "0.0.1")
set_store(f"local://{store_path}")
```

## Define a Preliminary `Specification`

A `Specification` (or `Spec`) represents the requirements the completed model must meet in order to be acceptable for use in the system into which it will be integrated. In IMT, we use the `Spec` in a preliminary fashion so the development team can do an initial round of model testing. Here we define a `Spec` using accuracy as a performance metric. 

```python
from mlte.spec.spec import Spec

from mlte.property.functionality import TaskEfficacy

spec = Spec(properties={
    TaskEfficacy("Important to understand if the model is useful for this case"): 
                    {"accuracy": Real.greater_or_equal_to(0.98)}
    })
spec.save(parents=True, force=True)
```

## Collect Evidence

After building the `Spec`, `MLTE` allows you to collect evidence to attest to whether or not the model realizes the desired properties. Here we collect evidence by wrapping the output from scikit-learn's <a href="https://scikit-learn.org/stable/modules/model_evaluation.html#accuracy-score" target="_blank">accuracy_score</a> with a builtin `MLTE` type. Note that this example does not include data and model training code, but those can be found in the full `MLTE` <a href="https://github.com/mlte-team/mlte/tree/500a80c9dd15310e1f37b127a289472533200c24/demo" target="_blank">demo notebooks</a>.

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

## Validate Results

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

## Examine Findings

To communicate results and examine findings, `MLTE` produces a report. Once the report is built, it can be accessed through the `MLTE` user interface.

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

```python
from mlte.report import render

# Build the base report
report = build_report()
# Attach the validated specification
report.spec = validated_spec

# Save the report as an HTML document
report.to_html(REPORTS_DIR / "report.html", local=True)
```

After building the report, you can run the `MLTE` user interface (UI) by running the following in your command line:
```
$ mlte-ui
```
Once you run it, follow the link to view the `MLTE` UI homepage. In the UI, you'll see a section titled Reports. When you expand the section, you'll see all the reports you've generated under your defined context. You can click on the report and it will render in a new tab.

Congrats on finishing the tutorial! If you're interested in continuing to learn more about `MLTE`, you can look at our other tutorials [coming soon!], or head over to our guide on [using `MLTE`](using_mlte.md).