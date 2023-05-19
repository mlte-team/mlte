# Generating a Report

## Load a Specification
In MLTE, loading a specification is simple but requires the proper context to be set up. 

```Python
# Set up the MLTE context
import mlte

store_path = os.path.join(os.getcwd(), "store")

mlte.set_model("IrisClassifier", "0.0.1")
mlte.set_artifact_store_uri(f"local://{store_path}")

# Import necessary modules
from mlte.spec import Spec, ValidatedSpec

# Load the specification
spec = Spec.load()
```

## Validate Values and get an upadted ValidatedSpec wih Results
Now that we have our Spec ready and we have enough evidence, we create a SpecValidator with our spec, and add all the Values we have. With that we can validate our spec and generate an output ValidatedSpec, with the validation results.

```Python
from mlte.spec import Spec
from mlte.validation import SpecValidator
from mlte.value.types import Integer, Real, Image
from mlte.measurement.cpu import CPUStatistics
from mlte.measurement.memory import MemoryStatistics
from confusion_matrix import ConfusionMatrix

# Add all values to the validator.
spec_validator = SpecValidator(spec)
spec_validator.add_value("StorageCost", "size", Integer.load("model size"))
spec_validator.add_value("TrainingComputeCost", "cpu", CPUStatistics.load("training cpu"))
spec_validator.add_value("TrainingMemoryCost", "mem", MemoryStatistics.load("training memory"))
spec_validator.add_value("TaskEfficacy", "accuracy", Real.load("accuracy"))
spec_validator.add_value("TaskEfficacy", "confusion matrix", ConfusionMatrix.load("confusion matrix"))
spec_validator.add_value("TaskEfficacy", "classes", Image.load("class distribution"))

# Validate requirements and get validated details.
validated_spec = spec_validator.validate()

# ValidatedSpec also supports persistence
validated_spec.save()
```

## Write a Report
The final step of MLTE is the generation of a report to communicate the results of model evaluation. A report encapsulates all of the knowledge gained about the model and the system as a consequence of the evaluation process. Report production ensures that teams have a method through which they can both examine and display the results of their work. See below for an example of writing a report.

```Python
import time
from mlte.report import Report, Dataset, User, UseCase, Limitation

def unix_timestamp() -> str:
    return f"{int(time.time())}"

def build_report() -> Report:
    report = Report()
    report.metadata.project_name = "IrisClassificationProject"
    report.metadata.authors = ["Kyle Dotterrer", "Kate Maffey"]
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

## Persist/View a Report
Persisting and viewing reports are simple; once the report is saved, it can be opened in any browser and will be rendered like a webpage. See example below.

```Python
from mlte.report import render

# Build the base report
report = build_report()
# Attach the validated specification
report.spec = validated_spec

# Save the report as an HTML document
report.to_html(REPORTS_DIR / "report.html", local=True)
```